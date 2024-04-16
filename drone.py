import asyncio
import time
import utils
import spade
from utils import haversine
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import json

class Drone(Agent):
    id = None
    capacity = None # kg
    autonomy = None # km
    velocity = None # m/s
    initial_pos = None

    def __init__(self, jid, password, id, capacity=0, autonomy=0,velocity=0, initial_pos=None,orders=None):
        super().__init__(jid, password) # Assuming Agent is a parent class and needs initialization
        self.id = id
        self.hostname = jid.split('@')[-1]

        self.capacity = capacity
        self.current_capacity = capacity

        self.autonomy = autonomy
        self.current_autonomy = autonomy

        self.velocity = velocity
        self.current_velocity = 0

        self.initial_pos = initial_pos
        self.current_pos = initial_pos

        # {center1: center_obj, center2: center_obj}
        self.centerAgents = {}
        # {center1: center1_orders, center2: center2_orders}
        self.orders = orders if orders is not None else {}
    
    def setCenters(self, centerAgents):
        self.centerAgents = centerAgents
        return

    def deliverOrders(self, orders):
        self.current_loc = orders[-1]["destination"]
        return
    
    def receive_ack(self, order, ack):
        
        if (ack==False):
            return False
        if (ack==True):
            self.current_capacity = self.current_capacity + order.weight
            self.orders.append(order)
    
    # Define um percurso de orders otimo para entrega tendo em conta varios fatores
    def select_orders(self, order):

        if (order.weight + self.current_capacity > self.capacity):
            return False
        
        distance = 0
        if (self.capacity != 0):
            for i in range(len(self.orders) + 1):
                if (i==0):
                    distance = haversine(self.current_pos, self.orders[i].destination)
                elif (i==len(self.orders)):
                    distance += haversine(self.orders[i-1].destination, order.destination)
                    distance += haversine(order.destination, self.current_pos)
                else:
                    distance += haversine(self.orders[i-1].destination, self.orders[i].destination)
        else:
            distance = 2*haversine(self.current_pos, order.destination)

        if (distance > self.autonomy):
            return False
        else:
            return True



    class InformBehav(OneShotBehaviour):

        async def run(self):
            
            print("InformBehav running")
            msg = Message(to=f"admin@{self.agent.hostname}")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

            # Set the message content            
            msg.body = "ID=" + str(self.agent.id) + "\n"
            msg.body = "Velocity=" + str(self.agent.velocity) + "\n"
            msg.body += "Capacity=" + str(self.agent.capacity) + "\n"
            msg.body += "Autonomy=" + str(self.agent.autonomy) + "\n"
            msg.body += "Initial_pos=" + str(self.agent.initial_pos) + "\n"
            msg.body += "Current_pos=" + str(self.agent.current_pos)

            await self.send(msg)
            print("Inform sent!")
            
    class RecvOrdersMultipleBehav(OneShotBehaviour):

        async def run(self):

            for center in self.agent.centerAgents.keys():
                msg = await self.receive(60)  # Wait for a message
                if msg:
                    msg_body = json.loads(msg.body)
                    self.agent.center_orders[msg_body["center_id"]] = msg_body["orders"]
                else:
                    print("Did not receive any message")

            print("ORDERS FROM THE FIRST CENTER: ", len(self.agent.center_orders["center1"]))
            print("ORDERS FROM THE SECOND CENTER: ", len(self.agent.center_orders["center2"]))
            
            # Stop agent from behavior
            # await self.agent.stop()

    class RequestOrdersBehav(OneShotBehaviour):
        
        # Obtain the center agents that are close to the drone
        def get_close_centers(self):
            close_centers = []
            for center in self.agent.centerAgents.values():
                if utils.haversine(center.pos, self.agent.current_pos) <= self.agent.current_autonomy:
                    close_centers.append(center)
            return close_centers
        
        async def request_center_orders(self):
            print(f"{self.agent.id}: Requesting orders for {self.agent.id}")

            close_centers = self.get_close_centers()

            for center in close_centers:
                msg = Message(to=f"{center.id}@{center.hostname}")
                msg.sender = str(self.agent.jid)
                msg.set_metadata("performative", "request")
                msg.body = f"get_orders : {time.time()}"
                await self.send(msg)
                msg = await self.receive(60)  # Wait for a response
                if msg:
                    print(f"{self.agent.id}: Received response to request from {center.id}: {len(msg.body)}")
                    msg_body = json.loads(msg.body)
                    self.agent.center_orders[msg_body["center_id"]] = msg_body["orders"]
                else:
                    print(f"{self.agent.id}: Timeout waiting for request response")

        async def select_center_orders(self):
            print(f"{self.agent.id}: Selecting orders for {self.agent.id}")


            interesting_orders = self.agent.select_orders()

            for order in interesting_orders:

                center = self.agent.centerAgents[order["center"]]

                print("center:", center)

                msg = Message(to=f"{center.id}@{center.hostname}")
                msg.sender = str(self.agent.jid)
                msg.set_metadata("performative", "request")
                msg.body = f"select_order : {order['order_id']} {time.time()}"
                await self.send(msg)
                response = await self.receive(60)  # Wait for a response
                if response:
                    print(f"{self.agent.id}: Received response to request from {center.id}: {response.body}")
                else:
                    print(f"{self.agent.id}: Timeout waiting for request response")

        async def confirm_center_orders(self):
            return

        async def run(self):
            await self.request_center_orders()
            # print(len(self.agent.center_orders))
            await self.select_center_orders()

            # await self.confirm_center_orders()

            # stop agent from behaviour
            # await self.agent.stop()

    # class SelectOrdersBehav(OneShotBehaviour):
        
    #     async def run(self):
    #         print(f"{self.agent.id}: Selecting orders for {self.agent.id}")

    #         interesting_orders = []
    #         while self.agent.center_orders is None:
    #             interesting_orders = self.agent.select_orders()

    #         print("interresting:",interesting_orders)
    #         for order in interesting_orders:
                
    #             center = self.agent.center_orders[order["center"]]

    #             print("center:", center)

    #             msg = Message(to=f"{center.id}@{center.hostname}")
    #             msg.sender = str(self.agent.jid)
    #             msg.set_metadata("performative", "request")
    #             msg.body = f"select_order : {order['order_id']} {time.time()}"
    #             await self.send(msg)
    #             response = await self.receive(60)  # Wait for a response
    #             if response:
    #                 print(f"{self.agent.id}: Received response to request from {center.id}: {response.body}")
    #             else:
    #                 print(f"{self.agent.id}: Timeout waiting for request response")

    #         # stop agent from behaviour
    #         # await self.agent.stop()

    class LongBehav(OneShotBehaviour):
        async def run(self):
            await asyncio.sleep(100)
            print("Long Behaviour has finished")

    class WaitingBehav(OneShotBehaviour):
        async def run(self):
            await self.agent.L.join()  # this join must be awaited
            print("Waiting Behaviour has finished")
            # Stop agent from behavior
            await self.agent.stop()


    async def setup(self):
        print(f"{self.id}: agent started")
        b = self.RecvOrdersMultipleBehav()
        requestOrders = self.RequestOrdersBehav()
        # selectOrders = self.SelectOrdersBehav()
        self.L = self.LongBehav()
        W = self.WaitingBehav()


        # print(self.presence.state)  # Gets your current PresenceState instance.

        # print(self.presence.is_available())  # Returns a boolean to report wether the agent is available or not

        self.add_behaviour(requestOrders)
        # await requestAvailOrders.join()
        # self.add_behaviour(selectOrders)
        # template = Template()
        # template.setmes_metadata("performative", "inform")
        # self.add_behaviour(b, template)
        # self.add_behaviour(b)
        # self.add_behaviour(self.L)
        # self.add_behaviour(W)
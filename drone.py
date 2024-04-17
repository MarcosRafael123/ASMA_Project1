import asyncio
import time
import utils
import spade
import random
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
        self.current_capacity = 0

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
        # Update weight, capacity and autonomy
        self.current_loc = orders[-1]["destination"]
        return
    
    def receive_ack(self, order, ack):
        
        if (ack==False):
            return False
        if (ack==True):
            self.current_capacity = self.current_capacity + order.weight
            self.orders.append(order)
        return
    
    # Receives an order and defines a proposal for IT
    # If accept -> returns time_needed_to_deliver
    # If refuse -> returns -1
    def accept_order(self, order, center):

        if (order["weight"] + self.current_capacity > self.capacity):
            return -1

        distance = 0

        # Distance to fetch the order from the center
        distance += haversine(self.current_pos, self.centerAgents[center].pos)

        # print(f"{self.id}: distance to fetch order: {distance}")

        if (self.current_capacity != 0):
            for i in range(len(self.orders) + 1):
                if (i==0):
                    distance = haversine(self.current_pos, self.orders[i]["destination"])
                elif (i==len(self.orders)):
                    distance += haversine(self.orders[i-1]["destination"], order["destination"])
                    distance += haversine(order["destination"], self.current_pos)
                else:
                    distance += haversine(self.orders[i-1]["destination"], self.orders[i]["destination"])
        else:
            distance += 2*haversine(self.centerAgents[center].pos, order["destination"])

        if (distance > self.current_autonomy):
            return -1.0
        else:
            return distance/(self.velocity*3.6)
        

    # def accept_order(self,order):

    #     # If order accept -> return time_neeeded
    #     # If order refuse -> return -1

    #     if random.randint(1, 10) < 4:
    #         return -1

    #     return -1


    def process_proposals(self,proposals):

        # # Extract the proposal strings from the tuple
        # proposal_values = [proposal[2] for proposal in proposals]

        # Separate proposals into accepted and rejected
        accept_proposals = [proposal for proposal in proposals if proposal[2] != -1]
        res_proposals = [proposal for proposal in proposals if proposal not in accept_proposals]

        # If only one proposal is accepted, return all proposals
        if len(accept_proposals) <= 1:
            return proposals

        # Find the best accepted proposal
        best_proposal = min(accept_proposals, key=lambda x: float(x[2]))

        # Generate new proposals for rejected ones
        new_proposals = [(proposal[0],proposal[1],-1) for proposal in accept_proposals if proposal != best_proposal]

        new_proposals.append(best_proposal)

        # Append new proposals to rejected proposals
        res_proposals += new_proposals

        # Return the updated tuple with new proposals
        return [(proposal[0], proposal[1], proposal[2]) for proposal in res_proposals]
    
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
            # await self.request_center_orders()
            # print(len(self.agent.center_orders))
            # await self.select_center_orders()

            # await self.confirm_center_orders()

            # stop agent from behaviour
            # await self.agent.stop()
            return


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


    class RecvOrdersBehav(OneShotBehaviour):

        async def recv_msgs(self, template):
            msgs = []
            for center in self.agent.centerAgents.keys():
                msg = None
                while msg is None:
                    msg = await self.receive(60)  # Wait for a message
                    if not msg is None and template.match(msg):
                        break
                msgs.append(msg)
            return msgs
        
        async def send_proposal(self, center_proposer, order_offer_center, drone_proposal):

            msg = Message(to=f"{str(center_proposer )}")
            msg.sender = str(self.agent.jid)
            msg.set_metadata("performative", "order_proposal")

            if drone_proposal == -1:
                msg.body = f"Deny Offer {order_offer_center}"
            else:
                msg.body = f"Accept Offer {order_offer_center} Time_Needed: {drone_proposal}"
            await self.send(msg)

            return
        
        async def run(self):

            template_orderOffer = Template()
            template_orderOffer.metadata = {"performative": "order"}

            template_decision = Template()
            template_decision.metadata = {"performative": "decision"}
            
            # num = 0
            while True:
                # print(f"{self.agent.id}: Iteration {num}")
                # num += 1
                # Receive order offers
                msgs = await self.recv_msgs(template_orderOffer)

                # Process received offers from centers and create proposals
                proposals = []
                for msg in msgs:
                    # Process received message containing offer
                    order = json.loads(msg.body)
                    center_proposer = msg.sender
                    order_offer_center = json.loads(msg.body)["order_id"]
                    # print(f"{self.agent.id}: received offer {order}")

                    # Evaluate received offer and create proposal
                    drone_proposal = self.agent.accept_order(order,center_proposer.localpart)
                    # print(f"{self.agent.id}: drone proposal {drone_proposal}")
                    # await self.send_proposal(center_proposer,order_offer_center, drone_proposal)
                    proposals.append((center_proposer,order_offer_center,drone_proposal))
                
                
                print(f"{self.agent.id}: proposals {proposals}")
                # Clear possible conflicts with proposals (drone cannot accept the two orders)
                proposals = self.agent.process_proposals(proposals)
                print(f"{self.agent.id}: clean proposals {proposals}")

                # Send proposals to centers
                for proposal in proposals:
                    await self.send_proposal(proposal[0], proposal[1], proposal[2])

                # Receive confirmations of sent proposals from centers
                msgs = await self.recv_msgs(template_decision)

                # Receive and process confirmation
                for msg in msgs:
                    print(f"{self.agent.id} : {msg.body }")


            await asyncio.sleep(100)
            # Stop agent from behavior
            # await self.agent.stop()

# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR
# USE TEMPLATES/ASSERT OR PROBLEMS WILL OCCUR


    async def setup(self):
        print(f"{self.id}: agent started")
        # b = self.RecvOrdersMultipleBehav()
        # requestOrders = self.RequestOrdersBehav()
        # selectOrders = self.SelectOrdersBehav()
        # self.L = self.LongBehav()
        # W = self.WaitingBehav()


        recvOrder = self.RecvOrdersBehav()
        self.add_behaviour(recvOrder)


        # print(self.presence.state)  # Gets your current PresenceState instance.

        # print(self.presence.is_available())  # Returns a boolean to report wether the agent is available or not

        # self.add_behaviour(requestOrders)
        # await requestAvailOrders.join()
        # self.add_behaviour(selectOrders)
        # template = Template()
        # template.setmes_metadata("performative", "inform")
        # self.add_behaviour(b, template)
        # self.add_behaviour(b)
        # self.add_behaviour(self.L)
        # self.add_behaviour(W)
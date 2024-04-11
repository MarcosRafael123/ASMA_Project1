import asyncio
import spade
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

    def __init__(self, jid, password, id, capacity=0, autonomy=0,velocity=0, initial_pos=None, orders_center1=None, orders_center2=None):
        super().__init__(jid, password) # Assuming Agent is a parent class and needs initialization
        self.id = id
        self.capacity = capacity
        self.autonomy = autonomy
        self.velocity = velocity
        self.initial_pos = initial_pos
        self.orders_center1 = orders_center1 if orders_center1 is not None else []
        self.orders_center2 = orders_center2 if orders_center2 is not None else []

    
    def setCenters(self, center_ids):
        self.center_ids = center_ids

    class InformBehav(OneShotBehaviour):

        async def run(self):
            print("InformBehav running")
            msg = Message(to="admin@hplaptop")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative

            msg.body = "ID=" + str(self.agent.id) + "\n"  
            msg.body = "Velocity=" + str(self.agent.velocity) + "\n"                    # Set the message content
            msg.body += "Capacity=" + str(self.agent.capacity) + "\n" 
            msg.body += "Autonomy=" + str(self.agent.autonomy) + "\n"
            msg.body += "Initial_pos=" + str(self.agent.initial_pos)

            print("body: \n" + msg.body)

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()
            
    class RecvBehav(OneShotBehaviour):

        #def parseOrders():

        async def run(self):

            for center_id in self.agent.center_ids:
                msg = await self.receive(60)  # Wait indefinitely for a message
                if msg:
                    #print("Message received with content: {}".format(msg.body))
                    if (json.loads(msg.body)["orders"][0].get("order_id") == "order1_1"):
                        self.orders_center1 = json.loads(msg.body)["orders"]
                    else:
                        self.orders_center2 = json.loads(msg.body)["orders"]
                    
                else:
                    print("Did not receive any message")

            print("ORDERS FROM THE FIRST CENTER: ", self.orders_center1)
            print("ORDERS FROM THE SECOND CENTER: ", self.orders_center2)
            
            # Stop agent from behavior
            # await self.agent.stop()

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
        print(f"{self.id} ReceiverBehav started")
        b = self.RecvBehav()
        self.L = self.LongBehav()
        W = self.WaitingBehav()

        # print(self.presence.state)  # Gets your current PresenceState instance.

        # print(self.presence.is_available())  # Returns a boolean to report wether the agent is available or not

        template = Template()
        # template.setmes_metadata("performative", "inform")
        # self.add_behaviour(b, template)
        self.add_behaviour(b)
        # self.add_behaviour(self.L)
        # self.add_behaviour(W)




# class ReceiverAgent(Agent):

    # async def setup(self):
    #     print("ReceiverAgent started")
    #     b = self.RecvBehav()
    #     template = Template()
    #     template.set_metadata("performative", "inform")
    #     self.add_behaviour(b, template)
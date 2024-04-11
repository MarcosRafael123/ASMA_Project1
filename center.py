import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import pickle


class Center(Agent):
    def __init__(self, jid, password, id, pos=(),orders=None):
        super().__init__(jid, password) # Assuming Agent is a parent class and needs initialization
        self.id = id
        self.pos = pos # (latitude, longitude)
        self.orders = orders if orders is not None else []
        return
    
    def get_pos(self):
        return self.pos
    
    def get_orders(self):
        return self.orders
    
    def clear_orders(self):
        self.orders = []
        return
    
    def setDrones(self, drone_ids):
        self.drone_ids = drone_ids

    def add_order(self,order):
        self.orders.append(order)
        return
    
    class InformBehav(OneShotBehaviour):

        async def run(self):
            print(f"Sending Messages from {self.agent.id}")
            # orders = self.agent.get_orders()  # Get orders from the center
            # orders_serialized = pickle.dumps(orders)  # Serialize orders using pickle

            for drone_id in self.agent.drone_ids:
                msg = Message(to=f"{drone_id}@localhost")
                msg.set_metadata("performative", "inform")
                msg.body = f"DATA from {self.agent.id}"

                await self.send(msg)
            print("Messages sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print(f"{self.id} agent started")
        b = self.InformBehav()
        self.add_behaviour(b)
        
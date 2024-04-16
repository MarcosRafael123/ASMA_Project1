import spade
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import json


SELECTION_TIME = 10

class Center(Agent):
    def __init__(self, jid, password, id, pos=(),orders=None):
        super().__init__(jid, password) # Assuming Agent is a parent class and needs initialization
        self.id = id
        self.hostname = jid.split('@')[-1]
        self.pos = pos # (latitude, longitude)
        self.orders = orders if orders is not None else []
        self.interestOrders = {}
        for ord in self.orders:
            self.interestOrders[ord.id] = []
        return
    
    def get_pos(self):
        return self.pos
    
    def get_orders(self):
        return self.orders
    
    def clear_orders(self):
        self.orders = []
        self.interestOrders = {}
        return
    
    def setDrones(self, drone_ids):
        self.drone_ids = drone_ids

    def add_order(self,order):
        self.orders.append(order)
        self.interestOrders[order.id] = []
        return
    
    class SendOrdersBehav(OneShotBehaviour):

        async def run(self):
            print(f"Sending Orders from {self.agent.id}")
            orders = self.agent.get_orders()  # Get orders from the center
            
            serialized_orders = [order.to_dict() for order in orders]

            for drone_id in self.agent.drone_ids:
                msg = Message(to=f"{drone_id}@{self.agent.hostname}")
                msg.sender = self.agent.id
                msg.set_metadata("performative", "inform")
                msg.body = json.dumps({
                    "center_id": self.agent.id,
                    "orders": serialized_orders
                })

                await self.send(msg)
            print("Messages sent!")

            # stop agent from behaviour
            await self.agent.stop()


    class HandleRequestsBehav(OneShotBehaviour):

        tasks = {}

        async def timer(self,duration, callback):
            while duration > 0:
                print(f"Timer: {duration} seconds remaining...")
                await asyncio.sleep(1)
                duration -= 1
            await callback()

        async def confirm_order(self,order_id,drone_jid):
            msg = Message(to=str(drone_jid))
            msg.sender = str(self.agent.jid)
            msg.set_metadata("performative", "confirmation")
            msg.body = f"{order_id} confirmed"
            await self.send(msg)

        async def confirm_interests(self,order_id):
            print(f"{self.agent.id}: interested drones in {order_id}:",self.agent.interestOrders[order_id])
            #Start negotiation or confirm order if len = 1
            if len(self.agent.interestOrders[order_id]) == 1:
                await self.confirm_order(order_id, self.agent.interestOrders[order_id])
            #Remove task and interestOrders and Order

        async def respond_to_request(self, request):

            orders = self.agent.get_orders()  # Get orders from the center
            serialized_orders = [order.to_dict() for order in orders]

            sender_jid = request.sender

            msg = Message(to=str(sender_jid))
            msg.sender = str(self.agent.jid)
            msg.set_metadata("performative", "response")

            if request.body.split()[0] == "get_orders":
                msg.body = json.dumps({
                    "center_id": self.agent.id,
                    "orders": serialized_orders
                })
                await self.send(msg)
            elif request.body.split()[0] == "select_order":
                order_id = request.body.split()[2]
                if order_id in self.agent.orders:
                    msg.body = f"{order_id} not available"
                else:
                    msg.body = f"{order_id} selected"
                
                self.agent.interestOrders[order_id].append(str(sender_jid))
                if order_id in self.tasks:
                    self.tasks[order_id].cancel()
                self.tasks[order_id] = asyncio.create_task(self.timer(SELECTION_TIME, lambda: self.confirm_interests(order_id)))
                await self.send(msg)

            return

        async def run(self):

            while True:
                print(f"{self.agent.id}: receiving requests")
                msg = None
                while msg is None:
                    msg = await self.receive(60)  # Wait for a message
                    if msg:
                        print(f"{self.agent.id}: Received request {msg.body} from {msg.sender}")
                        await self.respond_to_request(msg)
                    else:
                        print(f"{self.agent.id}: Timeout")

            # stop agent from behaviour
            # await self.agent.stop()

    async def setup(self):
        print(f"{self.id}: agent started")

        handleRequestsBehav = self.HandleRequestsBehav()
        self.add_behaviour(handleRequestsBehav)

        b = self.SendOrdersBehav()
        # self.add_behaviour(b)
        
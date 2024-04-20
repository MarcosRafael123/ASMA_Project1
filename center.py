import spade
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import json


NUM_RETRIES_OFFER = 3

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


    # return null if there are no accept proposals
    def select_proposal(self, proposals):
        # Filter proposals where the first word is not "Accept"
        filtered_proposals = {proposal: value for proposal, value in proposals.items() if value.split()[0] == "Accept"}

        if not filtered_proposals:
            return None
        

        items = list(filtered_proposals.items())
        random.shuffle(items)

        # Extract proposal values and find the minimum
        min_proposal = min(items, key=lambda x: float(x[1].split()[4]))

        return min_proposal

    class SendOrdersBehav(OneShotBehaviour):

        async def recv_msg(self,template):
            msg = None
            while msg is None:
                msg = await self.receive(60)  # Wait for a message
                if not msg is None and template.match(msg):
                    break
            return msg

        async def send_order_offer(self, order):
            serialized_order = order.to_dict()
            for drone_id in self.agent.drone_ids:
                msg = Message(to=f"{drone_id}@{self.agent.hostname}")
                msg.sender = str(self.agent.jid)
                msg.set_metadata("performative", "order")
                msg.body = json.dumps(serialized_order)
                await self.send(msg)
            print(f"{self.agent.id}: Order offer sent! ({order})")

        async def recv_order_proposals(self):

            template_orderProposal = Template()
            template_orderProposal.metadata = {"performative": "order_proposal"}
        
            proposals = {}
            for drone_id in self.agent.drone_ids:
                msg = await self.recv_msg(template_orderProposal)
                proposals[str(msg.sender)[:str(msg.sender).find("@")]] = msg.body
            # print(f"{self.agent.id}: Proposals received!")
            return proposals
        
        async def send_decision(self, decision,order):
            for drone_id in self.agent.drone_ids:

                msg = Message(to=f"{drone_id}@{self.agent.hostname}")
                msg.sender = str(self.agent.jid)
                msg.set_metadata("performative", "decision")

                if decision != None and decision[0] == drone_id:
                    msg.body = "Accept proposal"
                else:
                    msg.body = "Deny proposal"

                msg.body += " " + order.id

                await self.send(msg)
                
            return 
        
        async def send_end_msg(self):
            print(f"{self.agent.id}:  Sending End Msg")
            for drone_id in self.agent.drone_ids:

                msg = Message(to=f"{drone_id}@{self.agent.hostname}")
                msg.sender = str(self.agent.jid)
                msg.set_metadata("performative", "end")
                msg.body = f"{self.agent.id} has finished execution"
                await self.send(msg)
            return

        async def run(self):

            orders = self.agent.orders
            too_many_retries = False

            for order in orders:

                if not too_many_retries:
                    print("------------------------")
                too_many_retries = False 

                decision = None

                for retry in range(NUM_RETRIES_OFFER):
                # while decision is None:
                    await self.send_order_offer(order)
                    proposals = await self.recv_order_proposals()
                    decision = self.agent.select_proposal(proposals)
                    print(f"{self.agent.id}: Decision:", decision)
                
                    # print(f"{self.agent.id} proposals: {proposals}")

                    # print(f"{self.agent.id} Sending Decisions")
                    await self.send_decision(decision,order)
                    
                    await asyncio.sleep(1)
                    if decision != None:
                         break

                    if retry == NUM_RETRIES_OFFER-1:
                        too_many_retries = True

                if too_many_retries:
                    print("NEEDED TO PLACE ORDER AT THE END")
                    orders.append(order)

            await self.send_end_msg()
            
            
            await asyncio.sleep(100)

            # stop agent from behaviour
            # await self.agent.stop()

    async def setup(self):
        print(f"{self.id}: agent started")

        # handleRequestsBehav = self.HandleRequestsBehav()
        # self.add_behaviour(handleRequestsBehav)

        b = self.SendOrdersBehav()
        self.add_behaviour(b)
        
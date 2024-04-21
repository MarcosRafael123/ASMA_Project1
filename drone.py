import asyncio
import time
import utils
import spade
import itertools
import random
from utils import haversine
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import json

TIME_FACTOR = 1000


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

        self.initial_pos = initial_pos
        self.current_pos = initial_pos

        # {center1: center_obj, center2: center_obj}
        self.centerAgents = {}

        self.orders = orders if orders is not None else []
        self.path = []

        self.isDelivering = False

        self.record = [initial_pos]
        self.total_delivery_distance = 0
        self.total_delivery_time = 0
        self.total_weight_carried = 0
        self.total_delivered_orders = 0
        self.total_num_trips = 0
        self.max_time = 0
        self.min_time = 1000000000
    
    def setCenters(self, centerAgents):
        self.centerAgents = centerAgents
        return
    
    def add_order(self,order):

        self.current_capacity += order["weight"]
        self.orders.append(order)
        return
    
    def print_stats(self):
        print(f"{self.id} : ----------STATS-----------")
        print(f"{self.id} : Record: {self.record}")
        print(f"{self.id} : Total Delivery Time: {self.total_delivery_time}")
        print(f"{self.id}: Total orders delivered: {self.total_delivered_orders }")
        print(f"{self.id}: Mean time to deliver: {self.total_delivery_time / self.total_delivered_orders }")
        print(f"{self.id}: Total number of trips: {self.total_num_trips }")
        print(f"{self.id}: Total weight carried: {self.total_weight_carried }")
        print(f"{self.id}: Total distance travelled: {self.total_delivery_distance }")
        print(f"{self.id}: Maximum delivery time: {self.max_time }")
        print(f"{self.id}: Minimum delivery time: {self.min_time }")
        print(f"{self.id} : --------------------------")
        return


    # Start and end at the same center
    def calculate_path(self, order = None):
        
        orders = self.orders.copy()

        if order:
            orders.append(order)

        order_ids = [item["order_id"] for item in orders]

        if len(order_ids) == 0:
            return [], -1.0


        # Generate all possible permutations of orders
        order_permutations = itertools.permutations(order_ids)

        # print(f"ITER: {list(order_permutations)}")

        # Initialize variables to track the best route and its distance
        best_route = None
        min_distance = float('inf')

        # Iterate through each permutation of orders
        for order_sequence in order_permutations:
            # Create a list of locations to visit (start and end at center)
            locations_to_visit = [self.current_pos] + list(order_sequence) + [self.current_pos]

            # Calculate the total distance of the route
            total_distance = 0
            for i in range(len(locations_to_visit) - 1):
                origin = None
                destination = None
                if locations_to_visit[i][:5] == "order":
                    origin = [item for item in orders if item["order_id"] == locations_to_visit[i]][0]["destination"]
                else:
                    origin = self.centerAgents[locations_to_visit[i]].pos

                if locations_to_visit[i+1][:5] == "order":
                    destination = [item for item in orders if item["order_id"] == locations_to_visit[i+1]][0]["destination"]
                else:
                    destination = self.centerAgents[locations_to_visit[i+1]].pos
                
                total_distance += haversine(origin, destination)

            # Check if this route is better than the current best
            if total_distance < min_distance:
                best_route = locations_to_visit
                min_distance = total_distance


        return best_route, min_distance

    # def calculate_path1(self):

    #     path = []

    #     if self.record == {}:
    #         path.append(self.current_pos)
        
    #     for order in self.orders:
    #         path.append(order["order_id"])

    #     path.append(self.current_pos)
        

    #     return path,None


    def ready_to_deliver(self):
        
        cap_cond = self.current_capacity >= self.capacity*0.75

        return cap_cond


    async def deliver_orders(self, path):

        self.isDelivering = True

        total_time = 0

        for stop in path:

            isCenter = stop[:6] == "center"

            current_pos = None
            if self.current_pos[:5] == "order":
                current_pos = [item for item in self.orders if item["order_id"] == self.current_pos][0]["destination"]
            else:
                current_pos = self.centerAgents[self.current_pos].pos
            
            
            if not isCenter:
                order = [item for item in self.orders if item["order_id"] == stop][0]
                self.current_capacity -= order["weight"]

                distance = haversine(current_pos,order["destination"])
                time = (distance)/self.velocity

                await asyncio.sleep(time/TIME_FACTOR)
                self.total_delivery_distance += distance
                self.total_weight_carried += order["weight"]
                self.total_delivery_time += time
                self.total_delivered_orders += 1
                if (time > self.max_time):
                    self.max_time = time
                if (time < self.min_time and time > 0):
                    self.min_time = time

                self.current_autonomy -= distance
                
                self.current_pos = stop
            else:
                distance = haversine(current_pos,self.centerAgents[stop].pos)
                time = (distance)/self.velocity

                await asyncio.sleep(time/TIME_FACTOR)
                self.total_delivery_distance += distance
                self.total_delivery_time += time
                
                self.current_autonomy = self.autonomy
                self.current_pos = stop


        self.orders = []
        self.record += path
        self.total_num_trips += 1

        self.isDelivering = False

        return
    
    # Receives an order and defines a proposal for IT
    # If accept -> returns time_needed_to_deliver
    # If refuse -> returns -1
    def accept_order(self, order, center):

        if self.isDelivering:
            return -1.0

        if (order["weight"] + self.current_capacity > self.capacity):
            return -1
        
        distance = 0

        # Distance to fetch the order from the center
        distance += haversine(self.centerAgents[self.current_pos].pos, self.centerAgents[center].pos)

        # print(f"{self.id}: distance to fetch order: {distance}")

        if (self.current_capacity != 0):
            for i in range(len(self.orders) + 1):
                if (i==0):
                    distance += haversine(self.centerAgents[center].pos, self.orders[i]["destination"])
                elif (i==len(self.orders)):
                    distance += haversine(self.orders[i-1]["destination"], order["destination"])
                    distance += haversine(order["destination"], self.centerAgents[center].pos)
                else:
                    distance += haversine(self.orders[i-1]["destination"], self.orders[i]["destination"])
        else:
            distance += 2*haversine(self.centerAgents[center].pos, order["destination"])


        # print(f"{self.id} : Distance needed to travel: {distance}")

        if (distance > self.current_autonomy*1000):
            return -1.0
        else:
            return distance/(self.velocity)
        

    # Receives an order and defines a proposal for IT
    # If accept -> returns time_needed_to_deliver
    # If refuse -> returns -1
    def accept_order(self, order, center):


        if self.isDelivering:
            return -1.0
        
        if (order["weight"] + self.current_capacity > self.capacity):
            return -1.0
        
        # print(f"{self.id}: Passed init")

        _, dist1 = self.calculate_path(order=order)
        _, dist2 = self.calculate_path()

        time1 = dist1/self.velocity
        time2 = dist2/self.velocity

        if (dist1 > self.current_autonomy*1000):
            return -1.0
        elif dist2 == -1.0:
            return time1
        else:
            return time1 - time2
            #return distance/(self.velocity*3.6)


    # def accept_order1(self, order, center):

    #     # If order accept -> return time_neeeded
    #     # If order refuse -> return -1

    #     if self.isDelivering:
    #         return -1.0

    #     if (order["weight"] + self.current_capacity > self.capacity):
    #         return -1

    #     if random.randint(1, 10) < 4:
    #         return -1

    #     return random.randint(1, 10)


    def clean_proposals(self,proposals):

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


    class RecvOrdersBehav(OneShotBehaviour):

        async def recv_msgs(self, template, end_template=None):
            msgs = []
            for center in range(self.agent.numActiveCenterAgents):
                msg = None
                while msg is None:
                    msg = await self.receive(60)  # Wait for a message
                    if msg:
                        if template.match(msg):
                            msgs.append(msg)
                        if end_template and end_template.match(msg):
                            self.agent.numActiveCenterAgents -=1
                        break

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
        
        def process_confirmations(self,msgs,orders):
            
            for confirmation in msgs:
                confirmation = confirmation.body.split()
                if confirmation[0] == "Accept":
                    print(f"{self.agent.id}: DRONE ADDING ORDER {orders[confirmation[2]]}")
                    self.agent.add_order(orders[confirmation[2]])
            
            return

        async def run(self):

            template_centerFinished = Template()
            template_centerFinished.metadata = {"performative": "end"}

            template_orderOffer = Template()
            template_orderOffer.metadata = {"performative": "order"}

            template_decision = Template()
            template_decision.metadata = {"performative": "decision"}

            self.agent.numActiveCenterAgents = len(self.agent.centerAgents)
            
            deliver_task = None
            while True:
                # Receive order offers
                msgs = await self.recv_msgs(template_orderOffer,end_template=template_centerFinished)
                
                # If all centers ended ended execution -> end drone execution
                if len(msgs)==0:
                    break

                # Process received offers from centers and create proposals
                proposals = []
                orders = {}
                for msg in msgs:
                    # Process received message containing offer
                    order = json.loads(msg.body)
                    center_proposer = msg.sender
                    order_offer_center = json.loads(msg.body)["order_id"]

                    orders[order["order_id"]] = order

                    # Evaluate received offer and create proposal
                    drone_proposal = self.agent.accept_order(order,center_proposer.localpart)

                    proposals.append((center_proposer,order_offer_center,drone_proposal))
                
                
                # print(f"{self.agent.id}: proposals {proposals}")
                # Clear possible conflicts with proposals (drone cannot accept the two orders)
                proposals = self.agent.clean_proposals(proposals)

                for proposal in proposals:
                    if proposal[2] == -1.0:
                        print(f"{self.agent.id} : Drone Proposal for {proposal[1]}: Deny")
                    else:
                        print(f"{self.agent.id} : Drone Proposal for {proposal[1]}: Accept! time={proposal[2]}")
                
                print(f"{self.agent.id}: Current capacity: {self.agent.current_capacity }")

                # Send proposals to centers
                for proposal in proposals:
                    await self.send_proposal(proposal[0], proposal[1], proposal[2])

                # Receive confirmations of sent proposals from centers
                msgs = await self.recv_msgs(template_decision)

                # Process confirmations
                # for msg in msgs:
                #     print(f"{self.agent.id} : {msg.body }")
                self.process_confirmations(msgs,orders)
                
                if (not self.agent.isDelivering) and self.agent.ready_to_deliver():
                    path,_ = self.agent.calculate_path()
                    print(f"{self.agent.id}: With path = {path} Delivering...")
                    deliver_task = asyncio.create_task(self.agent.deliver_orders(path))
            

            #If there are undelivered drone attributed orders after termination -> deliver them
            if deliver_task:
                await deliver_task
            if len(self.agent.orders) > 0:
                path,_ = self.agent.calculate_path()
                print(f"{self.agent.id}: With path = {path} Delivering...")
                await self.agent.deliver_orders(path)

            # Print stats
            self.agent.print_stats()

            await asyncio.sleep(100)

            # Stop agent from behavior
            # await self.agent.stop()

    async def setup(self):
        print(f"{self.id}: agent started")

        recvOrder = self.RecvOrdersBehav()
        self.add_behaviour(recvOrder)


        # print(self.presence.state)  # Gets your current PresenceState instance.

        # print(self.presence.is_available())  # Returns a boolean to report wether the agent is available or not

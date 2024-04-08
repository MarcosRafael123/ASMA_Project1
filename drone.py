import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

class Drone(Agent):
    id = None
    capacity = None # kg
    autonomy = None # km
    velocity = None # m/s
    initial_pos = None

    def __init__(self, jid, password, id, capacity=0, autonomy=0,velocity=0, initial_pos=None):
        super().__init__(jid, password) # Assuming Agent is a parent class and needs initialization
        self.id = id
        self.capacity = capacity
        self.autonomy = autonomy
        self.velocity = velocity
        self.initial_pos = initial_pos

    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="admin@leandro")     # Instantiate the message
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
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=30) # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()

        self.add_behaviour(b)

class ReceiverAgent(Agent):

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
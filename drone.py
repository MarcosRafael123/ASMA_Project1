import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template

class Drone(Agent):
    def __init__(self):
        self.capacity = None
        self.autonomy = None
        self.velocity = None
        self.number = None

    @property
    def capacity(self):
        return self.capacity

    @capacity.setter
    def capacity(self, value):
        self.capacity = value

    @property
    def autonomy(self):
        return self.autonomy

    @autonomy.setter
    def autonomy(self, value):
        self.autonomy = value

    @property
    def velocity(self):
        return self.velocity

    @velocity.setter
    def velocity(self, value):
        self.velocity = value

    @property
    def number(self):
        return self.number

    @number.setter
    def number(self, value):
        self.umber = value

    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="admin@leandro")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()

        self.add_behaviour()

class ReceiverAgent(Agent):
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
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)



async def main():
    
    receiveragent = ReceiverAgent("admin@leandro", "admin")
    await receiveragent.start(auto_register=True)
    print("Receiver started")

    senderagent = SenderAgent("dummy@leandro", "dummy")
    await senderagent.start(auto_register=True)
    print("Sender started")

    await spade.wait_until_finished(receiveragent)
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
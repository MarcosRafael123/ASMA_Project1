import spade
import asyncio
import pandas as pd
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
from order import Order

class Center(Agent):
    def __init__(self, jid, password, id=None, pos=(), data_file=None):
        super().__init__(jid, password) # Assuming Agent is a parent class and needs initialization
        self.id = id
        self.pos = pos
        self.orders = []
        self.data_file = data_file

    async def setup(self):
        if self.data_file:
            data = pd.read_csv(self.data_file, sep=';')
            self.id = data.at[0, 'id']
            self.pos = self.pos + (data.at[0, 'latitude'], data.at[0, 'longitude'])

    def get_orders(self):
        return self.orders

    async def add_order(self, order):
        self.orders.append(order)


async def main():
    
    # Create instances of Center
    center1 = Center('admin@hplaptop', 'admin', data_file='data/delivery_center1.csv')
    center2 = Center('admin@hplaptop', 'admin', data_file='data/delivery_center2.csv')

    # Start the agents
    await center1.start()
    await center2.start()

    data1 = pd.read_csv('data/delivery_center1.csv', sep=';')
    for i in range (data1.shape[0]):
        if (i == 0):
            continue
        await center1.add_order(Order(data1.at[i,'id'], (data1.at[i,'latitude'], data1.at[i,'longitude']), data1.at[i,'weight']))

    data2 = pd.read_csv('data/delivery_center2.csv', sep=';')
    for i in range (data2.shape[0]):
        if (i == 0):
            continue
        await center2.add_order(Order(data2.at[i,'id'], (data2.at[i,'latitude'], data2.at[i,'longitude']), data2.at[i,'weight']))

    print(center1.get_orders())  # Should print ["Order1"]
    print(center2.get_orders())  # Should print ["Order2"]

    """ # Stop the agents when done
    await center1.stop()
    await center2.stop() """

# Run the main function
asyncio.run(main())









        

""" class SenderAgent(Agent):
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
        self.add_behaviour(b)

class ReceiverAgent(Agent):
    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
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
        self.add_behaviour(b, template) """

import spade
import os
from drone import Drone

DATASET = os.path.join(os.getcwd(), "data", "Delivery_data.xlsx")

# center1 = loc1
# center2 = loc2
# center3 = loc3

# Um excel para cada centro/warehouse
# Several drones scattered around the enviroment
# Centers/warehouses send requests to the drones and drones decide what to accept


# def build_enviroment():


async def main():


    # O main deve criar os agentes
    
    drone = Drone("admin@leandro", "admin",velocity=1,capacity=2,autonomy=3)

    await drone.start(auto_register=True)
    print("Drone started")

    # senderagent = SenderAgent("dummy@leandro", "dummy")
    # await senderagent.start(auto_register=True)
    # print("Sender started")

    await spade.wait_until_finished(drone)
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
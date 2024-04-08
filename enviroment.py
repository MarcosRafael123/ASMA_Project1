import spade
import os
import csv
import utils
from drone import Drone
from center import Center
from order import Order

DATA_DIR = "data"
DRONE_DATA = os.path.join(os.getcwd(), DATA_DIR, "delivery_drones.csv")

# XMPP account details
username = "admin"
password = "admin"
hostname = "leandro"


# center1 = loc1
# center2 = loc2
# center3 = loc3

# Um excel para cada centro/warehouse
# Several drones scattered around the enviroment
# Centers/warehouses send requests to the drones and drones decide what to accept


# def build_enviroment():


def build_droneAgents():
    droneAgents = []
    with open(DRONE_DATA, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile,delimiter=';')
        next(csvreader)  # Skip the header row
        for row in csvreader:
            id = row[0]
            capacity = int(row[1][:(len(row[1])-2)])
            autonomy = int(row[2][:(len(row[2])-2)])
            velocity = int(row[3][:(len(row[3])-3)])
            init_pos = row[4]

            new_drone = Drone(f"{id}@{hostname}", password, id,velocity=velocity,capacity=capacity,autonomy=autonomy,initial_pos=init_pos)
            droneAgents.append(new_drone)
    return droneAgents


def build_centerAgents(files):
    centerAgents = {}

    for file in files:
        with open(file, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile,delimiter=';')
            next(csvreader)  # Skip the header row

            # Center Data
            row = next(csvreader)
            id = row[0]
            lat = float(row[1].replace(',', '.'))
            long = float(row[2].replace(',', '.'))
            new_center = Center(f"{id}@{hostname}", password, id, pos=(lat,long))
            print(id)

            # Center Orders Data
            for row in csvreader:

                ord_id = row[0]
                ord_lat = float(row[1].replace(',', '.'))
                ord_long = float(row[2].replace(',', '.'))
                ord_weight = int(row[3])
                ord_dest=(ord_lat,ord_long)
                
                order = Order(id=ord_id, destination=ord_dest, weight=ord_weight)

                new_center.add_order(order)
            print(len(new_center.get_orders()))
            
        centerAgents[id] = new_center

    return centerAgents

def build_enviroment():

    center_files = []
    csv_data_files = utils.find_files(DATA_DIR, ".csv")
    for file in csv_data_files:
        if file[:(len(file)-4)] == 'delivery_drones':
            continue
        file = os.path.join(os.getcwd(), DATA_DIR, file)
        center_files.append(file)

    centerAgents = build_centerAgents(center_files)
    print(centerAgents)
    # print(len(centerAgents[0].get_orders()))
    print(len(centerAgents['center2'].get_orders()))
    droneAgents = build_droneAgents()

    return None



async def main():


    build_enviroment()

    # O main deve criar os agentes
    
    # drone = Drone("admin@leandro", "admin",velocity=1,capacity=2,autonomy=3)

    # await drone.start(auto_register=True)
    # print("Drone started")

    # senderagent = SenderAgent("dummy@leandro", "dummy")
    # await senderagent.start(auto_register=True)
    # print("Sender started")

    # await spade.wait_until_finished(drone)
    # print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
import spade
import asyncio
import os
import csv
import utils
from drone import Drone
from center import Center
from order import Order

DATA_DIR = "data"
DRONE_DATA = os.path.join(os.getcwd(), DATA_DIR, "delivery_drones.csv")

# XMPP Host name
hostname = "localhost"


def build_droneAgents(centerAgents):
    droneAgents = {}
    with open(DRONE_DATA, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile,delimiter=';')
        next(csvreader)  # Skip the header row
        for row in csvreader:
            id = row[0]
            capacity = int(row[1][:(len(row[1])-2)])
            autonomy = int(row[2][:(len(row[2])-2)])
            velocity = int(row[3][:(len(row[3])-3)])

            init_pos = centerAgents[row[4]].pos

            new_drone = Drone(f"{id}@{hostname}", id, id,velocity=velocity,capacity=capacity,autonomy=autonomy,initial_pos=init_pos)
            droneAgents[id] = new_drone
    return droneAgents


def build_centerAgents(files):
    centerAgents = {}

    for file in files:
        with open(file, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile,delimiter=';')
            next(csvreader)  # Skip the header row

            # Center Data
            center_data = next(csvreader)
            id = center_data[0]
            lat = float(center_data[1].replace(',', '.'))
            long = float(center_data[2].replace(',', '.'))
            new_center = Center(f"{id}@{hostname}", id, id, pos=(lat,long))

            # Center Orders Data
            for row in csvreader:

                ord_id = row[0]
                ord_lat = float(row[1].replace(',', '.'))
                ord_long = float(row[2].replace(',', '.'))
                ord_weight = int(row[3])
                ord_center = id
                ord_dest = (ord_lat,ord_long)
                
                order = Order(id=ord_id, center=ord_center, destination=ord_dest, weight=ord_weight)

                new_center.add_order(order)

            csvfile.close()
        centerAgents[id] = new_center
            

    return centerAgents

def build_enviroment():

    # Get all the files related to centers
    center_files = []
    csv_data_files = utils.find_files(DATA_DIR, ".csv")
    for file in csv_data_files:
        if file[:(len(file)-4)] == 'delivery_drones':
            continue
        file = os.path.join(os.getcwd(), DATA_DIR, file)
        center_files.append(file)

    # Build the center agents according to data on the files
    centerAgents = build_centerAgents(center_files)

    # Build drone agents
    droneAgents = build_droneAgents(centerAgents)

    return (centerAgents, droneAgents)



async def main():


    (centerAgents, droneAgents) = build_enviroment()

    print("Starting agents")

    for drone in droneAgents.values():
        drone.setCenters(centerAgents)

    # Start all drone agents concurrently
    drone_starts = [droneAgents[drone_id].start(auto_register=True) for drone_id in droneAgents]
    await asyncio.gather(*drone_starts)
    droneAgents[list(droneAgents.keys())[0]].web.start(hostname="127.0.0.1", port="10000")

    for center in centerAgents.values():
        center.setDrones(droneAgents.keys())

    # Start all center agents concurrently
    center_starts = [centerAgents[center_id].start(auto_register=True) for center_id in centerAgents]
    await asyncio.gather(*center_starts)
    centerAgents[list(centerAgents.keys())[0]].web.start(hostname="127.0.0.1", port="10001")


    await spade.wait_until_finished(drone)
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
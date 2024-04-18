import math
import os

def haversine(pos1, pos2):
    """
    Calculate distance between two points
    on the Earth's surface using the Haversine formula.
    
    Parameters:
        pos1: Tuple containing latitude and longitude of point 1 (in degrees)
        pos2: Tuple containing latitude and longitude of point 2 (in degrees)
        
    Returns:
        Distance between the two points in meters.
    """
    lat1, lon1 = pos1
    lat2, lon2 = pos2
    
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Calculate the distance
    distance = R * c
    return distance*1000


def find_files(directory, extension):
    """
    Search for files with a specific extension in a directory and its subdirectories.

    Parameters:
        directory (str): The directory to search in.
        extension (str): The file extension to search for (e.g., '.txt', '.jpg').

    Returns:
        List of file paths matching the specified extension.
    """
    files = []

    # Walk through the directory tree
    for root, _, dir_files in os.walk(directory):
        for file in dir_files:
            # Check if the file has the specified extension
            if file.endswith(extension):
                # Append file name
                files.append(file)

    return files
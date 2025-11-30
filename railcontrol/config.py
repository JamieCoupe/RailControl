import os

# Create context data path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT, "data")

#Default Files
default_route_file = os.path.join(DATA_PATH, 'passenger_routes.yml')


#Timetables
dwell_safety_buffer_seconds = 10
block_occupancy_buffer = 1
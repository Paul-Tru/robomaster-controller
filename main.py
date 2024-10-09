import os
import setup
import robot_controll as rc
import vars

import controller
import threading
import asyncio

# Install required packages if not available
try:
    import customtkinter as ctk
    import configparser
    from PIL import Image
except ImportError as e:
    print(f"Error: {e}\nInstalling required packages...")
    os.system("pip install -r requirements.txt")
    import customtkinter as ctk
    import configparser
    from PIL import Image

config = configparser.ConfigParser()
config.read("config.ini")

rob_ip = config["IP"]["rob"]
pc_ip = config["IP"]["pc"]

if not config["GENERAL"]["debug"]:
    from robomaster import robot, camera
    robot.config.ROBOT_IP_STR = rob_ip
    robot.config.LOCAL_IP_STR = pc_ip
    vars.ep_robot = robot.Robot()
    vars.ep_robot.initialize(conn_type="sta")
    vars.ep_camera = vars.ep_robot.camera
    vars.ep_camera.start_video_stream(display=False)

# Function to run the async joystick reader in a separate thread
def run_joystick_reader():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(controller.read())  # Assuming read() is your async function

# Create and start the thread for joystick reading
joystick_thread = threading.Thread(target=run_joystick_reader)
joystick_thread.start()

# Start the main setup
setup.Setup()
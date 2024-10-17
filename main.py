import time
import configparser
from CTkMessagebox import CTkMessagebox
import threading
import asyncio
from PIL import Image
import cv2

import setup
import gui
import controller
import robot_controll as rc
import vars

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")

rob_ip = config["IP"]["rob"]
pc_ip = config["IP"]["pc"]

# Initialize robot if not in debug mode
if config["GENERAL"].getboolean("debug") is False:
    try:
        from robomaster import robot
        robot.config.ROBOT_IP_STR = rob_ip
        robot.config.LOCAL_IP_STR = pc_ip
        ep_robot = robot.Robot()
        ep_robot.initialize(conn_type="sta")
        ep_camera = ep_robot.camera
        ep_camera.start_video_stream(display=False)
        ep_sensor = ep_robot.sensor
        ep_chassis = ep_robot.chassis

        # Make variables global
        vars.ep_chassis = ep_chassis
        vars.ep_sensor = ep_sensor
        vars.ep_robot = ep_robot

        # Callback to update distance
        def distance(value):
            vars.distance = value[0]/10
        ep_sensor.sub_distance(freq=10, callback=distance)

    except Exception as e:
        CTkMessagebox(setup.app, title="Error", message=str(e), icon="cancel")

def run_joystick_reader():
    """Makes async controller function runnable in sync function."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(controller.read())

# Start the joystick reader thread
joystick_thread = threading.Thread(target=run_joystick_reader)
joystick_thread.start()

def run_guis():
    """Makes async GUI functions runnable in sync function."""
    setup.Setup()  # Start the setup GUI
    gui.MainGui()  # Start the main GUI

def update_frame():
    while True:
        """Update the video frame."""
        if config["GENERAL"].getboolean("debug") is False:
            # Get the current frame from the robot
            img = ep_camera.read_cv2_image(strategy="newest")
            # Convert the frame to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)  # Convert to PIL image
            
            vars.ep_camera = img_pil

            time.sleep(0.02)

# Start the camera frame update thread
camera_thread = threading.Thread(target=update_frame)
camera_thread.start()

rc_thread = threading.Thread(target=rc.main)
rc_thread.start()

run_guis()

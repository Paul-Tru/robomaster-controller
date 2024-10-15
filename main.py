import configparser
from CTkMessagebox import CTkMessagebox
import threading
import asyncio
from PIL import Image
import cv2

import setup
import robot_controll as rc
import controller
import vars

config = configparser.ConfigParser()
config.read("config.ini")

rob_ip = config["IP"]["rob"]
pc_ip = config["IP"]["pc"]

if not config["GENERAL"]["debug"]:
    try:
        from robomaster import robot
        robot.config.ROBOT_IP_STR = rob_ip
        robot.config.LOCAL_IP_STR = pc_ip
        ep_robot = robot.Robot()
        ep_robot.initialize(conn_type="sta")
        ep_camera = vars.ep_robot.camera
        ep_camera.start_video_stream(display=False)
        ep_sensor = ep_robot.sensor

        # make variables global
        vars.ep_sensor = ep_sensor
        vars.ep_robot = ep_robot
        #vars.ep_camera = ep_camera

        def distance(value):
            vars.distance = value
        ep_sensor.sub_distance(freq=10, callback=distance)

    except Exception as e:
        CTkMessagebox(title="Error", message=e, icon="cancel")

def run_joystick_reader():
    """makes async controller function runnable in sync function"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(controller.read())

def update_frame():
    """update the video frame"""
    if not config["GENERAL"]["debug"]:
        # get the current frame from the robot
        img = ep_camera.read_cv2_image(strategy="newest")
        # Convert the frame to RGB (OpenCV uses BGR by default)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)  # Convert to PIL image


        vars.ep_camera = img_pil


# Create and start the thread for joystick reading
joystick_thread = threading.Thread(target=run_joystick_reader)
joystick_thread.start()

# Create and start the thread for joystick reading
robot_thread = threading.Thread(target=rc.main)
robot_thread.start()

# Start the main setup gui
setup.Setup()
import os

import configparser
import customtkinter as ctk
from PIL import Image
import threading
import asyncio

import setup
import robot_controll as rc
import controller
import vars

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

def run_joystick_reader():
    """makes async controller function runable in sync funtion"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(controller.read())

# Create and start the thread for joystick reading
joystick_thread = threading.Thread(target=run_joystick_reader)
joystick_thread.start()

# Start the main setup gui
setup.Setup()
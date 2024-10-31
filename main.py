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
import detect_person

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")

rob_ip = config["IP"]["rob"]
pc_ip = config["IP"]["pc"]

# Initialize robot if not in debug mode
if config["GENERAL"].getboolean("debug") is False:
    try:
        from robomaster import robot, vision, led
        robot.config.ROBOT_IP_STR = rob_ip
        robot.config.LOCAL_IP_STR = pc_ip
        ep_robot = robot.Robot()
        ep_robot.initialize(conn_type="sta")
        ep_vision = ep_robot.vision
        ep_camera = ep_robot.camera
        ep_camera.start_video_stream(display=False)
        result = ep_vision.sub_detect_info(name="person", callback=detect_person.on_detect_person)
        ep_sensor = ep_robot.sensor
        ep_chassis = ep_robot.chassis
        ep_led = ep_robot.led
        ep_battery = ep_robot.battery

        # Make variables global
        vars.ep_chassis = ep_chassis
        vars.ep_sensor = ep_sensor
        vars.ep_robot = ep_robot
        vars.ep_led = ep_led
        vars.ep_battery = ep_battery
        vars.result = result
        vars.led = led

        vars.ep_led.set_led(comp=vars.led.COMP_ALL,
                            r=0, g=5, b=5, 
                            effect=vars.led.EFFECT_ON)

        # Callback to update distance
        def distance(value):
            vars.distance = value[0]/10
        ep_sensor.sub_distance(freq=10, callback=distance)

        def battery(value):
            vars.battery = value

        ep_battery.sub_battery_info(freq=5, callback=battery)

    except Exception as e:
        CTkMessagebox(title="Error", message=str(e), icon="cancel")

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
    #setup.Setup()  # Start the setup GUI
    gui.MainGui()  # Start the main GUI

def update_frame():
    while True:
        persons = vars.persons
        """Update the video frame."""
        if not config["GENERAL"].getboolean("debug"):
            # Get the current frame from the robot
            img_camera = ep_camera.read_cv2_image(strategy="newest")
            img = img_camera.copy()  # Make a copy of the camera image for processing
                        
            # Draw rectangles around detected persons
            for person in persons:
                cv2.rectangle(img, person.pt1, person.pt2, (255, 255, 255), 2)

            # Convert the frame to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)  # Convert to PIL image
            
            # Store the image with rectangles in vars.camera
            vars.ep_camera = img_pil
            
            time.sleep(0.02)

# Start the camera frame update thread
camera_thread = threading.Thread(target=update_frame)
camera_thread.start()

rc_thread = threading.Thread(target=rc.main)
rc_thread.start()

run_guis()

def stop_program():
    """stop everything its doing"""
    vars.result = ep_vision.unsub_detect_info(name="person")
    cv2.destroyAllWindows()
    vars.ep_camera.stop_video_stream()
    vars.ep_led.set_led(comp=vars.led.COMP_ALL, 
                        effect=vars.led.EFFECT_OFF)
    vars.ep_robot.close()
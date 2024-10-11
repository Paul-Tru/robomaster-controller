import pygame
import configparser
from CTkMessagebox import CTkMessagebox
import asyncio

import vars

# read config
config = configparser.ConfigParser()
config.read("config.ini")

# Get values
max_speed = int(config["ROBOT"]["max_speed"])
threshold = int(config["CONTROLLER"]["threshold"])

# Initialize pygame and joystick module
pygame.init()
pygame.joystick.init()

async def read():
    """read the values from the controller and store it into vars"""
    num_joysticks = pygame.joystick.get_count()

    # Check if a controller is connected
    if num_joysticks > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        clock = pygame.time.Clock()

        # Print the joystick's name
        name = joystick.get_name()
        print("Joystick name:", name)

        # Loop to read inputs
        while True:
            clock.tick(int(config["CONTROLLER"]["repeats_second"]))  # Set the loop to run at the configured rate

            # Process events
            for event in pygame.event.get():
                # process joystick
                if event.type == pygame.JOYAXISMOTION:
                    # calculate joystick value
                    value = round(event.value * max_speed)
                    value = -value  # Invert the axis if needed
                    trigger = int(config["CONTROLLER"]["trigger"])
                    # continue only when value is over threshold
                    if value >= threshold or value <= -threshold:
                        axis = event.axis
                        print(f"Axis {event.axis} value: {value}")
                        if axis == 1:
                            # left joystick y value
                            vars.joy_l_y = value
                        elif axis == 0:
                            # left joystick x value
                            vars.joy_l_x = value
                        elif axis == 3:
                            # right joystick x value
                            vars.joy_r_y = value
                        elif axis == 2:
                            # left joystick y value
                            vars.joy_r_x = value
                        # calculate trigger value
                        elif axis == 4:  # trigger left
                            value = round(-value * trigger)
                            value = round((-value + trigger) / 2)
                            vars.tr_l = value
                        elif axis == 5:  # trigger right
                            value = round(-value * trigger)
                            value = round((-value + trigger) / 2)
                            vars.tr_r = value
                        else:
                            # reset values
                            vars.joy_l_x = 0
                            vars.joy_l_y = 0

                            vars.joy_r_x = 0
                            vars.joy_r_y = 0

                            vars.tr_l = 0
                            vars.tr_r = 0

                button_states = {}

                if event.type == pygame.JOYBUTTONDOWN:
                    # change variable in vars.py to True
                    button_name = f"vars.btn_{event.button}"
                    button_states[button_name] = True
                    print(f"Button {event.button} pressed")

                if event.type == pygame.JOYBUTTONUP:
                    # change variable in vars.py to False
                    setattr(vars, f'btn_{event.button}', False)
                    print(f"Button {event.button} released")

                elif event.type == pygame.JOYHATMOTION:
                    print(f"Hat {event.hat} value: {event.value}")

    else:
        # handle non-successful connection
        print("No joysticks connected")
        show_warning()

def quit():
    """stop controller program"""
    pygame.quit()

def run_async_read():
    """make the async function runnable with sync function"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read())


def show_warning():
    """Show retry/cancel warning when controller not connected"""
    msg = CTkMessagebox(title="Controller", message="Unable to connect!",
                        icon="warning", option_1="Cancel", option_2="Retry")

    if msg.get() == "Retry":
        run_async_read()
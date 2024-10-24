import pygame
import configparser

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

def read():
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
        vars.controller = name

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
                            value = round((round(-value) + max_speed) / 2)
                            print(value)
                            vars.tr_l = value
                        elif axis == 5:  # trigger right
                            value = round((round(-value) + max_speed) / 2)
                            print(value)
                            vars.tr_r = value
                    else:
                        # reset values
                        vars.motor_bl = 0
                        vars.motor_br = 0
                        vars.motor_fl = 0
                        vars.motor_fr = 0

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
                    #(-1, 1) (0, 1) (1, 1)
                    #(-1, 0) (0, 0) (1, 0)
                    #(-1, 0) (0, -1) (1, -1)
                    hat = event.value
                    value = vars.tr_r
                    print(f"Hat value: {hat}")
                    if hat == (-1, 0):
                        vars.motor_fl, vars.motor_fr = -value, value
                        vars.motor_bl, vars.motor_br = value, -value

                print(button_states)

    else:
        # handle non-successful connection
        print("No joysticks connected")

def quit():
    """stop controller program"""
    pygame.quit()
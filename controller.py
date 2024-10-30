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
    """Read the values from the controller and store it into vars."""
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

        # Initialize hat and joystick values
        hat_position = (0, 0)
        right_trigger_value = 0
        left_trigger_value = 0

        # Loop to read inputs
        while True:
            clock.tick(int(config["CONTROLLER"]["repeats_second"]))  # Set the loop to run at the configured rate

            # Process events
            for event in pygame.event.get():
                # Handle hat motion first
                if event.type == pygame.JOYHATMOTION:
                    hat_position = event.value
                    #print(f"Hat value: {hat_position}")

                # Process joystick movement for right trigger
                if event.type == pygame.JOYAXISMOTION:
                    value = round(event.value * max_speed)
                    value = -value  # Invert the axis if needed

                    # Continue only when value is over threshold
                    if value >= threshold or value <= -threshold:
                        axis = event.axis
                        if axis == 5:  # right trigger
                            right_trigger_value = round((round(-value) + max_speed) / 2)
                            vars.tr_r = right_trigger_value

                        if axis == 4:  # left trigger
                            left_trigger_value = round((round(-value) + max_speed) / 2)
                            vars.tr_l = left_trigger_value


                # Reset values if the trigger is not pressed enough
                if event.type == pygame.JOYAXISMOTION and abs(value) < threshold:
                    right_trigger_value = 0
                    left_trigger_value = 0
                    vars.tr_r = 0

                # Process button events
                button_states = {}

                if event.type == pygame.JOYBUTTONDOWN:
                    button_name = f"btn_{event.button}"
                    button_states[button_name] = True
                    setattr(vars, button_name, True)  # Update button state
                    print(f"Button {event.button} pressed")

                if event.type == pygame.JOYBUTTONUP:
                    setattr(vars, f'btn_{event.button}', False)
                    print(f"Button {event.button} released")

            # Output the current hat and right trigger value
            vars.trigger_hat = hat_position, right_trigger_value, left_trigger_value

    else:
        # Handle non-successful connection
        print("No joysticks connected")


def quit():
    """stop controller program"""
    pygame.quit()
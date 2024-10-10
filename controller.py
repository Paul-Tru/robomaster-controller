import pygame
import configparser
import vars
import asyncio

config = configparser.ConfigParser()
config.read("config.ini")
max_speed = int(config["ROBOT"]["max_speed"])  # Scaling for joystick axes
threshold = int(config["CONTROLLER"]["threshold"])  # Threshold to consider joystick movement

# Initialize pygame and joystick module
pygame.init()
pygame.joystick.init()

async def read():
    num_joysticks = pygame.joystick.get_count()

    # Check if a controller is connected
    if num_joysticks > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

        clock = pygame.time.Clock()

        # Print the joystick's name
        name = joystick.get_name()
        print("Joystick name:", name)
        config["CONTROLLER"]["name"] = name

        # Loop to read inputs
        while True:
            clock.tick(int(config["CONTROLLER"]["repeats_second"]))  # Set the loop to run at the configured rate

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    value = round(event.value * max_speed)
                    value = -value  # Invert the axis if needed
                    MAX = int(config["ROBOT"]["turn_speed"])
                    if value >= threshold or value <= -threshold:
                        axis = event.axis
                        print(f"Axis {event.axis} value: {value}")
                        if axis == 1:
                            vars.joy_l_y = value
                        elif axis == 0:
                            vars.joy_l_x = value
                        elif axis == 3:
                            vars.joy_r_y = value
                        elif axis == 2:
                            vars.joy_r_x = value
                        elif axis == 4:  # Turn left
                            value = round(-value * MAX)
                            value = round((-value + MAX) / 2)  # Map value to [0, 1000]
                            vars.tr_l = value
                        elif axis == 5:  # Turn right
                            value = round(-value * MAX)
                            value = round((-value + MAX) / 2)
                            vars.tr_r = value
                        else:
                            vars.joy_l_x = 0
                            vars.joy_l_y = 0

                            vars.joy_r_x = 0
                            vars.joy_r_y = 0

                            vars.tr_l = 0
                            vars.tr_r = 0

                button_states = {}

                if event.type == pygame.JOYBUTTONDOWN:
                    button_name = f"vars.btn_{event.button}"  # Construct button name directly
                    button_states[button_name] = True
                    print(f"Button {event.button} pressed")

                if event.type == pygame.JOYBUTTONUP:
                    #button_name = f"vars.btn_{event.button}"  # Construct button name directly for release
                    #button_states[button_name] = False  # Set the button state to released
                    setattr(vars, f'btn_{event.button}', False)
                    print(f"Button {event.button} released")



                elif event.type == pygame.JOYHATMOTION:
                    print(f"Hat {event.hat} value: {event.value}")

    else:
        print("No joysticks connected")
        config["CONTROLLER"]["name"] = "None"

def quit():
    pygame.quit()

# Function to run the async read function
def run_async_read():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read())

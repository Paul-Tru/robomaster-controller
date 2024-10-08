import pygame
import configparser

class ReadController:
    def __init__(self):
        self.config = configparser.ConfigParser()

        self.config.read("config.ini")
        self.max = int(self.config["CONTROLLER"]["max_speed"] ) # Scaling for joystick axes
        self.threshold = int(self.config["CONTROLLER"]["threshold"])  # Threshold to consider joystick movement

        # Initialize pygame and joystick module
        pygame.init()
        pygame.joystick.init()

    def read(self):
        num_joysticks = pygame.joystick.get_count()

        # Check if a controller is connected
        if num_joysticks > 0:
            # Get the first joystick (assuming it's the Xbox controller)
            joystick = pygame.joystick.Joystick(0)
            joystick.init()

            clock = pygame.time.Clock()

            # Print the joystick's name
            name = joystick.get_name()
            print("Joystick name:", name)
            self.config["CONTROLLER"]["name"] = name

            # Loop to read inputs
            while True:
                clock.tick(int(self.config["CONTROLLER"]["repeats_second"]))  # Set the loop to run at 60 FPS

                # Process events
                for event in pygame.event.get():
                    if event.type == pygame.JOYAXISMOTION:
                        # Process axis motion (e.g., analog sticks)
                        value = round(event.value * self.max)
                        value = -value  # Invert the axis if needed
                        if value >= self.threshold or value <= -self.threshold:
                            print(f"Axis {event.axis} value: {value}")
                            speed = [event.axis, value]
                            print(f"Updated speed: {speed}")

                    elif event.type == pygame.JOYBUTTONDOWN:
                        # Print the button number and that it was pressed
                        print(f"Button {event.button} pressed")

                    elif event.type == pygame.JOYBUTTONUP:
                        # Print the button number and that it was released
                        print(f"Button {event.button} released")

                    elif event.type == pygame.JOYHATMOTION:
                        # Print the hat (D-pad) and its value
                        print(f"Hat {event.hat} value: {event.value}")

        else:
            print("No joysticks connected")
            self.config["CONTROLLER"]["name"] = "None"

    def quit(self):
        pygame.quit()
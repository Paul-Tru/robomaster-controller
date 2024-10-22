import configparser
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

import vars

class MainGui:
    """Gui to see the robot camera and start drag race"""
    def __init__(self):
        # read config.ini
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        # get debug from config.ini
        self.debug = self.config.getboolean("GENERAL", "debug")

        # set values for ctk window
        self.app = ctk.CTk()
        ctk.set_appearance_mode(self.config["GUI"]["appearance"])
        self.app.geometry(self.config["GUI"]["geometry_main"])
        if not self.debug:
            self.app.title("Titan")
        else:
            self.app.title("Titan (Debug)")
        self.frame_pad = self.config["GUI"]["frame_pad"]
        self.frame_font = eval(self.config["GUI"]["frame_font"])
        self.comp_pad = self.config["GUI"]["component_pad"]

        # call functions
        self.video()
        self.left_frame()
        self.right_frame()

        self.app.mainloop()

    def left_frame(self):
        left_frame = ctk.CTkFrame(self.app)
        left_frame.grid(row=0, column=0,
                        padx=self.frame_pad, pady=self.frame_pad)

        def show_motor_value():
            """Shows value of each motor"""
            motor_frame = ctk.CTkFrame(left_frame)
            motor_frame.grid(row=0, column=0, padx=self.comp_pad, pady=self.comp_pad, sticky="nsew")

            # Configure grid to make motor_frame expand
            left_frame.grid_rowconfigure(0, weight=1)
            left_frame.grid_columnconfigure(0, weight=1)

            label = ctk.CTkLabel(motor_frame, text="Motors", font=self.frame_font)
            label.grid(columnspan=2, padx=self.comp_pad, pady=self.comp_pad)

            def make_progressbar():
                """Make progressbars to show values from each wheel"""
                row, column = 1, 0
                progressbars = []

                # Configure grid inside motor_frame to expand and fill space
                motor_frame.grid_rowconfigure(1, weight=1)
                motor_frame.grid_rowconfigure(2, weight=1)
                motor_frame.grid_columnconfigure(0, weight=1)
                motor_frame.grid_columnconfigure(1, weight=1)

                # Creating one progressbar for every wheel
                for i in range(4):
                    progressbar = ctk.CTkProgressBar(motor_frame, orientation="vertical")
                    progressbar.grid(row=row, column=column, padx=25, pady=self.comp_pad, sticky="nsew")
                    progressbars.append(progressbar)

                    column += 1
                    if column == 2:
                        row = 2
                        column = 0

                return progressbars

            progressbars = make_progressbar()

            def update():
                """updating values according to variables in vars.py"""
                max_speed = int(self.config["ROBOT"]["max_speed"])
                progressbars[0].set((vars.motor_fl + max_speed) / (max_speed*2))
                progressbars[1].set((vars.motor_fr + max_speed) / (max_speed*2))
                progressbars[2].set((vars.motor_bl + max_speed) / (max_speed*2))
                progressbars[3].set((vars.motor_br + max_speed) / (max_speed*2))

                motor_frame.after(5, update)

            update()

        def start_drag_race():
            frame = ctk.CTkFrame(left_frame)
            frame.grid(row=2, column=0, padx=self.comp_pad, pady=self.comp_pad)

            label = ctk.CTkLabel(frame, text="Drag Race")
            label.grid(row=0, column=0)

            stop_cntdw = False  # Flag to control countdown
            rp = 0  # Race progress counter

            # Function to reset the button and label after stopping or completing
            def reset_button():
                nonlocal stop_cntdw, rp
                stop_cntdw = False
                rp = 0
                button.configure(text="Go!", command=lambda: race(5))  # Reset command
                label.configure(text="Drag Race", font=("Arial", 15))

            def stop():
                nonlocal stop_cntdw
                stop_cntdw = True  # Set flag to stop the countdown
                label.configure(text="Stopped", font=("Arial", 25))  # Show stopped message
                frame.after(1000, reset_button)  # Wait a second before resetting

            def race(count):
                nonlocal stop_cntdw, rp
                if count >= 0 and not stop_cntdw:
                    if count % 2 == 0:
                        vars.ep_led.set_led(comp=vars.led.COMP_ALL,
                                            r=0, g=0, b=5, 
                                            effect=vars.led.EFFECT_ON)
                    else:
                        vars.ep_led.set_led(comp=vars.led.COMP_ALL,
                                            r=0, g=5, b=5, 
                                            effect=vars.led.EFFECT_ON)
                    button.configure(text="ABORT", command=stop)  # Change button to abort
                    label.configure(text=str(count), font=("Arial", 25, "bold"))
                    frame.after(1000, race, count - 1)  # Continue countdown
                elif stop_cntdw:
                    reset_button()  # Reset button and label after abort
                else:
                    vars.overwrite = True
                    label.configure(text="Go!", font=("Arial", 25, "bold"))  # Show go message
                    if rp == 0:
                        vars.ep_chassis.move(x=5, xy_speed=3.5).wait_for_completed()
                        vars.ep_chassis.move(x=5, xy_speed=3.5).wait_for_completed()
                        race(0)  # Start next countdown from 5
                    elif rp == 1:
                        race(2)  # Start next countdown from 3
                    elif rp == 2:
                        label.configure(text="Bringing back", font=("Arial", 15))  # Display bringing back
                        vars.ep_chassis.move(x=-5, xy_speed=1.5).wait_for_completed()
                        vars.ep_chassis.move(x=-5, xy_speed=1.5).wait_for_completed()
                        vars.overwrite = False
                        try:
                            vars.bring_back = False
                        except Exception as e:
                            CTkMessagebox(self.app,
                                        title="Drive",
                                        message=e,
                                        icon="warning")
                    rp += 1  # Increment race progress

            button = ctk.CTkButton(frame, text="Go!", command=lambda: race(5))  # Button setup
            button.grid(row=1, column=0)  # Adding button to the frame

        show_motor_value()
        start_drag_race()

    def video(self):
        """shows video preview or test picture"""
        frame = ctk.CTkFrame(self.app)
        frame.grid(row=0, column=2,
                   padx=self.comp_pad, pady=self.comp_pad,
                   sticky="n")

        self.video_label = ctk.CTkLabel(frame, text="",
                                        width=960, height=540)
        self.video_label.pack()

        def update_frame():
            """update the video frame"""
            if not self.debug:
                try:
                    imgtk = ctk.CTkImage(vars.ep_camera, size=(960, 540))  # Adjust the size as necessary

                    # Update the video label with the new frame
                    self.video_label.configure(image=imgtk, text="")
                    self.video_label.imgtk = imgtk  # Keep a reference to avoid garbage collection

                except:
                    # Display an error message or a placeholder image
                    self.video_label.configure(text="Error: unable to read video stream", fg_color="darkred")
            else:
                # show debug picture
                placeholder_imgtk = ctk.CTkImage(vars.test_png, size=(960, 540))
                self.video_label.configure(image=placeholder_imgtk)
                self.video_label.image = placeholder_imgtk

            # Call this function again after a delay (e.g., 100ms)
            self.video_label.after(100, update_frame)

        update_frame()

    def right_frame(self):
        right_frame = ctk.CTkFrame(self.app)
        right_frame.grid(row=0, column=3,
                         padx=self.frame_pad, pady=self.frame_pad,
                         sticky="n")

        def update_values():
            distance = vars.distance
            if distance <= int(self.config["ROBOT"]["max_distance"]):
                current_distance_frame.configure(fg_color="darkred")
            else:
                current_distance_frame.configure(fg_color="#2E2E2E")
                vars.motor_fl, vars.motor_fr = 0, 0
                vars.motor_bl, vars.motor_br = 0, 0
            current_distance_label.configure(text=f"{vars.distance}cm")

            right_frame.after(100, update_values)

        def distance_label():
            global current_distance_label, current_distance_frame
            """shows current distance from distance sensor"""
            current_distance_frame = ctk.CTkFrame(right_frame)
            current_distance_frame.grid(row=0, column=0,
                       padx=self.comp_pad, pady=self.comp_pad)

            label = ctk.CTkLabel(current_distance_frame, text="Distance")
            label.pack(padx=self.comp_pad, pady=(10, 0))

            current_distance_label = ctk.CTkLabel(current_distance_frame,
                                                  text="N/A", font=self.frame_font)
            current_distance_label.pack(padx=self.comp_pad, pady=self.comp_pad)

        def battery_label():
            """shows current battery level from the robot"""
            frame = ctk.CTkFrame(right_frame)
            frame.grid(row=0, column=1,
                       padx=(0, 10), pady=self.comp_pad)

            label = ctk.CTkLabel(frame,
                                 text="Battery")
            label.pack(padx=self.comp_pad, pady=(10,0))

            current_battery_label = ctk.CTkLabel(frame,
                                                 text="N/A", font=self.frame_font)
            current_battery_label.pack(padx=self.comp_pad, pady=self.comp_pad)

        battery_label()
        distance_label()
        update_values()

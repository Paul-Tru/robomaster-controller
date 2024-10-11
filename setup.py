import vars

import configparser
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import cv2

class Setup:
    """gui to make settings for the robot and controller
    and to test basic functionality"""

    def __init__(self):
        # read config.ini
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        
        # get debug from config.ini
        self.debug = self.config.getboolean("GENERAL", "debug")

        # set values for ctk window
        self.app = ctk.CTk()
        ctk.set_appearance_mode(self.config["GUI"]["appearance"])
        self.app.geometry(self.config["GUI"]["geometry"])
        if not self.debug:
            self.app.title("Titan Setup")
        else:
            self.app.title("Titan Setup (Debug)")
        self.frame_pad = self.config["GUI"]["frame_pad"]
        self.frame_font = eval(self.config["GUI"]["frame_font"])
        self.comp_pad = self.config["GUI"]["component_pad"]

        # list to update button values in a frame
        self.btn_label_ = []

        # calling functions
        self.ip_config()
        self.robot()
        self.debug_switch()
        self.tabview_frame()
        self.update_values()
        self.start_main_btn()
        self.app.mainloop()

    def save_config(self):
        """save values into config.ini after being changed"""
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def update_values(self):
        """updating values in progressbars from controller input"""

        # getting nessesary values from config file
        max_speed = int(self.config["ROBOT"]["max_speed"])
        trigger = int(self.config["CONTROLLER"]["trigger"])

        # Update the corresponding progress bar based on the name provided
        self.l_x_stick.set((vars.joy_l_x + max_speed) / (2 * max_speed))
        self.l_y_stick.set((vars.joy_l_y + max_speed) / (2 * max_speed))
        self.r_x_stick.set((vars.joy_r_x + max_speed) / (2 * max_speed))
        self.r_y_stick.set((vars.joy_r_y + max_speed) / (2 * max_speed))

        self.l_trigger.set(-(vars.tr_l + trigger) / (2 * trigger))
        self.r_trigger.set(-(vars.tr_r + trigger) / (2 * trigger))

        for i in range(12):
            value = getattr(vars, f'btn_{i}')
            label_text = f"{i}: {value}"
            self.btn_label_[i].configure(text=label_text)

        # updating every 10ms
        self.app.after(10, self.update_values)

    def ip_config(self):
        """frame to change connect settings"""

        # creating frame
        frame = ctk.CTkFrame(self.app)
        frame.grid(column=0, row=0, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        # creating label
        label = ctk.CTkLabel(frame, text="Wifi", font=self.frame_font)
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        # read values
        rob_ip_ini = self.config.get("IP", "rob", fallback="")
        pc_ip_ini = self.config.get("IP", "pc", fallback="")

        # create entrys for ip addresses
        self.entry_rob_ip = ctk.CTkEntry(frame, placeholder_text=rob_ip_ini)
        self.entry_rob_ip.pack(padx=self.comp_pad, pady=self.comp_pad)

        self.entry_pc_ip = ctk.CTkEntry(frame, placeholder_text=pc_ip_ini)
        self.entry_pc_ip.pack(padx=self.comp_pad, pady=self.comp_pad)

        # setting default connect status
        status = ctk.CTkLabel(frame, text="❌ Not Connected")
        status.pack(padx=self.comp_pad, pady=self.comp_pad)

        def get_values():
            """get values from entries and write them into config"""
            # get values
            rob_ip = self.entry_rob_ip.get()
            pc_ip = self.entry_pc_ip.get()
            if rob_ip is not None:
                # use entry input when not none and write it into config
                self.config["IP"]["rob"] = rob_ip
                self.config["IP"]["pc"] = pc_ip

            try:
                # import here to make it runnable in debug mode
                import robot_controll as rc

                # check if computer is connected to the robot
                check = rc.check_conn()

            except:
                check = False

            # change status
            if check:
                frame.configure(fg_color="#302c2c")
                status.configure(text="✅ Connected")
            elif self.debug:
                frame.configure(fg_color="#302c2c")
                status.configure(text="DEBUG")
            else:
                frame.configure(fg_color="darkred")
                status.configure(text="❌ Not Connected")

        # button to get the values from entry
        self.get_btn = ctk.CTkButton(frame, text="Get", command=get_values)
        self.get_btn.pack(padx=15, pady=10)

    def debug_switch(self):
        """turn debug mode on or off"""
        frame = ctk.CTkFrame(self.app)
        frame.grid(column=0, row=1, sticky="n", padx=self.comp_pad, pady=self.comp_pad)

        def change():
            """change the config according to value"""
            value = switch.get()
            if value == 0:
                self.config["GENERAL"]["debug"] = "True"
            else:
                self.config["GENERAL"]["debug"] = "False"
            self.save_config()
            print(value)

        # create switch
        switch = ctk.CTkSwitch(frame, text="Debug", command=change)
        switch.pack(padx=self.comp_pad, pady=self.comp_pad)

        # set switch to current state of debug
        if self.debug:
            switch.select()
        else:
            switch.deselect()

    def robot(self):
        """show information about the robot"""

        # crete frame on the right
        self.right_frame = ctk.CTkFrame(self.app)
        self.right_frame.grid(column=3, row=0, rowspan=2, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        # create title
        label = ctk.CTkLabel(self.right_frame, text="Robot", font=self.frame_font)
        label.grid(row=0, padx=self.comp_pad, pady=self.comp_pad)

        def max_speed():
            """create slider in frame to change the max speed"""
            """in repeats per minute"""
            
            # create frame
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=1, padx=self.comp_pad, pady=self.comp_pad)

            # get value
            max_speed = self.config["ROBOT"]["max_speed"]

            # add text
            label = ctk.CTkLabel(frame, text=f"Max Speed: {max_speed} rpm")
            label.grid(padx=self.comp_pad, pady=self.comp_pad)


            def get(value):
                """get value from slider"""
                """shows it and writes it into config"""

                max_speed = int(value)  # Slider value is passed automatically
                label.configure(text=f"Max Speed: {max_speed} rpm")  # Update label with formatted value

                # save value
                self.config["ROBOT"]["max_speed"] = str(max_speed)
                self.save_config()
                print("Max Speed: " + str(max_speed))

            # configure slider
            self.max_speed_slider = ctk.CTkSlider(frame, number_of_steps=10, to=1000, command=get)
            self.max_speed_slider.grid(padx=self.comp_pad, pady=self.comp_pad)
            self.max_speed_slider.set(int(max_speed))

        def max_distance():
            """creates frame to change value"""
            """when to stop in front of an obstacle"""

            # create frame
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=2, padx=self.comp_pad, pady=self.comp_pad)

            # get value
            max_distance = self.config["ROBOT"]["max_distance"]

            # create text
            label = ctk.CTkLabel(frame, text=f"Max Distance: {max_distance} cm")
            label.grid(padx=self.comp_pad, pady=self.comp_pad)

            def get(value):
                """get value from sliders, print it out and change config"""
                max_distance = int(value)  # Slider value is passed automatically
                label.configure(text=f"Max Distance: {max_distance} cm")  # Update label with formatted value
                self.config["ROBOT"]["max_distance"] = str(max_distance)
                self.save_config()
                print("Max Speed: " + str(max_distance))

            # create slider
            slider = ctk.CTkSlider(frame, number_of_steps=6, to=300, command=get)
            slider.grid(padx=self.comp_pad, pady=self.comp_pad)
            slider.set(int(max_distance))

        def curr_distance():
            """get current distance from distance sensor"""
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=3, sticky="nsew", padx=self.comp_pad, pady=self.comp_pad)

            label = ctk.CTkLabel(frame, text="Distance: N/A")
            label.grid(padx=self.comp_pad, pady=self.comp_pad)

            def update():
                """update distance label"""
                label.configure(text=f"Distance: {vars.distance} cm")
                frame.after(20, update)

            if not self.debug:
                update()

        def video():
            """shows video preview or test picture"""
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=4, padx=self.comp_pad, pady=self.comp_pad)

            self.video_label = ctk.CTkLabel(frame, text="")
            self.video_label.pack()

            def update_frame():
                """update the video frame"""
                if not self.debug:
                    # get the current frame from the robot
                    img = vars.ep_camera.read_cv2_image(strategy="newest")
                    try:
                        # Convert the frame to RGB (OpenCV uses BGR by default)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img_pil = Image.fromarray(img)  # Convert to PIL image

                        # Convert to CTkImage for display in CustomTkinter
                        imgtk = ctk.CTkImage(img_pil, size=(160, 90))  # Adjust the size as necessary

                        # Update the video label with the new frame
                        self.video_label.configure(image=imgtk)
                        self.video_label.imgtk = imgtk  # Keep a reference to avoid garbage collection

                    except:
                        # Display an error message or a placeholder image
                        self.video_label.configure(text="Error: unable to read video stream", fg="darkred")
                else:
                    # show debug picture
                    placeholder_imgtk = ctk.CTkImage(vars.test_png, size=(160, 90))
                    self.video_label.configure(image=placeholder_imgtk)
                    self.video_label.image = placeholder_imgtk

                # Call this function again after a delay (e.g., 100ms)
                self.video_label.after(100, update_frame)

            update_frame()

        max_speed()
        max_distance()
        curr_distance()
        video()

    def tabview_frame(self):
        """split controller and keyboard frame """
        self.tabview = ctk.CTkTabview(master=self.app)
        self.tabview.grid(column=1, columnspan=2, row=0, rowspan=3, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        self.tabview.add("Controller")  # add tab at the end
        self.tabview.add("Keyboard")  # add tab at the end
        self.tabview.set("Controller")  # set currently visible tab

        def controller():
            """shows information from controller"""
            # create frame
            self.controller_frame = ctk.CTkFrame(self.tabview.tab("Controller"))
            self.controller_frame.grid(padx=self.comp_pad, pady=self.comp_pad)

            # create label
            label = ctk.CTkLabel(self.controller_frame, text="Controller", font=self.frame_font)
            label.grid(column=0, columnspan=2, row=0, padx=self.comp_pad, pady=self.comp_pad)

            def threshold_slider():
                """create slider in frame to change and show joystick threshold"""
                # create frame
                frame = ctk.CTkFrame(self.controller_frame)
                frame.grid(column=0, row=1, sticky="n", padx=self.comp_pad, pady=self.comp_pad)

                # get values
                threshold = self.config["CONTROLLER"]["threshold"]
                max_speed = self.config["ROBOT"]["max_speed"]

                # calculate max slider value
                to = int(int(max_speed) / 2)

                # calculate steps that change the value by 50
                steps = int(to / 50)

                # calculate threshold percentage
                percent = round(int(threshold) / int(max_speed) * 100)

                # show results
                label = ctk.CTkLabel(frame, text=f"Threshold: {threshold}/{max_speed}\n\n"
                                                 f"{percent}%")
                label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                def get(threshold):
                    """update threshold frame"""
                    max_speed = self.config["ROBOT"]["max_speed"]
                    percent = round(int(threshold) / int(max_speed) * 100)
                    # update text
                    label.configure(text=f"Threshold: {threshold}/{max_speed}\n\n"
                                         f"{str(percent)}%")

                    # save to config
                    self.config["CONTROLLER"]["threshold"] = str(threshold)
                    self.save_config()

                    # configure slider
                    slider.configure(to=int(max_speed) / 2, number_of_steps=int(to / 50))
                    print("Threshold: " + str(threshold))

                # create slider
                slider = ctk.CTkSlider(frame, number_of_steps=steps, to=to, command=get)
                slider.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)
                slider.set(int(threshold))

            def buttons():
                """show buttons pressed in 2 columns in one frame"""
                # create frame
                buttons_frame = ctk.CTkFrame(self.controller_frame)
                buttons_frame.grid(column=1, row=1, sticky="ew", padx=self.comp_pad, pady=self.comp_pad)

                # Configure columns to ensure even spacing
                buttons_frame.grid_columnconfigure(0, weight=1)
                buttons_frame.grid_columnconfigure(1, weight=1)

                # Configure rows to ensure even spacing
                for i in range(6):
                    buttons_frame.grid_rowconfigure(i, weight=1)

                # create label for each button
                for i in range(12):
                    # create label with text
                    value = getattr(vars, f'btn_{i}')
                    label = ctk.CTkLabel(buttons_frame, text=f"{i}: N/A")
                    self.btn_label_.append(label) 

                    column = 0 if i < 6 else 1  # Use 0 for the first 6, 1 for the next 6
                    row = i if i < 6 else i - 6  # Adjust row index for the second column
                    label.grid(row=row, column=column, sticky="ew", padx=5, pady=5)  # Add padding for better spacing


            def joysticks():
                """show joystick values"""
                # create frame
                self.js_frame = ctk.CTkFrame(self.controller_frame)
                self.js_frame.grid(column=0, columnspan=2, row=2, padx=self.comp_pad, pady=self.comp_pad)

                # create label
                label = ctk.CTkLabel(self.js_frame, text="Joystick", font=self.frame_font)
                label.grid(column=0, columnspan=2, row=0, padx=self.comp_pad, pady=self.comp_pad)

                def create_joystick(side:str, column:int):
                    """Create joystick display for either left or right side"""
                    # Create frame
                    frame = ctk.CTkFrame(self.js_frame)
                    frame.grid(column=column, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    # Create title
                    label = ctk.CTkLabel(frame, text=side)
                    label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                    # Create x-level value progressbar
                    if side == "Left":
                        self.l_x_stick = ctk.CTkProgressBar(frame)
                        self.l_x_stick.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                        # Create y-level value progressbar
                        self.l_y_stick = ctk.CTkProgressBar(frame)
                        self.l_y_stick.grid(column=0, row=2, padx=self.comp_pad, pady=self.comp_pad)

                    elif side == "Right":
                        self.r_x_stick = ctk.CTkProgressBar(frame)
                        self.r_x_stick.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                        self.r_y_stick = ctk.CTkProgressBar(frame)
                        self.r_y_stick.grid(column=0, row=2, padx=self.comp_pad, pady=self.comp_pad)

                # Call for left joystick
                create_joystick("Left", 0)

                # Call for right joystick
                create_joystick("Right", 1)

            def trigger():
                """show trigger values"""
                self.trigger_frame = ctk.CTkFrame(self.controller_frame)
                self.trigger_frame.grid(column=0, columnspan=2, row=3, padx=self.comp_pad, pady=self.comp_pad)

                label = ctk.CTkLabel(self.trigger_frame, text="Trigger", font=self.frame_font)
                label.grid(column=0, columnspan=2, row=0, padx=self.comp_pad, pady=self.comp_pad)

                def trigger_create(side:str, column:int):
                    """Create trigger display for either left or right side"""
                    frame = ctk.CTkFrame(self.trigger_frame)
                    frame.grid(column=column, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    label = ctk.CTkLabel(frame, text=side)
                    label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                    if side == "Left":
                        self.l_trigger = ctk.CTkProgressBar(frame)
                        self.l_trigger.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    elif side == "Right":
                        self.r_trigger = ctk.CTkProgressBar(frame)
                        self.r_trigger.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                trigger_create("Left", 0)
                trigger_create("Right", 1)

            threshold_slider()
            buttons()
            joysticks()
            trigger()
        controller()

    def start_main_btn(self):
        """create button to start the main gui"""

        def start():
            """start main gui"""
            pass

        btn = ctk.CTkButton(self.app, text="Start", command=start)
        btn.grid(column=3, row=2)
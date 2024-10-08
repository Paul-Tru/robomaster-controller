import vars

import configparser
import customtkinter as ctk
from PIL import Image
import cv2

class Setup:
    """gui to make settings for the robot and controller"""
    """and to test basic functionality"""

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

        # calling functions
        self.ip_config()
        self.robot()
        self.debug_switch()
        self.tabview_frame()
        self.update_bars()
        self.start_main_btn()
        self.app.mainloop()

    def save_config(self):
        """save values into config.ini after being changed"""
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def update_bars(self):
        """updating values in progressbars from controller input"""

        # getting nessesary values from config file
        max_speed = int(self.config["ROBOT"]["max_speed"])
        turn_speed = int(self.config["ROBOT"]["turn_speed"])

        # Update the corresponding progress bar based on the name provided
        self.l_x_stick.set((vars.joy_l_x + max_speed) / (2 * max_speed))
        self.l_y_stick.set((vars.joy_l_y + max_speed) / (2 * max_speed))
        self.r_x_stick.set((vars.joy_r_x + max_speed) / (2 * max_speed))
        self.r_y_stick.set((vars.joy_r_y + max_speed) / (2 * max_speed))
        self.l_trigger.set(-(vars.tr_l + turn_speed) / (2 * turn_speed))
        self.r_trigger.set(-(vars.tr_r + turn_speed) / (2 * turn_speed))

        # updating every 10ms
        self.app.after(10, self.update_bars)

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
            """get values from entrys"""
            rob_ip = self.entry_rob_ip.get()
            pc_ip = self.entry_pc_ip.get()
            if rob_ip is not None:
                self.rob_ip = rob_ip
                self.pc_ip = pc_ip
            else:
                self.rob_ip = rob_ip_ini
                self.pc_ip = pc_ip_ini
                
            try:
                # import here to make it runable in debug mode
                import robot_controll as rc

                # check if computer is connected to the robot
                check = rc.check_conn(self.rob_ip, self.pc_ip)
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
            self.max_speed_slider = ctk.CTkSlider(frame, number_of_steps=10, to=5000, command=get)
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
                """get value from slider"""
                """print it out change config"""
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
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=3, sticky="nsew", padx=self.comp_pad, pady=self.comp_pad)

            label = ctk.CTkLabel(frame, text="Distance: N/A")
            label.grid(padx=self.comp_pad, pady=self.comp_pad)

            def update():
                label.configure(text=f"Distance: {vars.distance} cm")
                frame.after(20, update)

            if not self.debug:
                update()

        def video():
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=4, padx=self.comp_pad, pady=self.comp_pad)

            self.video_label = ctk.CTkLabel(frame, text="")
            self.video_label.pack()

            def update_frame():
                if not self.debug:
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
        self.tabview = ctk.CTkTabview(master=self.app)
        self.tabview.grid(column=1, columnspan=2, row=0, rowspan=3, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        self.tabview.add("Controller")  # add tab at the end
        self.tabview.add("Keyboard")  # add tab at the end
        self.tabview.set("Controller")  # set currently visible tab

        def controller():
            self.controller_frame = ctk.CTkFrame(self.tabview.tab("Controller"))
            self.controller_frame.grid(padx=self.comp_pad, pady=self.comp_pad)

            label = ctk.CTkLabel(self.controller_frame, text="Controller", font=self.frame_font)
            label.grid(column=0, columnspan=2, row=0, padx=self.comp_pad, pady=self.comp_pad)

            def threshold_slider():
                frame = ctk.CTkFrame(self.controller_frame)
                frame.grid(column=0, row=1, sticky="n", padx=self.comp_pad, pady=self.comp_pad)

                threshold = self.config["CONTROLLER"]["threshold"]
                max_speed = self.config["ROBOT"]["max_speed"]
                to = int(int(max_speed) / 2)
                steps = int(to / 50)

                percent = round(int(threshold) / int(max_speed) * 100)
                label = ctk.CTkLabel(frame, text=f"Threshold: {threshold}/{max_speed}\n\n"
                                                 f"{percent}%")
                label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                def get(value):
                    threshold = int(value)
                    max_speed = self.config["ROBOT"]["max_speed"]
                    percent = round(int(threshold) / int(max_speed) * 100)
                    label.configure(text=f"Threshold: {threshold}/{max_speed}\n\n"
                                         f"{str(percent)}%")
                    self.config["CONTROLLER"]["threshold"] = str(threshold)
                    self.save_config()
                    slider.configure(to=int(max_speed) / 2, number_of_steps=int(to / 50))
                    print("Threshold: " + str(threshold))

                slider = ctk.CTkSlider(frame, number_of_steps=steps, to=to, command=get)
                slider.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)
                slider.set(int(threshold))

            def buttons():
                buttons_frame = ctk.CTkFrame(self.controller_frame)
                buttons_frame.grid(column=1, row=1, padx=self.comp_pad, pady=self.comp_pad)

                a_frame = ctk.CTkFrame(buttons_frame)
                a_frame.grid(column=0, row=0, sticky="nsew")  # Use sticky to expand the frame

                b_frame = ctk.CTkFrame(buttons_frame)
                b_frame.grid(column=1, row=0, sticky="nsew")  # Use sticky to expand the frame

                # Configure rows and columns to ensure even spacing
                buttons_frame.grid_columnconfigure(0, weight=1)
                buttons_frame.grid_columnconfigure(1, weight=1)
                buttons_frame.grid_rowconfigure(list(range(6)), weight=1)  # Adjust weights for the first 6 rows
                buttons_frame.grid_rowconfigure(list(range(6, 12)), weight=1)  # Adjust weights for the second 6 rows

                for i in range(12):
                    value = getattr(vars, f'btn_{i}', None)  # Assuming btn_0, btn_1, ... are attributes of self
                    label_text = f"{i}: {value}" if value is not None else f"{i}: Not set"
                    label = ctk.CTkLabel(buttons_frame, text=label_text)

                    column = 0 if i < 6 else 1  # Use 0 for the first 6, 1 for the next 6
                    row = i if i < 6 else i - 6  # Row remains the same for first 6, adjusted for the second 6
                    label.grid(row=row, column=column, sticky="ew")  # Expand label to fill available space

                self.controller_frame.after(20, buttons)

            def joysticks():
                self.js_frame = ctk.CTkFrame(self.controller_frame)
                self.js_frame.grid(column=0, columnspan=2, row=2, padx=self.comp_pad, pady=self.comp_pad)

                label = ctk.CTkLabel(self.js_frame, text="Joystick", font=self.frame_font)
                label.grid(column=0, columnspan=2, row=0, padx=self.comp_pad, pady=self.comp_pad)

                def joystick_left():
                    frame = ctk.CTkFrame(self.js_frame)
                    frame.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    label = ctk.CTkLabel(frame, text="Left")
                    label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                    self.l_x_stick = ctk.CTkProgressBar(frame)
                    self.l_x_stick.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    self.l_y_stick = ctk.CTkProgressBar(frame)
                    self.l_y_stick.grid(column=0, row=2, padx=self.comp_pad, pady=self.comp_pad)

                def joystick_right():
                    frame = ctk.CTkFrame(self.js_frame)
                    frame.grid(column=1, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    label = ctk.CTkLabel(frame, text="Right")
                    label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                    self.r_x_stick = ctk.CTkProgressBar(frame)
                    self.r_x_stick.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    self.r_y_stick = ctk.CTkProgressBar(frame)
                    self.r_y_stick.grid(column=0, row=2, padx=self.comp_pad, pady=self.comp_pad)

                joystick_left()
                joystick_right()

            def trigger():
                self.trigger_frame = ctk.CTkFrame(self.controller_frame)
                self.trigger_frame.grid(column=0, columnspan=2, row=3, padx=self.comp_pad, pady=self.comp_pad)

                label = ctk.CTkLabel(self.trigger_frame, text="Trigger", font=self.frame_font)
                label.grid(column=0, columnspan=2, row=0, padx=self.comp_pad, pady=self.comp_pad)

                def trigger_left():
                    frame = ctk.CTkFrame(self.trigger_frame)
                    frame.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    label = ctk.CTkLabel(frame, text="Left")
                    label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                    self.l_trigger = ctk.CTkProgressBar(frame)
                    self.l_trigger.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                def trigger_right():
                    frame = ctk.CTkFrame(self.trigger_frame)
                    frame.grid(column=1, row=1, padx=self.comp_pad, pady=self.comp_pad)

                    label = ctk.CTkLabel(frame, text="Right")
                    label.grid(column=0, row=0, padx=self.comp_pad, pady=self.comp_pad)

                    self.r_trigger = ctk.CTkProgressBar(frame)
                    self.r_trigger.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                trigger_left()
                trigger_right()

            threshold_slider()
            buttons()
            joysticks()
            trigger()
        controller()

    def start_main_btn(self):
        def start():
            pass

        btn = ctk.CTkButton(self.app, text="Start", command=start)
        btn.grid(column=3, row=2)
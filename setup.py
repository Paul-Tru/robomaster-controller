import os

try:
    import customtkinter as ctk
    import configparser
    from PIL import Image

except ImportError as e:
    print(f"Error: {e}\nInstalling required packages...")
    os.system("pip install -r requirements.txt")
    # Optionally re-import after installation
    import customtkinter as ctk
    import configparser
    from PIL import Image

class Setup:
    def __init__(self):
        self.l_x_stick = None
        self.config = configparser.ConfigParser()

        self.config.read("config.ini")
        self.debug = self.config.getboolean("GENERAL", "debug")
        ctk.set_appearance_mode(self.config["GUI"]["appearance"])

        self.app = ctk.CTk()
        self.app.geometry(self.config["GUI"]["geometry"])
        if not self.debug:
            self.app.title("Titan Setup")
        else:
            self.app.title("Titan Setup (Debug)")
        self.frame_pad = self.config["GUI"]["frame_pad"]
        self.frame_font = eval(self.config["GUI"]["frame_font"])
        self.comp_pad = self.config["GUI"]["component_pad"]

        self.ip_config()
        self.robot()
        self.debug_switch()
        self.tabview_frame()
        self.app.mainloop()

        try:
            self.rob_ip = self.config["IP"]["rob"]
            self.pc_ip = self.config["IP"]["pc"]
        except KeyError:
            self.rob_ip = None
            self.pc_ip = None

    def save_config(self):
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def change_bar(self, name, value):
        max_speed = int(self.config["ROBOT"]["max_speed"])
        # Normalize value based on max_speed
        normalized_value = (value + max_speed) / (2 * max_speed)  # Scales value between 0 and 1

        # Update the corresponding progress bar based on the name provided
        if name == "l_x_stick":
            self.l_x_stick.set(normalized_value)
        elif name == "l_y_stick":
            self.l_y_stick.set(normalized_value)
        elif name == "r_x_stick":
            self.r_x_stick.set(normalized_value)
        elif name == "r_y_stick":
            self.r_y_stick.set(normalized_value)
        elif name == "l_trigger":
            self.l_trigger.set(normalized_value)
        elif name == "r_stick":
            self.r_stick.set(normalized_value)
        else:
            print(f"Unknown bar name: {name}")

    def ip_config(self):
        frame = ctk.CTkFrame(self.app)
        frame.grid(column=0, row=0, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        label = ctk.CTkLabel(frame, text="Wifi", font=self.frame_font)
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        rob_ip_ini = self.config.get("IP", "rob", fallback="")
        pc_ip_ini = self.config.get("IP", "pc", fallback="")

        self.entry_rob_ip = ctk.CTkEntry(frame, placeholder_text=rob_ip_ini)
        self.entry_rob_ip.pack(padx=self.comp_pad, pady=self.comp_pad)

        self.entry_pc_ip = ctk.CTkEntry(frame, placeholder_text=pc_ip_ini)
        self.entry_pc_ip.pack(padx=self.comp_pad, pady=self.comp_pad)

        status = ctk.CTkLabel(frame, text="❌ Not Connected")
        status.pack(padx=self.comp_pad, pady=self.comp_pad)

        def get_values():
            rob_ip = self.entry_rob_ip.get()
            pc_ip = self.entry_pc_ip.get()
            if rob_ip is not None:
                self.rob_ip = rob_ip
                self.pc_ip = pc_ip
            else:
                self.rob_ip = rob_ip_ini
                self.pc_ip = pc_ip_ini
                
            try:
                import robot_controll as rc
                check = rc.check_conn(self.rob_ip, self.pc_ip)
            except:
                check = False

            if check:
                frame.configure(fg_color="#302c2c")
                status.configure(text="✅ Connected")
            elif self.debug:
                frame.configure(fg_color="#302c2c")
                status.configure(text="DEBUG")
            else:
                frame.configure(fg_color="darkred")
                status.configure(text="❌ Not Connected")

        self.get_btn = ctk.CTkButton(frame, text="Get", command=get_values)
        self.get_btn.pack(padx=15, pady=10)

    def debug_switch(self):
        frame = ctk.CTkFrame(self.app)
        frame.grid(column=0, row=1, sticky="n", padx=self.comp_pad, pady=self.comp_pad)

        def change():
            value = switch.get()
            if value == 0:
                self.config["GENERAL"]["debug"] = "True"
            else:
                self.config["GENERAL"]["debug"] = "False"
            self.save_config()
            print(value)

        switch = ctk.CTkSwitch(frame, text="Debug", command=change)
        switch.pack(padx=self.comp_pad, pady=self.comp_pad)

        if self.debug:
            switch.select()
        else:
            switch.deselect()

    def robot(self):
        self.right_frame = ctk.CTkFrame(self.app)
        self.right_frame.grid(column=3, row=0, rowspan=2, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        label = ctk.CTkLabel(self.right_frame, text="Robot", font=self.frame_font)
        label.grid(row=0, padx=self.comp_pad, pady=self.comp_pad)

        def max_speed():
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=1, padx=self.comp_pad, pady=self.comp_pad)

            max_speed = self.config["ROBOT"]["max_speed"]

            label = ctk.CTkLabel(frame, text=f"Max Speed: {max_speed} rpm")
            label.grid(padx=self.comp_pad, pady=self.comp_pad)


            def get(value):
                max_speed = int(value)  # Slider value is passed automatically
                label.configure(text=f"Max Speed: {max_speed} rpm")  # Update label with formatted value
                self.config["ROBOT"]["max_speed"] = str(max_speed)
                self.save_config()
                print("Max Speed: " + str(max_speed))

            slider = ctk.CTkSlider(frame, number_of_steps=10, to=5000, command=get)
            slider.grid(padx=self.comp_pad, pady=self.comp_pad)
            slider.set(int(max_speed))

        def max_distance():
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=2, padx=self.comp_pad, pady=self.comp_pad)

            max_distance = self.config["ROBOT"]["max_distance"]

            label = ctk.CTkLabel(frame, text=f"Max Distance: {max_distance} cm")
            label.grid(padx=self.comp_pad, pady=self.comp_pad)

            def get(value):
                max_distance = int(value)  # Slider value is passed automatically
                label.configure(text=f"Max Distance: {max_distance} cm")  # Update label with formatted value
                self.config["ROBOT"]["max_distance"] = str(max_distance)
                self.save_config()
                print("Max Speed: " + str(max_distance))

            slider = ctk.CTkSlider(frame, number_of_steps=6, to=300, command=get)
            slider.grid(padx=self.comp_pad, pady=self.comp_pad)
            slider.set(int(max_distance))

        def video():
            frame = ctk.CTkFrame(self.right_frame)
            frame.grid(row=3, padx=self.comp_pad, pady=self.comp_pad)

            self.video_label = ctk.CTkLabel(frame, text="Initializing video stream...")
            self.video_label.pack()

            if self.debug:
                placeholder_image = Image.open("test.png")  # Load your image file here
                placeholder_imgtk = ctk.CTkImage(placeholder_image, size=(160, 90))
                self.video_label.configure(image=placeholder_imgtk, text="")
                self.video_label.image = placeholder_imgtk

        max_speed()
        max_distance()
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

            def config_buttons():
                def configure():
                    print("pressed")

                button = ctk.CTkButton(self.controller_frame, text="Configure", command=configure)
                button.grid(column=0, row=1, sticky="s", padx=self.comp_pad, pady=self.comp_pad)

            def buttons():
                self.buttons_text = ctk.CTkTextbox(self.controller_frame)
                self.buttons_text.grid(column=1, row=1, padx=self.comp_pad, pady=self.comp_pad)

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

                    self.r_stick = ctk.CTkProgressBar(frame)
                    self.r_stick.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

                trigger_left()
                trigger_right()

            threshold_slider()
            config_buttons()
            buttons()
            joysticks()
            trigger()
        controller()

    # Example usage:
setup = Setup()
setup.change_bar("l_x_stick", 100)
setup.change_bar("r_y_stick", 200)
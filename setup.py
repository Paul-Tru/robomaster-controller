import os

try:
    import customtkinter as ctk
    import configparser

except ImportError as e:
    print(f"Error: {e}\nInstalling required packages...")
    os.system("pip install -r requirements.txt")
    # Optionally re-import after installation
    import customtkinter as ctk
    import configparser

class Setup:
    def __init__(self):
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
        self.controller()
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
        frame.grid(column=0, row=1, padx=self.comp_pad, pady=self.comp_pad)

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
        self.right_frame.grid(column=2, row=0, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        label = ctk.CTkLabel(self.right_frame, text="Robot", font=self.frame_font)
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        self.max_speed()
        self.max_distance()

    def max_speed(self):
        frame = ctk.CTkFrame(self.right_frame)
        frame.pack(padx=self.comp_pad, pady=self.comp_pad)

        max_speed = self.config["ROBOT"]["max_speed"]

        label = ctk.CTkLabel(frame, text=f"Max Speed: {max_speed} rpm")
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        
        def get(value):
            max_speed = int(value)  # Slider value is passed automatically
            label.configure(text=f"Max Speed: {max_speed} rpm")  # Update label with formatted value
            self.config["ROBOT"]["max_speed"] = str(max_speed)
            self.save_config()
            print("Max Speed: " + str(max_speed))

        slider = ctk.CTkSlider(frame, number_of_steps=10, to=5000, command=get)
        slider.pack(padx=self.comp_pad, pady=self.comp_pad)
        slider.set(int(max_speed))

    def max_distance(self):
        frame = ctk.CTkFrame(self.right_frame)
        frame.pack(padx=self.comp_pad, pady=self.comp_pad)

        max_distance = self.config["ROBOT"]["max_distance"]

        label = ctk.CTkLabel(frame, text=f"Max Distance: {max_distance} cm")
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        def get(value):
            max_distance = int(value)  # Slider value is passed automatically
            label.configure(text=f"Max Distance: {max_distance} cm")  # Update label with formatted value
            self.config["ROBOT"]["max_distance"] = str(max_distance)
            self.save_config()
            print("Max Speed: " + str(max_distance))

        slider = ctk.CTkSlider(frame, number_of_steps=6, to=300, command=get)
        slider.pack(padx=self.comp_pad, pady=self.comp_pad)
        slider.set(int(max_distance))

    def controller(self):
        self.controller_frame = ctk.CTkFrame(self.app)
        self.controller_frame.grid(column=1, row=0, sticky="n", padx=self.frame_pad, pady=self.frame_pad)

        label = ctk.CTkLabel(self.controller_frame, text="Controller", font=self.frame_font)
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        self.threshold_slider()

    def threshold_slider(self):
        frame = ctk.CTkFrame(self.controller_frame)
        frame.pack(padx=self.frame_pad, pady=self.frame_pad)

        threshold = self.config["CONTROLLER"]["threshold"]
        max_speed = self.config["ROBOT"]["max_speed"]
        to=int(int(max_speed)/2)
        steps = int(to/50)

        label = ctk.CTkLabel(frame, text=f"Threshold: {threshold}/{max_speed}\n \n"
                             f"{str(round(int(threshold)/int(max_speed)*100))}%")
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        def get(value):
            threshold = int(value)
            max_speed = self.config["ROBOT"]["max_speed"]  # Slider value is passed automatically
            label.configure(text=f"Threshold: {threshold}/{max_speed}\n \n"
                            f"{str(round(int(threshold)/int(max_speed)*100))}%")
            self.config["CONTROLLER"]["threshold"] = str(threshold)
            self.save_config()
            slider.configure(to=int(max_speed)/2, number_of_steps = int(to/50))
            print("Threshold: "+ str(threshold))

        slider = ctk.CTkSlider(frame, number_of_steps=steps, to=to, command=get)
        slider.pack(padx=self.comp_pad, pady=self.comp_pad)
        slider.set(int(threshold))

setup = Setup()
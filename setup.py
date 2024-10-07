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
        self.debug = bool(self.config["GENERAL"]["debug"])
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
        self.app.mainloop()

        if not self.debug:
            import robot_controll as rc

        try:
            self.rob_ip = self.config["IP"]["rob"]
            self.pc_ip = self.config["IP"]["pc"]
        except KeyError:
            self.rob_ip = None
            self.pc_ip = None


    def write_ini(self, sec, var, value):
        self.config[sec][var] = value
        with open('config.ini', 'w') as configfile:  # save
            self.config.write(configfile)

    def ip_config(self):
        left_frame = ctk.CTkFrame(self.app)
        left_frame.pack(side="left", padx=self.frame_pad, pady=self.frame_pad)

        label = ctk.CTkLabel(left_frame, text="Wifi", font=self.frame_font)
        label.pack(padx=self.comp_pad, pady=self.comp_pad)

        self.entry_rob_ip = ctk.CTkEntry(left_frame, placeholder_text="Robot IP")
        self.entry_rob_ip.pack(padx=self.comp_pad, pady=self.comp_pad)

        self.entry_pc_ip = ctk.CTkEntry(left_frame, placeholder_text="Computer IP")
        self.entry_pc_ip.pack(padx=self.comp_pad, pady=self.comp_pad)

        status = ctk.CTkLabel(left_frame, text="❌ Not Connected")
        status.pack(padx=self.comp_pad, pady=self.comp_pad)

        def get_values():
            rob_ip = self.entry_rob_ip.get()
            pc_ip = self.entry_pc_ip.get()
            if rob_ip is not None:
                self.rob_ip = rob_ip
                self.pc_ip = pc_ip

            try:
                check = rc.check_conn(self.rob_ip, self.pc_ip)
            except:
                check = False

            if check or self.debug:
                left_frame.configure(fg_color="#302c2c")
                status.configure(text="✅ Connected")
            else:
                left_frame.configure(fg_color="darkred")
                status.configure(text="❌ Not Connected")

        self.get_btn = ctk.CTkButton(left_frame, text="Get", command=get_values)
        self.get_btn.pack(padx=15, pady=10)

    def robot(self):
        right_frame = ctk.CTkFrame(self.app)
        right_frame.pack(side="right", padx=self.frame_pad, pady=self.frame_pad)

        label = ctk.CTkLabel(right_frame, text="Robot", font=self.frame_font)
        label.pack(padx=self.comp_pad, pady=self.comp_pad)
        

setup = Setup()
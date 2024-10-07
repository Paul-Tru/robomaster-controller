import os

try:
    import customtkinter as ctk
    import configparser
    from robomaster import robot
except ImportError as e:
    print(f"Error: {e}\nInstalling required packages...")
    os.system("pip install -r requirements.txt")
    # Optionally re-import after installation
    import customtkinter as ctk
    import configparser
    from robomaster import robot

class Setup():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.rob_ip = None
        self.pc_ip = None
        ctk.set_appearance_mode("dark")
        self.app = ctk.CTk()
        self.app.geometry("1050x500")
        self.app.title("Titan")
        self.create_frames()
        self.ip_config()
        self.app.mainloop()

    def read_ini(self):
        self.config.read("config.ini")
        try:
            rob_ip = self.config["ip"],["rob"]
            pc_ip = self.config["ip"],["pc"]
            self.check_connection(rob_ip, pc_ip)
        except:
            print("reading ini ip config failed")

    def check_connection(self, rob_ip, pc_ip):
        try:
            robot.config.ROBOT_IP_STR = rob_ip
            robot.config.LOCAL_IP_STR = pc_ip
            ep_robot = robot.Robot()
            ep_robot.initialize(conn_type="sta")
            SN = ep_robot.get_sn()
            print("Robot SN:", SN)
            ep_robot.close()
            return True
        except Exception as e:
            print("Error while checking connection:", e)
            return False

    def create_frames(self):
        self.left_frame = ctk.CTkFrame(self.app)
        self.left_frame.pack(side="left", padx=20, pady=20)

    def ip_config(self):
        label = ctk.CTkLabel(self.left_frame, text="Wifi Config", font=("Arial", 15, "bold"))
        label.pack(padx=10, pady=10)

        entry_rob_ip = ctk.CTkEntry(self.left_frame, placeholder_text="Robot IP")
        entry_rob_ip.pack(padx=10, pady=10)

        entry_pc_ip = ctk.CTkEntry(self.left_frame, placeholder_text="Computer IP")
        entry_pc_ip.pack(padx=10, pady=10)

        def get_values():
            rob_ip = entry_rob_ip.get()
            pc_ip = entry_pc_ip.get()
            print(self.check_connection(rob_ip=str(rob_ip), pc_ip=str(pc_ip)))
            self.pc_ip = entry_pc_ip.get()

        self.get_btn = ctk.CTkButton(self.left_frame, text="Get", command=get_values)
        self.get_btn.pack(padx=15, pady=10)
        

setup = Setup()
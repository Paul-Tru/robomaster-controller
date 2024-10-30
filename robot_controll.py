import vars
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

def check_conn() -> bool:
    """checks connection to robot"""
    try:
        sn = vars.ep_robot.get_sn()
        print("Robot SN:", sn)
        return True
    except Exception as e:
        print("Error while checking connection:", e)
        return False
    
def main():
    trigger = 0
    threshold = int(config["CONTROLLER"]["threshold"])
    while not vars.overwrite:
        hat = vars.trigger_hat[0]
        trigger_right = vars.trigger_hat[1]
        trigger_left = vars.trigger_hat[2]

        # -1, 1 | 0, 1 | 1, 1
        # -------------------
        # -1, 0 | 0, 0 | 1, 0
        # -------------------
        # -1,-1 | 0,-1 | 1,-1

        # w1: fore right
        # w2: fore left
        # w3: back left
        # w4: back right

        # stop movement
        if hat == (0, 0) and trigger_right < threshold and trigger_left < threshold:
            vars.ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
            vars.motor = [0, 0, 0, 0]
        
        # move forward or backward
        elif hat == (0, 0):
            if trigger_left > threshold and trigger_right < threshold:
                trigger = -trigger_left
            elif trigger_right > threshold and trigger_left < threshold:
                trigger = trigger_right
            else:
                print("Dont press both triggers at the same time")      

            vars.ep_chassis.drive_wheels(w1=trigger, 
                                         w2=trigger, 
                                         w3=trigger,
                                         w4=trigger)
            
            vars.motor = [trigger, trigger, trigger, trigger]
        
        # move sideways
        elif hat == (1, 0) or hat == (-1, 0):

            if hat == (-1, 0):
                trigger_right = -trigger_right
                
            vars.ep_chassis.drive_wheels(w1=-trigger_right, 
                                         w2=trigger_right, 
                                         w3=-trigger_right,
                                         w4=trigger_right)
            
            vars.motor = [-trigger_right, trigger_right,
                          -trigger_right, trigger_right]
            

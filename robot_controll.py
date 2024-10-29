import vars

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
    while not vars.overwrite:
        hat = vars.trigger_hat[0]
        trigger = vars.trigger_hat[1]
        # print(hat, trigger)

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
        if hat == (0, 0):
            vars.ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
            vars.motor = [0, 0, 0, 0]
        
        # move forward or backward
        elif hat == (0, 1) or hat == (0, -1):

            if hat == (0, -1):
                trigger = -trigger

            vars.ep_chassis.drive_wheels(w1=trigger, 
                                         w2=trigger, 
                                         w3=trigger,
                                         w4=trigger)
            
            vars.motor = [trigger, trigger, trigger, trigger]
        
        # move sideways
        elif hat == (1, 0) or hat == (-1, 0):

            if hat == (-1, 0):
                trigger = -trigger
                
            vars.ep_chassis.drive_wheels(w1=-trigger, 
                                         w2=trigger, 
                                         w3=-trigger,
                                         w4=trigger)
            
            vars.motor = [-trigger, trigger, -trigger, trigger]

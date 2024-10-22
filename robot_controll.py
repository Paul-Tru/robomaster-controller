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
        vars.ep_chassis.drive_wheels(w1=vars.motor_fr, 
                                    w2=vars.motor_fl, 
                                    w3=vars.motor_bl,
                                    w4=vars.motor_br)
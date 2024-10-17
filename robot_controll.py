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
    while True:
        # and vars.distance > 100
        if not vars.bring_back:
            vars.ep_chassis.drive_wheels(w1=vars.motor_fr, 
                                        w2=vars.motor_fl, 
                                        w3=vars.motor_bl,
                                        w4=vars.motor_br)
        elif vars.bring_back:
            vars.ep_chassis.move(x=-8, xy_speed=1).wait_for_completed()
            vars.ep_chassis.move(x=-3, xy_speed=1).wait_for_completed()
            vars.bring_back = False
        
        #elif vars.distance < 100:
        #    vars.ep_chassis.move(x=-1, xy_speed=0.5)
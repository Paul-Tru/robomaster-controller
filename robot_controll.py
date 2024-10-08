from robomaster import robot, camera

def check_conn(rob_ip, pc_ip):
    try:
        robot.config.ROBOT_IP_STR = rob_ip
        robot.config.LOCAL_IP_STR = pc_ip
        ep_robot = robot.Robot()
        ep_robot.initialize(conn_type="sta")
        sn = ep_robot.get_sn()
        print("Robot SN:", sn)
        ep_robot.close()
        return True
    except Exception as e:
        print("Error while checking connection:", e)
        return False
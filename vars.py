from PIL import Image

"""file to store global variables"""

# Controller
# Joystick
joy_l_x:int = 0
joy_l_y:int = 0

joy_r_x:int = 0
joy_r_y:int = 0

# Trigger
tr_l:int = 0
tr_r:int = 0

# Buttons
btn_0 = False
btn_1 = False
btn_2 = False
btn_3 = False
btn_4 = False
btn_5 = False
btn_6 = False
btn_7 = False
btn_8 = False
btn_9 = False
btn_10 = False
btn_11 = False

# Movement
trigger_hat = ((0, 0), 0, 0)

# Robot
overwrite = False
distance:int = 0
battery:int = 0
ep_robot = None
ep_sensor = None
ep_camera = None
ep_chassis = None
ep_led = None
ep_battery = None
test_png = Image.open("test.png")

# detect persons
persons = []

# motors
motor:list = [0, 0, 0, 0]

# drag race
bring_back = False
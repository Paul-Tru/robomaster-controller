from PIL import Image

"""file to store global variables"""

# Controller
joy_l_up:bool = None
joy_l_down:bool = None
joy_l_forwards:bool = None
joy_l_backwards:bool = None

# Trigger
tr_l:int = 0
tr_r:int = 0

# Buttons
button = []

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
ep_arm = None
ep_led = None
ep_battery = None
test_png = Image.open("test.png")

# detect persons
persons = []

# motors
motor:list = [0, 0, 0, 0]

# drag race
bring_back = False
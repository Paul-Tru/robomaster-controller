from PIL import Image

# Controller
joy_l_x:int = 0
joy_l_y:int = 0

joy_r_x:int = 0
joy_r_y:int = 0

tr_l:int = 0
tr_r:int = 0

# Robot
distance:int = 0
ep_camera = None
test_png = Image.open("test.png")
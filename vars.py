from PIL import Image

# Controller
joy_l_x:int = 0
joy_l_y:int = 0

joy_r_x:int = 0
joy_r_y:int = 0

tr_l:int = 0
tr_r:int = 0

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

# Robot
distance:int = 0
ep_camera = None
test_png = Image.open("test.png")
import picounicorn

class Button(object):
    def __init__(self, btn, x, y):
        self.btn = btn
        self.x = x
        self.y = y

BUTTON_A = Button(picounicorn.BUTTON_A, 0, 1)
BUTTON_B = Button(picounicorn.BUTTON_B, 0, 4)
BUTTON_X = Button(picounicorn.BUTTON_X, 15, 1)
BUTTON_Y = Button(picounicorn.BUTTON_Y, 15, 4)

COLOURS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

def draw_button_sign(button, colour):
    picounicorn.set_pixel(button.x, button.y, *COLOURS[colour])
    picounicorn.set_pixel(button.x, button.y + 1, *COLOURS[colour])

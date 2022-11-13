import picounicorn
import time
import uasyncio

import ui

'''W = picounicorn.get_width()
H = picounicorn.get_height()
print(W, H)'''


async def switch_app(App, old_app):
    old_app.active = False
    App(is_switched_to=True)


class PicoUnicoApp(object):
    def __init__(self, is_switched_to=False):
        print('Starting app:', self.__class__.__name__)
        self.active = True
        self.screen_renderer = uasyncio.create_task(self._screen_renderer_process())
        if is_switched_to:
            time.sleep(1)
        self.button_listener = uasyncio.create_task(self._button_listener_process())

    def _draw_screen(self):
        pass

    def _draw_ui(self):
        for button in self.button_layout:
            ui.draw_button_sign(button['button'], button['colour'])

    async def _screen_renderer_process(self):
        while self.active:
            #print('SR', self.__class__.__name__)
            self._draw_screen()
            self._draw_ui()
            if self.screen_renderer_frequency == -1:
                break
            else:
                await uasyncio.sleep(self.screen_renderer_frequency)

    async def _button_listener_process(self):
        while self.active:
            #print('BL', self.__class__.__name__)
            for button in self.button_layout:
                if picounicorn.is_pressed(button['button'].btn):
                    if button['action']:
                        fn = button['action'][0]
                        params = button['action'][1]
                        if params:
                            await fn(*params)
                        else:
                            await fn()
                    else:
                        pass
            await uasyncio.sleep(self.button_listener_frequency)


class PicoUnicoAppMain(PicoUnicoApp):
    def __init__(self, is_switched_to=False):
        self.button_layout = [
            {'button': ui.BUTTON_A, 'action': (switch_app, [PicoUnicoAppTorch, self]), 'colour': 'white'},
            {'button': ui.BUTTON_B, 'action': (switch_app, [PicoUnicoAppTorch, self]), 'colour': 'white'},
            {'button': ui.BUTTON_X, 'action': (switch_app, [PicoUnicoAppStandBy, self]), 'colour': 'red'},
            {'button': ui.BUTTON_Y, 'action': (switch_app, [PicoUnicoAppTorch, self]), 'colour': 'white'},
        ]
        self.button_listener_frequency = 0.1
        self.screen_renderer_frequency = 0.1
        super().__init__(is_switched_to)

    def _draw_screen(self):
        picounicorn.clear()
        picounicorn.set_pixel_value(3, 3, 5)
        picounicorn.set_pixel_value(3, 4, 20)


class PicoUnicoAppStandBy(PicoUnicoApp):
    def __init__(self, is_switched_to=False):
        self.button_layout = [
            {'button': ui.BUTTON_X, 'action': (switch_app, [PicoUnicoAppMain, self])},
        ]
        self.button_listener_frequency = 4
        self.screen_renderer_frequency = -1
        super().__init__(is_switched_to)

    def _draw_ui(self):
        picounicorn.clear()
        picounicorn.set_pixel(15, 0, 30, 0, 0)


class PicoUnicoAppTorch(PicoUnicoApp):
    def __init__(self, is_switched_to=False):
        self.button_layout = [
            {'button': ui.BUTTON_A, 'action': (self._raise_torch_brightness, None), 'colour': 'blue'},
            {'button': ui.BUTTON_B, 'action': (self._lower_torch_brightness, None), 'colour': 'blue'},
            {'button': ui.BUTTON_X, 'action': (switch_app, [PicoUnicoAppMain, self]), 'colour': 'red'},
        ]
        self.button_listener_frequency = 0.1
        self.screen_renderer_frequency = 1
        self.torch_brightness = 255
        super().__init__(is_switched_to)

    def _draw_screen(self):
        for x in range(0, 16):
            for y in range(0, 7):
                picounicorn.set_pixel_value(x, y, self.torch_brightness)

    async def _raise_torch_brightness(self):
        self.torch_brightness += 5
        if self.torch_brightness >= 255:
            self.torch_brightness = 255

    async def _lower_torch_brightness(self):
        self.torch_brightness -= 5
        if self.torch_brightness <= 10:
            self.torch_brightness = 10


if __name__ == "__main__":
    picounicorn.init()
    picounicorn.clear()

    loop = uasyncio.get_event_loop()
    PicoUnicoAppMain()
    loop.run_forever()

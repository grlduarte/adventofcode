'''
gduarte@home-vm
Created on 27-ago-2021
'''

from tkinter import *

from computer import Computer


class Video(Canvas):
    def __init__(self, master, scale=5):
        self.x_size = 26
        self.y_size = 46
        self.scale = scale
        self.width = scale * self.y_size
        self.height = scale * self.x_size
        super().__init__(master, width=self.width,
                         height=self.height, bg='black')
        self.keyboard = {'a': -1, 'd': 1}
        self.pack()

    def start(self, fname):
        self.bind_all("<KeyPress>", self.press_key)
        self.bind_all("<KeyRelease>", self.release_key)
        self.pressed_keys = [None]
        self.last_key = IntVar(self)
        self.cpu = Computer(fname, mem_alloc=4096, video=self)
        self.cpu.memory[0] = 2
        self.step()

    def press_key(self, e):
        key = e.keysym
        try:
            self.last_key.set(self.keyboard[key])
            self.pressed_keys.append(self.keyboard[key])
        except KeyError:
            pass
        if key == 'Escape':
            self.last_key.set(0)
            self.master.destroy()

    def release_key(self, e):
        key = e.keysym
        try:
            self.pressed_keys.remove(self.keyboard[key])
            self.pressed_keys[-1] = None
        except (ValueError, KeyError):
            pass

    def step(self):
        self.cpu.cycle(self.pressed_keys[-1])
        self.ident = self.after(1, self.step)

    def stop(self):
        self.after_cancel(self.ident)

    def update(self):
        self.delete(ALL)
        screen = self.cpu.screen
        for i, line in enumerate(screen):
            for j, px in enumerate(line):
                    if (px == 1):
                        coords = (i*self.scale, j*self.scale,
                                  (i+1)*self.scale, (j+1)*self.scale)
                        self.create_rectangle(coords, fill='white')
                    elif (px == 2):
                        coords = (i*self.scale, j*self.scale,
                                  (i+1)*self.scale, (j+1)*self.scale)
                        self.create_rectangle(coords, fill='grey')
                    elif (px == 3):
                        coords = (i*self.scale, j*self.scale,
                                  (i+1)*self.scale, (j+1)*self.scale)
                        self.create_rectangle(coords, fill='red')
                    elif (px == 4):
                        coords = (i*self.scale, j*self.scale,
                                  (i+1)*self.scale, (j+1)*self.scale)
                        self.create_rectangle(coords, fill='blue')
                        

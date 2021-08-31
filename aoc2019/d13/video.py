'''
gduarte@home-vm
Created on 27-ago-2021
'''

import numpy as np
from tkinter import Tk, Canvas

from computer import Computer


class Video(Canvas):
    def __init__(self, master):
        self.x_size = 23
        self.y_size = 45
        self.scale = 20
        self.width = self.scale * self.y_size
        self.height = self.scale * self.x_size
        self.cpu = Computer('input.dat', mem_alloc=4096)
        x, y = [23, 45]
        screen = [[0 for _ in range(y)] for _ in range(x)]
        self.screen = np.array(screen)
        self.img_ref = np.empty_like(screen)
        super().__init__(master, width=self.width,
                         height=self.height, bg='white')
        self.pack()

    def start(self):
        self.cpu.memory[0] = 2
        self.timer = 'idle'
        self.step()

    def step(self):
        try:
            x_ball = np.where(self.screen == 4)[1][0]
            x_pad = np.where(self.screen == 3)[1][0]
            self.timer = 1
            if (x_ball > x_pad):
                signal = 1
            elif (x_ball < x_pad):
                signal = -1
            else:
                signal = 0
        except IndexError:
            signal = None
        except Exception as e:
            self.master.destroy()
            raise e
        self.cpu.cycle(signal)
        self.draw()
        self.ident = self.after(self.timer, self.step)

    def draw(self):
        try:
            x, y, v = self.cpu.output
            self.cpu.output = []
            if (x < 0) and (y == 0):
                print(v)
                return
        except ValueError:
            return
        try:
            c = (x*self.scale, y*self.scale)
            c += ((x+1)*self.scale, (y+1)*self.scale)
            fill = 'white' if (v == 0) else 'black'
            self.delete(self.img_ref[y, x])
            self.screen[y, x] = v
            self.img_ref[y, x] = self.create_rectangle(c, fill=fill, outline='white')
        except KeyError as e:
            self.master.destroy()
            print("KeyError: " + e)
    

if __name__ == '__main__':
    root = Tk()
    game = Video(root)
    game.start()
    root.mainloop()


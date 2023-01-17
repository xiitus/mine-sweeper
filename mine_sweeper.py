import tkinter
from tkinter import messagebox
from random import randint
from sys import setrecursionlimit as LimitBreak

LimitBreak(10 ** 6)

grid_width = 30
grid_height = 30
mine_count = 1

mine_color = "#ff0000"
flag_color = "#ffff00"
empty_color = "#dcdcdc"

bg_color = {
    1: "#4169e1",
    2: "#008000",
    3: "#ff4500",
    4: "#191970",
    5: "#a0522d",
    6: "#00ffff",
    7: "#000000",
    8: "#696969",
}

mine_constant = -1


class MineSweeper():
    def __init__(self, Application):

        self.Application = Application
        self.cells = None
        self.labels = None
        self.width = grid_width
        self.height = grid_height
        self.mine_count = mine_count
        self.empty_count = (self.width * self.height) - self.mine_count
        self.opened_count = 0
        self.open_mine = False
        self.play_game = False

        # initialize grid
        self.init_grid()

        # add mine
        self.set_mines()

        # count mine
        self.set_mine_count()

        # add widgets
        self.create_widgets()

        # set
        self.add_events()

        # start game
        self.play_game = True

    def init_grid(self):
        self.cells = [[0] * self.width for _ in [0] * self.height]

    def set_mines(self):
        mine_count = 0
        while (mine_count < self.mine_count):

            j = randint(0, self.height - 1)
            i = randint(0, self.width - 1)

            if (self.cells[j][i] != mine_constant):

                self.cells[j][i] = mine_constant
                mine_count += 1

    def set_mine_count(self):
        for j in range(self.height):
            for i in range(self.width):

                if (self.cells[j][i] == mine_constant):
                    continue

                num_mine = 0

                for y in [-1, 0, 1]:
                    for x in [-1, 0, 1]:
                        if (y == x == 0):
                            continue
                        else:
                            is_mine = self.is_mine(i + x, j + y)

                            if is_mine:
                                num_mine += 1

                self.cells[j][i] = num_mine

    def is_mine(self, i, j):

        if (0 <= j < self.height) and (0 <= i < self.width):
            return (self.cells[j][i] == mine_constant)

    def create_widgets(self):

        self.labels = [[None] * self.width for j in [0] * self.height]
        for j in range(self.height):
            for i in range(self.width):
                label = tkinter.Label(
                    self.Application,
                    width=2,
                    height=1,
                    bg=empty_color,
                    relief=tkinter.RAISED
                )
                label.grid(column=i, row=j)
                self.labels[j][i] = label

    def add_events(self):
        for j in range(self.height):
            for i in range(self.width):
                label = self.labels[j][i]
                label.bind("<ButtonPress-1>", self.open_cell)
                label.bind("<ButtonPress-2>", self.set_flag)
                label.bind("<ButtonPress-3>", self.set_flag)

    def set_flag(self, event):

        if not (self.play_game):
            return -1

        label = event.widget

        if (label.cget("relief") != tkinter.RAISED):
            return -1

        if (label.cget("text") != "F"):
            bg = flag_color
            label.config(
                text=chr(128681),
                bg=bg
            )

        else:
            bg = empty_color
            label.config(
                text="",
                bg="background"
            )

    def open_cell(self, event):
        if not self.play_game:
            return -1

        label = event.widget
        for y in range(self.height):
            for x in range(self.width):
                if (self.labels[y][x] == label):
                    j, i = y, x

        cell = self.cells[j][i]

        if (label.cget("relief") != tkinter.RAISED):
            return -1

        text, bg, fg = self.GetTextInfo(cell)

        if (cell == mine_constant):
            self.open_mine = True

        label.config(
            text=text,
            bg=bg,
            fg=fg,
            relief=tkinter.SUNKEN
        )

        self.opened_count += 1

        if (cell == 0):
            for y in [-1, 0, 1]:
                for x in [-1, 0, 1]:
                    if (y == x == 0):
                        continue
                    else:
                        self.open_round(i + y, j + x)

        if (self.open_mine):
            self.Application.after_idle(self.game_over)

        elif (self.opened_count == self.empty_count):
            self.Application.after_idle(self.game_clear)

    def open_round(self, i, j):

        if (self.open_mine):
            return -1

        if not ((0 <= j < self.height) and (0 <= i < self.width)):
            return -1

        label = self.labels[j][i]

        if (label.cget("relief") != tkinter.RAISED):
            return -1

        if (self.cells[j][i] == mine_constant):
            return -1

        text, bg, fg = self.GetTextInfo(self.cells[j][i])

        label.config(
            text=text,
            bg=bg,
            fg=fg,
            relief=tkinter.SUNKEN
        )

        self.opened_count += 1

        if (self.cells[j][i] == 0):
            for y in [-1, 0, 1]:
                for x in [-1, 0, 1]:
                    if (y == x == 0):
                        continue
                    else:
                        self.open_round(i + y, j + x)

    def game_over(self):

        self.open_all()
        self.play_game = False

        messagebox.showerror(
            "",
            "GAME OVER"
        )

    def game_clear(self):

        self.open_all()
        fg = "#53ed00"

        self.play_game = False

        messagebox.showinfo(
            "",
            "GAME CLEAR"
        )

        

    def open_all(self):

        for j in range(self.height):
            for i in range(self.width):
                label = self.labels[j][i]

                text, bg, fg = self.GetTextInfo(self.cells[j][i])

                label.config(
                    text=text,
                    bg=bg,
                    fg=fg,
                    relief=tkinter.SUNKEN
                )

    def GetTextInfo(self, num):

        if (num == mine_constant):
            text = chr(128163)
            bg = "#53ed00"
            fg = "#8b0000"
        elif (num == 0):
            text = ""
            bg = empty_color
            fg = "#000000"
        else:
            text = str(num)
            bg = empty_color
            fg = bg_color[num]
        return (text, bg, fg)

# run game
Application = tkinter.Tk()
game = MineSweeper(Application)
Application.mainloop()
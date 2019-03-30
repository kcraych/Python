import tkinter as tki
from threading import Timer
import random

class App(object):

    # define window and make window content expandable
    def __init__(self):
        self.root = tki.Tk()
        self.root.wm_title("The Matching Game")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # set window size as 2/3 that of screen size and center window on the screen
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen
        w = 2 * ws / 3
        h = 2 * hs / 3
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(("%dx%d+%d+%d" % (w,h,x,y)))

        game = Game(self.root)


class Game(object):
    def __init__(self,parent):
        self.parent = parent

        # define a frame of the window and set to fill entire window (I don't think this is necessary, but might be useful if I want to put more frames in the window)
        # for example:  if I want to add a frame to the side that counts number of clicks made until solution
        self.frame = tki.Frame(parent)
        self.frame.grid(row=0, column=0, sticky='w, e, n, s')

        #define grid size for gameboard - must multiply to even grid #
        self.gh = 3
        self.gw = 2
        self.t = self.gh * self.gw

        #define hidden number selections for matching
        self.numbers = []
        self.options = set(range(self.t))
        for i in range(int(self.t/2)):
            self.rand = random.choice(list(self.options))
            self.numbers.append(self.rand)
            self.numbers.append(self.rand)
            self.options.remove(self.rand)
        random.shuffle(self.numbers)

        #assign #s on main window frame and cover with buttons
        self.clk_n = 0
        self.k = 0
        for x in range(self.gh):
            for y in range(self.gw):
                self.frame.rowconfigure(x, weight=1)
                self.frame.columnconfigure(y, weight=1)
                self.value = self.numbers[self.k]

                label_font = ('times', 20, 'bold')
                label = tki.Label(self.frame, text=self.value)
                label.config(font=label_font)
                label.grid(row=x, column=y, sticky='w, e, n, s')

                button = Button(self,self.value,x,y)

                self.k += 1

class Button(object):
    def __init__(self,parent,btn_v,btn_x,btn_y):
        self.parent = parent
        self.btn_v = btn_v
        self.btn_x = btn_x
        self.btn_y = btn_y
        self.button = tki.Button(self.parent.frame, command=self.click())
        self.button.grid(row=btn_x, column=btn_y, sticky='w, e, n, s')

    # define action to take place if 2nd click isn't a match (action = recover #s with buttons for both attempted cells)
    def replace_button(self):
        self.button.grid(row=self.btn_x, column=self.btn_y, sticky='w, e, n, s')

    # compare whether the values of two buttons are the same
    def compare_button(self, btn_c):
        return True if self.btn_v == btn_c.btn_v else False

    # define event to check whether click is a first or second click.
    # Show number under button
    #  If first click then save the value for comparison on second click.
    #  If second click + does not match first click #, then flash second # and hide both first and second #s.
    def click(self):
        def case():
            self.parent.clk_n += 1
            self.button.grid_forget()
            if self.parent.clk_n % 2 == 1:
                self.parent.btn_h = self
            else:
                if not self.compare_button(self.parent.btn_h):
                    self.parent.frame.update_idletasks()
                    Timer(0.5, self.replace_button).start()
                    Timer(0.5, self.parent.btn_h.replace_button).start()

        return case

app = App()
app.root.mainloop()

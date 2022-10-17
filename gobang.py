from cProfile import label
from tkinter import *
import numpy as np
from pyparsing import col

t = Tk()
t.title("五子棋")

white = [255, 255, 255]
black = [0, 0, 0]
board_color = [139, 126, 102]
red = [200, 0, 0]

r = 10
pieces_black = []
pieces_white = []
pieces = []
person_round = 1 #1 black turn, 0 white turn
over = False

# create the checkboard
canvas = Canvas(t, bg="SandyBrown", width=480, height=480)
canvas.grid(row=0, column=0, rowspan=10)

# draw the line
for i in range(15):
    canvas.create_line(30, (30 * i + 30), 450, (30 * i + 30))
    canvas.create_line((30 * i + 30), 30, (30 * i + 30), 450)

bold_point_x = [3, 3, 11, 11, 7]
bold_point_y = [3, 11, 3, 11, 7]

# bold points
for i in range(5):
    canvas.create_oval(30 * bold_point_x[i] + 27, 30 * bold_point_y[i] + 27,
                        30 * bold_point_x[i] + 33, 30 * bold_point_y[i] + 33, fill="black")

# get mouse position
def getPosition(event):
    global mouse_x
    global mouse_y
    mouse_x = event.x
    mouse_y = event.y
    validPoistion()

canvas.bind("<Button-1>",getPosition)

def validPoistion():
    global mouse_x
    global mouse_y
    global person_round
    global pieces
    for i in range(15):
        if (30 * i + 15) <= mouse_x <= (30 * (i + 1) + 15):
            mouse_x = 30 * i + 30
            break
    for i in range(15):
        if (30 * i + 15) <= mouse_y <= (30 * (i + 1) + 15):
            mouse_y = 30 * i + 30
            break
    if person_round == 1:
        dropPieces("black")
    elif person_round == -1:
        dropPieces("white")

def dropPieces(color):
    global pieces
    global person_round
    global pieces_black
    global pieces_white
    if mouse_x >= 30 and mouse_x <= 450 and mouse_y >= 30 and mouse_y <= 450:
        if (mouse_x, mouse_y) not in pieces:
            if not over:
                canvas.create_oval(mouse_x - r, mouse_y - r, mouse_x + r, mouse_y + r,
                                    fill=color, tags=("Pieces"))
                person_round *= -1
                if color == "black":
                    show()
                    #pieces_black.append([mouse_x, mouse_y])
                    pieces.append([[mouse_x, mouse_y], "black"])
                elif color == "white":
                    show()
                    pieces.append([[mouse_x,mouse_y], "white"])
                res = checkWin(pieces)
                Tips(pieces, res)

def show():
    var1 = StringVar()
    if person_round == 1:
        piece_canvas = Canvas(t, width=200, height=50)
        piece_canvas.grid(row=0, column=1)
        piece_canvas.create_oval(100 -r, 30 - r, 100 + r, 30 + r, fill="black")
        var1.set("black turn")
        label = Label(t, textvariable=var1, font=("宋体", 16))
        label.grid(row=1, column=1)
    if person_round == -1:
        piece_canvas = Canvas(t, width=200, height=50)
        piece_canvas.grid(row=0, column=1)
        piece_canvas.create_oval(100 -r, 30 - r, 100 + r, 30 + r, fill="white")
        var1.set("white turn")
        label = Label(t, textvariable=var1, font=("宋体", 16))
        label.grid(row=1, column=1)

def checkWin(p):
    mp = np.zeros([15, 15],dtype=int)
    for var in p:
        x = int((var[0][0] - 30) / 30)
        y = int((var[0][1] - 30) / 30)
        if var[1] == "black":
            mp[x][y] = 2
        else:
            mp[x][y] = 1
    for i in range(15):
        pos1 = []
        pos2 = []
        for j in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]
    for j in range(15):
        pos1 = []
        pos2 = []
        for i in range(15):
            if mp[i][j] == 1:
                pos1.append([i, j])
            else:
                pos1 = []
            if mp[i][j] == 2:
                pos2.append([i, j])
            else:
                pos2 = []
            if len(pos1) >= 5:
                return [1, pos1]
            if len(pos2) >= 5:
                return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i + k >= 15 or j + k >= 15:
                    break
                if mp[i+k][j+k] == 1:
                    pos1.append([i+k, j+k])
                else:
                    pos1 = []
                if mp[i+k][j+k] == 2:
                    pos2.append([i+k, j+k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    for i in range(15):
        for j in range(15):
            pos1 = []
            pos2 = []
            for k in range(15):
                if i + k >= 15 or j - k < 0:
                    break
                if mp[i+k][j-k] == 1:
                    pos1.append([i+k, j-k])
                else:
                    pos1 = []
                if mp[i+k][j-k] == 2:
                    pos2.append([i+k, j-k])
                else:
                    pos2 = []
                if len(pos1) >= 5:
                    return [1, pos1]
                if len(pos2) >= 5:
                    return [2, pos2]
    return [0, []]

def Tips(p, res):
    global over
    var2 = StringVar()
    if len(p) == 224:
        var2.set("Tie Game")
        label = Label(t, textvariable=var2, font=("宋体",16))
        label.grid(row=2, column=1)
        over = True
        return over
    if res[0] == 1:
        var2.set("White Win")
        label = Label(t, textvariable=var2, font=("宋体",16))
        label.grid(row=2, column=1)
        over = True
        return over
    if res[0] == 2:
        var2.set("Black Win")
        label = Label(t, textvariable=var2, font=("宋体",16))
        label.grid(row=2, column=1)
        over = True
        return over
    return 0

def click_start():
    global pieces
    global over
    global person_round
    canvas.delete("Pieces")     
    pieces = []
    over = False
    person_round = 1
    var3 = StringVar()
    var3.set("               ")   
    label = Label(t, textvariable=var3, font=("宋体", 16))
    label.grid(row=2, column=1)

start = Button(t, text="Start/Reset", font=('黑体', 10), fg='blue',
                width=10, height=2, command=click_start)
start.grid(row=4, column=1)

var = StringVar()
piece_canvas = Canvas(t, width=200, height=50)
piece_canvas.grid(row=0, column=1)
piece_canvas.create_oval(100 -r, 30 -r, 100 + r, 30 + r, fill="black")
var.set("black turn")
label = Label(t, textvariable=var, font=("宋体", 16))
label.grid(row=1, column=1)

t.mainloop()
from tkinter import *
import random
import uuid
from random import seed
from tkinter import ttk
import numpy as np
import time
from threading import Timer
import tkinter.messagebox


PuzzleWindow = Tk()  # library of basic elements of gui widgets.
PuzzleWindow.title('Memory Puzzle Game')# setting the title of the screen
base = Canvas(PuzzleWindow, width=500, height=500)#creates the window of the easy difficulty having the 500x500 area
base.pack()


moves = IntVar()
moves = 0
ids = [0, 1, 2, 3, 4, 5, 6, 7]
colors = []
shapes = []
id_board = np.zeros((4,4))
matched = np.zeros((4,4))

#function that draw shapes with different color
def draw_square(m,l,color_code):
    global base
    return base.create_rectangle(100*l+20 + 30, m*100+20 + 30, 100*l+100-20 + 30, 100*m+100-20 + 30, fill= color_code, outline = color_code)

def draw_circle(m,l, color_code):
    global base
    return base.create_oval(100*l+20 + 30, m*100+20 + 30, 100*l+100-20 + 30, 100*m+100-20 + 30, fill=color_code, outline = color_code)

def draw_triangle(m,l, color_code):
    global base
    return base.create_polygon(100*l+50 + 30, m*100+20 + 30, 100*l+20 + 30, 100*m+100-20 + 30,100*l+100-20 + 30, 100*m+100-20 + 30, fill=color_code)

def draw_empty(m,l, color_code):
    global base
    return base.create_rectangle(100*l+20 + 30, m*100+20 + 30,100*l+100-20 + 30, 100*m+100-20 + 30, fill= color_code, outline = color_code)

#generates a list of random colors
def choose_colors():
    i = 0
    while i <= 7:
        # Generate a random RGB color code
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color_code = f"#{r:02x}{g:02x}{b:02x}"
        colors.append(color_code)
        i += 1
    return colors

#generates random number of shapes used
def generate_shapes():
    squares = random.randint(0, 7)
    print(squares)
    circles = random.randint(0, 7 - squares)
    print(circles)
    triangles = 8 - squares - circles
    print(triangles)
    for i in range(8):
        if i < squares:
            shapes.append(1)
        elif i < triangles + squares and i >= squares:
            shapes.append(2)
        else:
            shapes.append(3)
    return shapes

def build_shapes(i, j, shape_id, visibility):
    global colors, shapes 
    shape_id = int(shape_id)
    if visibility == 1:
        if(shapes[shape_id] == 1):
            draw_square(i, j, colors[shape_id])
        if(shapes[shape_id] == 2):    
            draw_circle(i, j, colors[shape_id])
        if(shapes[shape_id] == 3):
            draw_triangle(i, j, colors[shape_id])
    else:
        draw_empty(i, j, '#ffffff')
        
def generate_unique_coordinates():
    used_coordinates = set()
    while True:
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        k = random.randint(0, 3)
        l = random.randint(0, 3)
        if (i, j) not in used_coordinates and  (k, l) not in used_coordinates and ((i, j) != (k, l)):
            used_coordinates.add((i, j))
            used_coordinates.add((k, l))
            yield (i, j, k, l)

def build_id_board():
    global ids
    id_board = np.zeros((4,4))
    generator = generate_unique_coordinates()
    for index in range(8):
        i,j,k,l = next(generator) 
        id_board[i][j] = ids[index]
        id_board[k][l] = ids[index]
    return id_board


colors = choose_colors()
shapes = generate_shapes()
id_board = build_id_board()

prev_i = -1
prev_j = -1
consecutive_clicks = 0
clicks = []
visible = 0
visible_min = 0
# clicks.append([-1, -1])

show_moves = base.create_text(240,465   , text = "Moves = " + str(moves) + "\nMatches = " + str(visible_min) + "/16", font=('arial', 10))

# prev_shape = build_shapes(prev_j, prev_j, id_board[prev_i][prev_j], 1)
# shape = None

print(id_board)


def on_click(event):

    def dissapear_current():
        shape = build_shapes(clicks[-1][0], clicks[-1][1], id_board[clicks[-1][0]][clicks[-1][1]], 0)

    def dissapear_previous():
        shape = build_shapes(clicks[-2][0], clicks[-2][1], id_board[clicks[-2][0]][clicks[-2][1]], 0)

    def dissapear_both():
        shape = build_shapes(clicks[-1][0], clicks[-1][1], id_board[clicks[-1][0]][clicks[-1][1]], 0)
        shape = build_shapes(clicks[-2][0], clicks[-2][1], id_board[clicks[-2][0]][clicks[-2][1]], 0)
    
    
    global moves, prev_i,prev_j
    global matched, id_board
    global consecutive_clicks, prev_shape, shape, clicks, visible, visible_min
    
    j = (event.x - 30)//100
    i = (event.y - 30)//100
    
    clicks.append([i, j])
    print(clicks)
        
    # print("clickilyty = ", set([[x[0], y[0]] for x, y in clicks]))
    
    # moves = len(set(tuple(l) for l in clicks))

    # # The length of this set will give the count of unique sublists
    # print("clickilyty = ", len(unique_clicks)) 
    
    moves += 1  # increment move counter
    
    print("\n\n")
    print(matched)
    print("=====")
    
    print("m-am activat din nou")

    shape = build_shapes(i, j, id_board[i][j], 1)
    
    visible += 1    
    
    # if visible + visible_min > 2:
    #     print("thats quite enough")
    #     t = Timer(1, dissapear_previous)
    #     t.start()
    
    if [i, j] == [prev_i, prev_j] and visible != 1:
        print("no bestie")
        pass
    elif prev_i == -1 and prev_j == -1:
        pass
    else:
        if id_board[i][j] == id_board[prev_i][prev_j] and visible == visible_min + 2:
            print("~matchyy~")
            matched[i][j] = 1
            matched[prev_i][prev_j] = 1
            visible_min += 2
        # elif matched[clicks[-1][0]][clicks[-1][1]] == 0:
        #     shape = build_shapes(clicks[-1][0], clicks[-1][1], id_board[clicks[-1][0]][clicks[-1][1]], 1)
        elif matched[prev_i][prev_j] == 1 and matched[i][j] == 0 and visible != visible_min + 1:
            print("machy no machy")
            t = Timer(1, dissapear_current)
            t.start()
            visible = visible_min + 1
        elif visible == visible_min + 2:
            print("vis = vis_min + 2")
            t = Timer(1, dissapear_both)
            t.start()
            visible = visible_min
        else:
            print("final else with visible = ", visible)
            pass
        # print("current", id_board[clicks[-1][0]][clicks[-1][1]])
        # print("previous", id_board[clicks[-2][0]][clicks[-2][1]])

    if matched[i][j] == 1 and matched[prev_i][prev_j] == 1:
        print("yoopi")
        shape = build_shapes(i, j, id_board[i][j], 1)
        shape = build_shapes(prev_i, prev_j, id_board[prev_i][prev_j], 1)
    # if id_board[clicks[-1]] == clicks[-2]:
    #     print("~matchy~")
        
    
    base.itemconfigure(show_moves, text = "Moves = " + str(moves) + "\nMatches = " + str(visible_min) + "/16")    
        
    
    if visible_min == 16:
        # base.itemconfigure(show_moves, text = "Moves = " + str(moves) + "\nMatches = ALL DONE GREAT JOB")
        tkinter.messagebox.showinfo("Game Over", "Well done! You have finished the game. Thanks for playing!")

    if moves > 100:
         tkinter.messagebox.showinfo("You are Over", "I don't think this game is quite for you.")
    

    # if consecutive_clicks < 2:
    #     if prev_i == -1 and prev_j == -1:
    #         shape = build_shapes(i, j, id_board[i][j], 1)
    #         print("first move")
    #         print("consecutive: ", consecutive_clicks)
    #         consecutive_clicks += 1
    #     else:
    #         print("else")
    #         if id_board[i][j] == id_board[prev_i][prev_j]:
    #             print("~matchy~")
    #             shape = build_shapes(i, j, id_board[i][j], 1)
    #             matched[i][j] = 1
    #             matched[prev_i][prev_j] = 1
    #             print("consecutive: ", consecutive_clicks)
    #         elif matched[i][j] == 0 and matched[prev_i][prev_j] == 0:
    #             shape = build_shapes(i, j, id_board[i][j], 1)
    #             consecutive_clicks += 1
    #             print("consecutive: ", consecutive_clicks)
    # else:
    #     print("pai valei")
    #     shape = build_shapes(i, j, id_board[i][j], 0)
    #     prev_shape = build_shapes(prev_j, prev_j, id_board[prev_i][prev_j], 0)
    #     consecutive_clicks = 0
    
    # if shape:
    #     prev_shape = shape 
    # else:
    #     prev_shape = None
    
    prev_i = i
    prev_j = j   
    

    print(matched)
    
    
    
    ################ bia's doing ###########################
    
    # if matched[prev_i][prev_j] == 0 and prev_i != -1:
    #     prev_shape = None
    #     shape = build_shapes(i, j, id_board[i][j])
        
    # if matched[i][j] == 0 and matched[prev_i][prev_j] == 1:
    #     prev_shape =  build_shapes(prev_j, prev_j, id_board[prev_i][prev_j])
    #     shape = build_shapes(i, j, id_board[i][j])
        
    # shape = None

    # if matched[i][j] == 0:
    #     # shape = build_shapes(i, j, id_board[i][j])
    #     if id_board[i][j] == id_board[prev_i][prev_j]:
    #         print("case 1")
    #         matched[i][j] = 1
    #         matched[prev_i][prev_j] = 1
    #     elif matched[prev_i][prev_j] == 1:
    #         # prev_shape = None
    #         print("case 2")
    #         matched[i][j] = 0
    #     else:
    #         # prev_shape = None
    #         print("case 3")
    #         matched[i][j] = 0
    #         matched[prev_i][prev_j] = 0
            
    #     prev_i = i
    #     prev_j = j
    #     prev_shape = shape
    # if matched.all() == 1:
    #     pass
    
    ################ bia's ending ###########################
    
    
# def on_click(i,j):
#     global moves, selected, id_board, board1, base1
#     # check if id has already been selected
#     if id_board[i][j] in selected:
#         board1[i][j] = dictionary[id_board[i][j]]  # retrieve shape from dictionary
#     else:
#         # create new shape if id hasn't been selected
#         board1[i,j] = build_shapes(i, j, id_board[i,j])
#         selected.append(id_board[i][j]) 

## --------------------------------- 
#         build_shapes(k, l, id_board[k,l])
        
#visualise the board 
# for i in range(4):
#     for j in range(4):
#         build_shapes(i,j, id_board[i][j])

for k in range(4):
    for l in range(4):
        #draws the board square by square
        # rec = base.create_rectangle(100*k + 3, l*100 + 3, 100*k+100 + 3, 100*l+100 + 3, fill="white")
        rec = base.create_rectangle(100*k + 30, l*100 + 30, 100*k+100 + 30, 100*l+100 + 30, fill="white")

################ bia's doing ###########################

for i in range(4):
    for j in range(4):
        shape = build_shapes(i, j, id_board[i][j], 1)

def delayed():
    for i in range(4):
        for j in range(4):
            shape = build_shapes(i, j, id_board[i][j], 0)

t = Timer(2, delayed)
t.start()

################ bia's ending ###########################

#binds the mouse click button to the function call
base.bind("<Button-1>", on_click)
base.mainloop()

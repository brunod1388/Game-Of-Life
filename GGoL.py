import GameOfLife as gof
import tkinter as tk
import threading
import time

LINE_COLOR = 'dark green'
ALIVECELL_COLOR = '#002b36'
NOCELL_COLOR= '#268bd2'
BGCOLOR = 'light grey'
TESTCOLOR = 'pink' #    ,bg=TESTCOLOR

C_DEFAULT_WIDTH = 460
C_DEFAULT_HEIGHT = 460
NB_CELLS_X_DEFAULT = 20
NB_CELLS_Y_DEFAULT = 20
CELL_SIZE_DEFAULT = 10
LINE_SIZE_DEFAULT = 1

auto_play = False

root = tk.Tk()
root.title("Game of Life")
root.configure(bg=BGCOLOR, padx=10, pady=10)

f_Menu = tk.Frame(root, bg=BGCOLOR)
f_Menu.pack(side='left', fill=tk.Y)

lf_map = tk.LabelFrame(root, text='Map World', bg=BGCOLOR)
lf_map.pack(side='left', expand=True, fill=tk.BOTH, ipadx = 10, ipady=10)

l_nbCycles = tk.Label(lf_map, text="Cycle 0", bg=BGCOLOR)
l_nbCycles.pack(side='top', anchor='e', padx=10)

c_map = tk.Canvas(lf_map, bg=NOCELL_COLOR, width=C_DEFAULT_WIDTH, height=C_DEFAULT_HEIGHT, highlightthickness=0)
c_map.pack(side='bottom',expand=True)

nb_cells_X = tk.IntVar(value=NB_CELLS_X_DEFAULT)
nb_cells_Y = tk.IntVar(value=NB_CELLS_Y_DEFAULT)
cell_size = tk.IntVar(value=CELL_SIZE_DEFAULT)
line_size = tk.IntVar(value=LINE_SIZE_DEFAULT)


world = gof.World(nb_cells_X.get(), nb_cells_Y.get())

def draw_0Map(c, nb_cells_X, nb_cells_Y, cell_width=cell_size.get(), line_width=line_size.get()):

    c['width'] = nb_cells_X * cell_width + (nb_cells_X + 1) * line_width
    c['height'] = nb_cells_Y * cell_width + (nb_cells_Y + 1) * line_width
    c.create_rectangle(0, 0, c['width'], c['height'], fill=NOCELL_COLOR, outline="")

    for x in range(nb_cells_Y + 1):
        c.create_line(0,
                      x*(cell_width+line_width)+line_width//2,
                      c['width'],
                      x*(cell_width+line_width)+line_width//2,
                      width=line_width,
                      fill=LINE_COLOR)

    for y in range(nb_cells_X + 1):
        c.create_line(y*(cell_width+line_width)+line_width//2,
                      0,
                      y*(cell_width+line_width)+line_width//2,
                      c['height'],
                      width=line_width,
                      fill=LINE_COLOR)
        continue

def newMap(c=c_map,w=world, x=nb_cells_X, y=nb_cells_Y, cell_width=cell_size, line_width=line_size):

    if x.get()>330 or y.get()>180 or x.get() < 10 or y.get() < 10:
        top_dimension = tk.Toplevel(bg=BGCOLOR)
        top_dimension.title('Too small dimensions')
        s = 'Dimensions not aavailable'
        tk.Label(top_dimension, text=s, bg=BGCOLOR).pack(ipadx=10, ipady=5)
        tk.Button(top_dimension,highlightthickness=0, text='OK',
                   command=top_dimension.destroy).pack(pady=10)

    else:
        l_nbCycles['text'] = 'Cycle 0'
        c.configure(width=x.get())
        c.configure(height=y.get())
        draw_0Map(c_map, x.get(), y.get(), cell_width.get(), line_width.get())
        world.reset(x.get(),y.get())

def randMap(c,w):
    w.genRandomWorld()
    draw_World(c,w)

def draw_cell(c,x,y,cell_color, cell_width=cell_size,line_width=line_size):
    c.create_rectangle(x*(cell_width.get()+line_width.get())+line_width.get(),
                       y*(cell_width.get()+line_width.get())+line_width.get(),
                       x*(cell_width.get()+line_width.get())+cell_width.get()+line_width.get(),
                       y*(cell_width.get()+line_width.get())+cell_width.get()+line_width.get(),
                       fill=cell_color,
                       outline="")

def draw_World(c,w):
    for x in range(w.nbColumns):
        for y in range(w.nbRows):
            if w.cells[y][x].is_alive():
                draw_cell(c,x,y,ALIVECELL_COLOR)
            else:
                draw_cell(c,x,y,NOCELL_COLOR)

def draw_changedCells(c,changed_cells):

    for cell in changed_cells:
        if cell.is_alive():
            draw_cell(c, cell.X, cell.Y, ALIVECELL_COLOR)
        else:
            draw_cell(c, cell.X, cell.Y, NOCELL_COLOR)

def cell_onclick(eventorigin, cell_width=cell_size, line_width=line_size):
    xCell = eventorigin.x//(cell_width.get()+line_width.get())
    yCell = eventorigin.y//(cell_width.get()+line_width.get())

    if world.cells[yCell][xCell].is_alive():
        world.cells[yCell][xCell].kill()
        draw_cell(c_map,xCell,yCell,NOCELL_COLOR)
    else:
        world.cells[yCell][xCell].live()
        draw_cell(c_map,xCell,yCell,ALIVECELL_COLOR)

def stop(c, world):
    global auto_play
    auto_play = False
    print('stop')

def nextCycle(c, world):
    changed_cells = world.nextCycle()
    draw_changedCells(c,changed_cells)
    l_nbCycles['text'] = 'Cycle {}'.format(world.nbCycle)
    
'''
def auto_NextCycle(c, world):
    global auto_play
    auto_play = True
    while auto_play:
        nextCycle(c, world)
        time.sleep(0.2)


def autoPlay(c, world):
    print('Autoplay')
    
    t1=threading.Thread(target= lambda c=c, w=world : auto_NextCycle(c,w))
    t1.start()
    
    global timer
    timer = threading.Timer(.5, lambda c=c,w=world : nextCycle(c,w))
    timer.start()
'''

def newList():
    print("newList")

def chargeList():
    print("chargeList")

def deleteList():
    print("deleteList")


'''
*************************************************
                    Map size configuration
*************************************************
'''
lf_Config = tk.LabelFrame(f_Menu, text="Map size", bg=BGCOLOR)
lf_Config.pack(side='top', ipadx=10, ipady=5)

f_dimension = tk.Frame(lf_Config, bg=BGCOLOR)
f_dimension.pack()

f_xydimension = tk.Frame(f_dimension, bg=BGCOLOR)
f_xydimension.pack(side="left")

f_xdimension_row = tk.Frame(f_xydimension, bg=BGCOLOR)
f_xdimension_row.pack(side="top")
l_xdimension = tk.Label(f_xdimension_row, text="X Axe", bg=BGCOLOR)
l_xdimension.pack(side="left", pady=10)
e_xdimension = tk.Entry(f_xdimension_row, width=3, highlightthickness=0, textvariable=nb_cells_X)
e_xdimension.pack(side="left")

f_ydimension_row = tk.Frame(f_xydimension, bg=BGCOLOR)
f_ydimension_row.pack(side="top")
l_ydimension = tk.Label(f_ydimension_row, text="Y Axe", bg=BGCOLOR)
l_ydimension.pack(side="left")
e_ydimension = tk.Entry(f_ydimension_row, width=3, highlightthickness=0, textvariable=nb_cells_Y)
e_ydimension.pack(side="left")

f_sizedimension_row = tk.Frame(f_xydimension, bg=BGCOLOR)
f_sizedimension_row.pack(side="top")
l_sizedimension = tk.Label(f_sizedimension_row, text="size", bg=BGCOLOR)
l_sizedimension.pack(side="left")
e_sizedimension = tk.Entry(f_sizedimension_row, width=3, highlightthickness=0, textvariable=cell_size)
e_sizedimension.pack(side="left")

f_linedimension_row = tk.Frame(f_xydimension, bg=BGCOLOR)
f_linedimension_row.pack(side="top")
l_linedimension = tk.Label(f_linedimension_row, text="line width", bg=BGCOLOR)
l_linedimension.pack(side="left")
e_linedimension = tk.Entry(f_linedimension_row, width=3, highlightthickness=0, textvariable=line_size)
e_linedimension.pack(side="left")


f_dimensionGen = tk.Frame(f_dimension, bg=BGCOLOR)
f_dimensionGen.pack(side="left")

b_newMap = tk.Button(f_dimensionGen, text="New Map", width=9, height=3, highlightthickness=0,
                  command=newMap)
b_newMap.pack()

b_rand = tk.Button(f_dimensionGen, text="Randomize", width=9, height=3, highlightthickness=0,
                  command=lambda c=c_map, w=world : randMap(c,w))
b_rand.pack()



'''
*************************************************
                    Starting Model management
*************************************************

lf_StartingModels = tk.LabelFrame(f_Menu, text='Starting Models', bg=BGCOLOR)
lf_StartingModels.pack(side='top', fill=tk.BOTH, ipady=10, expand=True)
tk.Label(lf_StartingModels, text='Choose your model:', bg=BGCOLOR).pack(side='top', anchor='w')

listModels = tk.Listbox(lf_StartingModels)
listModels.insert(1,"Model TSAMERE")
listModels.insert(2,"Model Yahouuuu")
listModels.insert(3,"Model kikou")
listModels.insert(4,"Model monkey")
listModels.insert(5,"Model balek")
listModels.pack(expand=True, fill=tk.Y)


   ** list commands **

f_ListCommand = tk.Frame(lf_StartingModels, bg=BGCOLOR)
f_ListCommand.pack(ipadx=5, ipady=5)

b_newList = tk.Button(f_ListCommand, text='New List', highlightthickness=0, command=newList)
b_newList.pack(side='left', fill=tk.X)
b_chargeList = tk.Button(f_ListCommand, text='Charge List', highlightthickness=0, command=chargeList)
b_chargeList.pack(side='left')
b_delete = tk.Button(f_ListCommand, text='Delete', highlightthickness=0, command=deleteList)
b_delete.pack(side='left')

'''
'''
*************************************************
                    Command Panel
*************************************************
'''
lf_Command = tk.LabelFrame(f_Menu, text='Command', bg=BGCOLOR)
lf_Command.pack(side='bottom',ipadx=10, ipady=10, fill=tk.X)
f_Command = tk.Frame(lf_Command, bg=BGCOLOR)
f_Command.pack(expand=True)
'''
b_Stop = tk.Button(f_Command,
                   text='Stop',
                   highlightthickness=0,
                   command=lambda c=c_map,w=world:stop(c,w))
b_Stop.pack(side='left', fill=tk.X)
b_AutoPlay = tk.Button(f_Command,
                       text='Auto Play',
                       highlightthickness=0,
                       command=lambda c=c_map,w=world:autoPlay(c,w))
b_AutoPlay.pack(side='left')
'''
b_NextCycle = tk.Button(f_Command,
                        text='Next Cycle',
                        highlightthickness=0,
                        command=lambda c=c_map,w=world:nextCycle(c,w))
b_NextCycle.pack(side='left')

draw_0Map(c_map, nb_cells_X.get(), nb_cells_Y.get(), cell_size.get(), line_size.get())
#mouseclick event
c_map.bind("<Button 1>", cell_onclick)
root.mainloop()

import random

class Cell():

    def __init__(self, alive, x, y):
        self.__alive = alive
        self.__x = x
        self.__y = y
        self.__neighbours = []
        self.__neighboursAliveCount = 0

    def __str__(self):
        if self.__alive :
            return "0"
        else :
            return "."

    def kill(self):
        self.__alive = False

    def live(self):
        self.__alive = True

    def is_alive(self):
        return self.__alive

    def add_neighbour(self, cell):
        self.__neighbours.append(cell)

    def set_neighboursAliveCount(self):
        nb = 0
        for cell in self.__neighbours:
            if cell.is_alive():
                nb += 1
        self.__neighboursAliveCount = nb

    @property
    def X(self):
        return self.__x

    @property
    def Y(self):
        return self.__y

    @property
    def neighboursAlive(self):
        return self.__neighboursAliveCount

    def print(self):
        print("Mummy : x={},y={}".format(self.__x, self.__y))
        s="Voisine : "
        for v in self.__neighbours:
            print("x={},y={}".format(v.X, v.Y))
        print(10*'*')


class World():

    def __init__(self, nbColumns, nbRows, startState=None):
        self.__nbCycle = 0
        self.__nbRows = nbRows
        self.__nbColumns = nbColumns
        self.__startState = startState
        if startState == None:
            self.__cells = [[Cell(False, x,y) for x in range(self.__nbColumns)] for y in range(self.__nbRows)]
            self.__startState = self.cellsArray()
        else:
            '''
                insert code
            '''
        self.generateNeighboursList();

    @property
    def cells(self):
        return self.__cells

    @property
    def nbRows(self):
        return self.__nbRows

    @property
    def nbColumns(self):
        return self.__nbColumns

    @property
    def nbCycle(self):
        return self.__nbCycle

    def reset(self, nbColumns=0, nbRows=0, startState=None):
        self.__nbCycle = 0
        if startState==None and nbColumns==0 and nbRows==0:
            self.__cells = [[Cell(False, x,y) for x in range(self.__nbColumns)] for y in range(self.__nbRows)]
        elif startState!=None:
            '''
                insert
            '''
        elif nbColumns>0 and nbRows>0:
            self.__nbRows = nbRows
            self.__nbColumns = nbColumns
            self.__cells = [[Cell(False, x,y) for x in range(nbColumns)] for y in range(nbRows)]
            self.__startState = self.cellsArray()
            self.generateNeighboursList();

    def generateNeighboursList(self):
        #generate list of neighbours
        for x in range(self.__nbColumns):
            for y in range(self.__nbRows):
                for i in [x-1,x,x+1]:
                    if i < 0 or i >= self.__nbColumns:
                        continue
                    for j in [y-1, y, y+1]:
                        if j < 0 or j >= self.__nbRows:
                            continue
                        if i == x and j == y:
                            continue
                        self.__cells[y][x].add_neighbour(self.__cells[j][i])

    def cellsArray(self):

        ar = []
        for x in range(self.__nbColumns):
            row = []
            for y in range(self.__nbRows):
                row.append(True if self.__cells[y][x].is_alive() else False)
            ar.append(row)
        return ar


    def print(self, printArray=False):
        print("Cycle ", self.__nbCycle)
        for y in range(self.__nbRows):
            s = ""
            for x in range(self.__nbColumns):
                s += str(self.__cells[y][x]) + " "
            print(s)

    def genRandomWorld(self):
        for row in self.__cells:
            for cell in row:
                if random.getrandbits(1):
                    cell.live()
                else:
                    cell.kill()

    def nextCycle(self):

        self.__nbCycle += 1
        changed_cells = []

        for row in self.__cells:
            for cell in row:
                cell.set_neighboursAliveCount()
        for row in self.__cells:
            for cell in row:
                if cell.neighboursAlive < 2 or cell.neighboursAlive > 3:
                    if cell.is_alive():
                        changed_cells.append(cell)
                    cell.kill()
                if cell.neighboursAlive == 3:
                    if not cell.is_alive():
                        changed_cells.append(cell)
                    cell.live()
        return changed_cells

if __name__ == "__main__":
    
    print();
    print("**********************************************************")
    print("*****                  Game of Life                   ****")
    print("**********************************************************")
    print()
    print("How big do you want the dimension ?")
    width = int(input("Width :  "))
    height = int(input("Height :  "))
    while width < 5 or height < 5:
        print("Too small dimensions")
        width = input("Width:")
        height = input("Height :  ")

    monde = World(width, height)
    monde.genRandomWorld()
    monde.print()
    
    user_action = ""
    while user_action != "q":
        user_action = input("Press enter to add generation or q to quit: ")
        if user_action == "":
            monde.nextCycle()
            monde.print(True)




    '''
    monde.cells[23][23].live()
    monde.cells[24][23].live()
    monde.cells[25][23].live()
    monde.cells[25][24].live()
    monde.cells[25][25].live()
    monde.cells[24][25].live()
    monde.cells[23][25].live()
    '''
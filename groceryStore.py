from cmu_112_graphics import *
import random
import copy

#Taken from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

def appStarted(app):
    app.rows = 10
    app.cols = 10
    app.store = make2dList(app.rows,app.cols)
    app.dimensionTime = True
    app.barrierTime = False
    app.selectionTime = False
    app.inputsAccepted = False
    app.storeLooksFinal = False
    app.simulationEnded = False
    app.countItems = 0
    app.sideLenH = 0
    app.sideLenV = 0
    app.person = []
    app.results = []
    app.paths = 0
    app.total = 0
    app.timerDelay = 500
    app.infectedLocations = []
    app.infectedInteractions = 0
    app.switch = 0
    app.selection = False
    

def timerFired(app):
    app.sideLenH = app.width / app.cols
    app.sideLenV = app.height / app.rows
    if(not app.dimensionTime):
        app.store[0][0] = 0       
    if(app.inputsAccepted):
        app.people[0][0] = 0
    if(app.storeLooksFinal and not app.simulationEnded):
        getLocations(app)
    if(app.selectionTime and not app.selection):
        app.items = make2dList(app.rows,app.cols)
        app.selection = True

def getLocations(app):
    finalPosns = []
    app.independentInteractions = []
    for col in range(app.cols):
        for row in range(app.rows):
            if(app.store[row][col] == 2):
                finalPosns.append([row,col])
    lengthResults = len(finalPosns)
    for i in range(lengthResults):
        app.paths = 0
        if(i == 0):
            startRow = 0
            startCol = 0
        else:
            startRow = finalPosns[i-1][0]
            startCol = finalPosns[i-1][1]
        app.rowOfResult = finalPosns[i][0]
        app.colOfResult = finalPosns[i][1]
        app.results.append(get_paths(app,startRow,startCol))
        app.independentInteractions.append(app.infectedInteractions)
        app.infectedInteractions = 0
    app.simulationEnded = True


def checkIntersect(app,row,col):
    if((row,col) in app.infectedLocations):
        app.infectedInteractions += 1

def get_paths(app, row, col): 
    checker = True
    checkBlackRows = False
    if ((row == app.rowOfResult) and (col == app.colOfResult)):
            app.paths += 1
            return
    else:
        if(col + 1 < app.cols):
            if (app.store[row][col+1] == 1 and app.colOfResult > col
                or row == 0 and app.store[row+1][col+1] == 1 and 
                app.colOfResult > col):
                colCount = 0
                for i in range(col,app.cols-1):
                    if(row == 0):
                        if(app.store[row+1][i + 1] == 1): colCount += 1
                        else:   break
                    else:
                        if(app.store[row][i + 1] == 1): colCount += 1
                        else:   break
                for i in range(row): 
                    row -= 1
                    app.person[row][col] = 1
                    checkIntersect(app,row,col)
                for i in range(colCount+1): 
                    col += 1
                    app.person[row][col] = 1
                    checkIntersect(app,row,col)                   
        if row > app.rowOfResult and col < app.colOfResult and valid(app,row,col+1):
            checkUpRight(app,row,col)
        elif (row > app.rowOfResult): checkUp(app,row,col)
        else: checkDown(app,row,col,checker,checkBlackRows)
    return app.paths


def checkUp(app,row,col):
    app.person[row-1][col] = 1
    checkIntersect(app,row-1,col)
    get_paths(app, row - 1, col)

def checkUpRight(app,row,col):
    app.person[row-1][col] = 1
    app.person[row][col+1] = 1
    checkIntersect(app,row-1,col)
    checkIntersect(app,row,col+1)
    get_paths(app, row - 1, col)
    get_paths(app, row, col+1)

def checkDown(app,row,col,checker,checkBlackRows):
    if col < app.colOfResult and valid(app,row,col + 1):
        app.person[row][col+1] = 1
        checkIntersect(app,row,col+1)
        checker = False
        get_paths(app,row,col + 1)
    if row < app.rowOfResult and valid(app,row + 1, col): 
        for c in range(col, app.colOfResult):
            if(app.store[row][c] == 1):
                checkBlackRows = True
        if(checkBlackRows):
            pass
        else:
            app.person[row+1][col] = 1
            checkIntersect(app,row+1,col)
            get_paths(app, row + 1, col)
           

def valid(app, row, col):
    if(row >= app.rows or col >= app.cols):
        return False
    if(app.store[row][col] == 1):
        return False
    return True

def changeDimensions(app):
    app.store = make2dList(app.rows,app.cols)

def keyPressed(app, event):
    if(app.dimensionTime): 
        if(event.key == "Up"):
            app.rows += 1
        if(app.rows > 1):
            if(event.key == "Down"):
                app.rows -= 1
        if(event.key == "Right"):
            app.cols += 1
        if(app.cols > 1):
            if(event.key == "Left"):
                app.cols -= 1  
        changeDimensions(app)
        app.person = make2dList(app.rows, app.cols)
        app.person[0][0] = 1
    if(event.key == "n" and app.dimensionTime):
        app.dimensionTime = False
        app.barrierTime = True
    if(event.key == "k" and app.barrierTime):
        app.barrierTime = False
        app.selectionTime = True
    if(event.key == "i" and app.selectionTime):
        app.selectionTime = False
        createInputLocation(app)
    if(event.key == "q" and app.inputsAccepted):
        import tp3
    

def mousePressed(app, event):
    rows = app.rows
    cols = app.cols
    for row in range(1,rows):
        for col in range(cols):
            cx0 = app.sideLenH*col
            cx1 = cx0 + app.sideLenH
            cy0 = app.sideLenV*row
            cy1 = cy0 + app.sideLenV
            if(app.barrierTime):
                if(app.store[row][col] == 0):
                    if(event.x >= cx0 and event.x <= cx1 and 
                        event.y >= cy0 and event.y <= cy1):
                        for r in range(1,rows):
                            app.store[r][col] = 1
                elif(event.x >= cx0 and event.x <= cx1 and 
                    event.y >= cy0 and event.y <= cy1):
                    app.store[row][col] = 0
            if(app.selectionTime):
                if(app.store[row][col] == 1):
                    pass
                elif(app.store[row][col] != 2):
                    if(event.x >= cx0 and event.x <= cx1 and 
                        event.y >= cy0 and event.y <= cy1):
                        orderItems(app,row,col)
                elif(event.x >= cx0 and event.x <= cx1 and 
                    event.y >= cy0 and event.y <= cy1):
                    changeInfo(app, row, col)

def orderItems(app, row, col):
    app.countItems += 1
    itemNumIterator = 1
    app.store[row][col] = 2
    for col in range(app.cols):
        for row in range(app.rows):
            if(app.store[row][col] == 2):
                app.items[row][col] = itemNumIterator
                itemNumIterator += 1

def changeInfo(app, row, col):
    app.store[row][col] = 0
    app.countItems -= 1
    numChanging = app.items[row][col]
    app.items[row][col] = 0
    for row in range(app.rows):
        for col in range(app.cols):
            if(app.items[row][col] > numChanging):
                app.items[row][col] -= 1



def createInputLocation(app):
    app.root = Tk()
    title = Label(app.root, text="Grocery Store Selector", font="Arial 15 bold")
    title.pack()

    #first 
    textBox1Label = Label(app.root, text='How many infected people would ' +
                        'you like in the model', width=50, height=10)
    textBox1Label.pack()
    app.textBox1 = Text(app.root, height=5, width=20)
    app.textBox1.pack()

    button = Button(app.root, height=1, width=10, text="select", 
                            command=lambda: getInputsStore(app))
    button.pack()
    mainloop()


def getInputsStore(app):
    app.infectedPeople = int(app.textBox1.get("1.0","end-1c"))
    app.root.destroy()
    app.inputsAccepted = True
    modelPeople(app)

def modelPeople(app):
    openSpots = 0
    takenSpots = 0
    app.people = make2dList(app.rows,app.cols)
    for row in range(app.rows):
        for col in range(app.cols):
            app.people[row][col] = -1
            if(app.store[row][col] != 1):
                app.people[row][col] = 0
                openSpots += 1
    addInfectedPeople(app, takenSpots, openSpots)

def addInfectedPeople(app, takenSpots, openSpots):
    takenSpots = 0
    for row in range(app.rows):
        for col in range(app.cols):
            if(takenSpots < app.infectedPeople and app.people[row][col] == 0):
                app.people[row][col] = 1
    selectSpots(app,openSpots,takenSpots)

def selectSpots(app, openSpots, takenSpots):
    if(openSpots == 0 or takenSpots == app.infectedPeople):
        return
    randomPos = random.randint(0,openSpots)
    row = randomPos // app.cols
    col = randomPos - row*app.cols
    if(valid(app,row,col) and app.people[row][col] != -1 and app.store[row][col] != 2): 
        app.people[row][col] = 2
        app.infectedLocations.append((row,col))
        selectSpots(app, openSpots, takenSpots + 1)
    else: 
        selectSpots(app, openSpots, takenSpots)
    app.storeLooksFinal = True

   
def drawStore(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            cx0 = app.sideLenH*col
            cx1 = cx0 + app.sideLenH
            cy0 = app.sideLenV*row
            cy1 = cy0 + app.sideLenV
            if(app.store[row][col] == 0):
                canvas.create_rectangle(cx0,cy0,cx1,cy1,fill="blue")
            elif(app.store[row][col] == 1):
                canvas.create_rectangle(cx0,cy0,cx1,cy1,fill="black")
            else:
                canvas.create_rectangle(cx0,cy0,cx1,cy1,fill="green")


def drawText(app, canvas):
    if(app.dimensionTime):
        canvas.create_text(app.width/2, app.height/20, 
                    text="Press up to increase rows, down to decrease rows, " +
                         "right to increase cols, left to decrease cols",
                         fill = "red", font="Arial 12")
        canvas.create_text(app.width/2, 19*app.height/20, 
                    text="Press n once you are finished", fill = "red",
                    font= "Arial 12")
    elif(app.barrierTime):
        canvas.create_text(app.width/2, app.height/20, 
                    text="Click on a box to make the column an aisle, twice " +
                         "to return it back to normal",
                         fill = "red", font="Arial 12")
        canvas.create_text(app.width/2, 19*app.height/20, 
                    text="Press k once you are finished", fill = "red",
                    font= "Arial 12")
    elif(app.selectionTime):
        canvas.create_text(app.width/2, app.height/20, 
                    text="Click on a box once to make it a location, twice " +
                         "to return it back to normal",
                         fill = "red", font="Arial 12")
        canvas.create_text(app.width/2, 19*app.height/20, 
                    text="Press i once you are finished", fill = "red",
                    font= "Arial 12")

    
def drawGroceries(app, canvas):
    if(app.selectionTime):
        for row in range(app.rows):
            for col in range(app.cols):
                if(app.selection and app.items[row][col] > 0):
                    cx = app.sideLenH*col + app.sideLenH/2
                    cy = app.sideLenV*row + app.sideLenV/2
                    canvas.create_text(cx, cy, text=str(app.items[row][col]),
                                        fill="red")                

def drawSimulation(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            if(app.people[row][col] == 2):
                cx = app.sideLenH*col + app.sideLenH/2
                cy = app.sideLenV*row + app.sideLenV/2
                sh = app.sideLenH
                sv = app.sideLenV
                canvas.create_polygon(cx - sh/2, cy, cx, cy + sv/2, cx + sh/2, 
                                    cy, cx, cy - sv/2, fill="red")       

def drawPerson(app, canvas):
    if(app.switch %2 == 0):
        for row in range(app.rows):
            for col in range(app.cols):
                if(app.person[row][col] == 1):
                    cx = app.sideLenH*col + app.sideLenH/2
                    cy = app.sideLenV*row + app.sideLenV/2
                    sh = app.sideLenH
                    sv = app.sideLenV
                    canvas.create_oval(cx - sh/2, cy - sv/2, cx + sh/2, cy + sv/2, 
                                    fill="purple")

def drawResults(app, canvas):
    if(app.simulationEnded):
        if(app.results != []):
            total = app.results[0]
            #by multiplication principle, we can multiply events
            for i in app.results[1:]:
                total *= i
        else:
            total = 0
        if(app.independentInteractions != []):
            totalInfections = 0
            strInfections = ""
            for i in range(len(app.independentInteractions)):
                strInfections += "grocery item " + str(i + 1) + ") " + str(app.independentInteractions[i]) + """ chances of 
                intersecting with an infected person\n"""

        
        canvas.create_text(app.width/2, 17*app.height/20, text="There are a total " +
        str(total) + """ ways to collect all of your groceries in the fashion that
        the circles represent. \n""" + strInfections, 
        font= "Arial 12 bold", fill="orange")

def drawGoBack(app,canvas):
    canvas.create_text(9*app.width/10, app.height/20, 
        text="Press q to return to main screen ", fill="red")

def drawEntrance(app, canvas):
    canvas.create_text(app.width/20, app.height/20, 
        text="Entrance ", fill="green")

def redrawAll(app, canvas):
    drawStore(app,canvas)
    drawText(app, canvas)
    drawGroceries(app, canvas)
    if(app.inputsAccepted):
        drawPerson(app, canvas)
        drawSimulation(app, canvas)
        drawResults(app, canvas)
        drawGoBack(app,canvas)
        drawEntrance(app,canvas)

runApp(width=1500, height=1500)
import pandas as pd
from cmu_112_graphics import *
from tkinter import *
import states
import random

def appStarted(app):
    app.countyCalculated = False
    app.firstStep = True
    app.charsCalculated = False
    app.pos = []
    app.R = 4
    app.showVisualization = False
    app.correctInput = True
    app.timerDelay = 1000
    app.blueCircles = []
    app.redCircles = []
    app.numBlueCircles = 0
    app.numRedCircles = 0
    app.dirX = "right"
    app.dirY = "up"


def createPosn(app, cases, deaths):
    for i in range(cases):
        cx = random.randint(0, app.width)
        cy = random.randint(int(app.height/10), app.height)
        color = "blue"
        app.pos.append([cx,cy,color,-1,"right","up"])
        app.blueCircles.append([cx,cy,color,-1])
        app.numBlueCircles = len(app.blueCircles)

    for i in range(deaths):
        cx = random.randint(0, app.width)
        cy = random.randint(int(app.height/10), app.height)
        color = "red"
        app.pos.append([cx,cy,color,-1,"right","up"])
        app.redCircles.append([cx,cy,color,-1])
        app.numRedCircles = len(app.redCircles)
    for pos in app.pos:
        if(pos[2] == "blue"):
            pos[3] += 1
            if(pos[3] >= 14):
                app.pos.remove(pos)


def moveCircles(app):
    movementX = app.width // 20
    movementY = app.height // 20
    for circle in app.pos:
        if(circle[4] == "right"):
            circle[0] += random.randint(0,movementX)
        if(circle[4] == "left"):
            circle[0] -= random.randint(0,movementX)
        if(circle[5] == "up"):
            circle[1] -= random.randint(0,movementY)
        if(circle[5] == "down"):
            circle[1] += random.randint(0,movementY)
        if(circle[0] >= app.width):
            circle[4] = "left"
        if(circle[0] <= 0):
            circle[4] = "right"
        if(circle[1] <= app.width//10):
            circle[5] = "down"
        if(circle[1] >= app.height):
            circle[5] = "up"

def findCircles(app):
    createPosn(app, app.increasesCasesL[0])

def timerFired(app):
    if(app.countyCalculated):
        createPosn(app, app.increasesCasesL[0] - app.increasesDeathsL[0],
                    app.increasesDeathsL[0])
        app.increasesCasesL.pop(0)
        app.increasesDeathsL.pop(0)
        moveCircles(app)
        app.datesL.pop(0)


def createInputLocation(app):
    app.root = Tk()
    title = Label(app.root, text="County Selector", font="Arial 15 bold")
    title.pack()

    #first 
    textBox1Label = Label(app.root, text='Enter your state name', width=50, height=10)
    textBox1Label.pack()
    app.textBox1 = Text(app.root, height=5, width=20)
    app.textBox1.pack()

    textBox2Label = Label(app.root, text="Enter your county name", width=50, height=10)
    textBox2Label.pack()
    app.textBox2 = Text(app.root, height=5, width=20)
    app.textBox2.pack()

    button = Button(app.root, height=1, width=10, text="select", 
                            command=lambda: getInputsLocation(app))
    button.pack()

    mainloop()


def getInputsLocation(app):
    app.inputState = app.textBox1.get("1.0","end-1c")
    app.inputCounty = app.textBox2.get("1.0","end-1c")
    app.root.destroy()
    getCountyData(app)
    app.countyCalculated = True


def getCountyData(app):
    countyData = r'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    readableData = pd.read_csv(countyData)
    app.state_data = readableData[readableData['state'] == app.inputState]
    app.county = app.state_data[app.state_data['county'] == app.inputCounty]
    createLists(app)
    totals(app)
    increases(app)
    analysisIncreasesCases(app)
    app.loadingCalculating = False

def createLists(app):
    app.datesL = []
    app.countiesL = []
    app.statesL = []
    app.casesL = []
    app.deathsL = []
    for date in app.county.date:
        app.datesL.append(date)
    if(len(app.datesL) == 0):
        app.correctInput = False
        return
    else:
        app.correctInput = True
    for county in app.county.county:
        app.countiesL.append(county)
    for state in app.county.state:
        app.statesL.append(state)
    for cases in app.county.cases:
        app.casesL.append(cases)
    for deaths in app.county.deaths:
        app.deathsL.append(deaths)
    

def totals(app):
    app.totalRecorded = len(app.datesL)
    app.totalCases = app.casesL[len(app.casesL) -1]
    app.totalDeaths = app.deathsL[len(app.deathsL) - 1] 

def increases(app):
    app.increasesCasesL = []
    app.increasesDeathsL = []
    #first recordings have increase of 0
    app.increasesCasesL.append(0)
    app.increasesDeathsL.append(0) 
    #increase in cases list
    for i in range(1, len(app.casesL)):
        increase = app.casesL[i] - app.casesL[i-1]
        app.increasesCasesL.append(increase)
    #increase in deaths list
    for j in range(1, len(app.deathsL)):
        increase = app.deathsL[j] - app.deathsL[j-1]
        app.increasesDeathsL.append(int(increase))

def avgIncreaseCases(app, n):
    sumIncreasesCases = 0
    lengthCases = len(app.increasesCasesL)
    for i in range(lengthCases - n, lengthCases):
        sumIncreasesCases += app.increasesCasesL[i]
    avgIncCases = sumIncreasesCases / n
    return avgIncCases

def avgIncreaseDeaths(app,n): 
    sumIncreasesDeaths = 0
    lengthDeaths = len(app.increasesDeathsL)
    for i in range(lengthDeaths - n, lengthDeaths):
        sumIncreasesDeaths += app.increasesDeathsL[i]
    avgIncDeaths = sumIncreasesDeaths / n
    return avgIncDeaths


def analysisIncreasesCases(app):
    app.last12WeeksInc = 0
    startPoint = len(app.increasesCasesL) - 84
    endPoint =  len(app.increasesCasesL)
    for i in range(startPoint, endPoint):
        app.last12WeeksInc += app.increasesCasesL[i]
    app.last4WeeksInc = 0
    startPoint = len(app.increasesCasesL) - 28
    for i in range(startPoint, endPoint):
        app.last4WeeksInc += app.increasesCasesL[i]
    startPoint = len(app.increasesCasesL) - 7
    app.lastWeekInc = 0
    for i in range(startPoint, endPoint):
        app.lastWeekInc += app.increasesCasesL[i]
    app.weekToMonth = app.lastWeekInc / app.last4WeeksInc
    app.monthTo3Months = app.last4WeeksInc / app.last12WeeksInc    


def keyPressed(app, event):
    if(event.key == "1" and app.countyCalculated == False):
        app.firstStep = False
        createInputLocation(app)
    if(not app.correctInput and event.key == "s"):
        createInputLocation(app)
    if(event.key == "2" and app.charsCalculated == False):
        app.firstStep = False
        import groceryStore
    if(event.key == "3"):
        import visual
    if(event.key == "b" and app.countyCalculated or app.charsCalculated):
        runApp(width=1500, height=1500)
    if(event.key == "n" and app.countyCalculated):
        app.showVisualization = True
        



def announcements(app, canvas):
    if(app.firstStep):
        canvas.create_rectangle(0,0,app.width,app.height,fill="yellow")
        canvas.create_text(app.width/2, app.height/10,
                            text='What do you want to do?', 
                            font='Arial 30 bold')
        canvas.create_text(app.width/2, app.height/3,
                            text='1) Calculate detailed location data by county', 
                            font='Arial 20 bold')
        canvas.create_text(app.width/2, app.height/2,
                            text='2) Start grocery store simulation', 
                            font='Arial 20 bold')
        canvas.create_text(app.width/2, 2*app.height/3,
                            text='3) Start general infection simulation', 
                            font='Arial 20 bold')

def drawCountyCalcs(app,canvas):
    if(not app.showVisualization):
        canvas.create_rectangle(0,0,app.width,app.height,fill="green")
        canvas.create_text(app.width/2, app.height/8,
                            text='Calculated risk based on county location: ', 
                            font='Arial 20 bold')
        canvas.create_text(app.width/2, app.height/4,
                            text="Over the last week, there are " + 
                            str(app.lastWeekInc) + " cases.", 
                            font='Arial 15 bold')
        canvas.create_text(app.width/2, 3*app.height/8,
                            text="Over the last 4 weeks, there are " + 
                            str(app.last4WeeksInc) + " cases.", 
                            font='Arial 15 bold')
        canvas.create_text(app.width/2, app.height/2,
                            text="Over the last 12 weeks, there are " + 
                            str(app.last12WeeksInc) + " cases.", 
                            font='Arial 15 bold')
        canvas.create_text(app.width/2, 5*app.height/8,
                            text="The cases from the last week account for " +
                            str(round(app.weekToMonth*100,3)) + "%" + 
                            " of the cases from the last 4 weeks." , 
                            font='Arial 15 bold')
        canvas.create_text(app.width/2, 3*app.height/4,
                            text="The cases from the last 4 weeks account for " +
                            str(round(app.monthTo3Months*100,3)) + "%" + 
                            " of the cases from the last 12 weeks." , 
                            font='Arial 15 bold')
        canvas.create_text(app.width/2, 7*app.height/8,
                            text="press 'n' to look at visual" , 
                            font='Arial 10 bold')
        
def drawCharsCalcs(app, canvas):
    canvas.create_text(app.width/2, 7*app.height/8,
                        text=str(app.worseConds) + str(app.betterConds), 
                        font='Arial 10 bold')


def drawVisualization(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="orange")
    for circle in app.pos:
        cx0 = circle[0] - app.R
        cy0 = circle[1] - app.R
        cx1 = circle[0] + app.R
        cy1 = circle[1] + app.R
        color = circle[2]
        canvas.create_oval(cx0,cy0,cx1,cy1,fill=color)
    canvas.create_text(app.width/2, app.height/20,
                        text="There were " + str(app.numBlueCircles) + 
                        " (blue) active cases and " + str(app.numRedCircles) + 
                        " (red) deaths in " + str(app.inputCounty) + 
                        " county, " + str(app.inputState) + " during " +
                        str(app.datesL[0]), 
                        font='Arial 10 bold')
    canvas.create_text(app.width/2, 7*app.height/8,
                        text="press 'b' to return to start" , 
                        font='Arial 10 bold')

def drawCorrectInput(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="orange")
    canvas.create_text(app.width/2,app.height/2,text="""Invalid state and/or
    county, press s to try again""", font="Arial 25 bold")

def redrawAll(app,canvas):
    announcements(app,canvas)
    if(app.countyCalculated):
        drawCountyCalcs(app, canvas)
        if(app.showVisualization):
            drawVisualization(app,canvas)
    if(app.charsCalculated):
        drawCharsCalcs(app,canvas)
    if(not app.correctInput):
        drawCorrectInput(app,canvas)



runApp(width=1500, height=1500)
import pandas as pd
from cmu_112_graphics import *
from tkinter import *
import random
import math
import copy

#From class notes: https://www.cs.cmu.edu/~112/notes/notes-graphics.html
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

def appStarted(app):
    app.blueCircles = []
    app.numBlueCircles = 0
    app.redCircles = []
    app.allCircles = []
    app.purpleCircles = []
    app.greenCircles = []
    app.deadCircles = []
    app.numRedCircles = 0
    app.R = 10
    app.infectionR = app.R*10
    app.simulating = False
    app.inputsAccepted = False
    app.timerDelay = 250
    app.newL = []
    app.day = 0
    app.factor = 1
    app.factorUp = True
    #got this matrix from research at 
    #https://web.cortland.edu/matresearch/MarkovChainCovid2020.pdf
    app.markov = [[0.93, 0.07, 0, 0, 0],
                [0.1, 0.8, 0.1, 0, 0],
                [0, 0.15, 0.8, 0.05, 0],
                [0, 0, 0.35, 0.6, 0.05],
                [0, 0, 0, 0, 1]]
    app.matched = []
    app.pastDayNum = 0
    app.circleRiskyDays = []
    app.allCirclesPast = []


def createInputSim(app):
    app.root = Tk()
    title = Label(app.root, text="Simulation selector", font="Arial 15 bold")
    title.pack()

    #first 
    textBox1Label = Label(app.root, text='How many people will you model?', width=50, height=5)
    textBox1Label.pack()
    app.textBox1 = Text(app.root, height=1, width=20)
    app.textBox1.pack()
    #second
    textBox2Label = Label(app.root, text="How many do you want to begin " +
                            "with COVID", width=50, height=5)
    textBox2Label.pack()
    app.textBox2 = Text(app.root, height=1, width=20)
    app.textBox2.pack()
    #third
    textBox3Label = Label(app.root, text="How many people starting with COVID"+
                         " will wear masks", width=50, height=5)
    textBox3Label.pack()
    app.textBox3 = Text(app.root, height=1, width=20)
    app.textBox3.pack()
    #fourth
    textBox4Label = Label(app.root, text="How many people starting healthy" +
                         " will wear masks", width=50, height=5)
    textBox4Label.pack()
    app.textBox4 = Text(app.root, height=1, width=20)
    app.textBox4.pack()

    button = Button(app.root, height=1, width=10, text="select", 
                            command=lambda: getInputsSim(app))
    button.pack()

    mainloop()


def getInputsSim(app):
    app.numCircles = int(app.textBox1.get("1.0","end-1c"))
    app.numInfected = int(app.textBox2.get("1.0","end-1c"))
    app.numMaskedInfected = int(app.textBox3.get("1.0","end-1c"))
    app.numMaskedHealthy = int(app.textBox4.get("1.0","end-1c"))
    app.inputsAccepted = True
    createCircles(app)
    app.root.destroy()

def addCircles(app, colorSelect):
    cx = random.randint(0, app.width)
    cy = random.randint(int(app.height/5), app.height)
    color = colorSelect
    angle = random.randint(0,360)
    angle = math.radians(angle)
    risk = 0
    daysI = 1
    daysH = 0
    daysICU = 0
    masked = False
    #                       0  1   2     3    4     5     6      7    8       9
    app.allCircles.append([cx,cy,color,risk,False,angle,masked,daysI,daysH,daysICU])
    if(color == "blue"):
        app.blueCircles.append([cx,cy,color,risk,False,angle,masked,daysI,daysH,daysICU])
        app.numBlueCircles = len(app.blueCircles)
    else:
        app.redCircles.append([cx,cy,color,risk,False,angle,masked,daysI,daysH,daysICU])
        app.numBlueCircles = len(app.blueCircles)


def createCircles(app):
    numHealthy = app.numCircles - app.numInfected
    for i in range(numHealthy):
        if(i < app.numMaskedHealthy):
            masked = True
        else:
            masked = False
        cx = random.randint(0, app.width)
        cy = random.randint(int(app.height/5), app.height)
        color = "blue"
        angle = random.randint(0,360)
        angle = math.radians(angle)
        risk = 0
        daysI = 1
        daysH = 0
        daysICU = 0
        #                       0  1   2     3    4     5     6      7    8       9
        app.allCircles.append([cx,cy,color,risk,False,angle,masked,daysI,daysH,daysICU])
        app.blueCircles.append([cx,cy,color,risk,False,angle,masked,daysI,daysH,daysICU])
        app.numBlueCircles = len(app.blueCircles)
    for i in range(app.numInfected):
        if(i < app.numMaskedInfected):
            masked = True
        else:
            masked = False
        cx = random.randint(0, app.width)
        cy = random.randint(int(app.height/5), app.height)
        color = "red"
        angle = random.randint(0,360)
        angle = math.radians(angle)
        risk = 0
        daysI = 1
        daysH = 0
        daysICU = 0
        app.allCircles.append([cx,cy,color,risk,False,angle,masked,daysI,daysH,daysICU])
        app.redCircles.append([cx,cy,color,risk,False,angle,masked,daysI,daysH,daysICU])
        app.numRedCircles = len(app.blueCircles)


def proximityMeasure(app):
    for circleRed in app.redCircles:    
        for circleBlue in app.blueCircles:
            riskPercent = 0
            separation = ((circleBlue[0] - circleRed[0])**2 + 
                        (circleBlue[1] - circleRed[1])**2)**(0.5)
            if(separation < app.infectionR):
                circleBlue[4] = True
                circleBlue[3] += 1 #days in danger
                app.matched.append((circleRed, circleBlue))
            if((circleRed, circleBlue) in app.matched and separation >= app.infectionR):
                circleBlue[4] = False
                app.matched.remove((circleRed, circleBlue))
            elif(not circleBlue[4] and circleBlue[3] > 0 and separation >= app.infectionR):
                circleBlue[3] = 0


def multiplyMarkov(app, power,m1, m2):
    #same rows and cols for both since we are just taking a power
    rows =  5
    cols = 5     
    multipliedL = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for x in range(rows):
        for y in range(cols):
            for z in range(rows):
                #takes the dot product of two vectors by adding
                #then moves on to a new position
                    addition = m1[x][z]*m2[z][y]
                    multipliedL[x][y] += addition
    if(power == 1):
        return app.markov
    elif(power <= 2):
        return multipliedL
    else:
        power -= 1
        return multiplyMarkov(app,power,multipliedL, app.markov)


def blueToOthers(app):
    for circle in app.blueCircles:
        if(circle[3] > 0):
            riskM = multiplyMarkov(app, circle[3], app.markov, app.markov)
            if(circle[6]):
                x = 1.1*random.randint(0,100)
            else:
                x = 1.1*random.randint(0,100)
            riskI = 100*riskM[0][1]
            if(x <= riskI):
                app.blueCircles.remove(circle)
                app.redCircles.append([circle[0],circle[1],"red", 0, circle[4],
                         circle[5],circle[6],circle[7],circle[8],circle[9]])


def redToOthers(app):
    for circle in app.redCircles:
        probM = multiplyMarkov(app, circle[7], app.markov, app.markov)
        circle[7] += 1
        if(circle[6]):
                x = 1.1*random.randint(0,100)
        else:
            x = 1.1*random.randint(0,100)
        healChance = 100*probM[1][0]
        hospitalizeChance = 100*probM[1][2]
        ICUChance = 100*probM[1][3]
        if(x <= healChance):
            app.redCircles.remove(circle)
            app.blueCircles.append([circle[0],circle[1],"blue",circle[3],
                        circle[4], circle[5],circle[6],1,circle[8],circle[9]])
        if(x > healChance and x <= healChance + hospitalizeChance):
            app.redCircles.remove(circle)
            app.purpleCircles.append([circle[0],circle[1],"red",circle[3],
                        circle[4], circle[5],circle[6],1,1,circle[9]])
        if(x > healChance + hospitalizeChance and 
            x <= healChance + hospitalizeChance + ICUChance):
            app.redCircles.remove(circle)
            app.greenCircles.append([circle[0],circle[1],"red",circle[3],
                        circle[4], circle[5],circle[6],1,circle[8],1])


def purpleToOthers(app):
    for circle in app.purpleCircles:
        probM = multiplyMarkov(app, circle[8], app.markov, app.markov)
        circle[8] += 1
        x = random.randint(0,100)
        backToIChance = 100*probM[2][1]
        ICUChance = 100*probM[2][3]
        if(x <= backToIChance):
            app.purpleCircles.remove(circle)
            app.redCircles.append([circle[0],circle[1],"red",circle[3],
                        circle[4], circle[5],circle[6],0,0,circle[9]])
        if(x > backToIChance and x <= backToIChance + ICUChance):
            app.purpleCircles.remove(circle)
            app.greenCircles.append([circle[0],circle[1],"red",circle[3],
                        circle[4], circle[5],circle[6],0,0,1])
        

def greenToOthers(app):
    for circle in app.greenCircles:
        probM = multiplyMarkov(app, circle[9], app.markov, app.markov)
        circle[9] += 1
        x = random.randint(0,100)
        hChance = 100*probM[3][2]
        deathChance = 100*probM[3][4]
        if(x <= hChance):
            app.greenCircles.remove(circle)
            app.purpleCircles.append([circle[0],circle[1],"red",circle[3],
                        circle[4], circle[5],circle[6],0,1,0])
        if(x > hChance and x <= hChance + deathChance):
            app.greenCircles.remove(circle)
            app.deadCircles.append([circle[0],circle[1],"red",circle[3],
                       circle[4], circle[5],circle[6],0,0,0])


def moveColor(app,typeCircle):
    for circle in typeCircle:
        if(not circle[8] and not circle[9]):
            movementX = 5*math.cos(circle[5])
            movementY = 5*math.sin(circle[5])
            circle[0] += movementX
            circle[1] += movementY
            if(circle[0] >= app.width or circle[0] <= 0):
                circle[5] = math.pi - circle[5]
            elif(circle[1] <= app.width//10 or circle[1] >= app.height):  
                circle[5] = 2*math.pi - circle[5]  


def moveCircles(app):
    moveColor(app,app.blueCircles)
    moveColor(app,app.redCircles)




def removeFaultyBlue(app):
    app.allCircles = []
    for circle in app.blueCircles:
        app.allCircles.append(circle)
    for circle in app.redCircles:
        app.allCircles.append(circle)
    for circle in app.allCircles:
        if(app.allCirclesPast != []):
            if(circle[2] == "blue"):
                i = app.allCircles.index(circle)
                if(circle[3] == app.allCirclesPast[i][3]):
                    indexBlue = app.blueCircles.index(circle)
                    app.blueCircles[indexBlue][3] = 0
    app.allCirclesPast = copy.deepcopy(app.allCircles)



def timerFired(app):
    if(app.inputsAccepted):
        moveCircles(app)
        proximityMeasure(app)
        blueToOthers(app)
        app.day += 1
        redToOthers(app)
        purpleToOthers(app)
        removeFaultyBlue(app)
        greenToOthers(app)
         

def keyPressed(app, event):
    if(event.key == "k"):
        app.simulating = True
        createInputSim(app)
    if(event.key == "b"):
        addCircles(app, "blue")
    if(event.key == "r"):
        addCircles(app,"red")
    if(event.key == "q" and app.inputsAccepted):
        import tp3


def mousePressed(app,event):
    for circle in app.blueCircles:
        cx0 = circle[0] - app.R
        cx1 = circle[0] + app.R
        cy0 = circle[1] - app.R
        cy1 = circle[1] + app.R
        if(event.x >= cx0 and event.x <= cx1 and 
                event.y >= cy0 and event.y <= cy1):
            app.blueCircles.remove(circle)
            app.redCircles.append([circle[0],circle[1],"red", 0, circle[4],
                        circle[5],circle[6],circle[7],circle[8],circle[9]])
            

def drawRedCircles(app, canvas):
    for circle in app.redCircles:
        cx = circle[0]
        cy = circle[1]
        cx0 = cx - app.R
        cy0 = cy - app.R
        cx1 = cx + app.R
        cy1 = cy + app.R
        cx0I = cx - app.infectionR
        cy0I = cy - app.infectionR
        cx1I = cx + app.infectionR
        cy1I = cy + app.infectionR
        color = circle[2]
        canvas.create_oval(cx0,cy0,cx1,cy1,fill=color)
        canvas.create_oval(cx0I,cy0I,cx1I,cy1I)
        if(circle[6]):
            canvas.create_arc(cx0, cy0, cx1, cy, start=180, 
                            extent=180, fill="green")


def drawBlueCircles(app, canvas):
    for circle in app.blueCircles:
        cx = circle[0]
        cy = circle[1]
        cx0 = cx - app.R
        cy0 = cy - app.R
        cx1 = cx + app.R
        cy1 = cy + app.R
        color = circle[2]
        canvas.create_oval(cx0,cy0,cx1,cy1,fill=color)
        if(color == "blue" and circle[3] > 0):
            canvas.create_text(cx,cy,text=str(int(circle[3])), 
                        font= "Arial " + str(app.R) + " bold", fill="red")
        if(circle[6]):
            canvas.create_arc(cx0, cy0, cx1, cy, start=180, 
                            extent=180, fill="green")


def drawCircles(app, canvas):
    drawBlueCircles(app,canvas)
    drawRedCircles(app,canvas)


def startingScreen(app,canvas):
    if(not app.simulating):
        canvas.create_text(app.width/2, app.height/2, 
                            text="Press k to start COVID simulation",
                            font="Arial 20 bold")

def writeData(app, canvas):
    if(app.inputsAccepted):
        canvas.create_text(app.width/2, app.height /10,
                        text="Day " + str(app.day) + ": there are currently " + 
                        str(len(app.redCircles)) + " people infected, " + 
                        str(len(app.blueCircles)) + " people not infected, "  + 
                        str(len(app.deadCircles)) + " people who have died"
                        , font= "Arial 15 bold")

def animationBreathe(app, canvas):
    for circle in app.redCircles:
        angle = circle[5] - math.pi
        for angleIteration in range(20):
            changeAngle = math.pi / 10
            cx0 = circle[0] + app.R*math.cos(angle)
            cy0 = circle[1] + app.R*math.sin(angle)
            cx1 = circle[0] + (circle[7]*20 % app.infectionR)*math.cos(angle)
            cy1 = circle[1] + (circle[7]*20 % app.infectionR)*math.sin(angle)
            cx2 = circle[0] + (circle[7]*20 % app.infectionR)*math.cos(angle-changeAngle)
            cy2 = circle[1] + (circle[7]*20 % app.infectionR)*math.sin(angle+changeAngle)
            cx3 = circle[0] + (circle[7]*20 % app.infectionR)*math.cos(angle+changeAngle)
            cy3 = circle[1] + (circle[7]*20 % app.infectionR)*math.sin(angle-changeAngle)
            iteratingColor = int(255*(circle[7]*25 % 255 / app.infectionR))
            rgbV = rgbString(iteratingColor, iteratingColor, iteratingColor)
            canvas.create_line(cx0, cy0, cx1 , cy1, fill=rgbV)
            angle += changeAngle



def hospitalizeDraw(app, canvas):
    if(app.inputsAccepted):
        canvas.create_text(app.width/15, app.height/40,
                    text="Hospital", fill="purple", font="Arial 15 bold")
        for circle in app.purpleCircles:
            i = app.purpleCircles.index(circle)
            numHospitalized = len(app.purpleCircles)
            cx = app.width/20 + i*app.R*4
            cy = app.height/18
            cx0 = cx - app.R
            cy0 = cy - app.R
            cx1 = cx + app.R
            cy1 = cy + app.R
            canvas.create_text(app.width/40, cy,text="Regular")
            canvas.create_line(cx0,cy0,cx1 + 2*app.R,cy0)
            canvas.create_line(cx0,cy0,cx0,cy1)
            canvas.create_line(cx0,cy1,cx1 + 2*app.R,cy1)
            if(i == len(app.purpleCircles) -1):
                canvas.create_line(cx1 + 2*app.R,cy0,cx1+2*app.R,cy1)
            canvas.create_oval(cx0,cy0,cx1,cy1,fill="red")
            if(circle[6]):
                canvas.create_arc(cx0, cy0, cx1, cy, start=180, 
                                extent=180, fill="green")

def ICUDraw(app, canvas):
    if(app.simulating):
        for circle in app.greenCircles:
            i = app.greenCircles.index(circle)
            numICU = len(app.greenCircles)
            cx = app.width/20 + i*app.R*4
            cy = app.height/18 + 2*app.R
            cx0 = cx - app.R
            cy0 = cy - app.R
            cx1 = cx + app.R
            cy1 = cy + app.R
            canvas.create_text(app.width/40, cy,text="ICU", font="Arial 12 bold")
            canvas.create_line(cx0,cy0,cx1 + 2*app.R,cy0)
            canvas.create_line(cx0,cy0,cx0,cy1)
            canvas.create_line(cx0,cy1,cx1 + 2*app.R,cy1)
            randomStrL = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            randomColor = rgbString(randomStrL[0],randomStrL[1],randomStrL[2])
            canvas.create_rectangle(cx0,cy0, cx1 + 2*app.R,cy1,fill=randomColor)
            if(i == len(app.purpleCircles) -1):
                canvas.create_line(cx1 + 2*app.R,cy0,cx1+2*app.R,cy1)
            canvas.create_oval(cx0,cy0,cx1,cy1,fill="red")
            if(circle[6]):
                canvas.create_arc(cx0, cy0, cx1, cy, start=180, 
                                extent=180, fill="green")

              

def drawDeath(app,canvas):
    for circle in app.deadCircles:
        cx0 = circle[0] - app.R
        cx1 = circle[0] + app.R
        cy0 = circle[1] - app.R
        cy1 = circle[1] + app.R
        canvas.create_line(cx0,cy0,cx1,cy1, fill="red",width=3)
        canvas.create_line(cx0,cy1,cx1,cy0,fill="red",width=3)

def background(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="green")

def explainKeys(app,canvas):
    if(app.inputsAccepted):
        canvas.create_text(9*app.width/10,app.height/20,text="""Press b to add a new blue 
        circle, r for a red circle""", fill="purple", font="Arial 12 bold")

def drawGoBack(app,canvas):
    if(app.inputsAccepted):
        canvas.create_text(app.width/2, 19*app.height/20, 
            text="Press q to return to main screen ", fill="red")

def redrawAll(app,canvas):
    background(app,canvas)
    startingScreen(app,canvas)
    ICUDraw(app,canvas)
    drawCircles(app, canvas)
    writeData(app,canvas)
    animationBreathe(app,canvas)
    hospitalizeDraw(app, canvas)
    drawDeath(app,canvas)
    explainKeys(app,canvas)
    drawGoBack(app,canvas)
    

runApp(width=1500, height=1500)
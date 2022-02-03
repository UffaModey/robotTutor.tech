from tkinter import *
from tkinter import ttk
import tkinter as tk
import webbrowser
from serial.tools import list_ports
import serial
import psycopg2
import random
import os

#Database credentials
host = ''
port = ''
username = ''
password = ''
database = ''
sslmode  = 'require'

root = Tk()

#connect to robottutor
conn = psycopg2.connect(dbname=database, user=username, password=password, host=host, port=port)
#conn = psycopg2.connect(password=os.environ.get('PASSWORD'),
#                        dbname = os.environ.get('DATABASE'),
#                       user=os.environ.get('USERNAME'),
#                       host=os.environ.get('HOST'),
#                       port=os.environ.get('PORT'))

#create cursor for operating the Database
c = conn.cursor()

#application title and instruction text
title = ttk.Label(root, text = "robottutor.tech")
title.config(font = ('Courier', 32, 'bold'), background = 'yellow')
title.pack(pady = 20)

text = ttk.Label(root, text = '''Connect your robot via Bluetooth to this computer.
From the droupdown list, select the COM port on the computer that the robot is connected to.
Click 'connect robot' to open the robot programming application on your web browser.
A beep sound on the robot indicates that it is ready for use :)
''')
text.config(wraplength = 800)
text.pack(pady = 20)


#select com port
label1 = ttk.Label(root, text = "Select COM port")
label1.config(font = ('Courier', 18 ,'bold'), foreground = 'blue')
label1.pack(pady = 20)

allComPorts = serial.tools.list_ports.comports(include_links=False)

optionsList = []

for i in allComPorts:
    optionsList.append(i.device)

valueInside = StringVar(root)
#(print (optionsList))

dropdownMenu = ttk.OptionMenu(root, valueInside, optionsList[0], *optionsList)
dropdownMenu.pack()

robotport = ""
#passcode generation and label placement
words = ("ant", "bat", "cat", "day", "egg", "fig", "get", "hat", "ice", "jet", "kit")
passcodeOne = random.choice(words)
correct = passcodeOne
passcodeTwo = random.choice(words)
correct = passcodeTwo
passcodeThree = random.choice(words)
correct = passcodeThree
passcodeFour = random.choice(words)
correct = passcodeFour

passcodeGenerated = (passcodeOne+"-"+passcodeTwo+"-"+passcodeThree+"-"+passcodeFour)

passcodegui = passcodeGenerated
passcodeguilabel = ttk.Label(root, text = "Passcode is: "+passcodegui)
passcodeguilabel.pack(pady = 20)

#Connection ststus label
connectionStatus = "Robot not connected"
connectionStatusLabel = ttk.Label(root, text = connectionStatus)
connectionStatusLabel.config(font = ('Courier', 11 ,'bold'), foreground = 'red')
connectionStatusLabel.pack(pady = 20)

#Run code status label
messageLabel = ""
statusLabel = ttk.Label(root, text = messageLabel)
statusLabel.pack(pady = 20)

#put the gui passcode in the robottutor
c.execute('''SELECT * FROM robottutor_program
                ''')
newDBid = c.rowcount + 3
runid = 0

insertQuery = '''INSERT INTO robottutor_program
(id, "editorCode", "robotAPI", PASSCODEGUIAPP, PASSCODEWEBAPP, RUNID)
VALUES (%s,%s,%s,%s,%s,%s)'''
insertRecord = (newDBid, "","",passcodegui,"",runid)
c.execute(insertQuery, insertRecord)
conn.commit()

#connect robot
connectButton = ttk.Button(root, text = "Connect Robot")
connectButton.pack(pady = 20)


#run robot
runButton = ttk.Button(root, text = "Run Code")
runButton.pack(pady = 20)
robotportapi = ""


def connectRobot():
    # write to the robot comport
    robotport = valueInside.get()
    passcodelink = passcodeGenerated

    data = "PlayNote 100/100"
    try:
        ser = serial.Serial(robotport, 9600)
        ser.write(data.encode())
        connectionStatusLabel.config(text="Robot connected on port: "+robotport)
        statusLabel.config(text='')
        webbrowser.open("http://robottutor.tech/"+passcodelink+"/")
        return robotport
    except:
        connectionStatusLabel.config(text="Unable to connect to port: "+robotport)
        statusLabel.config(text='')
        return robotport
    

def getRobotAPI():
    #print('hiiii')
    c.execute('''SELECT * FROM database_program
                ''')
    num = c.rowcount + 2
    #print(num)
    c.execute('''SELECT * FROM database_program
                WHERE id = %s
                ''', (num,))
    row = c.fetchone()
    runid=row[5]
    runidb = row[5]

    if runid == runidb:
        if (row[2] != "" and row[3] == row[4]):
            robotport = valueInside.get()
            #robotportapi = connectButton.invoke()
            executerobot =row[2]
            try:
                ser = serial.Serial(robotport, 9600)
                connectionStatusLabel.config(text="Robot connected on port: "+robotport)
                ser.write(executerobot.encode())
                statusLabel.config(text='Success! Code running on robot')
                runid = runid + 1
            except:
                connectionStatusLabel.config(text="Unable to connect to port: "+robotport)
                statusLabel.config(text='Robot is not connected')
        else:
            statusLabel.config(text='Robot is not connected or No code saved')
    else:
        print('no save code yet')
        
    #root.after(1000, getRobotAPI)  # reschedule event in 2 seconds
    

connectButton.config(command = connectRobot)


runButton.config(command = getRobotAPI)

#runid = root.after(1000, getRobotAPI)
#print(runid)

root.mainloop()
c.close()
conn.close()



#'/dev/tty.FA103962-Port'

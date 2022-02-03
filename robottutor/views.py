
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, JsonResponse

from textx import metamodel_from_str
from robottutor.models import Program

from json import dumps
import os

from serial.tools import list_ports
import serial


def home(request, passcodeguiapplink='Input passcode from GUI app'):
    defaultEditorMessage = "// Input a motion command to the robot. For example; go 100 \n// '//' is used for comments."
    
    if request.method == 'POST':
        code = request.POST.get('editorCode', None).strip()
        passcodeguiapplink = request.POST.get('passcodewebapp', None).strip()
        num = Program.objects.count() + 2
        codefordatabase = Program.objects.get(id=num)
        if passcodeguiapplink == codefordatabase.passcodeguiapp:
            try:
                codefordatabase.editorCode=code
                codefordatabase.passcodewebapp=passcodeguiapplink
                codefordatabase.save()

                grammar = '''
        
                Program:
                commands*=Command
                ;

                Command:
                    ForwardCommand | BackwardCommand | TurnCommand 
                ;

                ForwardCommand:
                    'go' f=INT
                ;

                BackwardCommand:
                    'back' b=INT
                ;

                TurnCommand:
                    'turn' t=INT
                ;

                Comment:
                    /\/\/.*$/
                ;
                '''
                robottutor_mm = metamodel_from_str(grammar)

                program = codefordatabase.editorCode 
                        #'''
                        #// Robot motion comment
                        #go 100
                    # back 100
                    # turn 90
                        #'''
                robottutor_model = robottutor_mm.model_from_str(program)

                class Robottutor(object):

                    def interpret(self, model):
                    
                    #initialise string
                        resultStr = ""

                    #model is an instance of program
                        for c in model.commands:

                            if c.__class__.__name__ == "ForwardCommand":
                                result = "Forwards " + str(c.f)
                                resultStr = resultStr + result + "\n"

                            elif c.__class__.__name__ == "BackwardCommand":
                                result = "Backwards " + str(c.b)
                                resultStr = resultStr + result + "\n"

                            elif c.__class__.__name__ == "TurnCommand":
                                result = "Right " + str(c.t)
                                resultStr = resultStr + result + "\n"

                            else:
                                print("Invalid")
                        return resultStr

                #call function to interpret the program
                robot = Robottutor()
                result = robot.interpret(robottutor_model)
                codefordatabase.robotAPI=result
                codefordatabase.runid = codefordatabase.runid + 1
                codefordatabase.save()


                codesaved = "Code saved. Click //RUN CODE// on the GUI app."

                return render (request, 'hello_django/index.html', {'codesaved':codesaved, 'code': code, 'passcodeguiapplink': passcodeguiapplink})
                
            except:
                invalidsyntax = "Invalid syntax, parameter or no command sent."
                return render(request, 'hello_django/index.html', { 'code': code,  'invalidsyntax':invalidsyntax, 'passcodeguiapplink': passcodeguiapplink} )
  
        else:

            invalidpasscode = "Invalid passcode. Please put the correct passcode."
            return render(request, 'hello_django/index.html', {'invalidpasscode':invalidpasscode, 'code': code, 'passcodeguiapplink': passcodeguiapplink,})

    else:
        
        return render (request, 'hello_django/index.html', {'defaultEditorMessage':defaultEditorMessage, 'passcodeguiapplink': passcodeguiapplink} )

def run(request):
    
    if request.method == 'POST':
        num = Program.objects.count() + 2
        codefordatabase = Program.objects.get(id=num)
        passcodewebapp = request.POST.get('passcodewebapp', None).strip()
        code = request.POST.get('editorCode', None).strip()
        #code = codefordatabase.editorCode
        #passcodewebapp = codefordatabase.passcodewebapp
        if (codefordatabase.editorCode != "" and codefordatabase.passcodeguiapp == codefordatabase.passcodewebapp):
            robotport = "/dev/tty.FA103962-Port"
            try:
                ser = serial.Serial(robotport, 9600)
            
                ser.write(code.encode())
                coderunning = 'Success! Code running on robot'
                return render (request, 'hello_django/index.html', {'coderunning':coderunning, 'code': code, 'passcodewebapp': passcodewebapp,})
            except:
                runcodeerror= "Unable to connect to port: "+robotport+ '. Robot is not connected.'
                return render (request, 'hello_django/index.html', {'runcodeerror':runcodeerror, 'code': code, 'passcodewebapp': passcodewebapp,})
        else:
            runcodeerror = 'Robot is not connected or No code saved'
            return render (request, 'hello_django/index.html', {'runcodeerror':runcodeerror, 'code': code, 'passcodewebapp': passcodewebapp,})
                
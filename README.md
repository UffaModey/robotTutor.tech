Understanding computer programming may be quite difficult for learners. A good starting point in redesigning teaching and learning methods for programming is to enable novice programmers to develop a positive attitude towards programming. Recently, robots have gained popularity as a tool for teaching computer programming across various academic levels. Robots enabled learners to understand the programming concepts better in real time as well improve their problem solving skills. This project develops an application for novice programmers to control a robot with step-wise commands and minimum configuration. Using an online editor, the leaner is able to write human readable commands that controls a Formula AllCode robot. 

robottutor.tech is a web application accessible from the user's web browser and it is supported by a desktop Graphic User Interface application for communicating via Bluetooth with the Formula AllCode robot. The project allows novice programmers to write executable programs using a Domain Specific Language to the Formula AllCode robot without having to pay much attention to more complex programming configurations that may be associated with the programming development.

### Robot hardware set up
1.  Switch on the robot and ensure it is connected to the user's pc via Bluetooth
2.  Identify the PC COM port the robot is connected to
	1.  Windows - [https://help.fleetmon.com/en/articles/2010900-how-do-i-get-my-com-port-number-windows](https://help.fleetmon.com/en/articles/2010900-how-do-i-get-my-com-port-number-windows)
	2.  MAC – run ls /dev/tty.* on the mac terminal
	
### User Instructions
1.  Run robotutor.tech  GUI app
2.  Select the PC COM port the robot is connected to
3.  Click on “Connect robot”. The application web interface will automatically open on your web browser
4.  Ensure the correct passcode is input. This is usually done automatically.
5.  Write code on the editor. The parameters are integer values that indicate the range of motion the robot should cover. For forward and backward motion, an integer parameter such as 100 is 10cm distance. For turning and integer parameter such as 90 is a turn in 90 degrees angle,
	1.  Forward motion syntax – go **int parameter**
	2.  Backward motion syntax – back **int parameter**
	3.  Right turn syntax – turn **int parameter**
	4. Left turn syntax – turn **int -parameter**
6. Click on "SAVE" to save code written on the editor
7. Click on "RUN CODE" on the GUI app  to execute commands to the robot

robottutor.tech application programming  https://youtu.be/4dxYRS2dRJ4
    
robottutor.tech video demonstration  https://youtu.be/84sxuDH_Y4Y
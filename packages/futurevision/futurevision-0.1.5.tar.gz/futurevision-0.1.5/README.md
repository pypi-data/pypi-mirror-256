<div align="center">
  <img src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/logo2.svg"><br><br>
</div>

<div align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg" width="130" alt="made with love  markdown badge" >
<img src="https://forthebadge.com/images/badges/open-source.svg" width="130" height="30" alt="open source  markdown badge">
<br>
<br>
<img src="https://forthebadge.com/images/badges/made-with-markdown.svg" width="230" height="30" alt="made with markdown badge">
  
<br>
<br>

[![Downloads](https://pepy.tech/badge/futurevision)](https://pepy.tech/project/futurevision)
[![Downloads](https://pepy.tech/badge/futurevision/month)](https://pepy.tech/project/futurevision)
[![Downloads](https://pepy.tech/badge/futurevision/week)](https://pepy.tech/project/futurevision)

</div>





---

# <img src="https://user-images.githubusercontent.com/74038190/216122041-518ac897-8d92-4c6b-9b3f-ca01dcaf38ee.png" width="40" /> Future Vision : A New Era in Robotics Education


# What is it? <img src='https://user-images.githubusercontent.com/74038190/221857969-f37e1717-1470-4fe4-abb5-88b334cf64ea.png' width="40">



It allows you to control the leds, RGB led, buttons and 8x8 led matrix on your Arduino board with **Python** language.

You can control Arduino with computer vision using your host computer and facilitate computer vision on a Raspberry Pi board.

A **Darwin Future Vision** mobile app created for the library allows you to control your iPhone phone's observational hardware: its flash, screen brightness and speaker volume ratio.

It pulls iPhone hardware information about the phone's screen brightness, speaker volume ratio, and which volume button is pressed, allowing you to retrieve and use this data in your python code

You can control 5 led graphs in the LEDs section of the iPhone app.

With the iPhone app, you can send data to your python code or see the data you send from your python code in the app.

# What is the Goal <img  src="https://user-images.githubusercontent.com/74038190/216122069-5b8169d7-1d8e-4a13-b245-a8e4176c99f8.png" width="40"/>

It aims to reawaken children's curiosity in robotics education and break new ground in robotics education by going beyond the classical robotics education.

# Modular and Features <img  src='https://user-images.githubusercontent.com/74038190/221857969-f37e1717-1470-4fe4-abb5-88b334cf64ea.png' width="40"> 

With the **Arduino** module of the **Future Vision** library, you can control the LEDs, RGB LEDs and 8x8 LED matrix on Arduino using Python language, and also read values from the buttons connected to the analog pins of Arduino.

With the **Raspberry Pi** module of the **Future Vision** library, you can read and control the LEDs, RGB LEDs, 8x8 LED matrix on the Sense HAT and Sense HAT sensors on the Raspberry Pi, you can also read the Sense HAT joystick values.

With the **Vision** module of the **Future Vision** library, you can create your own sign language, detect hands, detect happiness and unhappiness on your face, detect the instantaneous number of faces in a room, detect colors, detect whether eyes are closed or open, manage keys on the keyboard, measure volume, make your computer talk, analyze left and right arm movements, recognize objects and perform personal face recognition.

With the **iPhone** module of the **Future Vision** library and the mobile app, you can control your iPhone's observational hardware: flash, screen brightness and speaker volume. You can also see the screen brightness, speaker volume ratio and volume up or down button presses data on your computer and control your Arduino or Raspberry Pi board based on this data, or you can control your phone's flash with Arduino and Raspberry Pi, for example, by pressing the button.

# Using Modules <img  src='https://user-images.githubusercontent.com/74038190/206662607-d9e7591e-bbf9-42f9-9386-29efc927bc16.gif' width="40"> 

## Arduino <img  src='https://user-images.githubusercontent.com/74038190/206662607-d9e7591e-bbf9-42f9-9386-29efc927bc16.gif' width="35"> 



In order for the **Future Vision** library to work correctly with your Arduino Uno board, you need to install the [FutureVision-Arduino.ino](https://github.com/AliEdis/futurevision/blob/main/FutureVision-Arduino/FutureVision-Arduino.ino) code on your Arduino Uno board.


Pins 13, 12 and 11 are dedicated to LED matrix, pins 10, 9, 8 are dedicated to RGB LED. You can only use pins 7, 6, 5, 4, 3, 2 as digital outputs.

### Led on and off

```python
from futurevision import arduino
uno=arduino.Arduino(usb_port="/dev/cu.usbmodem101",baud=9600)
uno.on(pin=7)
uno.wait(1)
uno.off(pin=7)
```

**LED connections are as follows.**

<div align="center">
  <img src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/led1.png"><br>
</div>

### RGB Led Controlled

Colors you can display on RGB LED:

1. Red 🔴
2. Yellow 🟡
3. Green 🟢
4. Blue 🔵
5. Purple 🟣
6. White ⚪️
7. Light Blue 🩵

You can turn off your RGB led by entering one of these parameters: **clear** & **off**

Pin layout of the RGB LED: **R:10 G:9 B:8**

```python
from futurevision import arduino
uno=arduino.Arduino(usb_port="/dev/cu.usbmodem101",baud=9600)
uno.rgb_led("red")
uno.wait(1)
uno.rgb_led("yellow")
uno.wait(1)
uno.rgb_led("green")
uno.wait(1)
uno.rgb_led("blue")
uno.wait(1)
uno.rgb_led("purple")
uno.wait(1)
uno.rgb_led("white")
uno.wait(1)
uno.rgb_led("clear")
uno.wait(1)
```

**RGB LED connections are as follows.**

<div align="center">
  <br>
  <img src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/rgb_led_pin.png"><br>
</div>

### Reading Button Value

The values of the buttons are set to be read only from analog pins. The returned button value will be given as {PIN}. For example, let's say we have two buttons connected to pins A0 and A3. When we press the A3 pin three times and press the button on the A0 pin twice, the terminal output will be as follows.

```python
from futurevision import arduino
uno=arduino.Arduino(usb_port="/dev/cu.usbmodem101",baud=9600)
while True:
    read=uno.read()
    print(read)
```

Terminal Output

```sh
(base) ali@aliedis-MacBook-Air Desktop % python3 test.py
3
3
3
0
0
```

**The button connections are as follows.**

<div align="center">
  <br>
  <img  src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/button_pin1.png"><br>
</div>

### Led Matrix Controlled

Pin Layout of Led Matrix: DIN:13, CS:12, CLK:11

You can show any characters you want in Led Matrix. The character and shape list is as follows:

A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

1, 2, 3, 4, 5, 6, 7, 8, 9, 0

+, -, *, /, %, %, =, up, down, right, left, happy, unhappy, heart

You can turn off your led matrix by entering one of these commands: clear & off

Led Matrix is set to run vertically by default. To change this, you can change the direction parameter to 0.

Example: uno.show_led_matrix("A",0)

```python
from futurevision import arduino
uno=arduino.Arduino(usb_port="/dev/cu.usbmodem101",baud=9600)

upper_letter_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lower_letter_list=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

number_list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
sign_list=['+', '-', '*', '/', '%', '=', 'up', 'down', 'right', 'left', 'happy', 'unhappy', 'heart']

for i in upper_letter_list:
  uno.show_led_matrix(i)
  uno.wait(1)
  uno.show_led_matrix("clear")

for i in lower_letter_list:
  uno.show_led_matrix(i)
  uno.wait(1)
  uno.show_led_matrix("clear")

for i in number_list:
  uno.show_led_matrix(i)
  uno.wait(1)
  uno.show_led_matrix("clear")

for i in sign_list:
  uno.show_led_matrix(i)
  uno.wait(1)
  uno.show_led_matrix("clear")
```

**Led Matrix connections are as follows.**

<div align="center">
  <br>
  <img  src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/led_matrix1.png"><br>
</div>

## Raspberry Pi <img  src='https://user-images.githubusercontent.com/74038190/206662607-d9e7591e-bbf9-42f9-9386-29efc927bc16.gif' width="35"> 



### Led on and off

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi()
rpi.on(14)
rpi.wait(1)
rpi.off(14)
```

### RGB Led Controlled

Colors you can display on RGB LED:

1. Red 🔴
2. Yellow 🟡
3. Green 🟢
4. Blue 🔵
5. Purple 🟣
6. White ⚪️
7. Light Blue 🩵

You can turn off your RGB led by entering one of these parameters: clear & off

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi()
rpi.rgb_led("red",14,15,18)
rpi.wait(1)
rpi.rgb_led("yellow",14,15,18)
rpi.wait(1)
rpi.rgb_led("green",14,15,18)
rpi.wait(1)
rpi.rgb_led("blue",14,15,18)
rpi.wait(1)
rpi.rgb_led("purple",14,15,18)
rpi.wait(1)
rpi.rgb_led("white",14,15,18)
rpi.wait(1)
rpi.rgb_led("lightblue",14,15,18)
rpi.wait(1)
rpi.rgb_led("clear",14,15,18)
rpi.wait(1)
```

### Reading Button Value

The button is set to PULL UP.

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi()
while True:
    button=rpi.read_button(14)
    if(button):
     print("Button Pressed")
    rpi.wait(0.1)
```

Terminal Output

```sh
>>> %Run test.py
Button Pressed
```

### Displaying Letters or Numbers in Sense HAT LED Matrix

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.show_letter("A")
rpi.wait(1)
rpi.show_letter("1")
rpi.wait(1)
rpi.clear()
```

#### Change Font Color and Background Color

List of colors you can select in the Sense HAT LED matrix:

None
White
Red
Green
Blue
Yellow
Purple
Orange
Pink
Cyan
Brown
Lime
Teal
Maroon

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.show_letter("A",text_colour="red",back_colour="white")
rpi.wait(1)
rpi.clear()
```

### Displaying Message in Sense HAT LED Matrix

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.show_message("Future Vision")
```

#### Changing Sense Line Message Display Speed

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.show_message("Future Vision",scroll_speed=0.2)
```

### Sense Hat Led Matrix Painting

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.fill("red")
rpi.wait(1)
rpi.clear()
```

### Sense Hat Led Matrix Sign Display

Signs you can show up, down, right, left, happy, unhappy, heart

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
sign_list=['up', 'down', 'right', 'left', 'happy', 'unhappy', 'heart']
for i in sign_list:
  rpi.show_sign(i)
  rpi.wait(1)
  rpi.clear()
```

#### Using Sense Hat Sensors

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
temperature=rpi.get_temperature()
humidity=rpi.get_humidity()
pressure=rpi.get_pressure()
gyroscope=rpi.get_gyroscope()
accelerometer=rpi.get_accelerometer()
compass=rpi.get_compass()

print(temperature)
print(humidity)
print(pressure)
print(gyroscope)
print(accelerometer)
print(compass)
```

Terminal Output

```sh
>>> %Run test.py
34.51753616333008
38.123626708984375
0
[-0.535936176776886, 0.06923675537109375, -0.25748658180236816]
[0.11419202387332916, 0.3673451840877533, 0.8629305362701416]
174.1544422493143
```

### Sense Hat Joystick Button Click Detection

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
while True:
  btn=rpi.joystick_button()
  print(btn)
  rpi.wait(0.1)
```

Terminal Output

```sh
>>> %Run test.py
False
False 
True
False
```

### Sense Hat Joystick Movements

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
while True:
  btn=rpi.joystick()
  print(btn)
  rpi.wait(0.1)
```

Terminal Output

```sh
>>> %Run test.py
up
down 
right
left
middle
```

## Vision <img  src='https://user-images.githubusercontent.com/74038190/206662607-d9e7591e-bbf9-42f9-9386-29efc927bc16.gif' width="35"> 


### Hand Detection

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, fingers, status=vision.detect_hand(img)
    print("Finger List: ",fingers,"Hand Status: ",status)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

fingers returns a list with 0 for closed fingers and 1 for open fingers.

The status variable returns True if all fingers are open, False if all fingers are closed.

Terminal Output

```sh
>>> %Run test.py
Finger List:  [1, 1, 1, 1, 1] Hand Status:  True
Finger List:  [0, 0, 0, 0, 0] Hand Status:  False
```

<div align="center">
  
  <img loading="eager" width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/default_hand_detection.gif?raw=true"><br>
</div>

<br>

#### Change the Color of a Hand Drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, fingers, status=vision.detect_hand(img,line_color="red",circle_color="green")
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

<div align="center">
  
  <img width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/custom_hand_detection.gif?raw=true"><br>
</div>

<br>

#### Disable Hand Drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, fingers, status=vision.detect_hand(img,draw=False)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

### Creating sign language

The fingers represented by the indexes in the list are as in the picture below.

<div align="center">
  <br>
  <img width="250" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/fingers_numbers.png?raw=true"><br>
</div>

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
        _,img=cap.read()
        img,fingers,status=vision.detect_hand(img)
        if len(fingers) > 0:
               if(fingers==[0,0,0,0,0]):
                      print("off")
               if(fingers==[0,0,0,0,1]):
                      print("right")
               if(fingers==[1,1,0,0,0]):
                      print("left")
        cv2.imshow("Future Vision",img)
        cv2.waitKey(1)
```

### Emotion Detection

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, emotion,th=vision.detect_emotion(img)
    print(emotion,th)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

emotion variable returns unhappy or happy depending on the happiness state.
th variable returns the happiness rate.

Terminal Output

```sh
unhappy 0.025
happy 0.045
unhappy 0.025
happy 0.045
```

Happiness detection threshold is set at 0.035 You can change your happiness detection threshold according to your preferences and needs

Changing the Happiness Threshold

```python
img, emotion,th=vision.detect_emotion(img,threshold=0.040)
```

<div align="center">
  
  <img width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/emotion_default1.gif?raw=true"><br>
</div>

<br>

#### Drawing a Face and Changing the Color of the Text

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, emotion,th=vision.detect_emotion(img,line_color="green",text_color="green")
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

<div align="center">
  
  <img width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/custom_emotion2.gif?raw=true"><br>
</div>

<br>

#### Disable Face Drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, emotion=vision.detect_emotion(img,draw=False,text=False)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

### Instant Face Counter

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, count=vision.count_faces(img)
    print(count)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

The count variable returns how many faces there are.

Terminal OutputInstant Face Counter

```sh
2
2
2
2
```

<div align="center">
  
  <img width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/count_faces.gif?raw=true"><br>
</div>

<br>

#### Disabling Instant Face Counter Drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, count=vision.count_faces(img,draw=False)
    print(count)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

### Color Recognition

Colors it can recognize Red, Green, Blue

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img,name,list=vision.detect_colors(img)
    print(name,list)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

name variable returns the name of the detected color.
The list variable returns the RGB ratios of the detected color in the order R G B.

```sh
blue [844.5, 415.5, 173812.0]
red [600.5, 311.0, 530.5]
green [0, 772.0, 0]
```

The Threshold value is set to 1000 by default. You can lower or raise this value according to your needs.

```python
img,name,list=vision.detect_colors(img,threshold=500)
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/color.gif?raw=true"><br>
                                        
</div>

<br>

#### Change Drawing Color

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img,name,list=vision.detect_colors(img,rectangle_color="yellow")
    print(name,list)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/custom_color.gif?raw=true"><br>
</div>

<br>

#### Disable drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img,name,list=vision.detect_colors(img,draw=False)
    print(name,list)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

### Blink detection

For face recognition to work you need to download the face recognition model.[shape_predictor_68_face_landmarks.dat](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2)

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
vision.blink_setup(path="shape_predictor_68_face_landmarks.dat")
while True:
    _,img=cap.read()
    img,EAR,status,time=vision.detect_blink(img)
    print(EAR,status,time)
  
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

EAR variable returns the eye closure rate.
status returns the eye's closed and open status.
time returns how many seconds the eye was closed.

```sh
0.2 False None
0.21 False None
0.22 False None
0.1 True None
0.1 True None
0.17 False 1.50
0.23 False None
0.23 False None
0.21 False None
```

The Threshold value is set to 0.15 by default. You can lower or raise this value according to your needs.

```python
img,EAR,status,time=vision.detect_blink(img,threshold=0.20)
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/eye_blink.gif?raw=true"><br>
</div>

<br>

#### Disable eye drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
vision.blink_setup(path="shape_predictor_68_face_landmarks.dat")
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img,EAR,status,time=vision.detect_blink(img)
    print(EAR,status,time)
  
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

### Body Detection and Analysis

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img,left,right=vision.detect_body(img)
    print(left,right)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

left variable returns the proximity of your left arm to your shoulder.
right variable returns the proximity of your left arm to your shoulder.

```sh
175.43727322952194 186.38214534742016
159.12635745126173 181.2641703620141
0.8016276382526805 67.3130811726478
7.112369711132518 3.427382752073662
3.0965441578399973 3.4120390844959267
0.008587732984777094 1.7826284349542627
1.46573896432903 1.4118781257852226
5.318943889580121 1.1099510521746376
4.449516553979241 2.073257712440663
7.570394013983709 3.0725981509538887
16.59312469528359 22.83114476402925
20.703749065899352 95.33857084841868
168.733170676982 177.10299133508224
175.13547154106007 178.61997780496543

```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/body.gif?raw=true"><br>
</div>

<br>

#### Disable Body Drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img,left,right=vision.detect_body(img,draw=False)
    print(left,right)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

### Object Recognition

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img,name=vision.detect_objects(img)
    print(name)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

The name variable returns the name of the detected object.

```sh
person
person
person
person
person
person
```

<div align="center">
  
  <img width="700"   loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/object.gif?raw=true"><br>
</div>

<br>

### Face Recognition

For face recognition to work you need to download the face recognition model.[shape_predictor_68_face_landmarks.dat](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2)

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
vision.face_recognizer_setup(["Ali_Edis.png","Carl_Sagan.png"],path="shape_predictor_68_face_landmarks.dat")
while True:
    _,img=cap.read()
    img,name=vision.face_recognizer(img)
    print(name)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

```sh
['unknown', 'Ali Edis']
['unknown', 'Ali Edis']
['unknown', 'Ali Edis']
```

<div align="center">
  
  <img width="700" loading="lazy"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/face_rec.gif?raw=true"><br>
</div>

#### Disable drawing

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
vision.face_recognizer_setup(["Ali_Edis.png","Carl_Sagan.png"],path="shape_predictor_68_face_landmarks.dat")
while True:
    _,img=cap.read()
    img,name=vision.face_recognizer(img,draw=False)
    print(name)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

### Keyboard Controlled

```python
from futurevision import vision
vision=vision.Vision()
vision.press("a")
```

### Typing Text with Keyboard

```python
from futurevision import vision
vision=vision.Vision()
vision.write("future vision")
```

### Making Your Computer Talk

```python
from futurevision import vision
vision=vision.Vision()
vision.speak("Future Vision")
```

#### Language Switching

```python
from futurevision import vision
vision=vision.Vision()
vision.speak("Merhaba",lang="fr")
```

#### File name change

```python
from futurevision import vision
vision=vision.Vision()
vision.speak("Future Vision",filename="test.mp3")
```

### How to Measure Sound Intensity with Your Computer Microphone

To run this code, you need to run this command in the terminal.

```sh
pip3 install pyaudio
``` 

```python
from futurevision import vision
vision=vision.Vision ()
try:
    vision.start_stream()
    while True:
        sound= vision.detect_sound()
        print(sound)
except KeyboardInterrupt:
    vision.stop_stream ()
```

## iPhone <img  src='https://user-images.githubusercontent.com/74038190/206662607-d9e7591e-bbf9-42f9-9386-29efc927bc16.gif' width="35"> 


<div align="center">
<h3><b>You can download the app by pressing the App Store logo.</b><h/3><br><br>
<a href="https://apps.apple.com/tr/app/darwin-future-vision/id6476931869" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/App_Store-0D96F6?style=for-the-badge&logo=app-store&logoColor=white" alt="YouTube Logo" width="250">
</a>
<br>
</div>


## Application Sections and Sample Codes

<div align="center">
<img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/9.PNG"><br>
</div>

### Settings

In the Settings section, you should save the IP address and port information that your Python code will give you so that the application can communicate with the Python code you will write.

<div align="center">
<img loading="lazy" style="width:700px;" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/ip_result_terminal.PNG"><br>
</div>
<div align="center">
  <img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/10.PNG">
  <img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/11.PNG"><br><br>
  <img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/12.PNG"><br>
</div>

### HWC

In this section, the **iPhone** module of the **Future Vision** library allows you to control the observational hardware of your iPhone based on the code you write. It allows you to control the Flash with **flash_on()** and **flash_off()** functions, the Screen Brightness with **screen_brightness(value)** function, and the Speaker Volume with **volume_intensity(value)** function.

<div align="center">
  <br>
  <img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/hwc.PNG">
</div>

### CwH

In this section, the **iPhone** module of the **Future Vision** library sends the observational hardware information of your iPhone to your python code as a list. You can read this list data with the **read_data()** function. The sample data list includes the screen brightness value, the volume value and the volume key pressed on your phone:

```sh
['25', '70', 'Down']
['25', '75', 'Up']
```

<div align="center">
  <br>
  <img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/cwh.PNG">
</div>

### LEDs

In this section, the **iPhone** module of the **Future Vision** library allows you to control the 5 led graphics in the application according to the codes you write with the **iPhone** module and you can change the colors of the 5 leds to green, blue and red. You can use **led_on(pin)** to turn on the leds in the application and **led_off(pin)** to turn them off.

<div align="center">
  <br>
  <img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/leds.PNG">
</div>

### SEND&SHOW

In this section, according to the codes you will write with the **iPhone** module of the **future vision** library, you can send the data you will enter in the input in the application to your computer or send data from your computer to the mobile application. you can use **send_data(data)** functions to send data to the mobile application and **read_data()** functions to read the data sent by the mobile application.

<div align="center">
  <br>
  <img width="300" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/sendshow.PNG">
</div>

## Sample Codes

### HWC

#### Flash Controlled

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    iphone.flash_on()
    iphone.wait(3)
    iphone.flash_off()
    iphone.wait(3)
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/flash_hwc.gif?raw=true"><br>
</div>

#### Screen Brightness Controlled

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    iphone.screen_brightness(100)
    iphone.wait(3)
    iphone.screen_brightness(0)
    iphone.wait(3)
```

<div align="center">
 
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/sb_hwc.gif?raw=true"><br>
</div>

#### Volume Controlled

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    iphone.volume_intensity(100)
    iphone.wait(3)
    iphone.volume_intensity(0)
    iphone.wait(3)
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/si_hwc.gif?raw=true"><br>
</div>

### CwH

#### Reading Data from iPhone Observational Hardware

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    data=iphone.read_data()
    print(data)
```

Reading iPhone Observational Hardware Data**The first index in the index order of the list represents the screen brightness, the second index represents the volume, and the third index represents the volume up button pressed on the phone**

```sh
['25', '70', 'Down']
['25', '75', 'Up']
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/cwh_data.gif?raw=true"><br>
</div>

### LEDs

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    iphone.led_on(1)
    iphone.led_on(2)
    iphone.led_on(3)
    iphone.led_on(4)
    iphone.led_on(5)
    iphone.wait(3)
    iphone.led_off(1)
    iphone.led_off(2)
    iphone.led_off(3)
    iphone.led_off(4)
    iphone.led_off(5)
    iphone.wait(3)
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/leds_data.gif?raw=true"><br>
</div>

#### Change Drawing Color

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/colored_leds_data.gif?raw=true"><br>
</div>

### Read Data

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    data=iphone.read_data()
    print(data)
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/read_data.gif?raw=true"><br>
</div>

### Send Data

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    iphone.send_data("Future Vision")
```

<div align="center">
  
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/send_data.gif?raw=true"><br>
</div>


## Social Media

<br>

<a href="https://www.youtube.com/channel/UCZwR4LvkgdLl-T0cAf19b7A" target="_blank">
  <img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white" width="150">
</a>

<br>

<a href="https://www.linkedin.com/in/ali-edis-68267820a/" target="_blank">
  <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" width="150">
</a>

<br>

<a href="https://linktr.ee/aliedis" target="_blank">
  <img src="https://img.shields.io/badge/linktree-1de9b6?style=for-the-badge&logo=linktree&logoColor=white" width="150">
</a>







## License

[![Image](https://camo.githubusercontent.com/92ef5e7ebc8632fef4862d243dda949198df87928b72df01444fc213163a7e53/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f496c65726961796f2f6d61726b646f776e2d6261646765733f7374796c653d666f722d7468652d6261646765)](https://github.com/AliEdis/futurevision/blob/main/LICENSE)

<hr>
<hr>

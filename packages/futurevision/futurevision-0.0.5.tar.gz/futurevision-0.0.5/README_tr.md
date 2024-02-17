<div align="center">
  <img src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/logo2.svg"><br><br>
</div>

<div align="center">
<img src="https://forthebadge.com/images/badges/built-with-love.svg" width="130" alt="made with love  markdown badge" >
<img src="https://forthebadge.com/images/badges/open-source.svg" width="130" height="30" alt="open source  markdown badge">
<br>
<img src="https://forthebadge.com/images/badges/made-with-markdown.svg" width="230" height="30" alt="made with markdown badge">

</div>

---

# <img src="https://user-images.githubusercontent.com/74038190/216122041-518ac897-8d92-4c6b-9b3f-ca01dcaf38ee.png" width="40" /> Future Vision : Robotik Eğitiminde Yeni Bir Çağ


# Nedir <img src='https://user-images.githubusercontent.com/74038190/221857969-f37e1717-1470-4fe4-abb5-88b334cf64ea.png' width="40">



**Python** dili ile Arduino kartınızdaki led'leri, RGB led'i, butonları ve 8x8 led matrisi kontrol etmenizi sağlar.

Ana bilgisayarınızı kullanarak bilgisayarlı görü ile Arduino'yu kontrol edebilir ve Raspberry Pi kartında bilgisayarlı görüyü kolaylaştırır.

Kütüphane için oluşturulan bir **Darwin Future Vision** isimli mobil uygulaması, iPhone telefonunuzun gözlemsel donanımları olan flaşını, ekran parlaklığını ve hoparlör ses oranını kontrol etmenizi sağlar.

Telefonun ekran parlaklığı, hoparlör ses şiddeti oranı ve telefonun hangi ses düğmesine basıldığının verilerini iPhone donanım bilgilerini çekerek python kodunuzda bu verileri almanızı ve kullanabilmenize olanak tanır

iPhone uygulamasındaki LEDs bölümünde 5 led grafiğini kontrol edebilirsiniz.

iPhone uygulaması ile python kodunuza veri gönderebilir veya python kodunuzdan göndereceğiniz verileri uygulamada görebilirsiniz.

# Hedefi Nedir <img  src="https://user-images.githubusercontent.com/74038190/216122069-5b8169d7-1d8e-4a13-b245-a8e4176c99f8.png" width="40"/>

Klasikleşmiş robotik eğitiminin dışına çıkarak robotik eğitiminde çocukların merakını yeniden uyandırmayı ve robotik eğitiminde yeni bir çığır açmayı hedeflemektedir.

# Modüler ve Özellikleri <img  src='https://user-images.githubusercontent.com/74038190/221857969-f37e1717-1470-4fe4-abb5-88b334cf64ea.png' width="40"> 

**Future Vision** kütüphanesinin **Arduino** modülüyle Python dilini kullanarak Arduino'daki LED'leri, RGB LED'leri ve 8x8 LED matrisini kontrol edebilir, ayrıca Arduino'nun analog pinlerine bağlı olan butonlardan değer okuyabilirsiniz.

**Future Vision** kütüphanesinin **Raspberry Pi** modülüyle Raspberry Pi'daki LED'leri, RGB LED'leri, Sense HAT üzerindeki 8x8 LED matrisini ve Sense HAT sensörlerini okuyabilir ve kontrol edebilirsiniz, ayrıca Sense HAT joystick değerlerini de okuyabilirsiniz.

**Future Vision** kütüphanesinin **Vision** modülüyle kendi işaret dilinizi oluşturabilir, elleri tespit edebilir, yüzünüzdeki mutluluk ve mutsuzluk oranını tespit edebilir, bir odadaki anlık yüz sayısını tespit edebilir, renkleri algılayabilir, gözlerin kapalı veya açık olduğunu tespit edebilir, klavyedeki tuşları yönetebilir, ses şiddetini ölçebilir, bilgisayarınızı konuşturabilir, sağ ve sol kol hareketlerini analiz edebilir, objeleri tanıyabilir ve kişisel yüz tanıma yapabilirsiniz.

**Future Vision** kütüphanesinin **iPhone** modülü ve mobil uygulama ile iPhone telefonunuzun gözlemsel donanımları olan flaş, ekran parlaklığı ve hoparlörün ses şiddetini kontrol edebilirsiniz. Ayrıca, ekran parlaklığı, hoparlör ses şiddeti oranı ve sesi yükseltme veya alçaltma tuşlarına basılma verilerini bilgisayarınızda görebilir ve bu verilere göre Arduino veya Raspberry Pi kartınızı kontrol edebilirsiniz veya Arduino ve Raspberry Pi ile örneğin butona basarak telefonunuzun flaşını kontrol edebilirsiniz.


# Modüllerin Kullanımı <img  src='https://user-images.githubusercontent.com/74038190/206662607-d9e7591e-bbf9-42f9-9386-29efc927bc16.gif' width="40"> 

## Arduino


**Future Vision** kütüphanesinin Arduino Uno kartınızla doğru çalışabilmesi için [FutureVision-Arduino.ino](https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/FutureVision-Arduino/FutureVision-Arduino.ino) kodunu Arduino Uno kartınıza yüklemeniz gerekmektedir.


13, 12 ve 11 pinleri LED matrise ayrılmıştır, 10, 9, 8 pinleri RGB LED'e ayrılmıştır. Sadece 7, 6, 5, 4, 3, 2 pinlerini dijital çıkış olarak kullanabilirsiniz.

### Led açma ve kapatma

```python
from futurevision import arduino
uno=arduino.Arduino(usb_port="/dev/cu.usbmodem101",baud=9600)
uno.on(pin=7)
uno.wait(1)
uno.off(pin=7)
```

**LED bağlantıları aşağıdaki gibidir.**

<div align="center">
  <img src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/led1.png"><br>
</div>

### RGB Led Kontrollü

RGB LED'de gösterebileceğiniz renkler:

1. Kırmızı 🔴
2. Sarı 🟡
3. Yeşil 🟢
4. Mavi 🔵
5. Mor 🟣
6. Beyaz ⚪️
7. Açık Mavi 🩵

Bu parametrelerden birini girerek RGB ledinizi kapatabilirsiniz: clear & off

RGB LED'in pin düzeni: R:10 G:9 B:8

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

**RGB LED bağlantıları aşağıdaki gibidir.**

<div align="center">
  <img src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/rgb_led_pin.png"><br>
</div>

### Buton Değeri Okuma

Butonların değerleri sadece analog pinlerden okunacak şekilde ayarlanmıştır. Döndürülen buton değeri {PIN} olarak verilecektir. Örneğin, A0 ve A3 pinlerine bağlı iki butonumuzun olduğunu düşünelim. A3 pinine üç kez bastığımızda ve A0 pinindeki butona iki kez bastığımızda terminal çıktısı aşağıdaki gibi olacaktır.

```python
from futurevision import arduino
uno=arduino.Arduino(usb_port="/dev/cu.usbmodem101",baud=9600)
while True:
    read=uno.read()
    print(read)
```

Terminal Çıktısı

```sh
(base) ali@aliedis-MacBook-Air Desktop % python3 test.py
3
3
3
0
0
```

**Buton bağlantıları aşağıdaki gibidir.**

<div align="center">
  <img  src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/button_pin1.png"><br>
</div>

### Led Matrix Kontrollü

Led Matrixin Pin Düzeni: DIN:13, CS:12, CLK:11

Led Matrixte istediğiniz karakterleri gösterebilirsiniz. Karakter ve şekil listesi şu şekildedir:

A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z

a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

1, 2, 3, 4, 5, 6, 7, 8, 9, 0

+, -, *, /, %, =, up, down, right, left, happy, unhappy, heart

Bu komutlardan birini girerek led matrixinizi kapatabilirsiniz: clear & off

Led Matrix varsayılan olarak dikey çalışacak şekilde ayarlanmıştır. Bunun değiştirmek için direction parametresini 0 olarak değiştirebilirsiniz.

Örnek: uno.show_led_matrix("A",0)

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

**Led Matrix bağlantıları aşağadaki gibidir.**

<div align="center">
  <img  src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/led_matrix1.png"><br>
</div>

## Raspberry Pi


### Led açma ve kapatma

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi()
rpi.on(14)
rpi.wait(1)
rpi.off(14)
```

### RGB Led Kontrollü

RGB LED'de gösterebileceğiniz renkler:

1. Kırmızı 🔴
2. Sarı 🟡
3. Yeşil 🟢
4. Mavi 🔵
5. Mor 🟣
6. Beyaz ⚪️
7. Açık Mavi 🩵

Bu parametrelerden birini girerek RGB ledinizi kapatabilirsiniz: clear & off

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

### Buton Değeri Okuma

Buton PULL UP olarak ayarlanmıştır.

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi()
while True:
    button=rpi.read_button(14)
    if(button):
     print("Button Pressed")
    rpi.wait(0.1)
```

Terminal Çıktısı

```sh
>>> %Run test.py
Button Pressed
```

### Sense HAT LED Matrisinde Harf veya Sayı Gösterme

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.show_letter("A")
rpi.wait(1)
rpi.show_letter("1")
rpi.wait(1)
rpi.clear()
```

#### Yazı Rengi ve Arka Plan Rengi Değiştirme

Sense HAT LED matrisinde seçebileceğiniz renklerin listesi:

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

### Sense HAT LED Matrisinde Mesaj Gösterme

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.show_message("Future Vision")
```

#### Sense Hat Mesaj Gösterim Hızı Değiştirme

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.show_message("Future Vision",scroll_speed=0.2)
```

### Sense Hat Led Matris Boyama

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
rpi.fill("red")
rpi.wait(1)
rpi.clear()
```

### Sense Hat Led Matris İşaret Gösterme

Gösterebileceğiniz işaretler up, down, right, left, happy, unhappy, heart

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
sign_list=['up', 'down', 'right', 'left', 'happy', 'unhappy', 'heart']
for i in sign_list:
  rpi.show_sign(i)
  rpi.wait(1)
  rpi.clear()
```

### Sense Hat Sensörlerini Kullanma

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

Terminal Çıktısı

```sh
>>> %Run test.py
34.51753616333008
38.123626708984375
0
[-0.535936176776886, 0.06923675537109375, -0.25748658180236816]
[0.11419202387332916, 0.3673451840877533, 0.8629305362701416]
174.1544422493143
```

### Sense Hat Joystick Butonuna Tıklanmayı Algılama

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
while True:
  btn=rpi.joystick_button()
  print(btn)
  rpi.wait(0.1)
```

Terminal Çıktısı

```sh
>>> %Run test.py
False
False 
True
False
```

### Sense Hat Joystick Haraketleri

```python
from futurevision import raspberrypi
rpi=raspberrypi.RaspberryPi(sense_hat=True)
while True:
  btn=rpi.joystick()
  print(btn)
  rpi.wait(0.1)
```

Terminal Çıktısı

```sh
>>> %Run test.py
up
down 
right
left
middle
```

## Vision

### El Tespiti

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

fingers değişkeni, kapalı olan parmaklar için 0 değeri döndürür, açık olan parmaklar için 1 değeri döndüren bir liste verir.

status değişkeni ise, eğer bütün parmaklar açıksa True değerini döndürür, eğer bütün parmaklar kapalıysa False değerini döndürür.

Terminal Çıktısı

```sh
>>> %Run test.py
Finger List:  [1, 1, 1, 1, 1] Hand Status:  True
Finger List:  [0, 0, 0, 0, 0] Hand Status:  False
```

<div align="center">
  <img loading="eager" width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/default_hand_detection.gif?raw=true"><br>
</div>

<br>

#### El Çiziminin Rengini Değiştirme

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

#### El Çizimini Devredışı Bırakma

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

### İşaret dili oluşturma

Listedeki indexlerin temsil ettiği parmaklar aşağıdaki resimdeki gibidir.

<div align="center">
  <img width="300" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/fingers_numbers.png"><br>
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

### Duygu Tespiti

```python
from futurevision import vision
import cv2
vision=vision.Vision()
cap=cv2.VideoCapture(0)
while True:
    _,img=cap.read()
    img, emotion,th=vision.detect_emotion(img)
    print(emotion)
    cv2.imshow("Future Vision",img)
    cv2.waitKey(1)
```

emotion değişkeni mutluluk durumuna göre unhappy veya happy döndürür.
th değişkeni mutluluk oranını döndürür.

Terminal Çıktısı

```sh
unhappy 0.025
happy 0.045
unhappy 0.025
happy 0.045
```

Mutluluk algılama eşiği 0.035 olarak belirlenmiştir Tercih ve ihtiyaçlarınıza göre mutluluk algılama eşiğinizi değiştirebilirsiniz

Mutluluk Eşiği Değiştirme

```python
img, emotion,th=vision.detect_emotion(img,threshold=0.040)
```

<div align="center">
  <img width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/emotion_default1.gif?raw=true"><br>
</div>

<br>

#### Yüz Çizimi ve Yazının Rengini Değiştirme

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

#### Yüz Çizimini Devre Dışı Bırakma

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

### Anlık Yüz Sayaçı

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

count değişkeni kaç adet yüz olduğunu döndürür.

Terminal Çıktısı

```sh
2
2
2
2
1
1
2
2
```

<div align="center">
  <img width="700"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/count_faces.gif?raw=true"><br>
</div>

<br>

#### Anlık Yüz Sayaçı Çizimini Devre Dışı Bırakma

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

### Renk Tanıma

Tanıyabildiği renkler: Kırmızı, Yeşil, Mavi

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

name değişkeni tespit ettiğini rengin ismini döndürür.
list değişkeni tespit edilen rengin RGB oranlarını R G B sırası ile döndürür.

```sh
blue [844.5, 415.5, 173812.0]
red [600.5, 311.0, 530.5]
green [0, 772.0, 0]
```

Threshold değeri varsayılan olarak 1000 olarak ayarlanmıştır. İhtiyacınıza göre bu değeri düşürebilir veya yükseltebilirsiniz.

```python
img,name,list=vision.detect_colors(img,threshold=500)
```

<div align="center">
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/color.gif?raw=true"><br>
</div>

<br>

#### Çizim Rengini Değiştirme

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

#### Çizimi devre dışı bırakma

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

### Göz kırpma algılama

Yüz tanımanın çalışabilmesi için yüz tanıma modelini indirmelisiniz.[shape_predictor_68_face_landmarks.dat](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2)

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

EAR değişkeni gözün kapalılık oranını döndürür.
status değişkeni gözün kapalı ve açık olma durumunu döndürür.
time değişkeni gözün kaç saniye kapalı olduğunu döndürür.

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

Threshold değeri varsayılan olarak 0.15 olarak ayarlanmıştır. İhtiyacınıza göre bu değeri düşürebilir veya yükseltebilirsiniz.

```python
img,EAR,status,time=vision.detect_blink(img,threshold=0.20)
```

<div align="center">
  <img width="700"  loading="lazy" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/eye_blink.gif?raw=true"><br>
</div>

<br>

#### Göz çizimini devre dışı bırakma

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

### Vücut Tespiti ve Analizi

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

left değişkeni sol kolunuzun omzunuza yakınlık oranını döndürür.
right değişkeni sol kolunuzun omzunuza yakınlık oranını döndürür.

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

#### Vücut Çizimini Devre Dışı Bırakma

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

### Obje Tanıma

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

name değişkeni tespit edilen objenin ismini döndürür.

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

### Yüz Tanıma

Yüz tanımanın çalışabilmesi için yüz tanıma modelini indirmelisiniz.[shape_predictor_68_face_landmarks.dat](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2)

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
['Ali Edis']
['Ali Edis']
['Carl Sagan', 'Ali Edis']
['Carl Sagan', 'Ali Edis']
['Carl Sagan', 'Ali Edis']
['Carl Sagan', 'Ali Edis']
['unknown', 'Ali Edis']
['unknown', 'Ali Edis']
['unknown', 'Ali Edis']
['Ali Edis']
```

<div align="center">
  <img width="700" loading="lazy"  loading="eager" src="https://github.com/AliEdis/futurevision/blob/main/README-IMAGE/face_rec.gif?raw=true"><br>
</div>

Çizimi devre dışı bırakma

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

### Klavye Kontrollü

```python
from futurevision import vision
vision=vision.Vision()
vision.press("a")
```

### Klavye ile Metin Yazma

```python
from futurevision import vision
vision=vision.Vision()
vision.write("future vision")
```

### Bilgisayarınızı Konuşturma

```python
from futurevision import vision
vision=vision.Vision()
vision.speak("Future Vision")
```

#### Dil Değiştirme

```python
from futurevision import vision
vision=vision.Vision()
vision.speak("Merhaba",lang="tr")
```

#### Dosya ismi değiştirme

```python
from futurevision import vision
vision=vision.Vision()
vision.speak("Future Vision",filename="test.mp3")
```

### Bilgisayarınızın Mikrofonu ile Ses şiddeti Ölçme

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

## iPhone

<div align="center">
<h3><b>Uygulamayı App Store Logosuna Basarak İndirebilirsiniz.</b><h/3><br><br>
<a href="https://apps.apple.com/tr/app/darwin-future-vision/id6476931869" target="_blank">
  <img loading="lazy" src="https://img.shields.io/badge/App_Store-0D96F6?style=for-the-badge&logo=app-store&logoColor=white" alt="YouTube Logo" width="250">
</a>
<br>
</div>


## Uygulama Bölümleri ve Örnek Kodlar

<div align="center">
<img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/9.PNG"><br>
</div>

### Settings

Settings bölümünde, uygulamanın yazacağınız Python koduyla haberleşebilmesi için Python kodunuzun size vereceği IP adresi ve port bilgilerini kaydetmelisiniz.

<div align="center">
<img loading="lazy" style="width:700px;" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/ip_result_terminal.PNG"><br>
</div>
<div align="center">
  <img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/10.PNG">
  <img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/11.PNG">
  <img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/12.PNG"><br>
</div>

### HWC

Bu bölümde, **Future Vision** kütüphanesinin **iPhone** modülü ile yazacağınız kodlara göre iPhone telefonunuzun gözlemsel donanımlarını kontrol etme imkanını sunar. **flash_on()** ve **flash_off()** fonksiyonlarıyla Flaşı, **screen_brightness(value)** fonksiyonuyla Ekran Parlaklığını, **volume_intensity(value)** fonksiyonuyla Hoparlörün Ses Şiddetini kontrol etmenizi sağlar.

<div align="center">
  <img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/hwc.PNG">
</div>

### CwH

Bu bölümde **Future Vision** kütüphanesinin **iPhone** modülü ile yazacağınız kodlara göre iPhone telefonunuzun gözlemsel donanım bilgilerini python kodunuza bir liste olarak gönderir. Bu liste verisini **read_data()** fonksiyonu ile okuyabilirsiniz veriler arasında Ekran parlaklığı değeri Ses Şiddeti Değeri ve Telefonunuzun hangi ses tuşuna basıldığının verisini yer almaktadır örnek veri listesi:

```sh
['25', '70', 'Down']
['25', '75', 'Up']
```

<div align="center">
  <img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/cwh.PNG">
</div>

### LEDs

Bu bölümde **Future Vision** kütüphanesinin **iPhone** modülü ile yazacağınız kodlara göre uygulama içerisinde bulunan 5 adet led grafiğini kontrol etme imkanı sunar ve 5 adet ledin renklerini yeşil, mavi ve kirmizi olarak değiştirebilirsiniz. Uygulamadaki ledleri açmak için **led_on(pin)** kapatmak için **led_off(pin)** fonksiyonlarını kullanabilirsiniz.

<div align="center">
  <img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/leds.PNG">
</div>

### SEND&SHOW

Bu bölümde **future vision** kütüphanesinin **iPhone** modülü ile yazacağınız kodlara göre uygulama içerisindeki input'a gireceğiniz verileri bilgisayarınıza gönderebilir veya bilgisayarınızdan mobil uygulamaya veri gönderebilirsiniz. mobil uygulamaya veri göndermek için **send_data(data)** mobil uygulamanın göndereceği verileri okumak için **read_data()** fonksiyonlarını kullanabilirsiniz.

<div align="center">
  <img style="width:300px;" loading="lazy" src="https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/sendshow.PNG">
</div>

## Örnek Kodlar

### HWC

#### Flaş Kontrollü

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

#### Ekran Parlaklığı Kontrollü

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

#### Ses Şiddeti Kontrollü

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

#### iPhone Gözlemsel Donanımının Verilerini Okuma

```python
from futurevision import iphone
iphone=iphone.iPhone()
while True:
    data=iphone.read_data()
    print(data)
```

**Listenin index sıralamasındaki ilk index ekran parlaklığı, ikinci index ses şiddeti, üçüncü index telefonun hangi ses yükseltme tuşuna basıldığının bilgilerini temsil etmektedir**

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

#### Çizim Rengini Değiştirme

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


## Sosyal Medya

<a href="https://www.youtube.com/channel/UCZwR4LvkgdLl-T0cAf19b7A" target="_blank">
  <img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white" width="150">
</a>


<a href="https://www.linkedin.com/in/ali-edis-68267820a/" target="_blank">
  <img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" width="150">
</a>

<a href="https://linktr.ee/aliedis" target="_blank">
  <img src="https://img.shields.io/badge/linktree-1de9b6?style=for-the-badge&logo=linktree&logoColor=white" width="150">
</a>





## Lisans

[![Image](https://camo.githubusercontent.com/92ef5e7ebc8632fef4862d243dda949198df87928b72df01444fc213163a7e53/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f496c65726961796f2f6d61726b646f776e2d6261646765733f7374796c653d666f722d7468652d6261646765)](https://raw.githubusercontent.com/AliEdis/futurevision/main/README-IMAGE/LICENSE)

<hr>
<hr>

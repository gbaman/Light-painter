import math
from PIL import Image
from logging import debug, info, warning, basicConfig, INFO, DEBUG, WARNING

#Don't forget the max number of items in each array is 32767 items (max signed 16 bit int size).
#This means the max value for length below is 10922!
#Length is the number is pixels stored in each array, so should be the largest number divisible by pixels


basicConfig(level=WARNING)
pixels = 60
length = 10920
delay = 100

file="examples/pacman.bmp"
#file="examples/mario.bmp"
#file="examples/rainbow.bmp"




if length % pixels != 0:
    raise NameError("Length constant must be divisible by pixel number! Recommended length = " + str((length / pixels) * pixels))
if length > 10922:
    raise NameError('Length is too large! It only supports up to 10922 (due to 16 bit signed ints)')

def leadingZeros(sIn):
    complete = []
    for i in range(0, len(sIn)):
        temp = []
        for x in range(0, len(sIn[i])):
            if len(str(sIn[i][x])) == 1:
                temp.append("00" + str(sIn[i][x]))
            elif len(str(sIn[i][x])) == 2:
                temp.append("0" + str(sIn[i][x]))
            elif len(str(sIn[i][x])) == 3:
                temp.append(str(sIn[i][x]))
        complete.append(temp)
    return complete

def buildArduino(num, length):
    print(""" length = """ + str(length)) + ";"
    print("""   for (layer = 0; layer < (length / NUMPIXELS); layer = layer + 1){  //For each layer in the image
      for (pixel = 0; pixel < (NUMPIXELS + 1) ; pixel = pixel + 1){      //For each pixel
          gl = ((layer * (NUMPIXELS * 3)) + (pixel * 3) + 1); //Get location of the current green pixel
          rl = ((layer * (NUMPIXELS * 3)) + (pixel * 3) + 0); //Get location of the current red pixel
          bl = ((layer * (NUMPIXELS * 3)) + (pixel * 3) + 2); //Get location of the current blue pixel""")

    print("      g = pgm_read_byte (imageP" + str(num) + " + gl);                    //Get current green colour value")
    print("      r = pgm_read_byte (imageP" + str(num) + " + rl);                    //Get current red colour value")
    print("      b = pgm_read_byte (imageP" + str(num) + " + bl);                    //Get current blue colour value")
    print("""   pixels.setPixelColor(pixel , r, g, b);              //Set the pixel data
      }
      pixels.show();
      Serial.println("Displaying ");
      delay(""" + str(delay) + ");")
    print("""   }
    pixels.show();""")

def splitSmaller(longList, newList):
    numNeeded = len(longList)
    numNeeded = numNeeded /float(length)
    numNeeded = int(math.ceil(numNeeded))
    debug(len(longList))
    debug(numNeeded)
    for i in range(0, numNeeded):
        if i == numNeeded-1:
            start = i*length
            end = len(longList)
        else:
            start = i*length
            end = ((i+1) *length)
        newList.append(longList[start:end])
        debug("List number " + str(i))
        debug("Start " + str(start))
        debug("End " + str(end))
    return newList

def printAll(mainList):
    i = 0
    lengths = []

    print("""#include <Adafruit_NeoPixel.h>
#include <avr/pgmspace.h>
#define PIN            11  //Pin used for neopixels
#define NUMPIXELS      60  //How many neopixels are you using?

#define BUTTONPIN  8       //Pin used for control button

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

    """)

    for i in range(0, len(mainList)):
        bob = ""
        lengths.append(len(mainList[i]))
        for x in range(0, len(mainList[i])):
            for y in range(0,len(mainList[i][x])):
                bob = bob+ ", " + str(mainList[i][x][y])
        bob = bob[2:len(bob)]
        print("const byte imageP" + str(i) + " [" + str(len(mainList[i])*3) +"] PROGMEM = { " + bob + "};")
        debug((bob))

        debug("PROGMEM byte imageP[LENGTH*(NUMPIXELS *3)] = {")
    print("""int layer;
int pixel;
int r;  //Red pixel value
int g;  //Green pixel value
int b;  //Blue pixel value
int rl; //Red pixel location (in array)
int gl; //Green pixel location (in array)
int bl; //Blue pixel location (in array)
int length;




void setup() {
  pixels.begin();
  pinMode(2, INPUT);
  Serial.begin(9600);


}

void loop() {""")
    print("if (digitalRead(BUTTONPIN) == HIGH){")
    for x in range(0, i+1):
        buildArduino(str(x),lengths[x])
    print("}")
    print("""for (pixel = 0; pixel < (NUMPIXELS + 1) ; pixel = pixel + 1){     //Turns off all pixels at the end
        pixels.setPixelColor(pixel , 0, 0, 0);
      }
      pixels.show();
      delay(5000);      //Waits 5 seconds before going back to the start of the program
      }""")


#-------------------------Main program--------------------------


im = Image.open(file, "r")
pix_val = list(im.getdata())

pix_bin = []

for i in range(0, len(pix_val)):
    for x in range(0, 3):

        pix_bin.append('{:08b}'.format(int(pix_val[i][x])))

debug(pix_bin)

arduinostr = ""

for i in range(0, len(pix_bin)):
    arduinostr = arduinostr + str(", ") + "B" + pix_bin[i]
arduinostr = arduinostr[2:len(arduinostr)]


stringthing = ""

debug(pix_val)
for i in range(0, len(pix_val)):
    smallstring = ""
    for x in range(0, len(pix_val[i])):
        if smallstring == "":
            smallstring = smallstring + str(pix_val[i][x])
        else:
            smallstring = smallstring + ", " + str(pix_val[i][x])
    stringthing = stringthing + ", {" + smallstring + "}"
debug(stringthing)
debug(len(pix_val))
debug((pix_val))
printAll(splitSmaller(pix_val, []))
allTogether = ""
bob = 0
for i in range(0, len(pix_val)):
    for x in range(0, len(pix_val[i])):
        allTogether = allTogether + ", " + str(pix_val[i][x])
        bob = bob + 1
debug(allTogether)


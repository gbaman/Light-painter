Arduino Light painter technical information
=============
You may be wondering how all this works, especially on the software side. This is a brief explination of some of the technical parts of the projects.
   
##How did you store the pixel data directly on the Arduino flash?
This was one of the most complicated parts of the project, storing the pixel data.   
In the end I went with using ```PROGMEM``` from ```avr/pgmspace.h```. It allows you to store a data structure in flash memory at programming time. The data is **read only** but given this project never needed to edit the data, that was perfect.   
An array of bytes is used to store each colour value, given it can be between 0 and 255, making byte perfect.   
```const byte imageP0 [19980] PROGMEM = {0,0,255}``` is an example of one of the arrays, but it would have a **lot** more data, 19980 objects in fact.   

##Don't arrays have an object number limit?
Yes, arrays use a signed 16 bit integer as the datatype to store the IDs of each item.   
A signed 16 bit integer can be any number between between -32768 and 32767.   
This means there can be a max of 32767 elements in the array. This was is an issue as that means we can only store a maximum of around 10922 pixels. When using 60 neopixels, that means your image can only be 182 pixels long!   
The solution to this problem turned out to be just use multiple arrays.   
This in the end was one of the major reasons we use a python script to generate all the C++ code for Arduino, it adds as many arrays as it needs and all the supporting code for them.

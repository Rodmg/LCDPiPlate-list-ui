#LCDPiPlate List UI

List User interface for the Raspberry Pi LCD Plate from Adafruit (https://www.adafruit.com/products/1109)

##Installation:

- In /etc/modules (sudo nano /etc/modules), add:
```
i2c-bcm2708 
i2c-dev
```

- Install dependencies:
```
sudo apt-get install python-smbus i2c-tools python-dev python-rpi.gpio
```

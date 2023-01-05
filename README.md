# opi5_lcd_monitor
Using a 5$ LCD to monitor your Orange Pi 5

## What is it?
LCD 1602 or 2004 are little screens using 16 characters on 2 lines or 20 on 4 lines. They are really cheap. This project use this little screens to provide some monitoring information for the Orange Pi 5 and other Single Board Computers (SBC).

You can run the code:
* from command line
* from a container, maybe a bit overkill, but isolation, you know...

## I2C Protocol

I use the Debian CLI version from Orange Pi to run the Orange Pi 5 (OPi5). The I2C [protocol](https://en.wikipedia.org/wiki/I%C2%B2C) allows us to communicate with the backpack using only two cables. We need the data Pin and the clock Pin.

## I2C Activation and Pins

* for the **OPi5** add this line in the file `/boot/orangepiEnv.txt`:

`overlays=spi4-m0-cs1-spidev i2c1-m2 i2c3-m0 i2c5-m3`

* Usually with other cards you ave to use `orangepi-config` or `raspi-config` to activate I2C.


### For the OPi5 use:
* pin 12 for data SDA
* pin 15 for clock SCL



## PSUTIL ?

The script in python is just some glue between components.

The real big thing is [psutils](https://pypi.org/project/psutil/). This lib allows to grab all the information we want from the computer (cpu, ram, disks...)

## Usage

### From the CLI

grab the project from github
`git clone https://github.com/renaudrenaud/opi5_lcd_monitor.git`

go into the project folder
`cd cd opi5_lcd_monitor`

install the requirements 
`pip install -r requirements.txt`

**run it**

`sudo python3 lcd_cpu.py`

At this moment the code will print on your screen. To use the LCD, we want to deactivate the --virtual driver**:

`sudo python3 lcd_cpu.py -v no`

Working, but it's just the clock function! Ok, let's ask for **cpu info dipslay**:

`sudo python3 lcd_cpu.py -v no -d`
















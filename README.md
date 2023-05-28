# opi5_lcd_monitor
Using a 5$ LCD to monitor your Orange Pi 5

## What is it?
LCD 1602 or 2004 are little screens using 16 characters on 2 lines or 20 on 4 lines. They are really cheap. This project use this little screens to provide some monitoring information for the Orange Pi 5 and other Single Board Computers (SBC).

You can run the code:
* from command line
* from a [container](https://hub.docker.com/repository/docker/renaudrenaud/opi5_lcd_monitor), maybe a bit overkill, but isolation, you know...

## I2C Protocol

I use the Debian CLI version from Orange Pi to run the Orange Pi 5 (OPi5). The I2C [protocol](https://en.wikipedia.org/wiki/I%C2%B2C) allows us to communicate with the backpack using only two cables. We need the data Pin and the clock Pin.

## I2C Activation and Pins

* for the **OPi5** add this line in the file `/boot/orangepiEnv.txt`:

`overlays=spi4-m0-cs1-spidev i2c1-m2 i2c3-m0 i2c5-m3`

* Usually with other cards you ave to use `orangepi-config` or `raspi-config` to activate I2C.


### GPIO Pins
* OPi5 use
  * pin 12 for data SDA
  * pin 15 for clock SCL
* Rapsberry Pi 400
  * pin 3 for SDA - GPIO #8 SDA1 I2C
  * pin 5 for SCL - GPIO #7 SCL1 I2C



## PSUTIL ?

The script in python is just some glue between components.

The real big thing is [psutils](https://pypi.org/project/psutil/). This lib allows to grab all the information we want from the computer (cpu, ram, disks...)


## Install

grab the project from github
`git clone https://github.com/renaudrenaud/opi5_lcd_monitor.git`

go into the project folder
`cd cd opi5_lcd_monitor`

install the requirements 
`pip install -r requirements.txt`

## run it from the commande line

### On your screen

On the cli, use the following command:

`sudo python3 lcd_cpu.py`

![image](https://user-images.githubusercontent.com/9823965/210695728-c4d35d51-a839-4c1a-958c-5d9a2ef66a43.png)

### On the LCD

At this moment there is print on your screen. To use the LCD, we want to deactivate the --virtual driver**:

`sudo python3 lcd_cpu.py **-v no**`

### I want some monitoring info

Working, but it's just the clock function! Ok, let's ask for **cpu info dipslay** using the -d parameter:

`sudo python3 lcd_cpu.py -v no **-d cpu**`

You can try:
* cpuonly
* cpucore
* cpuram
* cpudisk
* cpu
* cpusmooth


**cpudu**
For Disk Usage
* line 3 shows user / total / pct for the root "/"
* line 4 shows user / total / pct for the -m mount drive

`sudo python3 lcd_cpu_2004.py -v no -d cpudu -m /mnt/opz2`

![image](https://user-images.githubusercontent.com/9823965/212914621-ef2149e8-2273-4a53-8d20-f5c0f5b67146.png)


## run it as a container

Install the [Container](https://hub.docker.com/repository/docker/renaudrenaud/opi5_lcd_monitor/general) with arm64 tag.

**Define the ENV:** (Env Panel in Portainer)
* `LMS_VIRTUAL_LCD=no`
* `LMS_DISPLAY_MODE=cpu`

**Map the device:** (Runtime & Resources Panel in Portainer)
Please use "privileged" mode to gain access to the device.

For the OPi5:
/dev/i2c-1:/dev/i2c-1


## Tested with

* Orange Pi 5 
  * `/dev/i2c-1`
  * `sudo python3 lcd_cpu_2004.py -v no -d cpusmooth`
* Orange Pi Zero 2 
  * `/dev/i2c-3`
  * `sudo python3 lcd_cpu_2004.py -v no -i 3 -d cpu`

## Next steps

Project is really at the begining. I want to:
* fix the cpudisk function

## Debug with Visual Studio Code 

At the moment the i2c device is not available without any sudo and VSCode does not like sudo, the way to debug is to use the lcd virtual driver.

One way is to use the launch.json file adding the env var **"LMS_VIRTUAL_LCD":"yes"** to the configuration.

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env":{"LMS_VIRTUAL_LCD":"yes",
                   "LMS_DISPLAY_MODE":"cpuonly",
                   "TIME_ZONE_2":"Africa/Addis_Ababa"
                   }
        }
    ]
}
```



## Acknoledgments

* Thanks to **kprasadvnsi** for the [discord](https://discord.com/channels/934722269522059335/1040242609626554408) even is this guy does not want to create an idependant #orangepi-zero2 considering this is the same as the Orange Pi Zero
* Thanks to [Armbian](https://www.armbian.com/) - please note the code is running on the debian from Orange Pi.
* LCD driver coming from https://github.com/sweetpi/python-i2c-lcd/blob/master/lcddriver.py

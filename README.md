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

-----

# Install and run

## Install

grab the project from github:

`git clone https://github.com/renaudrenaud/opi5_lcd_monitor.git`

## Run It With Docker

* Go to the folder
* Build the image
* Run it

`cd opi_5_lcd_monitor`

`sudo docker build -t opi5_lcd_monitor:07 .`

`docker run -d \
--name lcd_monitor_from_cli \
--restart always \
-e LMS_VIRTUAL_LCD=no \
-e LMS_DISPLAY_MODE=cpusmooth \
-e TZ=Asia/Shanghai \
-e TIME_ZONE_2=Europe/Paris \
--device /dev/i2c-3:/dev/i2c-3 \
opi5_lcd_monitor:07 \
python3 lcd_cpu_2004.py -i 3`

*Notes*
-i parameter depends on your card. It is 1 by default and work with the Orange Pi 5, the Orange Pi Zero 2 and Zero 3 needs 3. 
You need to run `sudo i2cdetect -y X` (X=1 or 2 or 3) and see the LCD to know the value :
- this is well documented in the user manual for the Orange Pi SBC (i2c part)




## Run It Without Docker
go into the project folder
`cd cd opi5_lcd_monitor`

install the requirements 
`pip install -r requirements.txt`

## run it from the commande line

On the cli, use the following command:

`sudo python3 lcd_cpu.py`

![image](https://user-images.githubusercontent.com/9823965/210695728-c4d35d51-a839-4c1a-958c-5d9a2ef66a43.png)


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

You can build the image locally or grab the container :
* Install the [Container](https://hub.docker.com/repository/docker/renaudrenaud/opi5_lcd_monitor/general) with arm64 tag.
* `docker build --no-cache -t renaudrenaud/opi5_lcd_monitor:1.0.0 .` or the line below if build stage get stuck on `fetch bla bla bla`
* `docker build --network host --no-cache -t renaudrenaud/opi5_lcd_monitor:1.0.0 .`

**Define the ENV:** (Env Panel in Portainer)
* `LMS_VIRTUAL_LCD=no`
* `LMS_DISPLAY_MODE=cpu`

**Map the device:** (Runtime & Resources Panel in Portainer)

For the OPi5:
/dev/i2c-1:/dev/i2c-1

For the OPi5 Plus:
/dev/i2c-2:/dev/i2c-2


## Tested with

* Orange Pi 5 Plus
  * On Command and loggin, use this command 'python3' `'lcd_cpu_2004.py' '-i' '2' '-l' '0x39'`
  * On runtime and ressources, add this device`/dev/i2c-2:/dev/i2c-2`
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

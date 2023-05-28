# Some info
# build: sudo docker build -t opi5_lcd_monitor:arm64 .
# tag: sudo docker tag opi5_lcd_monitor:arm64 renaudrenaud/opi5_lcd_monitor:arm64
# add user to the docker group sudo usermod -aG docker $USER and exit session
# login: docker login
# push: docker push renaudrenaud/opi5_lcd_monitor:arm64
#
# python3 lcd_cpu.py -d cpu -v yes 
################################################################
# I2C
# - RASPBERRY I2C should be activated with sudo raspi-config
# - ORANGE PI 5 I2C add to /boot/ornagepiEnv.txt : overlays=spi4-m0-cs1-spidev i2c1-m2 i2c3-m0 i2c5-m3
#   use pin 12 & 15
# then device has to be exposed with privileged mode
# devices:  
#  - "/dev/i2c-1:/dev/i2c-1" 
###############################################################
# env:
# TZ=Asia/Shanghai
# LMS_LCD=0x3F
# LMS_I2C_PORT=1
# LMS_VIRTUAL_LCD=no
# LMS_DISPLAY_MODE=cpu


FROM python:3.11.0-alpine

LABEL maintainer="renaudrenaud"

COPY requirements.txt /home/opi5_lcd_monitor/
COPY i2c_lib.py /home/opi5_lcd_monitor/
COPY lcd_cpu_2004.py /home/opi5_lcd_monitor/
COPY lcddriver.py /home/opi5_lcd_monitor/
COPY no_lcddriver.py /home/opi5_lcd_monitor/

WORKDIR /home/opi5_lcd_monitor

RUN apk update \
    && apk add --no-cache git \
                          python3 \
                          python3-dev \
                          build-base \
                          linux-headers \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install -r requirements.txt

CMD ["python3","lcd_cpu_2004.py"]

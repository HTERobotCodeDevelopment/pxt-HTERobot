'''
    HTERobot drive

    Author: LingJunMeng
    Date:   2018.6

    http://www.micropython.org.cn
'''
from microbit import *

PCA9685_ADDRESS = 0x40
MODE1 = 0x00
MODE2 = 0x01
SUBADR1 = 0x02
SUBADR2 = 0x03
SUBADR3 = 0x04
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09
ALL_LED_ON_L = 0xFA
ALL_LED_ON_H = 0xFB
ALL_LED_OFF_L = 0xFC
ALL_LED_OFF_H = 0xFD
     
STP_CHA_L = 2047
STP_CHA_H = 4095

STP_CHB_L = 1
STP_CHB_H = 2047

STP_CHC_L = 1023
STP_CHC_H = 3071

STP_CHD_L = 3071
STP_CHD_H = 1023


class robot():
    def __init__(self):
        self.setReg(MODE1, 0x00)
        self.setFreq(50)
        
    # set reg
    def	setReg(self, reg, dat):
        i2c.write(PCA9685_ADDRESS, bytearray([reg, dat]))

    # get reg
    def	getReg(self, reg):
        i2c.write(PCA9685_ADDRESS, bytearray([reg]))
        t = i2c.read(PCA9685_ADDRESS, 1)
        return t[0]
    
    def setFreq(self, freq):
        prescaleval = 25000000
        prescaleval /= 4096
        prescaleval /= freq
        prescaleval -= 1
        prescale = int(prescaleval)
        oldmode = self.getReg(MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.setReg(MODE1, newmode)
        self.setReg(PRESCALE, prescale)
        self.setReg(MODE1, oldmode)
        sleep(5)
        self.setReg(MODE1, oldmode | 0xa1)
    
    def setPwm(self,channel, on, off):
        if channel < 0 or channel > 15:
            return
    
        buf0 = LED0_ON_L + 4 * channel
        buf1 = on & 0xff
        buf2 = (on >> 8) & 0xff
        buf3 = off & 0xff
        buf4 = (off >> 8) & 0xff
        buf = bytearray([buf0,buf1,buf2,buf3,buf4])

        i2c.write(PCA9685_ADDRESS, buf)

    def Servo(self,index, degree):
        # 50hz: 20,000 us
        v_us = (degree * 1800 / 180 + 600)
        value = int(v_us * 4096 / 20000)
        self.setPwm(index + 7, 0, value)

    
    def MotorRun(self,index, speed):
        speed = speed * 16 # map 255 to 4096
        if speed >= 4096:
            speed = 4095
        if speed <= -4096:
            speed = -4095
        if index > 2 or index <= 0:
            return
        pp = (index - 1) * 2
        pn = (index - 1) * 2 + 1
        if speed >= 0:
            if index == 1:
                self.setPwm(pp, 0, 0)
                self.setPwm(pn, 0, speed) 
            else:
                self.setPwm(pp, 0, speed)
                self.setPwm(pn, 0, 0)
        else:
            if index == 1:
                self.setPwm(pp, 0, -speed)
                self.setPwm(pn, 0, 0)
            elif index == 2:
                self.setPwm(pp, 0, 0)
                self.setPwm(pn, 0, -speed) 
        

    def MotorStop(self,index):
        self.MotorRun(index, 0)
    

    def ServoAccurate(self,index, DegreeAcurrate):
        # 50hz: 20,000 us
        v_us = (DegreeAcurrate + 600)
        value = int(v_us * 4096 / 20000)
        self.setPwm(index + 7, 0, value)
    
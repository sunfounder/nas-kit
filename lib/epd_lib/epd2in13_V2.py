import logging
from . import epdconfig
# import epdconfig
import numpy as np
import time
# Display resolution
EPD_WIDTH       = 122
EPD_HEIGHT      = 250

class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
    FULL_UPDATE = 0
    PART_UPDATE = 1
    lut_full_update= [
0xA0,	0x90,	0x50,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
0x50,	0x90,	0xA0,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
0xA0,	0x90,	0x50,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
0x50,	0x90,	0xA0,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
	
0x0F,	0x0F,	0x00,	0x00,	0x00,		
0x0F,	0x0F,	0x00,	0x00,	0x03,		
0x0F,	0x0F,	0x00,	0x00,	0x00,		
0x00,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,
0x00,	0x00,	0x00,	0x00,	0x00,
0x00,	0x00,	0x00,	0x00,	0x00,	 
0x00,	0x00,	0x00,	0x00,	0x00,		
0x00,	0x00,	0x00,	0x00,	0x00,		
0x00,	0x00,	0x00,	0x00,	0x00,		
	
0x17,	0x41,	0xA8,	0x32,	0x50, 0x0A,	0x09,	

        # 0x80,0x60,0x40,0x00,0x00,0x00,0x00,             #LUT0: BB:     VS 0 ~7
        # 0x10,0x60,0x20,0x00,0x00,0x00,0x00,             #LUT1: BW:     VS 0 ~7
        # 0x80,0x60,0x40,0x00,0x00,0x00,0x00,             #LUT2: WB:     VS 0 ~7
        # 0x10,0x60,0x20,0x00,0x00,0x00,0x00,             #LUT3: WW:     VS 0 ~7
        # 0x00,0x00,0x00,0x00,0x00,0x00,0x00,             #LUT4: VCOM:   VS 0 ~7

        # 0x03,0x03,0x00,0x00,0x02,                       # TP0 A~D RP0
        # 0x09,0x09,0x00,0x00,0x02,                       # TP1 A~D RP1
        # 0x03,0x03,0x00,0x00,0x02,                       # TP2 A~D RP2
        # 0x00,0x00,0x00,0x00,0x00,                       # TP3 A~D RP3
        # 0x00,0x00,0x00,0x00,0x00,                       # TP4 A~D RP4
        # 0x00,0x00,0x00,0x00,0x00,                       # TP5 A~D RP5
        # 0x00,0x00,0x00,0x00,0x00,                       # TP6 A~D RP6

        # 0x15,0x41,0xA8,0x32,0x30,0x0A,
    ]

    lut_partial_update = [ #20 bytes
0x40,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	
0x80,	0x00,	0x00,	0x00,	0x00,	0x00,0x00,	0x00,	0x00,	0x00,	
0x40,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	
0x80,	0x00, 0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00, 0x00,	0x00,	
	
0x0A,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00, 0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,
0x00,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,	
0x00,	0x00,	0x00,	0x00,	0x00,	
0x00, 0x00,	0x00,	0x00,	0x00,		
										
0x15,	0x41,	0xA8,	0x32,	0x50,	0x2C, 0x0B,
    ]
        
    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(100)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(100)  

    def send_command(self, command):
        epdconfig.digital_write(self.cs_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        
        epdconfig.digital_write(self.cs_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        while(epdconfig.digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            pass
            # epdconfig.delay_ms(100)    

    def TurnOnDisplay(self):
        self.send_command(0x22)
        self.send_data(0xC7)
        self.send_command(0x20)        
        self.ReadBusy()
        
    def TurnOnDisplayPart(self):
        self.send_command(0x22)
        self.send_data(0x0c)
        self.send_command(0x20)        
        self.ReadBusy()
        
    def init(self, update):
        if (epdconfig.module_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()
        if(update == self.FULL_UPDATE):
            self.ReadBusy()
            self.send_command(0x12) # soft reset
            self.ReadBusy()

            self.send_command(0x74) #set analog block control
            self.send_data(0x54)
            self.send_command(0x7E) #set digital block control
            self.send_data(0x3B)

            self.send_command(0x01) #Driver output control
            self.send_data(0xF9)
            self.send_data(0x00)
            self.send_data(0x00)

            self.send_command(0x11) #data entry mode
            self.send_data(0x01)

            self.send_command(0x44) #set Ram-X address start/end position
            self.send_data(0x00)
            self.send_data(0x0F)    #0x0C-->(15+1)*8=128

            self.send_command(0x45) #set Ram-Y address start/end position
            self.send_data(0xF9)   #0xF9-->(249+1)=250
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            
            self.send_command(0x3C) #BorderWavefrom
            self.send_data(0x03)

            self.send_command(0x2C)     #VCOM Voltage
            self.send_data(0x50)    #

            self.send_command(0x03)
            self.send_data(self.lut_full_update[100])

            self.send_command(0x04) #
            self.send_data(self.lut_full_update[101])
            self.send_data(self.lut_full_update[102])
            self.send_data(self.lut_full_update[103])

            self.send_command(0x3A)     #Dummy Line
            self.send_data(self.lut_full_update[105])
            self.send_command(0x3B)     #Gate time
            self.send_data(self.lut_full_update[106])

            self.send_command(0x32)
            for count in range(100):
                self.send_data(self.lut_full_update[count])

            self.send_command(0x4E)   # set RAM x address count to 0
            self.send_data(0x00)
            self.send_command(0x4F)   # set RAM y address count to 0X127
            self.send_data(0xF9)
            self.send_data(0x00)
            self.ReadBusy()
        else:

            # self.send_command(0x2C)     #VCOM Voltage
            # self.send_data(0x26)

            self.ReadBusy()

            self.send_command(0x32)
            for count in range(100):
                self.send_data(self.lut_partial_update[count])

            self.send_command(0x37)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x40)
            self.send_data(0x00)
            

            self.send_command(0x22)
            self.send_data(0xC0)
            self.send_command(0x20)
            self.ReadBusy()

            # self.send_command(0x3C) #BorderWavefrom
            # self.send_data(0x01)
        return 0

    def getbuffer(self, image):
        if self.width%8 == 0:
            linewidth = int(self.width/8)
        else:
            linewidth = int(self.width/8) + 1
         
        buf = [0xFF] * (linewidth * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        
        if(imwidth == self.width and imheight == self.height):
            logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):                    
                    if pixels[x, y] == 0:
                        x = imwidth - x
                        buf[int(x / 8) + y * linewidth] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            logging.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        newy = imwidth - newy - 1
                        buf[int(newx / 8) + newy*linewidth] &= ~(0x80 >> (y % 8))
        return buf   
        
        
    def display(self, image):
        if self.width%8 == 0:
            linewidth = int(self.width/8)
        else:
            linewidth = int(self.width/8) + 1

        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, linewidth):
                self.send_data(image[i + j * linewidth])   
        self.TurnOnDisplay()
        
    def displayPartial(self, image):
        if self.width%8 == 0:
            linewidth = int(self.width/8)
        else:
            linewidth = int(self.width/8) + 1

        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, linewidth):
                self.send_data(image[i + j * linewidth])   
                
                
        # self.send_command(0x26)
        # for j in range(0, self.height):
            # for i in range(0, linewidth):
                # self.send_data(~image[i + j * linewidth])  
        self.TurnOnDisplayPart()

    def displayPartBaseImage(self, image):
        if self.width%8 == 0:
            linewidth = int(self.width/8)
        else:
            linewidth = int(self.width/8) + 1

        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, linewidth):
                self.send_data(image[i + j * linewidth])   
                
                
        self.send_command(0x26)
        for j in range(0, self.height):
            for i in range(0, linewidth):
                self.send_data(image[i + j * linewidth])  
        self.TurnOnDisplay()
    
    def Clear(self, color):
        if self.width%8 == 0:
            linewidth = int(self.width/8)
        else:
            linewidth = int(self.width/8) + 1
        # logging.debug(linewidth)
        
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, linewidth):
                self.send_data(color)   
        self.TurnOnDisplay()

    def sleep(self):
        # self.send_command(0x22) #POWER OFF
        # self.send_data(0xC3)
        # self.send_command(0x20)

        self.send_command(0x10) #enter deep sleep
        self.send_data(0x01)
        epdconfig.delay_ms(100)

        epdconfig.module_exit()

### END OF FILE ###

# if __name__ == '__main__':
#     epd_t = EPD()
#     epd_t.init(epd_t.PART_UPDATE)
#     a = 0xff
#     for i in range(0,9):
#         print(i)
#         if i % 2 == 0:
#             a = 0x0
#         else:
#             a = 0xff
#         epd_t.displayPartial(a)
#         time.sleep(0.5)
         
#     print("end")
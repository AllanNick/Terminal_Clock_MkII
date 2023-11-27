# Terminal Clock
# Author: Nick
# Nick Computer, 2023

class display_buffer():
    def __init__(self):
        self.container = []
        self.digi = digital_char()
        
    def write_buffer(self, char_2_draw):
        addr_set = self.digi.get_digi(char_2_draw)

        for addr in addr_set:
            row = []
            for i in range(8):
                row.append(addr >> i & 0x01)
            self.container.append(row)

    def draw_buffer(self):

        for i in range(len(self.container[0])):
            for j in range(len(self.container)):
                if self.container[j][i] == 1:
                    print('\033[4;37;47m  \033[0m',end='')
                else:
                    print('  ',end='')
            print('')
    
    def clear_buffer(self):
        self.container = []

    def draw_strint(self,string):
        for i in str(string):
            self.write_buffer(int(i))

    def write_addr(self,addr):
        row = []
        for i in range(8):
            row.append(addr >> i & 0x01)
        self.container.append(row)

    def draw_long_digit(self,num_a,num_b,step):
        if num_b > 9:
            num_b = 0
        bin_a = self.digi.get_digi(num_b)
        bin_b = self.digi.get_digi(num_a)

        to_buffer = []

        for i in range(5):
            com_bin = (bin_a[i] << 6) + bin_b[i] >> step
            com_bin = com_bin & 0x3f
            to_buffer.append(com_bin)

        for i in range(5):
            self.write_addr(to_buffer[i])

class digital_char():
    def __init__(self):
        self.digis =[0x1e,0x11,0x11,0x0f,0x00, #0
        0x00,0x00,0x00,0x1f,0x00, #1    
        0x1c,0x15,0x15,0x17,0x00, #2    
        0x14,0x15,0x15,0x1f,0x00, #3    
        0x07,0x04,0x04,0x1f,0x00, #4    
        0x17,0x15,0x15,0x1c,0x00, #5
        0x1f,0x15,0x15,0x1c,0x00, #6    
        0x00,0x01,0x01,0x1f,0x00, #7    
        0x1f,0x15,0x15,0x1f,0x00, #8    
        0x07,0x15,0x15,0x1f,0x00, #9
        0x00,0x00,0x0a,0x00,0x00, #:
        0x00,0x00,0x00,0x00,0x00
        ]

    def get_digi(self,num):
        return self.digis[num*5:num*5+5]
    
def set_cursor(x,y):
    print('\033[%s;%s'%(x,y))

import datetime
from time import sleep
from os import get_terminal_size

display_buffer = display_buffer()

def get_step(sec):
    if sec - 50 > 0:
        return ((sec - 50)+1)//2
    else:
        return 0
    
while True:
    now = datetime.datetime.now()
    hour = now.hour
    minu = now.minute
    sec = now.second

    print('\033c')
    display_buffer.clear_buffer()

    #fit the screen

    x = get_terminal_size().columns
    y = get_terminal_size().lines

    cx = int(x/5 - 25/5)
    cy = int(y/2 - 4 )

    for i in range(cy):
        print('')

    for i in range(cx-1):
        display_buffer.write_addr(0x00)

    #end control

    str_hour = '%02d'%(hour)
    str_minu = '%02d'%(minu)
    str_sec = '%02d'%(sec)

    display_buffer.draw_strint('%02d'%(hour))

    if sec%4 != 0:
        display_buffer.write_buffer(10)
    else:
        display_buffer.write_buffer(11)

    display_buffer.draw_strint(str('%02d'%(minu))[0])

    display_buffer.draw_long_digit(int(str_minu[1]),int(str_minu[1])+1,get_step(sec))

    display_buffer.draw_buffer()

    sleep(1)

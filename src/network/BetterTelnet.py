'''
Created on 2012-6-4

@author: Sky
'''
from SocketLib.Telnet import *

g_telnetcolors=[[[0 for x in range(3)] for y in range(3)] for z in range(3)]
g_telnetcolors[0][0][0] = black + dim
g_telnetcolors[0][0][1] = blue + dim
g_telnetcolors[0][0][2] = blue + bold
g_telnetcolors[0][1][0] = green + dim
g_telnetcolors[0][1][1] = cyan + dim
g_telnetcolors[0][1][2] = blue + bold
g_telnetcolors[0][2][0] = green + bold
g_telnetcolors[0][2][1] = green + bold
g_telnetcolors[0][2][2] = cyan + bold

g_telnetcolors[1][0][0] = red + dim
g_telnetcolors[1][0][1] = magenta + dim
g_telnetcolors[1][0][2] = magenta + bold
g_telnetcolors[1][1][0] = yellow + dim
g_telnetcolors[1][1][1] = white + dim
g_telnetcolors[1][1][2] = blue + bold
g_telnetcolors[1][2][0] = green + bold
g_telnetcolors[1][2][1] = green + bold
g_telnetcolors[1][2][2] = cyan + bold

g_telnetcolors[2][0][0] = red + bold
g_telnetcolors[2][0][1] = red + bold
g_telnetcolors[2][0][2] = magenta + bold
g_telnetcolors[2][1][0] = yellow + dim
g_telnetcolors[2][1][1] = red + bold
g_telnetcolors[2][1][2] = magenta + bold
g_telnetcolors[2][2][0] = yellow + bold
g_telnetcolors[2][2][1] = yellow + bold
g_telnetcolors[2][2][2] = white + bold

class BetterTelnet:
    def __init__(self):
        self.m_buffer = ""
        
    def GetBuffered(self):
        return len(self.m_buffer)
    
    def Translate(self, p_conn, p_buffer):
        for i in range(0, len(p_buffer)):
            c = p_buffer[i]
            buffersize = len(self.m_buffer)
            if int(c) >= 32 and int(c) != 127 and buffersize < 1024:
                self.m_buffer += chr(c)
            elif int(c) == 8 and buffersize > 0:
                self.m_buffer = self.m_buffer[0:buffersize - 1]
            elif c == 10 or c == 13:
                if buffersize > 0 and p_conn.Handler() != None:
                    p_conn.Handler().Handle(self.m_buffer)
                    self.m_buffer = ""
                    
    def SendString(self, p_conn, p_string):
        string = self.TranslateColors(p_string)
        p_conn.BufferData(string)
        
    def TranslateColors(self, p_str):
        string = p_str.replace("<$black>", black).replace("<$red>", red).replace("<$green>", green).replace("<$yellow>", yellow).replace("<$blue>", blue).replace("<$magenta>", magenta).replace("<$cyan>", cyan).replace("<$white>", white).replace("<$bold>", bold).replace("<$dim>", dim).replace("<$reset>", reset)
        i = p_str.find("<")
        
        while i != -1:
            if p_str[i + 1] == '#':
                j = p_str.find(">", i)
                if j != -1 and j - i == 8:
                    temp = p_str[i:j + 1]
                    string = string.replace(temp, self.TranslateNumberColor(temp))
            i = p_str.find("<", i + 1)
        
        return string
    
    def ASCIIToHex(self, c):
        if c >= '0' and c <= '9':
            return ord(c) - ord('0')
        if c >= 'A' and c <= 'F':
            return ord(c) - ord('A') + 10
        if c >= 'a' and c <= 'a':
            return ord(c) - ord('a') + 10
        return 0
    
    def TranslateNumberColor(self, p_str):
        #chop off the six digits, ie the "XXXXXX" inside "<#XXXXXX>"
        col = p_str[2:8]
        
        r = self.ASCIIToHex(col[0]) * 16 + self.ASCIIToHex(col[1])
        g = self.ASCIIToHex(col[2]) * 16 + self.ASCIIToHex(col[3])
        b = self.ASCIIToHex(col[4]) * 16 + self.ASCIIToHex(col[5])
        
        #convert the numbers to the 0-2 range
        #ie:  0 -  85 = 0
        #     86 - 171 = 1
        #     172 - 255 = 2
        #This gives a good approximation of the true color by assigning equal
        #ranges to each value.
        r = r // 86
        g = g // 86
        b = b // 86
        
        return g_telnetcolors[r][g][b]

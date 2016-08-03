#encoding=utf8

import pdb

from Xlib.display import Display
from Xlib import X, XK
from Xlib.protocol.event import KeyPress, KeyRelease, ButtonPress, ButtonRelease
from Xlib.ext.xtest import fake_input
import time
from parser import Parser
import os

disp=Display()
screen=disp.screen()
root=screen.root

'''
mods:

Shifts : Shift
Caps Lock : Lock
Ctrls : Control

Alt(normally) : Mod1
Win(normall) : Mod4

os.system("xmodmap")

'''

class Keys:
    Super_L= 133
    alpha = {
        "a":38,
        "b":56,
        "c":54,
        "d":40,
        "e":26,
        "f":41,
        "g":42,
        "h":43,
        "i":31,
        "j":44,
        "k":45,
        "l":46,
        "m":58,
        "n":57,
        "o":32,
        "p":33,
        "q":24,
        "r":27,
        "s":39,
        "t":28,
        "u":30,
        "v":55,
        "w":25,
        "x":53,
        "y":29,
        "z":52,
    }
    number = [
        19,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
    ]
    Space = 65
    BackSpace = 22
    PageUp = 112
    PageDown = 117
    DiaoHao = [x for x in range(67,72)]

    code_alpha = dict((v,k) for k,v in alpha.iteritems())
    print code_alpha

def grab_key(key_code,mod=X.NONE):
    root.grab_key(key_code, mod | X.NONE, 0, X.GrabModeAsync, X.GrabModeAsync)
    root.grab_key(key_code, mod | X.LockMask, 0, X.GrabModeAsync, X.GrabModeAsync)
    root.grab_key(key_code, mod | X.Mod2Mask, 0, X.GrabModeAsync, X.GrabModeAsync)
    root.grab_key(key_code, mod | X.Mod2Mask | X.LockMask, 0, X.GrabModeAsync, X.GrabModeAsync)

def ungrab_key(key_code,mod=X.NONE):
    root.ungrab_key(key_code, mod | X.NONE)
    root.ungrab_key(key_code, mod | X.LockMask)
    root.ungrab_key(key_code, mod | X.Mod2Mask)
    root.ungrab_key(key_code, mod | X.Mod2Mask | X.LockMask)

def grab_global_hot_key():
    #grab_key(Keys.Super_L) 
    #grab_key(Keys.alpha["h"], X.Mod4Mask) 
    grab_key(Keys.Space, X.ControlMask|X.Mod1Mask) #ctrl+alt+SPACE 


class HahaState:
    def __init__(self):
        self.active = False
        self.allGrabKeycodes = []
        self.allGrabKeycodes.append(Keys.Space)
        self.allGrabKeycodes.append(Keys.BackSpace)
        self.allGrabKeycodes.append(Keys.PageUp)
        self.allGrabKeycodes.append(Keys.PageDown)
        self.allGrabKeycodes.extend(Keys.number)
        self.allGrabKeycodes.extend(Keys.alpha.values())
        self.allGrabKeycodes.extend(Keys.DiaoHao)
        #print self.allGrabKeycodes
    def switchActive(self):
        if self.active:
            self.deactivate()
            self.active = False
            print "Haha deactivated."
        else:
            self.activate()
            self.active = True
            print "Haha activated."
    def activate(self):
        #print "grab all keys."
        for keycode in self.allGrabKeycodes:
            disp.sync()
            grab_key(keycode)
            disp.sync()

    def deactivate(self):
        #print "ungrab all keys."
        for keycode in self.allGrabKeycodes:
            disp.sync()
            ungrab_key(keycode)
            disp.sync()


        
hahaState = HahaState()
parser = Parser()
printed_result = []
current_page = 0

def print_selections(content_list,count_perpage=10):
    #current_result = parser.get_result()
    global printed_result
    i = 1
    global current_page
    print "> %s" % parser.get_search_sequence_string() 
    if len(content_list) < 1:
        print "No word found..."
        printed_result = []
        return
    page_count = len(content_list)/count_perpage
    if len(content_list) % count_perpage !=0:
        page_count += 1
    page_number_indicator= [ "□" for _ in range(page_count)]
    if current_page >=page_count:
        current_page = page_count - 1
    if current_page < 0 :
        current_page = 0
    page_number_indicator[current_page] = "■" 
    print " ".join(page_number_indicator)
    printed_result = content_list[current_page*count_perpage:(current_page+1)*count_perpage]
    for content in printed_result:
        print_index = i
        if i == 10:
            print_index = 0
        print "%d %s" % (print_index,content.content)
        i += 1
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^"

def main():
    pass

    print "start..."
    print "grab global hot key: Ctrl + Alt + Space"
    
    grab_global_hot_key()

    #L_shift = 50
    #print root.grab_key(50, X.NONE, 0, X.GrabModeAsync, X.GrabModeAsync)
    
    #grab_key(38)

    current_result = []
    global current_page
    global printed_result
    while 1:
        evt = root.display.next_event()
        #print type(evt)
        #pdb.set_trace()
        #print "evt.type:" +str(evt.type)
        if evt.type not in [X.KeyPress,X.KeyRelease]:
            #print "evt type not supported."
            continue
        #print "key_code:" + str(evt.detail)

        if evt.detail == Keys.Space \
        and evt.type == X.KeyRelease \
        and evt.state & X.ControlMask !=0 \
        and evt.state & X.Mod1Mask !=0:
            hahaState.switchActive()
            parser.reset_search()
            print ""
            #exit(0) 
        elif evt.detail in hahaState.allGrabKeycodes and hahaState.active and evt.type == X.KeyRelease:
            print "key: %d" % evt.detail

            #a alpha key pressed. need search words.
            if evt.detail in Keys.code_alpha.keys():
                if parser.add_search_char(Keys.code_alpha[evt.detail]):
                    current_result = parser.get_result()
                    current_page = 0
                    print_selections(current_result)
                else:
                    current_result = [] 
                    print_selections(current_result)
                continue
            #DiaoHao    
            if evt.detail >=67 and evt.detail <=71 :
                if len(parser.search_sequence) > 0:
                    if parser.add_search_char(str(evt.detail-66)):
                        current_result = parser.get_result()
                        current_page = 0
                        print_selections(current_result) 
                    continue
                    
                continue  


            #a number or space key pressed. push word onto screen 
            if evt.detail in Keys.number or evt.detail == Keys.Space:
                index = 1
                
                if evt.detail in Keys.number:
                    #if len(current_result) = 0:
                    #    os.system("")
                    index = Keys.number.index(evt.detail)
                    if index == 0:
                        index = 10
                

                if len(printed_result)>= index:
                    #hahaState.deactivate()
                    printed_result[index-1].send_content()
                    #hahaState.activate()
                    print "select: %s" % printed_result[index-1].content
                    current_result = []
                    printed_result = [] 
                    parser.reset_search()
                else:
                    print "invalid selection."
                    print_selections(current_result)
                
                continue
            
            #back space
            if evt.detail == Keys.BackSpace:
                if len(parser.search_sequence)>0:
                    parser.dec_search_char()
                    current_result = parser.get_result()
                    print_selections(current_result)
                    if len(parser.search_sequence) == 0:
                        parser.reset_search()
                else:
                    #hahaState.deactivate()
                    os.system("xdotool key --window `xdotool getwindowfocus` BackSpace")
                    #hahaState.activate()
                continue    
            if evt.detail == Keys.PageUp or evt.detail == Keys.PageDown:
                if evt.detail == Keys.PageUp:
                    current_page -= 1

                elif evt.detail == Keys.PageDown:
                    current_page += 1
                print_selections(current_result)
                continue


            print "WARNING:no func found."
if __name__ == "__main__":
    main()

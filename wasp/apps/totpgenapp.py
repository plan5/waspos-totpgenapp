# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson
"""The complete set of wasp-os application entry points are documented
below as part of a template application. Note that the template does
not rely on any specific parent class. This is because applications in
wasp-os can rely on *duck typing* making a class hierarchy pointless.

Code from https://medium.com/analytics-vidhya/understanding-totp-in-python-bbe994606087
New code from https://github.com/eddmann/pico-2fa-totp/
"""

import wasp
import widgets
import fonts
from gc import collect
from micropython import const
from totp import totp

collect()

# 2-bit RLE, 96x64, generated from /home/eloeffler/Art/totp.png, 264 bytes
icon = (
    b'\x02'
    b'`@'
    b"'\x8f?\x10\x93?\x0c\x97?\t\x99?\x06\x9d?\x03"
    b'\x9f?\x01\xa1>\x91\x01\x91=\x8e\x07\x8e<\x8c\r\x8c'
    b':\x8c\x0f\x8c9\x8b\x11\x8b8\x8b\x13\x8b6\x8b\x15\x8b'
    b'5\x8a\x17\x8a5\x89\x19\x894\x8a\x19\x8a3\x89\x1b\x89'
    b'2\x8a\x1b\x8a1\x89\x1d\x891\x89\x1d\x891\x88\x1f\x88'
    b'0\x89\x1f\x89/\x89\x1f\x89/\x89\x1f\x89/\x88!\x88'
    b'/\x88!\x88/\x88!\x88,@\x0cB\x80\x1e\xb3B'
    b"(A\xb7A'A\x98G\x98A'\x97K\x97'\x96"
    b"M\x96'\x95O\x95'\x95O\x95'\x94Q\x94'\x94"
    b"G\x83G\x94'\x94F\x85F\x94'\x94F\x85F\x94"
    b"'\x94F\x85F\x94'\x94G\x83G\x94'\x94Q\x94"
    b"'\x95O\x95'\x95O\x95'\x96M\x96'\x97K\x97"
    b"'\x99G\x99'\x99G\x99'\x99H\x98'\x98I\x98"
    b"'\x98I\x98'\x98I\x98'\x98I\x98'\x98J\x97"
    b"'\x98J\x97'\x98J\x97'\x98J\x97'\x97K\x97"
    b"'\x97L\x96'\xb9'\xb9'A\xb7A'A\xb7A"
    b'(B\xb3B\x16'
)

_LOCKED = const(0)
_UNLOCKED = const(1)

class TOTPGenApp():
    """Template application.

    The template application includes every application entry point. It
    is used as a reference guide and can also be used as a template for
    creating new applications.

    .. data:: NAME = 'Template'

       Applications must provide a short ``NAME`` that is used by the
       launcher to describe the application. Names that are longer than
       8 characters are likely to be abridged by the launcher in order
       to fit on the screen.

    .. data:: ICON = RLE2DATA

       Applications can optionally provide an icon for display by the
       launcher. Applications that expect to be installed on the quick
       ring will not be listed by the launcher and need not provide any
       icon. When no icon is provided the system will use a default
       icon.

       The icon is an opportunity to differentiate your application from others
       so supplying an icon is strongly recommended. The icon, when provided,
       must not be larger than 96x64.

    """
    NAME = 'TOTPGen'
    ICON = icon

    def __init__(self):
        collect()
        """Initialize the application."""
        self.index = 0
        self.secret = self.readsecret()
        self.state = _LOCKED

        pass

    def readsecret(self):
        collect()
        try:
            secretfile = open("totp.csv", "r")
            list = secretfile.readlines()
            self.index = self.index%len(list)
            secret = list[self.index].rstrip('\n').split(';')
            del list
            collect()
            secretfile.close()
            collect()
            return secret
        except:
            return 'totp.csv missing', 'NOTOTP'
            

    def foreground(self):
        collect()
        """Activate the application."""
        self.drawpins()
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH |
                                  wasp.EventMask.SWIPE_UPDOWN |
                                  wasp.EventMask.SWIPE_LEFTRIGHT |
                                  wasp.EventMask.BUTTON)
        wasp.system.request_tick(1000)

    def background(self):
        """De-activate the application."""
        pass

    def drawpins(self):
        self.pin1 = widgets.Spinner(0, 60, 0, 9, 2)
        self.pin2 = widgets.Spinner(60, 60, 0, 9, 2)
        self.pin3 = widgets.Spinner(120, 60, 0, 9, 2)
        self.pin4 = widgets.Spinner(180, 60, 0, 9, 2)
        self.pin1.value = 0
        self.pin2.value = 0
        self.pin3.value = 0
        self.pin4.value = 0

    def swipe(self, event):
        if event[0] == wasp.EventType.UP:
            self.index += 1
        elif event[0] == wasp.EventType.LEFT:
            self.unset()
            self.drawpins()
        elif event[0] == wasp.EventType.RIGHT:
            self.unset()
            self.drawpins()
        else:
            self.index -= 1
        self.secret = self.readsecret()
        self._draw()

    def tick(self, ticks):
        """Notify the application that its periodic tick is due."""
        if self.state == _LOCKED:
            pass
        else:
            self._update()
        pass

    def touch(self, event):
        """Notify the application of a touchscreen touch event."""
        collect()
        if self.state == _LOCKED:
            if self.pin1.touch(event) or self.pin2.touch(event) or self.pin3.touch(event) or self.pin4.touch(event):
                pass
            elif self.btn_start.touch(event):
                self.pin = str(self.pin1.value) + str(self.pin2.value) + str(self.pin3.value) + str(self.pin4.value)
                del self.pin1
                del self.pin2
                del self.pin3
                del self.pin4
                del self.btn_start
                collect()
                self._start()
        pass

    def _start(self):
        collect()
        self.state = _UNLOCKED
        self._draw()
        pass

    def unset(self):
        collect()
        try:
            del self.pin
            collect()
            self.state = _LOCKED
        except:
            pass

    def sleep(self):
        self.unset()
        collect()
        return False

    def _draw(self):
        collect()
        """Draw the display from scratch."""
        draw = wasp.watch.drawable
        draw.set_font(fonts.sans18)
        draw.fill()
        draw.string(self.NAME, 0, 6, width=240)
        if self.state == _LOCKED:
            self.pin1.draw()
            self.pin2.draw()
            self.pin3.draw()
            self.pin4.draw()
            self.btn_start = widgets.Button(x=20, y=200, w=200, h=40, label="START")
            self.btn_start.draw()
            draw.reset()
        else:
            self._update()

    def _update(self):
        collect()
        """Update the dynamic parts of the application display."""
        if self.state == _LOCKED:
            pass
        else:
            self.drawtotp()
        pass

    def press(self, button, state):
        collect()
        if state == True:
            wasp.system.sleep()
        else:
            pass

    def drawtotp(self):
        collect()
        draw = wasp.watch.drawable
        draw.set_font(fonts.sans18)
        # Add Offset before displaying time (for Colmi P8)
        time = wasp.watch.rtc.time()+946677600
        # Use this for testing in the simulator instead
        # time = wasp.watch.rtc.time()
        (password, expiry) = totp(int(time), self.decrypt(self.secret[1]), 30, 6)
        draw.string(self.secret[0], 0, 66, width=240)
        if self.secret[1] == "NOTOTP":
            draw.string("Please upload", 0, 108, width=240)
            draw.string("(wasptool)", 0, 150, width=240)
        else:
            draw.string(password, 0, 108, width=240)
            draw.string(str(expiry), 0, 150, width=240)
        del password
        del expiry
        collect()

    def decrypt(self, text, encrypt=0):
        collect()
        result = ""
        # transverse the plain text 
        for i in range(len(text)):
            char = text[i]
            # There is no zfill in micropython so this doesn't work
            # s = int(str(self.pin).zfill(4)[i%4])
            s = int(self.pin[i%4])
            # Reverse pin for encryption
            if encrypt == 1:
                s = -s
            # Decrypt capitalized characters into plain text
            if char.isdigit():
                result += char
            else:
                result += chr((ord(char) - s - 65) % 26 + 65)
        return result

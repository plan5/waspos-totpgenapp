# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson
"""The complete set of wasp-os application entry points are documented
below as part of a template application. Note that the template does
not rely on any specific parent class. This is because applications in
wasp-os can rely on *duck typing* making a class hierarchy pointless.

Code from https://medium.com/analytics-vidhya/understanding-totp-in-python-bbe994606087
New code from https://github.com/eddmann/pico-2fa-totp/
"""

def decrypt(pin, text, encrypt=0):
    result = ""
    # transverse the plain text 
    for i in range(len(text)):
        char = text[i]
        # There is no zfill in micropython so this doesn't work
        # s = int(str(pin).zfill(4)[i%4])
        s = int(pin[i%4])
        # Reverse pin for encryption
        if encrypt == 1:
            s = -s
        # Decrypt capitalized characters into plain text
        if char.isdigit():
            result += char
        else:
            result += chr((ord(char) - s - 65) % 26 + 65)
    return result

pin=input("PIN: ")
text=input("SECRET: ")
encrypted=decrypt(pin, text, 1)
print("Enc: ", encrypted)
print("Dec: ", decrypt(str(pin).zfill(4), text))

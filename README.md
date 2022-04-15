# TOTP app for Wasp OS
This is an unpolished TOTP app for wasp-os. It currently provides SHA-1 based
One-Time-Passwords with a cycle of 30 seconds. It requires a lot of memory so
you may want to remove as many apps as possible before compiling.

## Configuration
The app requires a file named totp.csv in your root directory. An example file
is included in this archive. The file is formatted simply. An account handle
(should be short) followed by a semicolon and the TOTP secret.

    ACCOUNT;SECRETSECRETSECRET

Run the makesecret.py to create a TOTP key with very light encryption (CAESAR).
If you do not wish to apply the CAESAR cipher, just add your secret to the
totp.csv file and your pin will be 0000. 

You may also apply the CAESAR cipher manually if you prefer that. Just write down
your secret string and write your repeated PIN below. Then increment the letters
based on the number written below them. 

Example:

    MYSECRET
    34563456
    PCXKFVJZ

## Building

Unzip the current release inside the wasp-os source root directory and add the following to
wasp/boards/manifest_240x240.py:

    'apps/totpgenapp.py', 
    'totp/__init__.py', 
    'totp/sha1.py', 
    'totp/base32.py',
    
Refer to the official build guide for the remaining steps.
    
You will likely run into compilation errors if you have many other apps frozen into the image.
Remove unneeded apps from the manifest file in this case.

## Usage and Testing
### Testing
Extract the archive to the wasp-os source directory and run `make sim`.

The generated codes will be wrong in the simulator: Calculatiion of the UNIX
time is adjusted for the Colmi P8 (and most probably for the Pinetime as well)
that uses a different epoch than the default. If you want to run it in the
simulator properly, change the drawotp() function (see comments there).

### Usage
When the app starts, it will ask for a pin. If you did not apply the CAESAR cipher to your 
secret then you can leave it at 0000.

If everything works, you will now see the account name, the current TOTP and the expiry time in seconds.

Swipe up/down to see other accounts.

Swipe left/right to lock the app.

Press the button to sleep and lock the app.

## Screenshots

![Screenshot of PIN entry screen](https://github.com/plan5/waspos-totpgenapp/blob/main/p8totp_pin.png?raw=true)
![Screenshot of TOTP screen](https://github.com/plan5/waspos-totpgenapp/blob/main/p8totp_totp.png?raw=true)

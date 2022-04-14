# TOTP app for Wasp OS
This is an unpolished TOTP app for wasp-os. It currently provides SHA-1 based
One-Time-Passwords with a cycle of 30 seconds. It requires a lot of memory so
you may want to remove as many apps as possible before compiling.

The app requires a file named totp.csv in your root directory. An example file
is included in this archive. The file is formatted simply. An account handle
(should be short) followed by a semicolon and the TOTP secret.
ACCOUNT;SECRETSECRETSECRET

The generated codes will be wrong in the simulator: Calculatiion of the UNIX
time is adjusted for the Colmi P8 (and most probably for the Pinetime as well)
that uses a different epoch than the default. If you want to run it in the
simulator properly, change the drawotp() function (see comments there).

Unzip the current release inside the wasp-os source root directory and add the following to
wasp/boards/manifest_240x240.py:

    'apps/totpgenapp.py', 
    'totp/__init__.py', 
    'totp/sha1.py', 
    'totp/base32.py',

Run the makesecret.py to create a TOTP key with very light encryption (CAESAR).
If you do not wish to apply the CAESAR cipher, just add your secret to the
totp.csv file and your pin will be 0000.

https://github.com/plan5 (repo for this project not yet created)
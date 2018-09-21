# FE-5680A
A python script to set the frequenzy for a Model FE-5680A Rubidium Atomic Frequency Standard

## Usage

```bash
$ ./FE-5680A.py -h
usage: FE-5680A.py [-h] [-p PORT] [-f FREQ] [-s] [-q | -v]

Tool to up- and download files to and from micropython.

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  path serial device (default = "/dev/ttyUSB0")
  -f FREQ, --freq FREQ  frequency (default = 10000000
  -s, --save            save config on FE-5680A
  -q, --quiet           turn off warnings
  -v                    set verbose loglevel
$ ./FE-5680A.py --port /dev/ttyUSB1 --freq 5000000 --save
```

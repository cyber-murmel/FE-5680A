#!/usr/bin/env python3

from sys import argv, stdout
from serial import Serial
import re

from argparse import ArgumentParser
from logging  import getLogger, StreamHandler
from logging  import ERROR, WARNING, INFO, DEBUG, NOTSET

def parse_arguments():
    parser = ArgumentParser(description='Tool to up- and download files to and from micropython.')
    verbose = parser.add_mutually_exclusive_group()
    operation = parser.add_mutually_exclusive_group()
    verbose.add_argument(  "-q", "--quiet",    action = "store_true",                help = "turn off warnings")
    verbose.add_argument(  "-v",               action = "count",                     help = "set verbose loglevel")
    parser.add_argument(   "-p", "--port",     type = str, default = "/dev/ttyUSB0", help = "path serial device (default = \"/dev/ttyUSB0\")")
    parser.add_argument(   "-f", "--freq",     type = float, default = 10000000,     help = "frequency (default = 10000000")
    args = parser.parse_args()
    return args

def generate_logger(verbose, quiet):
    logger = getLogger()
    logger.addHandler(StreamHandler())
    if verbose:
        if   1 == verbose:
            logger.setLevel(INFO)
            logger.info("Verbose output.")
        elif 2 <= verbose:
            logger.setLevel(DEBUG)
            logger.debug("Debug output.")
    elif quiet:
        logger.setLevel(ERROR)
    return logger

if __name__ == "__main__":
    global log
    args = parse_arguments()
    log = generate_logger(verbose=args.v, quiet=args.quiet)
    with Serial(port=args.port, baudrate=9600) as com:
        com.flush()
        com.write(b'S\r')
        status = com.read_until(b'OK\r')
        log.debug(status)
        p = re.compile('R=(.+)Hz F=(.+)\rOK\r')
        search = p.search(status.decode())
        if search:
            R=float(search.group(1))
            F=int(search.group(2), 16)
            log.info("Reference frequency is\t{}Hz".format(R))
            log.info("Current multiplier is\t{} ({}).".format(F, hex(F)))
            F = int(args.freq*(1<<64)/R)
            log.info("New multiplier is\t{} ({}).".format(F, hex(F)))
            com.write('F={:016x}\r'.format(F).encode())
            log.debug(com.read_until(b'OK\r'))
            com.write(b'S\r')
            log.debug(com.read_until(b'OK\r'))
        else:
            log.error("Could not communicate with FE-5680A")

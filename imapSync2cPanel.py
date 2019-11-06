#!/usr/bin/python3
from argparse import ArgumentParser
from sys import stdin, stdout, stderr
from os import path, getcwd


def parseIn(f):
    if not f:
        return [i.strip().split(';') for i in stdin.readlines()]
    with open(path.join(getcwd(), f)) as fl:
        return [i.strip().split(';') for i in fl.readlines()]


def createConf(ln, q):
    stdout.write("\n".join([f'{l[4]},{l[5]},{q}' for l in ln]))


if __name__ == "__main__":
    ap = ArgumentParser(epilog='', description='')
    ap.add_argument('--file', '-f', default=False)
    ap.add_argument('--quota', '-q', default=1024, type=int)
    p = ap.parse_args()
    createConf(parseIn(p.file), p.quota)

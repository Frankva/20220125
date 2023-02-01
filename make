#!/usr/bin/bash
py.exe main.py |& tee log.txt & vim log.txt

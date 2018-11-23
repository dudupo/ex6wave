#!/bin/sh
winrar.exe a -afzip ex6.zip ex6.py README
scp -P 1115 ex6.zip davidponar@localhost:ex6.zip

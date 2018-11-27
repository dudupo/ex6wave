#!/bin/sh
winrar.exe a -afzip ex6.zip ./wave_editor.py
scp -P 1115 ex6.zip davidponar@localhost:ex6.zip

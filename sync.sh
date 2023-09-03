#!/bin/bash
# Syncs local files to the CircuitPython device
rsync -avh --delete --inplace --exclude=".git" --exclude=".vscode" --exclude=".micropico" lib/ /run/media/enzy/CIRCUITPY/lib

cp -r boot.py /run/media/enzy/CIRCUITPY/boot.py
cp -r code.py /run/media/enzy/CIRCUITPY/code.py







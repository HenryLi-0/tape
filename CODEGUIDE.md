# Code Guide

Hello! Looks like you're interested in this code! Whether you're a programmer or someone who stumbled across this repository, here's the way this code is stored: (so that you don't have to look through every file for something)

**tape/** 

where the most important things are
- `main.py` : just initializes the window after checking
- `SETTINGS.py` : contains important constants, and some editable settings
- `README.md` : the readme.md?
- `CODEGUIDE.md` : idk what to call it, but here's some documentation on what files do

not really relevant stuff
- `experiments.py` : not really relevant to stuff yet
- `test.py` : not really relevant to stuff yet, just some testing


**tape/subsystems/** 

where useful code exists across different files
- `bay.py` : used for loading images and poorly manages them
- `checks.py` : checks that important resources exist to prevent random crashes
- `fonts.py` : used for anything font related
- `interface.py` : parts of the tk window (animation, timeline, editor, options)
- `pathing.py` : used to generate paths (idk what to call it) and things related to moving and coordinates
- `render.py` : things related to rendering and image stuff
- `visuals.py` : very silly way for buttons and visuals on the screen
- `window.py` : just the tk window

**other directories in tape/**
- `tape/resources/` : resources and things used (ex. test images, fonts)
- `tape/storage/` : planned to be used for storing images the user uploads
- `tape/updatelogs/` : where my silly silly fingers type strange update logs about what i did today (programming and not programming sutff included)
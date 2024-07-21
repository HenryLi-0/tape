# Code Guide

Hello! Looks like you're interested in this code! Whether someone who stumbled across this repository or future me who forgot what this is all about, here's the way this code is stored: (so that you don't have to look through every file for something)

**tape/** 

where the most important things are
- `main.py` : just initializes the window after checking
- `SETTINGS.py` : contains important constants, and some editable settings
- `README.md` : the readme.md?
- `CODEGUIDE.md` : idk what to call it, but here's some documentation on what files do
- `MANUAL.md` : a little instruction manual for default keybinds and things

not really relevant stuff
- `experiments.py` : not really relevant to stuff yet
- `test.py` : not really relevant to stuff yet, just some testing


**tape/subsystems/** 

where useful code exists across different files
- `bay.py` : used for loading images and poorly manages them
- `checks.py` : checks that important resources exist to prevent random crashes
- `counter.py` : just a counter, but it shockingly important!
- `fancy.py` : used for fancy rendering stuff (fonts, border boxes)
- `interface.py` : parts of the tk window (animation, timeline, editor, options). contains a lot of code.
- `pathing.py` : used to generate paths (idk what to call it) and things related to moving and coordinates
- `render.py` : things related to rendering and image stuff
- `sprite.py` : all things sprite related
- `visuals.py` : very silly way for buttons and visuals on the screen
- `window.py` : just the tk window

**other directories in tape/**
- `tape/resources/` : resources and things used (ex. test images, fonts)
- `tape/storage/` : used for storing images the user uploads
- `tape/subsystems/` : subsystems, see above!
- `tape/tapes/` : used as a storage space for Tape projects (tapes)!
- `tape/updatelogs/` : where my silly silly fingers type strange update logs about what i did today (programming and not programming stuff included)

### Probably something important:

I use a lot of words that probably don't mean what I think they mean. If there are any suggestions for better things to name stuff, I'll definitely be interested! 
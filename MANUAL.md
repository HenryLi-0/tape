# Tape - Usage Manual

---

### General:

- A: Creation
- S: Deletion
- Z: Move Left or Up
- X: Move Right or Down
- Up: Move up
- Down: Move down
- Mouse Scroll: Zoom or move up/down

### Default Keybinds

**All:**
- Left Mouse Click: Interact
- Control_L or Return/Enter: Submit/Finish

**Editor (Sprites):**
- A: Create a sprite (at mouse location if inside section, else at bottom)
- S: Deletes selected sprite
- Z: Move selected sprite up
- X: Move selected sprite down
- Up: Scroll Up
- Down: Scroll Down
- Mouse Scroll: Scroll

**Editor (Visual):**
- Graph Tabs
    - 1: Coordinates
    - 2: Rotations
    - 3: Apperance
    - 4: Size
    - 5: Hue
    - 6: Transparency
    - 7: Brightness
    - 8: Blur
- Points
    - Q: Linear Connection
    - W: Smooth Connection
    - A: Create Point (At mouse position)
    - S: Delete (selected) Point
    - Z: Move graph left
    - X: Move graph right
    - Mouse Scroll: Change zoom (centered at mouse)
- Coordinate Editor
    - D: Move selected point's waypoint to mouse location

**Timeline:**
- Left: Move timeline left
- Right: Move timeline right
- Mouse Scroll: Change zoom (centered at mouse)

### Buttons and Other UI Stuff

**Special Buttons**
- Editor > Sprites
    - Add: Creates a new sprite at the bottom of the sprites list
    - Delete: Deletes selected sprite
- Editor > Visuals:
    - Add: Imports an image
    - Points: Draggable points in a point-based editor
- Editor > Projects
    - Export GIF: Saves the animation to GIF
    - Export MP4: Saves the animation to MP4
- Timeline
    - Play/Pause: Play/pause the animation
    - Save: Saves project
    - Open: Opens project
- Options
    - Sprite, Visuals, Project: Switches to respective editor tab
    - Settings: Opens `SETTINGS.py`

**Others**
- Timeline
    - Colored bars represent different sprites and their "importance" ranges
    - Draggable timeline bar
- Options
    - Displayed are the mouse position (replaced with relative animation mouse position when in animation section), FPS, and the interacting object ID (brightens when mouse is pressed)

### Warnings:
- Opening projects from past versions may crash! The opening/saving code will try to stay the same throughout versions, but there is no guarantee that the project will always open properly through different versions
- It's highly recommended to save your project before exporting! Exporting will lag the window! (It will appear stuck, but let it run, assuming it didn't crash due to a bug!)
- Report any strange bugs/unexpected behavior in issues on GitHub! The repository can be found here: https://github.com/HenryLi-0/tape

---

### Version Info:

Tape Version: v1.1.0

Last Updated: 8/19/2024

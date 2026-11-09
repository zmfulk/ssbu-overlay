# Super Smash Bros. Ultimate Broadcast Overlay

A dynamic, web-based esports broadcast overlay and Python GUI controller designed for Super Smash Bros. Ultimate tournaments. Built for seamless integration with OBS Studio.

## Features
* **Live Web Overlay**: Clean HTML/CSS/JS frontend that instantly reacts to data changes without full page reloads.
* **Python Control Panel**: A Tkinter-based GUI for producers to update scores, player names, team colors, and series text on the fly.
* **Character Splash Integration**: Automatically pulls official high-resolution character renders directly from the smashbros.com asset database via dropdown selection.
* **Smart Framing**: Customizable Y-offset and Zoom sliders for every character to fix awkward image cropping (e.g., Sephiroth's sword or Ridley's wings), complete with automatic preset mapping.
* **Dynamic Logos**: Instant swapping between NACE and GLEC league branding.

## Setup Instructions

### 1. OBS Studio Integration
1. Open OBS Studio and add a new **Browser Source**.
2. Check the box for **Local file** and browse to the `index.html` file in this folder.
3. Set the dimensions to your canvas size (typically `1920` Width and `1080` Height).
4. Check **Refresh browser when scene becomes active**.

### 2. Running the Controller
**Option A: Executable (Recommended for Production)**
Download the latest `gui.exe` from the GitHub Releases page and place it in the same directory as the web files. Double-click to launch.

**Option B: Python Source**
Ensure Python 3 is installed on your system.
1. Clone this repository.
2. Run `python gui.py` in your terminal.

*Note: The controller automatically generates and updates a local `data.json` file. The web overlay polls this file every 500ms to smoothly animate any changes to the broadcast.*
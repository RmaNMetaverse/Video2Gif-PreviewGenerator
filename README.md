# **Video >> GIF Preview Generator**

A lightweight, robust python desktop application that automatically scans folders for MP4 video files and generates optimized GIF previews. It intelligently stitches together random segments from the video to create a comprehensive "trailer-style" preview, similar to YouTube's hover previews.

## **🚀 Features**

* **Smart Preview Logic:** Automatically grabs random timestamps throughout the video to give a true representation of the content.  
* **Intelligent Short Video Handling:** Automatically detects short videos (\< 12s) and converts the entire clip instead of fragmenting it.  
* **Highly Configurable:** \* Set custom output resolution.  
  * Choose the number of clips to sample.  
  * Set the duration for each sample clip.  
* **Optimized Output:** Generates small file sizes (\~1-3MB) using color palette optimization and quantization.  
* **Material Design GUI:** Clean, modern interface built with Python's Tkinter.  
* **Responsive:** Multithreaded processing ensures the UI never freezes during batch operations.  
* **Standalone Capable:** Includes scripts to compile into a single .exe file for portability.

## **🛠️ Installation**

### **Option A: Running from Source**

1. Ensure you have Python installed.  
2. Clone this repository.  
3. Run the provided installer script to set up dependencies:  
   InstallRequirements.bat

   *Alternatively, install manually:*  
   pip install opencv-python imageio pyinstaller

### **Option B: Standalone Executable**

If you have built the .exe (see Building section), simply double-click VideoPreviewGenerator.exe. No Python installation is required.

## **🖥️ Usage**

1. **Launch the App:**  
   python VideoGIFPreviewer-GUI.py

2. **Configure Settings (Optional):**  
   * **Resolution:** Width in pixels (default: 280px).  
   * **Points to Sample:** How many distinct parts of the video to grab (default: 3).  
   * **Duration:** How long each part plays (default: 2.0s).  
3. **Select Input:**  
   * **Select Files:** Pick specific MP4 files.  
   * **Scan Folder:** Pick a directory to process all MP4s inside it (top-level only).  
4. **View Results:** \* The tool will generate a .gif file next to every source .mp4 file with the same name.  
   * *Example:* vacation.mp4 \-\> vacation.gif

## **📦 Building the Executable**

To compile this tool into a standalone Windows .exe file that works on computers without Python:

1. Double-click build\_exe.bat.  
2. Wait for the process to finish.  
3. Find your application in the dist/ folder.

## **🔧 Technologies Used**

* **Python 3**  
* **Tkinter:** For the Graphical User Interface.  
* **OpenCV (cv2):** For high-performance video frame extraction.  
* **ImageIO:** For optimized GIF encoding.  
* **PyInstaller:** For building the executable.

## **📝 License**

This project is open-source and free to use.

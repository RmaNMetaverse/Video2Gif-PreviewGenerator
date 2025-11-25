import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk
import os
import threading
import cv2
import imageio
import random

class PreviewGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Preview Generator")
        self.root.geometry("700x600") # Increased height slightly for settings
        
        # --- MATERIAL DESIGN PALETTE ---
        self.colors = {
            'primary': '#2196F3',      # Blue
            'primary_dark': '#1976D2', # Darker Blue
            'background': '#FAFAFA',   # Off-white
            'surface': '#FFFFFF',      # Pure white
            'text': '#212121',         # Almost black
            'text_light': '#757575',   # Grey
            'accent': '#FFC107',       # Amber
            'success': '#4CAF50'       # Green
        }

        # --- THEME SETUP ---
        self.root.configure(bg=self.colors['background'])
        
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass

        # Configure Custom Styles
        style.configure("TFrame", background=self.colors['background'])
        style.configure("TLabel", background=self.colors['background'], foreground=self.colors['text'])
        
        # Modern Flat Button Style
        style.configure(
            "Material.TButton",
            background=self.colors['primary'],
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 10)
        )
        
        # Hover effect for buttons
        style.map(
            "Material.TButton",
            background=[('active', self.colors['primary_dark'])],
            relief=[('pressed', 'flat')]
        )

        # Progress Bar Style
        style.configure(
            "Material.Horizontal.TProgressbar",
            troughcolor="#E0E0E0",
            background=self.colors['success'],
            thickness=10,
            borderwidth=0
        )

        # --- VARIABLES ---
        self.var_width = tk.IntVar(value=280)
        self.var_num_clips = tk.IntVar(value=3)
        self.var_clip_duration = tk.DoubleVar(value=2.0)

        # --- UI LAYOUT ---

        # 1. Header Section (Blue Bar)
        header_frame = tk.Frame(root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame, 
            text="Video > GIF Preview Generator", 
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        title_label.pack(pady=20)

        # 2. Main Content Area
        main_container = tk.Frame(root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Instructions
        subtitle = tk.Label(
            main_container,
            text="Select video files to generate lightweight GIF previews.",
            font=("Segoe UI", 11),
            bg=self.colors['background'],
            fg=self.colors['text_light']
        )
        subtitle.pack(pady=(0, 15))

        # --- SETTINGS SECTION ---
        settings_frame = tk.LabelFrame(
            main_container, 
            text="Configuration",
            bg=self.colors['background'],
            fg=self.colors['text_light'],
            font=("Segoe UI", 9),
            bd=1,
            relief=tk.SOLID
        )
        settings_frame.pack(fill=tk.X, pady=(0, 20), ipady=5)

        # Grid layout for settings
        # Width
        tk.Label(settings_frame, text="Resolution Width (px):").grid(row=0, column=0, padx=(15, 5), pady=10)
        ttk.Entry(settings_frame, textvariable=self.var_width, width=8).grid(row=0, column=1, padx=5, pady=10)

        # Num Clips
        tk.Label(settings_frame, text="Points to Sample:").grid(row=0, column=2, padx=(15, 5), pady=10)
        ttk.Entry(settings_frame, textvariable=self.var_num_clips, width=5).grid(row=0, column=3, padx=5, pady=10)

        # Duration
        tk.Label(settings_frame, text="Duration per Point (s):").grid(row=0, column=4, padx=(15, 5), pady=10)
        ttk.Entry(settings_frame, textvariable=self.var_clip_duration, width=5).grid(row=0, column=5, padx=5, pady=10)


        # Buttons Frame
        btn_frame = tk.Frame(main_container, bg=self.colors['background'])
        btn_frame.pack(pady=10)

        self.btn_files = ttk.Button(
            btn_frame, 
            text="SELECT FILES", 
            style="Material.TButton",
            command=self.select_files
        )
        self.btn_files.grid(row=0, column=0, padx=10)

        self.btn_folder = ttk.Button(
            btn_frame, 
            text="SCAN FOLDER", 
            style="Material.TButton",
            command=self.select_folder
        )
        self.btn_folder.grid(row=0, column=1, padx=10)

        # Progress Section
        progress_frame = tk.Frame(main_container, bg=self.colors['background'])
        progress_frame.pack(fill=tk.X, pady=20)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready",
            font=("Segoe UI", 9),
            bg=self.colors['background'],
            fg=self.colors['text_light'],
            anchor="w"
        )
        self.progress_label.pack(fill=tk.X, pady=(0, 5))

        self.progress = ttk.Progressbar(
            progress_frame, 
            orient=tk.HORIZONTAL, 
            mode='determinate',
            style="Material.Horizontal.TProgressbar"
        )
        self.progress.pack(fill=tk.X)

        # Log Window
        log_frame = tk.Frame(main_container, bg="white", bd=1, relief=tk.SOLID)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=8, 
            state='disabled', 
            font=("Consolas", 9),
            bg="#F5F5F5",
            fg=self.colors['text'],
            borderwidth=0,
            highlightthickness=0
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.is_running = False

    def log(self, message):
        """Thread-safe logging to the text box"""
        self.root.after(0, self._log_internal, message)

    def _log_internal(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        last_line = message.split('\n')[-1]
        if len(last_line) > 60: last_line = last_line[:57] + "..."
        self.progress_label.config(text=last_line)

    def update_progress(self, value):
        self.root.after(0, lambda: self.progress.configure(value=value))

    def lock_ui(self, locked):
        state = 'disabled' if locked else 'normal'
        self.btn_files.config(state=state)
        self.btn_folder.config(state=state)
        # Also lock inputs during processing to prevent errors
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.configure(state=state)

    def get_resized_frame(self, cap, frame_index, target_width):
        """Helper to seek, read, resize and convert a specific frame"""
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if not ret:
            return None
        
        # Calculate new height to maintain aspect ratio
        h, w = frame.shape[:2]
        aspect_ratio = h / w
        target_height = int(target_width * aspect_ratio)
        
        # Resize
        resized = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
        
        # Convert BGR (OpenCV) to RGB (ImageIO/GIF)
        rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        return rgb_frame

    def generate_gif(self, video_path):
        """The core logic to create a preview GIF using OpenCV"""
        cap = None
        try:
            # --- GET SETTINGS FROM UI ---
            try:
                target_width = self.var_width.get()
                num_clips = self.var_num_clips.get()
                clip_duration = self.var_clip_duration.get()
                
                # Basic validation
                if target_width < 50: target_width = 50
                if num_clips < 1: num_clips = 1
                if clip_duration < 0.1: clip_duration = 0.1
            except:
                self.log("--> Error reading settings, using defaults.")
                target_width = 280
                num_clips = 3
                clip_duration = 2.0

            output_path = os.path.splitext(video_path)[0] + ".gif"
            self.log(f"Processing: {os.path.basename(video_path)}")

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                self.log(f"--> Error: Could not open video file.")
                return False

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            if fps <= 0 or total_frames <= 0:
                self.log(f"--> Error: Invalid metadata (fps/frames).")
                return False

            duration = total_frames / fps
            gif_frames = []
            
            # GIF settings
            gif_fps = 8
            
            # --- STRATEGY SELECTION ---
            # Calculate required total time + 20% margin
            required_time = num_clips * clip_duration
            short_video_threshold = required_time * 1.2
            
            if duration < short_video_threshold:
                # SHORT VIDEO: Capture entire video, but downsample to 8 FPS
                step = max(1, int(fps / gif_fps))
                for i in range(0, total_frames, step):
                    frame = self.get_resized_frame(cap, i, target_width)
                    if frame is not None:
                        gif_frames.append(frame)
            else:
                # LONG VIDEO: Random segments
                frames_per_clip = int(gif_fps * clip_duration)
                
                # Calculate segments
                valid_duration = duration - clip_duration
                segment_length = valid_duration / num_clips
                
                step = max(1, int(fps / gif_fps)) # Step to skip source frames

                for i in range(num_clips):
                    # Define the window for this segment
                    seg_start = i * segment_length
                    seg_end = (i + 1) * segment_length
                    
                    # Pick a random start time in this segment
                    t_start = random.uniform(seg_start, seg_end)
                    start_frame = int(t_start * fps)
                    
                    # Capture frames for this specific clip
                    current_frames_grabbed = 0
                    current_read_index = start_frame
                    
                    while current_frames_grabbed < frames_per_clip:
                        if current_read_index >= total_frames:
                            break
                        
                        frame = self.get_resized_frame(cap, current_read_index, target_width)
                        if frame is not None:
                            gif_frames.append(frame)
                            current_frames_grabbed += 1
                        
                        current_read_index += step

            cap.release()

            if gif_frames:
                # Write with optimization
                imageio.mimsave(
                    output_path, 
                    gif_frames, 
                    duration=1/gif_fps, 
                    loop=0, 
                    palettesize=128,
                    quantizer='nq'
                )
                self.log(f"--> Saved: {os.path.basename(output_path)}")
                return True
            else:
                self.log(f"--> Error: No frames extracted.")
                return False

        except Exception as e:
            if cap:
                cap.release()
            self.log(f"--> Error converting {os.path.basename(video_path)}: {str(e)}")
            return False

    def worker_thread(self, file_list):
        self.is_running = True
        total = len(file_list)
        count = 0
        
        self.log(f"--- Started Batch: {total} files ---")
        
        for file_path in file_list:
            self.generate_gif(file_path)
            count += 1
            progress_val = (count / total) * 100
            self.update_progress(progress_val)

        self.log("--- Batch Complete ---")
        self.lock_ui(False)
        self.is_running = False
        messagebox.showinfo("Done", "Processing Complete!")

    def start_processing(self, file_list):
        if not file_list:
            return
        
        self.lock_ui(True)
        self.progress['value'] = 0
        
        # Run in separate thread to keep GUI responsive
        t = threading.Thread(target=self.worker_thread, args=(file_list,))
        t.daemon = True
        t.start()

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select MP4 files", filetypes=[("MP4 Files", "*.mp4")])
        if files:
            self.start_processing(list(files))

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Scan")
        if folder:
            mp4_files = []
            self.log(f"Scanning directory: {folder}...")
            
            # Non-recursive scan (os.listdir)
            try:
                for file in os.listdir(folder):
                    full_path = os.path.join(folder, file)
                    # Check if it's a file and matches extension
                    if os.path.isfile(full_path) and file.lower().endswith(".mp4"):
                        mp4_files.append(full_path)
            except Exception as e:
                self.log(f"Error scanning folder: {e}")
            
            if mp4_files:
                self.log(f"Found {len(mp4_files)} videos.")
                self.start_processing(mp4_files)
            else:
                self.log("No MP4 files found in selected folder.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PreviewGeneratorApp(root)
    root.mainloop()
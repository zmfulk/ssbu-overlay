import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import json
import os
import shutil

# The file that the HTML/JS will read
DATA_FILE = 'data.json'

def update_overlay():
    data = {
        "left": {
            "team": left_team_var.get(),
            "name": left_name_var.get(),
            "score": left_score_var.get(),
            "setWins": left_set_var.get(),
            "bgImage": left_bg_var.get(),
            "logo": left_logo_var.get(),
            "showLogo": left_show_logo_var.get(),
            "color": left_color_var.get()
        },
        "right": {
            "team": right_team_var.get(),
            "name": right_name_var.get(),
            "score": right_score_var.get(),
            "setWins": right_set_var.get(),
            "bgImage": right_bg_var.get(),
            "logo": right_logo_var.get(),
            "showLogo": right_show_logo_var.get(),
            "color": right_color_var.get()
        }
    }
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        
    status_var.set("Overlay Updated Successfully!")
    root.after(3000, lambda: status_var.set(""))

def open_color_modal(color_var, preview_label):
    modal = tk.Toplevel(root)
    modal.title("Select Team Color")
    modal.geometry("300x180")
    modal.transient(root)
    modal.grab_set()
    modal.configure(padx=20, pady=20)

    ttk.Label(modal, text="Enter Hex Code (e.g., #ff6b6b):").pack(anchor=tk.W)
    
    hex_var = tk.StringVar(value=color_var.get())
    hex_entry = ttk.Entry(modal, textvariable=hex_var)
    hex_entry.pack(fill=tk.X, pady=(0, 10))

    def pick_native():
        chosen_color = colorchooser.askcolor(title="Select Team Color", initialcolor=hex_var.get())
        if chosen_color[1]:
            hex_var.set(chosen_color[1])

    ttk.Button(modal, text="Choose from Palette...", command=pick_native).pack(fill=tk.X, pady=(0, 10))

    def apply_color():
        new_color = hex_var.get().strip()
        try:
            preview_label.config(background=new_color)
            color_var.set(new_color)
            modal.destroy()
        except tk.TclError:
            hex_var.set(color_var.get())

    btn_frame = ttk.Frame(modal)
    btn_frame.pack(fill=tk.X, pady=(10, 0))
    ttk.Button(btn_frame, text="Cancel", command=modal.destroy).pack(side=tk.RIGHT, padx=(5, 0))
    ttk.Button(btn_frame, text="Apply", command=apply_color).pack(side=tk.RIGHT)

def browse_file(path_var, side_prefix):
    filepath = filedialog.askopenfilename(
        title="Select Logo Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.webp")]
    )
    if filepath:
        # Create an assets folder in the current directory if it doesn't exist
        os.makedirs("assets", exist_ok=True)
        
        # Copy the file to the assets folder so the browser doesn't block it
        filename = os.path.basename(filepath)
        safe_filename = f"{side_prefix}_{filename}"
        dest_path = os.path.join("assets", safe_filename)
        
        shutil.copy(filepath, dest_path)
        
        # Save as a relative web path with forward slash
        relative_path = f"assets/{safe_filename}"
        path_var.set(relative_path)

# --- GUI Setup ---
root = tk.Tk()
root.title("Smash Bros Ultimate Overlay Controller")
root.geometry("600x650")
root.configure(padx=20, pady=20)

# --- Variables ---
left_team_var = tk.StringVar(value="MANU")
left_name_var = tk.StringVar(value="DR. STANK")
left_score_var = tk.IntVar(value=12)
left_set_var = tk.IntVar(value=0)
left_bg_var = tk.StringVar(value="") 
left_logo_var = tk.StringVar(value="") 
left_show_logo_var = tk.BooleanVar(value=True)
left_color_var = tk.StringVar(value="#ff6b6b")

right_team_var = tk.StringVar(value="PFW")
right_name_var = tk.StringVar(value="ESPURRZ")
right_score_var = tk.IntVar(value=12)
right_set_var = tk.IntVar(value=0)
right_bg_var = tk.StringVar(value="")
right_logo_var = tk.StringVar(value="")
right_show_logo_var = tk.BooleanVar(value=True)
right_color_var = tk.StringVar(value="#4facfe")

status_var = tk.StringVar()

# --- Layout ---
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left Player Column
left_frame = ttk.LabelFrame(main_frame, text="Player 1 (Left)", padding=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

ttk.Label(left_frame, text="Team Color:").pack(anchor=tk.W)
left_color_frame = ttk.Frame(left_frame)
left_color_frame.pack(fill=tk.X, pady=(0, 10))
left_color_preview = tk.Label(left_color_frame, width=3, background=left_color_var.get(), relief="solid")
left_color_preview.pack(side=tk.LEFT, padx=(0, 5))
ttk.Button(left_color_frame, text="Set Color...", command=lambda: open_color_modal(left_color_var, left_color_preview)).pack(side=tk.LEFT)

ttk.Label(left_frame, text="Team Name:").pack(anchor=tk.W)
ttk.Entry(left_frame, textvariable=left_team_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(left_frame, text="Player Name:").pack(anchor=tk.W)
ttk.Entry(left_frame, textvariable=left_name_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(left_frame, text="Stocks (Score):").pack(anchor=tk.W)
ttk.Spinbox(left_frame, from_=0, to=99, textvariable=left_score_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(left_frame, text="Set Wins (0-2):").pack(anchor=tk.W)
ttk.Spinbox(left_frame, from_=0, to=2, textvariable=left_set_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(left_frame, text="Character Image Path/URL:").pack(anchor=tk.W)
ttk.Entry(left_frame, textvariable=left_bg_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(left_frame, text="Logo Setup:").pack(anchor=tk.W)
left_logo_frame = ttk.Frame(left_frame)
left_logo_frame.pack(fill=tk.X)
ttk.Entry(left_logo_frame, textvariable=left_logo_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
ttk.Button(left_logo_frame, text="Browse...", command=lambda: browse_file(left_logo_var, "p1")).pack(side=tk.LEFT)
ttk.Checkbutton(left_frame, text="Show Logo on Overlay", variable=left_show_logo_var).pack(anchor=tk.W, pady=(5, 10))


# Right Player Column
right_frame = ttk.LabelFrame(main_frame, text="Player 2 (Right)", padding=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

ttk.Label(right_frame, text="Team Color:").pack(anchor=tk.W)
right_color_frame = ttk.Frame(right_frame)
right_color_frame.pack(fill=tk.X, pady=(0, 10))
right_color_preview = tk.Label(right_color_frame, width=3, background=right_color_var.get(), relief="solid")
right_color_preview.pack(side=tk.LEFT, padx=(0, 5))
ttk.Button(right_color_frame, text="Set Color...", command=lambda: open_color_modal(right_color_var, right_color_preview)).pack(side=tk.LEFT)

ttk.Label(right_frame, text="Team Name:").pack(anchor=tk.W)
ttk.Entry(right_frame, textvariable=right_team_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(right_frame, text="Player Name:").pack(anchor=tk.W)
ttk.Entry(right_frame, textvariable=right_name_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(right_frame, text="Stocks (Score):").pack(anchor=tk.W)
ttk.Spinbox(right_frame, from_=0, to=99, textvariable=right_score_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(right_frame, text="Set Wins (0-2):").pack(anchor=tk.W)
ttk.Spinbox(right_frame, from_=0, to=2, textvariable=right_set_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(right_frame, text="Character Image Path/URL:").pack(anchor=tk.W)
ttk.Entry(right_frame, textvariable=right_bg_var).pack(fill=tk.X, pady=(0, 10))

ttk.Label(right_frame, text="Logo Setup:").pack(anchor=tk.W)
right_logo_frame = ttk.Frame(right_frame)
right_logo_frame.pack(fill=tk.X)
ttk.Entry(right_logo_frame, textvariable=right_logo_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
ttk.Button(right_logo_frame, text="Browse...", command=lambda: browse_file(right_logo_var, "p2")).pack(side=tk.LEFT)
ttk.Checkbutton(right_frame, text="Show Logo on Overlay", variable=right_show_logo_var).pack(anchor=tk.W, pady=(5, 10))

# Bottom Actions
action_frame = ttk.Frame(root, padding=10)
action_frame.pack(fill=tk.X, side=tk.BOTTOM)

update_btn = ttk.Button(action_frame, text="Update Overlay", command=update_overlay)
update_btn.pack(pady=5)

status_label = ttk.Label(action_frame, textvariable=status_var, foreground="green")
status_label.pack()

update_overlay()
root.mainloop()
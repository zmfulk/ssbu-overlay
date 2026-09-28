import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import json
import os
import shutil

DATA_FILE = 'data.json'

SMASH_CHARACTERS = {
    "None (Clear)": "",
    "Mario": "mario", "Donkey Kong": "donkey_kong", "Link": "link", "Samus": "samus", 
    "Dark Samus": "dark_samus", "Yoshi": "yoshi", "Kirby": "kirby", "Fox": "fox", 
    "Pikachu": "pikachu", "Luigi": "luigi", "Ness": "ness", "Captain Falcon": "captain_falcon", 
    "Jigglypuff": "jigglypuff", "Peach": "peach", "Daisy": "daisy", "Bowser": "bowser", 
    "Ice Climbers": "ice_climbers", "Sheik": "sheik", "Zelda": "zelda", "Dr. Mario": "dr_mario", 
    "Pichu": "pichu", "Falco": "falco", "Marth": "marth", "Lucina": "lucina", 
    "Young Link": "young_link", "Ganondorf": "ganondorf", "Mewtwo": "mewtwo", "Roy": "roy", 
    "Chrom": "chrom", "Mr. Game & Watch": "mr_game_and_watch", "Meta Knight": "meta_knight", 
    "Pit": "pit", "Dark Pit": "dark_pit", "Zero Suit Samus": "zero_suit_samus", "Wario": "wario", 
    "Snake": "snake", "Ike": "ike", "Pokemon Trainer": "pokemon_trainer", "Diddy Kong": "diddy_kong", 
    "Lucas": "lucas", "Sonic": "sonic", "King Dedede": "king_dedede", "Olimar": "olimar", 
    "Lucario": "lucario", "R.O.B.": "rob", "Toon Link": "toon_link", "Wolf": "wolf", 
    "Villager": "villager", "Mega Man": "mega_man", "Wii Fit Trainer": "wii_fit_trainer", 
    "Rosalina & Luma": "rosalina_and_luma", "Little Mac": "little_mac", "Greninja": "greninja", 
    "Mii Brawler": "mii_brawler", "Mii Swordfighter": "mii_swordfighter", "Mii Gunner": "mii_gunner", 
    "Palutena": "palutena", "Pac-Man": "pac_man", "Robin": "robin", "Shulk": "shulk", 
    "Bowser Jr.": "bowser_jr", "Duck Hunt": "duck_hunt", "Ryu": "ryu", "Ken": "ken", 
    "Cloud": "cloud", "Corrin": "corrin", "Bayonetta": "bayonetta", "Inkling": "inkling", 
    "Ridley": "ridley", "Simon": "simon", "Richter": "richter", "King K. Rool": "king_k_rool", 
    "Isabelle": "isabelle", "Incineroar": "incineroar", "Piranha Plant": "piranha_plant", 
    "Joker": "joker", "Hero": "hero", "Banjo & Kazooie": "banjo_and_kazooie", "Terry": "terry", 
    "Byleth": "byleth", "Min Min": "minmin", "Steve": "steve", "Sephiroth": "sephiroth", 
    "Pyra": "pyra", "Mythra": "mythra", "Kazuya": "kazuya", "Sora": "sora"
}

def load_saved_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return None

def update_overlay(silent=False):
    try:
        data = {
            "league": league_var.get(),
            "seriesText": series_var.get(),
            "left": {
                "team": left_team_var.get(),
                "name": left_name_var.get(),
                "score": left_score_var.get(),
                "setWins": left_set_var.get(),
                "bgImage": left_bg_var.get(),
                "bgOffsetY": left_offset_var.get(),
                "bgZoom": left_zoom_var.get(),
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
                "bgOffsetY": right_offset_var.get(),
                "bgZoom": right_zoom_var.get(),
                "logo": right_logo_var.get(),
                "showLogo": right_show_logo_var.get(),
                "color": right_color_var.get()
            }
        }
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
            
        if not silent:
            status_var.set("Overlay Updated Successfully!")
            root.after(3000, lambda: status_var.set(""))
    except Exception:
        pass 

def auto_update_score(*args):
    update_overlay(silent=True)

def apply_character(side):
    """Sets the background image URL based ONLY on a dropdown selection or enter key."""
    if side == "left":
        char_name = left_char_var.get()
        match = next((c for c in SMASH_CHARACTERS.keys() if c.lower() == char_name.lower()), None)
        if match == "None (Clear)":
            left_bg_var.set("")
            left_char_var.set("")
        elif match:
            slug = SMASH_CHARACTERS[match]
            left_bg_var.set(f"https://www.smashbros.com/assets_v2/img/fighter/{slug}/main.png")
            left_char_var.set(match)
        left_char_cb.event_generate('<Escape>') 
        
        left_offset_var.set(20)
        left_zoom_var.set(100)
    else:
        char_name = right_char_var.get()
        match = next((c for c in SMASH_CHARACTERS.keys() if c.lower() == char_name.lower()), None)
        if match == "None (Clear)":
            right_bg_var.set("")
            right_char_var.set("")
        elif match:
            slug = SMASH_CHARACTERS[match]
            right_bg_var.set(f"https://www.smashbros.com/assets_v2/img/fighter/{slug}/main.png")
            right_char_var.set(match) 
        right_char_cb.event_generate('<Escape>') 
        
        right_offset_var.set(20)
        right_zoom_var.set(100)
    
    update_overlay(silent=True)

def filter_chars(event, cb, var):
    """Filters the dropdown list safely."""
    if event.keysym in ('Up', 'Down', 'Return', 'Left', 'Right', 'Tab', 'Escape'):
        return
        
    typed = var.get()
    if typed == '':
        cb['values'] = char_list
    else:
        cb['values'] = [c for c in char_list if typed.lower() in c.lower()]

def swap_sides():
    temp_team = left_team_var.get()
    left_team_var.set(right_team_var.get())
    right_team_var.set(temp_team)

    temp_name = left_name_var.get()
    left_name_var.set(right_name_var.get())
    right_name_var.set(temp_name)

    temp_score = left_score_var.get()
    left_score_var.set(right_score_var.get())
    right_score_var.set(temp_score)

    temp_set = left_set_var.get()
    left_set_var.set(right_set_var.get())
    right_set_var.set(temp_set)

    temp_bg = left_bg_var.get()
    left_bg_var.set(right_bg_var.get())
    right_bg_var.set(temp_bg)
    
    temp_offset = left_offset_var.get()
    left_offset_var.set(right_offset_var.get())
    right_offset_var.set(temp_offset)

    temp_zoom = left_zoom_var.get()
    left_zoom_var.set(right_zoom_var.get())
    right_zoom_var.set(temp_zoom)

    temp_logo = left_logo_var.get()
    left_logo_var.set(right_logo_var.get())
    right_logo_var.set(temp_logo)

    temp_show = left_show_logo_var.get()
    left_show_logo_var.set(right_show_logo_var.get())
    right_show_logo_var.set(temp_show)

    temp_color = left_color_var.get()
    left_color_var.set(right_color_var.get())
    right_color_var.set(temp_color)

    left_color_preview.config(background=left_color_var.get())
    right_color_preview.config(background=right_color_var.get())
    
    temp_char = left_char_var.get()
    left_char_var.set(right_char_var.get())
    right_char_var.set(temp_char)

    update_overlay()
    status_var.set("Sides Swapped!")
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

def browse_file(path_var, prefix):
    filepath = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.webp")]
    )
    if filepath:
        os.makedirs("assets", exist_ok=True)
        filename = os.path.basename(filepath)
        safe_filename = f"{prefix}_{filename}"
        dest_path = os.path.join("assets", safe_filename)
        
        shutil.copy(filepath, dest_path)
        relative_path = f"assets/{safe_filename}"
        path_var.set(relative_path)
        update_overlay(silent=True) 

saved_data = load_saved_data()

l_off = saved_data["left"].get("bgOffsetY", 20) if saved_data and "bgOffsetY" in saved_data["left"] else 20
l_zm = saved_data["left"].get("bgZoom", 100) if saved_data and "bgZoom" in saved_data["left"] else 100
r_off = saved_data["right"].get("bgOffsetY", 20) if saved_data and "bgOffsetY" in saved_data["right"] else 20
r_zm = saved_data["right"].get("bgZoom", 100) if saved_data and "bgZoom" in saved_data["right"] else 100
league_val = saved_data.get("league", "NACE") if saved_data else "NACE"
series_val = saved_data.get("seriesText", "BEST OF 3") if saved_data else "BEST OF 3"

# --- GUI Setup ---
root = tk.Tk()
root.title("Smash Bros Ultimate Overlay Controller")
root.geometry("700x750") 
root.configure(padx=20, pady=20)

# --- Variables ---
league_var = tk.StringVar(value=league_val)
league_var.trace_add("write", auto_update_score)

series_var = tk.StringVar(value=series_val)
series_var.trace_add("write", auto_update_score)

left_team_var = tk.StringVar(value=saved_data["left"]["team"] if saved_data else "MANU")
left_name_var = tk.StringVar(value=saved_data["left"]["name"] if saved_data else "DR. STANK")
left_score_var = tk.IntVar(value=saved_data["left"]["score"] if saved_data else 0)
left_set_var = tk.IntVar(value=saved_data["left"]["setWins"] if saved_data else 0)
left_bg_var = tk.StringVar(value=saved_data["left"]["bgImage"] if saved_data else "") 
left_char_var = tk.StringVar(value="")
left_offset_var = tk.IntVar(value=l_off)
left_zoom_var = tk.IntVar(value=l_zm)
left_logo_var = tk.StringVar(value=saved_data["left"]["logo"] if saved_data else "") 
left_show_logo_var = tk.BooleanVar(value=saved_data["left"]["showLogo"] if saved_data else True)
left_color_var = tk.StringVar(value=saved_data["left"]["color"] if saved_data else "#ff6b6b")

right_team_var = tk.StringVar(value=saved_data["right"]["team"] if saved_data else "PFW")
right_name_var = tk.StringVar(value=saved_data["right"]["name"] if saved_data else "ESPURRZ")
right_score_var = tk.IntVar(value=saved_data["right"]["score"] if saved_data else 0)
right_set_var = tk.IntVar(value=saved_data["right"]["setWins"] if saved_data else 0)
right_bg_var = tk.StringVar(value=saved_data["right"]["bgImage"] if saved_data else "")
right_char_var = tk.StringVar(value="")
right_offset_var = tk.IntVar(value=r_off)
right_zoom_var = tk.IntVar(value=r_zm)
right_logo_var = tk.StringVar(value=saved_data["right"]["logo"] if saved_data else "")
right_show_logo_var = tk.BooleanVar(value=saved_data["right"]["showLogo"] if saved_data else True)
right_color_var = tk.StringVar(value=saved_data["right"]["color"] if saved_data else "#4facfe")

left_score_var.trace_add("write", auto_update_score)
right_score_var.trace_add("write", auto_update_score)
left_offset_var.trace_add("write", auto_update_score)
left_zoom_var.trace_add("write", auto_update_score)
right_offset_var.trace_add("write", auto_update_score)
right_zoom_var.trace_add("write", auto_update_score)

status_var = tk.StringVar()

# --- Layout ---
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

all_chars = list(SMASH_CHARACTERS.keys())
all_chars.remove("None (Clear)")
all_chars.sort()
char_list = ["None (Clear)"] + all_chars

# ================= PLAYER 1 (LEFT) =================
left_frame = ttk.LabelFrame(main_frame, text="Player 1 (Left)", padding=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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

ttk.Label(left_frame, text="Search/Select Character:").pack(anchor=tk.W)
left_char_cb = ttk.Combobox(left_frame, textvariable=left_char_var, values=char_list)
left_char_cb.pack(fill=tk.X, pady=(0, 5))
left_char_cb.bind('<KeyRelease>', lambda e: filter_chars(e, left_char_cb, left_char_var))
left_char_cb.bind("<<ComboboxSelected>>", lambda e: apply_character("left"))
left_char_cb.bind("<Return>", lambda e: apply_character("left"))

ttk.Label(left_frame, text="Background Framing:").pack(anchor=tk.W)
left_framing_frame = ttk.Frame(left_frame)
left_framing_frame.pack(fill=tk.X, pady=(0, 5))
ttk.Spinbox(left_framing_frame, from_=-50, to=150, textvariable=left_offset_var, width=5).pack(side=tk.LEFT)
ttk.Label(left_framing_frame, text="% Y-Offset").pack(side=tk.LEFT, padx=(5, 10))
ttk.Spinbox(left_framing_frame, from_=50, to=300, textvariable=left_zoom_var, width=5).pack(side=tk.LEFT)
ttk.Label(left_framing_frame, text="% Zoom").pack(side=tk.LEFT, padx=(5, 0))

ttk.Label(left_frame, text="Custom Splash Path/URL:").pack(anchor=tk.W)
left_bg_frame = ttk.Frame(left_frame)
left_bg_frame.pack(fill=tk.X, pady=(0, 10))
ttk.Entry(left_bg_frame, textvariable=left_bg_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
ttk.Button(left_bg_frame, text="Browse...", command=lambda: browse_file(left_bg_var, "p1_bg")).pack(side=tk.LEFT)

ttk.Label(left_frame, text="Logo Setup:").pack(anchor=tk.W)
left_logo_frame = ttk.Frame(left_frame)
left_logo_frame.pack(fill=tk.X)
ttk.Entry(left_logo_frame, textvariable=left_logo_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
ttk.Button(left_logo_frame, text="Browse...", command=lambda: browse_file(left_logo_var, "p1_logo")).pack(side=tk.LEFT)
ttk.Checkbutton(left_frame, text="Show Logo on Overlay", variable=left_show_logo_var).pack(anchor=tk.W, pady=(5, 10))


# ================= MIDDLE COLUMN =================
middle_frame = ttk.Frame(main_frame, padding=10)
middle_frame.pack(side=tk.LEFT, fill=tk.Y)

# LEAGUE DROPDOWN
ttk.Label(middle_frame, text="League:").pack(pady=(0, 5))
league_cb = ttk.Combobox(middle_frame, textvariable=league_var, values=["NACE", "GLEC", "Scrim"], width=13)
league_cb.pack(pady=(0, 10))

# SERIES LABEL TEXT (NEW)
ttk.Label(middle_frame, text="Series Label:").pack(pady=(0, 5))
ttk.Entry(middle_frame, textvariable=series_var, width=15).pack(pady=(0, 20))

swap_btn = ttk.Button(middle_frame, text="⇄\nSwap\nSides", command=swap_sides)
swap_btn.pack(expand=True)


# ================= PLAYER 2 (RIGHT) =================
right_frame = ttk.LabelFrame(main_frame, text="Player 2 (Right)", padding=10)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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

ttk.Label(right_frame, text="Search/Select Character:").pack(anchor=tk.W)
right_char_cb = ttk.Combobox(right_frame, textvariable=right_char_var, values=char_list)
right_char_cb.pack(fill=tk.X, pady=(0, 5))
right_char_cb.bind('<KeyRelease>', lambda e: filter_chars(e, right_char_cb, right_char_var))
right_char_cb.bind("<<ComboboxSelected>>", lambda e: apply_character("right"))
right_char_cb.bind("<Return>", lambda e: apply_character("right"))

ttk.Label(right_frame, text="Background Framing:").pack(anchor=tk.W)
right_framing_frame = ttk.Frame(right_frame)
right_framing_frame.pack(fill=tk.X, pady=(0, 5))
ttk.Spinbox(right_framing_frame, from_=-50, to=150, textvariable=right_offset_var, width=5).pack(side=tk.LEFT)
ttk.Label(right_framing_frame, text="% Y-Offset").pack(side=tk.LEFT, padx=(5, 10))
ttk.Spinbox(right_framing_frame, from_=50, to=300, textvariable=right_zoom_var, width=5).pack(side=tk.LEFT)
ttk.Label(right_framing_frame, text="% Zoom").pack(side=tk.LEFT, padx=(5, 0))

ttk.Label(right_frame, text="Custom Splash Path/URL:").pack(anchor=tk.W)
right_bg_frame = ttk.Frame(right_frame)
right_bg_frame.pack(fill=tk.X, pady=(0, 10))
ttk.Entry(right_bg_frame, textvariable=right_bg_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
ttk.Button(right_bg_frame, text="Browse...", command=lambda: browse_file(right_bg_var, "p2_bg")).pack(side=tk.LEFT)

ttk.Label(right_frame, text="Logo Setup:").pack(anchor=tk.W)
right_logo_frame = ttk.Frame(right_frame)
right_logo_frame.pack(fill=tk.X)
ttk.Entry(right_logo_frame, textvariable=right_logo_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
ttk.Button(right_logo_frame, text="Browse...", command=lambda: browse_file(right_logo_var, "p2_logo")).pack(side=tk.LEFT)
ttk.Checkbutton(right_frame, text="Show Logo on Overlay", variable=right_show_logo_var).pack(anchor=tk.W, pady=(5, 10))

# Bottom Actions
action_frame = ttk.Frame(root, padding=10)
action_frame.pack(fill=tk.X, side=tk.BOTTOM)

update_btn = ttk.Button(action_frame, text="Force Full Update", command=update_overlay)
update_btn.pack(pady=5)

status_label = ttk.Label(action_frame, textvariable=status_var, foreground="green")
status_label.pack()

root.mainloop()
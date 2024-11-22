import tkinter as tk
from tkinter import ttk
import asyncio

class TTSAppGUI:
    """Handles the GUI for the TTS application."""

    def __init__(self, root, on_speak_button, on_play_button, tts):
        self.root = root
        self.on_speak_button = on_speak_button
        self.on_play_button = on_play_button
        self.tts = tts  # Reference to TTS instance
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI elements."""
        self.root.title("TTS")

        # Text input
        tk.Label(self.root, text="Enter Text:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.text_entry = tk.Text(self.root, height=5, width=40)
        self.text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Speed control
        tk.Label(self.root, text="Speed (%):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.speed_scale = tk.Scale(self.root, from_=-100, to=100, orient="horizontal")
        self.speed_scale.set(0)  # Default value
        self.speed_scale.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Pitch control
        tk.Label(self.root, text="Pitch (%):").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.pitch_scale = tk.Scale(self.root, from_=-100, to=100, orient="horizontal")
        self.pitch_scale.set(0)  # Default value
        self.pitch_scale.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Volume control
        tk.Label(self.root, text="Volume (%):").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient="horizontal")
        self.volume_scale.set(100)  # Default value
        self.volume_scale.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        # Speak button
        speak_button = tk.Button(self.root, text="Speak", command=self.on_speak_button)
        speak_button.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        # Play button
        play_button = tk.Button(self.root, text="Play", command=self.on_play_button)
        play_button.grid(row=1, column=3, columnspan=2, padx=10, pady=10)
        
        # Voice selection
        tk.Label(self.root, text="Voice:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.voice_selector = ttk.Combobox(self.root)
        self.voice_selector.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Gender Dropdown
        tk.Label(self.root, text="Gender").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(self.root, textvariable=self.gender_var, values=["All"])
        self.gender_dropdown.set("All")
        self.gender_dropdown.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Language Dropdown
        tk.Label(self.root, text="Language").grid(row=6, column=2, padx=10, pady=5, sticky="w")
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self.root, textvariable=self.language_var, values=["All"])
        self.language_dropdown.set("All")
        self.language_dropdown.grid(row=6, column=3, padx=10, pady=5, sticky="w")
        
        # Content Categories label
        self.content_category_label = tk.Label(self.root, text="Content Categories").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.content_category_checkbuttons = []

        # Voice Personalities label
        self.voice_personality_label = None
        self.voice_personality_checkbuttons = []
        
        self.language_dropdown.bind("<<ComboboxSelected>>", lambda e: self.tts.apply_filters(self))
        self.gender_dropdown.bind("<<ComboboxSelected>>", lambda e: self.tts.apply_filters(self))

        # Initialize voices and filters
        asyncio.run(self.tts.update_voices(self, initial=True))

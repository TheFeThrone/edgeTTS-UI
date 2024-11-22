import edge_tts
import asyncio
from audio_player import AudioPlayer
import tkinter as tk

class TTS:
    """Handles text-to-speech functionality."""

    def __init__(self):
        self.audio_player = AudioPlayer()
        self.voices = {}

    async def get_available_voices(self):
        """Fetch available voices from EdgeTTS."""
        voices_manager = await edge_tts.VoicesManager.create()

        voices = {
            voice["FriendlyName"].replace("Multilingual", "").replace("Online ", "").replace("(Natural) ", "").replace("Microsoft", "").strip(): voice
            for voice in voices_manager.voices
        }

        return voices

    async def update_voices(self, gui, gender=None, language=None, content_categories=None, voice_personalities=None, initial=False):
        """Fetch available voices and update the GUI dropdown based on selected filters."""
        voices = await self.get_available_voices()

        # Filter voices based on selections
        filtered_voices = {}
        for voice_name, voice_data in voices.items():
            match = True

            # Gender filter
            if gender and voice_data['Gender'] != gender:
                match = False
            # Language filter
            if language and voice_data['Language'] != language:
                match = False
            # Content Categories filter
            if content_categories and not any(cat in voice_data['VoiceTag']['ContentCategories'] for cat in content_categories):
                match = False
            # Voice Personalities filter
            if voice_personalities and not any(personality in voice_data['VoiceTag']['VoicePersonalities'] for personality in voice_personalities):
                match = False

            if match:
                filtered_voices[voice_name] = voice_data

        # Update the GUI with filtered voices
        gui.root.after(0, self._update_gui_voices, filtered_voices, gui)

        if initial:
            # Update the dropdowns and categories based on the filtered voices
            gui.root.after(0, self._update_gui_filters, filtered_voices, gui)

    def _update_gui_voices(self, voices, gui):
        """Update the GUI ComboBox with the available voices."""
        voice_names = list(voices.keys())
        gui.voice_selector['values'] = voice_names
        if voice_names:
            gui.voice_selector.set("Select a voice")  # Default value
        self.voices = voices

    def _update_gui_filters(self, voices, gui):
        """Update the dropdowns for gender, language, and dynamically arrange checkbuttons for categories and personalities."""
        # Get unique values for filters
        genders = sorted(set(voice['Gender'] for voice in voices.values()))
        languages = sorted(set(voice['Language'] for voice in voices.values()))
        content_categories = sorted(set(category for voice in voices.values() for category in voice['VoiceTag']['ContentCategories']))
        voice_personalities = sorted(set(personality for voice in voices.values() for personality in voice['VoiceTag']['VoicePersonalities']))

        # Update the Gender dropdown
        gui.gender_var.set("All")
        gui.gender_dropdown['values'] = ["All"] + genders

        # Update the Language dropdown
        gui.language_var.set("All")
        gui.language_dropdown['values'] = ["All"] + languages

        # Dynamically add content category checkbuttons
        for cb in gui.content_category_checkbuttons:
            cb.grid_forget()  # Remove old checkbuttons from the grid

        category_row = 8
        current_row = category_row
        gui.content_category_checkbuttons = []
        for i, category in enumerate(content_categories):
            row = category_row  # Starting row for content categories
            column = 1 + (i % 3)  # Limit to 3 columns per row
            current_row = row + (i // 3)  # Calculate the row dynamically
            cb_var = tk.BooleanVar()
            cb = tk.Checkbutton(gui.root, text=category, variable=cb_var, command=lambda: self.apply_filters(gui))
            cb.variable = cb_var
            cb.grid(row=current_row, column=column, padx=10, pady=5, sticky="w")
            gui.content_category_checkbuttons.append(cb)

        personality_row = current_row+1
        gui.voice_personality = tk.Label(gui.root, text="Voice Personalities").grid(row=personality_row, column=0, padx=10, pady=5, sticky="w")
        # Dynamically add voice personality checkbuttons
        for cb in gui.voice_personality_checkbuttons:
            cb.grid_forget()  # Remove old checkbuttons from the grid

        gui.voice_personality_checkbuttons = []
        for i, personality in enumerate(voice_personalities):
            row = personality_row  # Starting row for voice personalities (below content categories)
            column = 1 + (i % 3)  # Limit to 3 columns per row
            current_row = row + (i // 3)  # Calculate the row dynamically
            cb_var = tk.BooleanVar()
            cb = tk.Checkbutton(gui.root, text=personality, variable=cb_var, command=lambda: self.apply_filters(gui))
            cb.variable = cb_var
            cb.grid(row=current_row, column=column, padx=10, pady=5, sticky="w")
            gui.voice_personality_checkbuttons.append(cb)

    def apply_filters(self, gui, event=None):
        """Apply filters based on selected dropdowns and checkboxes."""
        selected_gender = gui.gender_var.get() if gui.gender_var.get() != "All" else None
        selected_language = gui.language_var.get() if gui.language_var.get() != "All" else None

        selected_content_categories = [
            cb.cget("text") for cb in gui.content_category_checkbuttons if cb.variable.get()
        ]
        selected_voice_personalities = [
            cb.cget("text") for cb in gui.voice_personality_checkbuttons if cb.variable.get()
        ]

        # Update voices based on filters
        asyncio.run(self.update_voices(
            gui,
            gender=selected_gender,
            language=selected_language,
            content_categories=selected_content_categories or None,
            voice_personalities=selected_voice_personalities or None,
        ))


    async def speak_text(self, text, selected_voice, rate, pitch, volume):
        """Speak the provided text with the selected settings."""
        voice_settings = self.voices[selected_voice]
        rate = f"{'+' if not rate.startswith(('-', '+')) else ''}{rate}"
        pitch = f"{'+' if not pitch.startswith(('-', '+')) else ''}{pitch}"
        
        communicator = edge_tts.Communicate(
            text,
            voice_settings["ShortName"],
            pitch=pitch,
            rate=rate,
        )

        self.audio_player.stop_audio()
        # Save speech to a file (output.mp3)
        await communicator.save("output.mp3")
        print("Speech saved as output.mp3")

        # Play the audio
        self.audio_player.play_audio("output.mp3", volume)

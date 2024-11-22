import tkinter as tk
from tts import TTS
from gui import TTSAppGUI
import asyncio

def main():
    # Initialize Tkinter window
    root = tk.Tk()

    # Create TTS instance
    tts = TTS()

    # Define callback functions for speak and play buttons
    def on_speak_button():
        text = gui.text_entry.get("1.0", tk.END).strip()
        selected_voice = gui.voice_selector.get()
        rate = f"{gui.speed_scale.get()}%"
        pitch = f"{gui.pitch_scale.get()}Hz"
        volume = gui.volume_scale.get()
        asyncio.run(tts.speak_text(text, selected_voice, rate, pitch, volume))

    def on_play_button():
        tts.audio_player.play_audio("output.mp3", gui.volume_scale.get())

    # Create GUI instance
    gui = TTSAppGUI(root, on_speak_button, on_play_button, tts)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()

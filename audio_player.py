import pygame  # For audio playback
import os  # For file handling
import threading  # For running audio playback in a separate thread

# Initialize the pygame mixer
pygame.mixer.init()

class AudioPlayer:
    """Handles the audio playback logic including volume control."""

    def __init__(self):
        self._stop_event = threading.Event()

    def stop_audio(self):
        """Stop any currently playing audio."""
        self._stop_event.set()  # Signal playback to stop
        pygame.mixer.music.stop()
        self._unload_audio()

    def play_audio(self, audio_file, volume):
        """Play the provided audio file with the given volume in a separate thread."""
        if os.path.exists(audio_file):
            self._stop_event.clear()  # Reset stop event for new playback
            threading.Thread(target=self._play, args=(audio_file, volume), daemon=True).start()
        else:
            print("Audio file not found.")

    def set_volume(self, volume):
        """Set the volume while playing the audio."""
        pygame.mixer.music.set_volume(volume / 100.0)

    def _play(self, audio_file, volume):
        """Handle the playback logic in a thread-safe way."""
        try:
            self._load_audio(audio_file, volume)
            self._wait_until_finished()
            self._unload_audio()
        except Exception as e:
            print(f"Error during audio playback: {e}")

    def _load_audio(self, audio_file, volume):
        """Load the audio file and set the volume."""
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.set_volume(volume / 100.0)
        pygame.mixer.music.play()
        print(f"Playing audio from {audio_file}")

    def _unload_audio(self):
        """Unload the audio file to release the file lock."""
        pygame.mixer.music.unload()
        print("Audio playback finished. Resources released.")

    def _wait_until_finished(self):
        """Wait until the playback finishes or is stopped."""
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            if self._stop_event.is_set():
                break
            clock.tick(10)  # Check 10 times per second

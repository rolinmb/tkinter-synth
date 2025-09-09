import tkinter as tk
import numpy as np
import sounddevice as sd

# Global settings
SAMPLE_RATE = 44100
current_stream = None
current_note = None

# Note frequency mapping
key_to_note = {
    'q': ("C4", 261.63),
    '2': ("C#4/Db4", 277.18),
    'w': ("D4", 293.66),
    '3': ("D#4/Eb4", 311.13),
    'e': ("E4", 329.62),
    'r': ("F4", 349.23),
    '5': ("F#4/Gb4", 369.99),
    't': ("G4", 392.0),
    '6': ("G#4/Ab4", 415.30),
    'y': ("A4", 440.0),
    '7': ("A#4/Bb4", 466.16),
    'u': ("B4", 493.88),
    'i': ("C5", 523.25),
}

def sine_wave(frequency, duration=1.0, amplitude=0.5):
    """Generate a sine wave as numpy array."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave.astype(np.float32)

def play_note(note, freq):
    """Play a note continuously using a stream."""
    global current_stream, current_note
    current_note = note

    def callback(outdata, frames, time, status):
        t = (np.arange(frames) + callback.start) / SAMPLE_RATE
        outdata[:, 0] = 0.5 * np.sin(2 * np.pi * freq * t)
        callback.start += frames

    callback.start = 0

    if current_stream is not None:
        current_stream.stop()
        current_stream.close()

    current_stream = sd.OutputStream(
        channels=1,
        callback=callback,
        samplerate=SAMPLE_RATE
    )
    current_stream.start()

def stop_note():
    """Stop playing the current note."""
    global current_stream, current_note
    if current_stream is not None:
        current_stream.stop()
        current_stream.close()
        current_stream = None
    current_note = None
    note_label.config(text="Note: None")

def key_pressed(event):
    key = event.keysym.lower()
    if key in key_to_note:
        note, freq = key_to_note[key]
        note_label.config(text=f"Note: {note} (Key: {key.upper()})")
        play_note(note, freq)

def key_released(event):
    stop_note()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("tkinter-synth")

    info_label = tk.Label(root, text="Press 'A' for C4, 'I' for C5", font=("Arial", 14))
    info_label.pack(pady=10)

    note_label = tk.Label(root, text="Note: None", font=("Arial", 18), fg="blue")
    note_label.pack(pady=20)

    root.bind("<KeyPress>", key_pressed)
    root.bind("<KeyRelease>", key_released)

    root.mainloop()

import tkinter as tk
from tkinter import ttk
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class OrganSynth:
    def __init__(self, root):
        self.root = root
        self.root.title("Organ Synthesizer")

        # Synthesizer settings
        self.volume = 0.5  # Volume (0.0 to 1.0)
        self.sample_rate = 44100  # Sample rate in Hz

        # Frequencies for the 7 Swaras
        self.swaras = {
            "Sa": 261.63,  # C4
            "Re": 293.66,  # D4
            "Ga": 329.63,  # E4
            "Ma": 349.23,  # F4
            "Pa": 392.00,  # G4
            "Dha": 440.00,  # A4
            "Ni": 493.88   # B4
        }

        # Create GUI elements
        self.create_widgets()
        
        # Setup matplotlib figure and axes
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, 1)
        self.ax.grid()
        
        # Start animation
        self.ani = FuncAnimation(self.fig, self.update_plot, blit=True, interval=50)

    def create_widgets(self):
        # Volume Knob
        self.volume_label = ttk.Label(self.root, text="Volume")
        self.volume_label.pack()
        self.volume_scale = ttk.Scale(self.root, from_=0, to=1, orient='horizontal', command=self.update_volume)
        self.volume_scale.set(self.volume)
        self.volume_scale.pack()

        # Swara Buttons
        for swara, freq in self.swaras.items():
            button = ttk.Button(self.root, text=swara, command=lambda f=freq: self.play_swara(f))
            button.pack()

        # Stop Button
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_sound)
        self.stop_button.pack()

    def update_volume(self, value):
        try:
            self.volume = float(value)
        except ValueError:
            self.volume = 0.5  # Default to 0.5 if invalid input

    def generate_waveform(self, freq):
        t = np.linspace(0, 1, int(self.sample_rate), endpoint=False)
        return self.volume * np.sin(2 * np.pi * freq * t)

    def play_swara(self, freq):
        self.stop_sound()  # Ensure any existing stream is stopped before starting a new one
        self.waveform = self.generate_waveform(freq)
        try:
            self.stream = sd.OutputStream(callback=self.audio_callback, samplerate=self.sample_rate, channels=1)
            self.stream.start()
        except Exception as e:
            print(f"Error starting audio stream: {e}")

    def stop_sound(self):
        if hasattr(self, 'stream') and self.stream.active:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                print(f"Error stopping audio stream: {e}")

    def audio_callback(self, outdata, frames, time, status):
        if status:
            print(f"Audio stream status: {status}")
        outdata[:frames] = self.waveform[:frames].reshape(-1, 1)

    def update_plot(self, frame):
        if hasattr(self, 'waveform'):
            self.line.set_data(np.linspace(0, 1, len(self.waveform)), self.waveform)
        return self.line,

    def on_closing(self):
        self.stop_sound()
        plt.close(self.fig)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrganSynth(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Run the tkinter mainloop in a separate thread
    from threading import Thread
    Thread(target=root.mainloop).start()
    
    # Show the matplotlib plot
    plt.show()
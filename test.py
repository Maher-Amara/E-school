# import pyaudio
# import wave
# import time
# import sys
#
# wf = wave.open('Hate me.wav', 'rb')
#
# # instantiate PyAudio (1)
# p = pyaudio.PyAudio()
#
# # define callback (2)
# def callback(in_data, frame_count, time_info, status):
#     data = wf.readframes(frame_count)
#     return (data, pyaudio.paContinue)
#
# # open stream using callback (3)
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True,
#                 stream_callback=callback)
#
# # start the stream (4)
# stream.start_stream()
#
# # wait for stream to finish (5)
# while stream.is_active():
#     time.sleep(0.1)
#
# # stop stream (6)
# stream.stop_stream()
# stream.close()
# wf.close()
#
# # close PyAudio (7)
# p.terminate()

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

mygreen = "#d2ffd2"
myred = "#dd0202"

style = ttk.Style()

style.theme_create( "yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": mygreen },
            "map":       {"background": [("selected", myred)],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )

style.theme_use("yummy")

note = ttk.Notebook(root)
f1 = ttk.Frame(note, width=300, height=200)
note.add(f1, text = 'First')
f2 = ttk.Frame(note, width=300, height=200)
note.add(f2, text = 'Second')
note.pack(expand=1, fill='both', padx=5, pady=5)

tk.Button(root, text='yummy!').pack(fill='x')

root.mainloop()
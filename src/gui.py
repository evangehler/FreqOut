import tkinter as tk
from tkinter import filedialog as fd, scrolledtext
from tkinter import ttk
import sys

# Class for Console Output
class ConsoleRedirect:
    def __init__(self, text_widget, original_stream):
        self.text_widget = text_widget
        self.original_stream = original_stream

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.original_stream.write(message)

    def flush(self):
        self.original_stream.flush()
# Main GUI
class GUI:
    message = None
    inFile = None
    outFile = None
    callback = None

    def __init__(self):
        
        # Window Size / Config
        self.root = tk.Tk()
        self.root.geometry('1000x800')
        self.root.title("FreqOut")
        self.root.configure(background='dark green')
        
        # Style
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TLabel', background='dark green', foreground='silver', font=('Impact', 16))
        style.configure('TButton', font=('Arial', 12), padding=5)
        style.configure('TEntry', font=('Courier New', 12))

        # Title
        self.title = ttk.Label(self.root, text="FreqOut", font=("Impact", 64))
        self.title.pack(padx=30, pady=30)
        
        # Message input
        self.messageInstr = ttk.Label(self.root, text="Enter message you would like to encode (50 char max)")
        self.messageInstr.pack(pady=5)
        self.messagebox = ttk.Entry(self.root, width=60)
        self.messagebox.pack()
        
        # Hit button or enter to input mesage
        self.confirm_button = ttk.Button(self.root, text="Confirm Message", command=self.confirm_message)
        self.confirm_button.pack(pady=5)
        self.messagebox.bind("<Return>", lambda event: self.confirm_message())

        # Input file
        self.inFileInstruction = ttk.Label(self.root, text="Select your input file (.wav)")
        self.inFileInstruction.pack(pady=10)
        self.filebutton1 = ttk.Button(self.root, text="Select .wav file", command=self.select_infile)
        self.filebutton1.pack()

        # Output file
        self.outFileInstruction = ttk.Label(self.root, text="Select your write-to file")
        self.outFileInstruction.pack(pady=10)
        self.filebutton2 = ttk.Button(self.root, text="Select .wav file", command=self.select_outfile)
        self.filebutton2.pack()

        # Run Button
        self.runButton = ttk.Button(self.root, text="Run", command=self.run_backend)
        self.runButton.pack(pady=20)

        # Console Output
        self.console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=100, font=("Courier", 10))
        self.console.pack(padx=10, pady=20)

        # self.root.mainloop()

    # Confirm encoded message
    def confirm_message(self):
        self.message = self.messagebox.get()
        if not self.message:
            print("No message entered.")
            return

        print(f"Message to encode: {self.message}")
        self.messagebox.configure(state='readonly')
        self.confirm_button.configure(state='disabled')

    
    def select_infile(self):
        file_path = fd.askopenfilename(
            title="Select a file, must be .wav",
            filetypes=(("Wav files", "*.wav"), ("mp3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            print(f"Input file selected: {file_path}")
            self.inFile = file_path
    
    def select_outfile(self):
        file_path = fd.asksaveasfilename(
            title="Select a file, must be .wav",
            defaultextension=".wav",
            initialfile="encoded_file.wav",
            filetypes=(("Wav files", "*.wav"), ("mp3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            self.outFile = file_path
            print(f"Encoded audio saved to: {file_path}")
    
    def run_backend(self):
        self.message = self.messagebox.get()
        if self.message and self.inFile and self.outFile:
            if self.callback:
                self.callback(self.message, self.inFile, self.outFile)
        else:
            print("Missing input. Please enter a message and select both files.")


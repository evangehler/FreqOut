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
    # I/O
    message = None
    inFile = None
    outFile = None
    callback = None

    # Main Configuration
    def __init__(self):
        
        # Window Size / Config
        self.root = tk.Tk()
        self.root.geometry('725x800')
        self.root.title("FreqOut")
        self.root.configure(background='dark green')
        
        # Style
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TLabel', foreground='gray', font=('Helvetica', 16))
        style.configure('TButton', font=('Arial', 12), padding=5)
        style.configure('TEntry', font=('Courier New', 16))

        # Title
        self.title = ttk.Label(self.root, text="FreqOut!", foreground='silver', background='dark green', font=("Impact", 64))
        self.title.pack(padx=30, pady=20)
        
        # ===== Frame for inputs, all in one row-block container =====
        self.frame_top = ttk.Frame(self.root)
        self.frame_top.pack(pady=20, padx=40, fill='x')

        # Message Entry Row
        self.message_frame = ttk.Frame(self.frame_top)
        self.message_frame.pack(anchor='w', pady=5)

        self.messageInstr = ttk.Label(self.message_frame, text="Message:")
        self.messageInstr.grid(row=0, column=0, padx=5)

        self.messagebox = ttk.Entry(self.message_frame, width=60)
        self.messagebox.grid(row=0, column=1)
        self.messagebox.bind("<Return>", lambda event: self.confirm_message())

        # Confirm Button
        self.confirm_button = ttk.Button(self.message_frame, text="Encode Message", command=self.confirm_message)
        self.confirm_button.grid(row=0, column=2, padx=5)

        # Input File Row
        self.in_file_frame = ttk.Frame(self.frame_top)
        self.in_file_frame.pack(anchor='w', pady=5)

        self.inFileInstruction = ttk.Label(self.in_file_frame, text="Input File:")
        self.inFileInstruction.grid(row=0, column=0, padx=5)

        self.filebutton1 = ttk.Button(self.in_file_frame, text="Browse...", command=self.select_infile)
        self.filebutton1.grid(row=0, column=1)

        # Output File Row
        self.out_file_frame = ttk.Frame(self.frame_top)
        self.out_file_frame.pack(anchor='w', pady=5)

        self.outFileInstruction = ttk.Label(self.out_file_frame, text="Output File:")
        self.outFileInstruction.grid(row=0, column=0, padx=5)

        self.filebutton2 = ttk.Button(self.out_file_frame, text="Save As...", command=self.select_outfile)
        self.filebutton2.grid(row=0, column=1)

        # Run Button
        self.runButton = ttk.Button(self.frame_top, text="Run", command=self.run_backend)
        self.runButton.pack(pady=10)

        # Console Output
        self.console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=120, height=70, font=("Courier", 10))
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
 
    # Select Input
    def select_infile(self):
        file_path = fd.askopenfilename(
            title="Select a file, must be .wav",
            filetypes=(("Wav files", "*.wav"), ("mp3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            print(f"Input file selected: {file_path}")
            self.inFile = file_path
    
    # Select or Create Output
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
    
    # Run
    def run_backend(self):
        self.message = self.messagebox.get()
        if self.message and self.inFile and self.outFile:
            if self.callback:
                self.callback(self.message, self.inFile, self.outFile)
        else:
            print("Missing input. Please enter a message and select both files.")


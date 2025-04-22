import tkinter as tk
from tkinter import filedialog as fd
from tkinter import scrolledtext
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
    def __init__(self):
        self.message = None
        self.inFile = None
        self.outFile = None
        self.callback = None


        self.root = tk.Tk()
        self.root.geometry('1000x600')
        self.root.title("FreqOut")
        self.root.configure(background='dark green')
        #title
        self.title = tk.Label(self.root, text="FreqOut", font=("Impact", 64), fg="silver")
        self.title.pack(padx=30, pady=60)
        #box to enter message as well as instruction above it
        self.messageInstr = tk.Label(self.root, text="Enter message you would like to encode (50 char max)", font=("Impact", 16),
                                fg="silver", bg="dark green")
        self.messageInstr.pack(padx=30, pady=5)
        self.messagebox = tk.Entry(self.root)
        self.messagebox.pack( padx=0, pady=0)
       
        #--> Replaced, now whatever text is in box will be message, no need to hit enter
        # self.messagebox.bind("<Return>", self.enter_on_press)

        #both buttons to select files from computer

        self.inFileInstruction = tk.Label(self.root, text="Select your input file (.wav)", font=("Impact", 16), fg="silver", bg="dark green")
        self.inFileInstruction.pack(padx=30, pady=5)

        self.filebutton1 = tk.Button(self.root, text="Select .wav file", command=self.select_infile, font=("Arial"),fg="black", bg="grey")
        self.filebutton1.pack(padx=30)

        self.outFileInstruction = tk.Label(self.root, text="Select your write to file", font=("Impact", 16),
                                          fg="silver", bg="dark green")
        self.outFileInstruction.pack(padx=30, pady=5)

        self.filebutton2 = tk.Button(self.root, text="Select .wav file", command=self.select_outfile, font=("Arial"),fg="black", bg="grey")
        self.filebutton2.pack(padx=30)

        # Run Button
        self.runButton = tk.Button(self.root, text="Run", command=self.run_backend, font=("Arial"), fg="white", bg="black")
        self.runButton.pack(pady=20)

        # Console Output
        self.console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=20, font=("Courier", 10))
        self.console.pack(padx=10, pady=20)

        # self.root.mainloop()

    # Message will be whatever is in text box 
    # def enter_on_press(self, event):
    #     encoded_message = self.messagebox.get()
    #     self.message = encoded_message
    #     self.messagebox.delete(first=0, last=len(encoded_message))
    #     self.messagebox.configure(state="disabled")

    
    def select_infile(self):
        file_path = fd.askopenfilename(
            title="Select a file, must be .wav",
            filetypes=(("Wav files", "*.wav"), ("mp3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            print(f"File selected: {file_path}")
            self.inFile = file_path
    
    def select_outfile(self):
        file_path = fd.askopenfilename(
            title="Select a file, must be .wav",
            filetypes=(("Wav files", "*.wav"), ("mp3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            print(f"File selected: {file_path}")
            self.outFile = file_path
    
    def run_backend(self):
        self.message = self.messagebox.get()
        if self.message and self.inFile and self.outFile:
            if self.callback:
                self.callback(self.message, self.inFile, self.outFile)
        else:
            print("Missing input. Please enter a message and select both files.")


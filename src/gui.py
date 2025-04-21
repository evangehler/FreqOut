import tkinter as tk
from tkinter import filedialog as fd
class GUI:
    message = None
    inFile = None
    outFile = None


    def __init__(self):
        #initalize root/window
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
        self.messagebox.bind("<Return>", self.enter_on_press)

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


        self.root.mainloop()
    def enter_on_press(self, event):
        encoded_message = self.messagebox.get()
        message = encoded_message
        self.messagebox.delete(first=0, last=len(encoded_message))
        self.messagebox.configure(state="disabled")

    def select_infile(self):
        file_path = fd.askopenfilename(
            title="Select a file, must be .wav",
            filetypes=(("Wav files", "*.wav"), ("mp3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            print(f"File selected: {file_path}")
            inFile = file_path
    def select_outfile(self):
        file_path = fd.askopenfilename(
            title="Select a file, must be .wav",
            filetypes=(("Wav files", "*.wav"), ("mp3 files", "*.mp3"), ("All files", "*.*"))
        )
        if file_path:
            print(f"File selected: {file_path}")
            outFile = file_path

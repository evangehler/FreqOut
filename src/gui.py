import tkinter as tk
from tkinter import filedialog as fd
class GUI:
    message = None


    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1000x600')
        self.root.title("FreqOut")
        self.root.configure(background='dark green')

        self.title = tk.Label(self.root, text="FreqOut", font=("Impact", 64), fg="silver")
        self.title.pack(padx=30, pady=60)

        self.messageInstr = tk.Label(self.root, text="Enter message you would like to encode (50 char max)", font=("Impact", 16),
                                fg="silver", bg="dark green")
        self.messageInstr.pack(padx=30, pady=5)
        self.messagebox = tk.Entry(self.root)
        self.messagebox.pack(padx=0, pady=0)
        self.messagebox.bind("<Return>", self.enter_on_press)

        self.filebutton = tk.Button(self.root, text="Select .wav file", command=self.select_file, font=("Arial"), fg= "black", bg= "grey")
        self.filebutton.pack(padx=30, pady=15)

        self.root.mainloop()
    def enter_on_press(self, event):
        encoded_message = self.messagebox.get()
        message = encoded_message
        self.messagebox.delete(first=0, last=len(encoded_message))
        self.messagebox.configure(state="disabled")

    def select_file(self):
        file_path = fd.askopenfilename(
            title="Select a file, must be .wav",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            print(f"File selected: {file_path}")
            self.selected_file = file_path  # store it if you need it

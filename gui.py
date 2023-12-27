#for UI
import customtkinter as ct
#file dialog
import tkinter as tk
from tkinter import filedialog
#for getting the file name from path
import os

ct.set_appearance_mode("system")  # Modes: system (default), light, dark
ct.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

class Ui :

    def __init__(self):
        self.root = ct.CTk()
        
        #init members
        self.inputPath = ""

        #init window dimensions + title
        self.root.geometry("900x500")
        self.root.title("Xml Parsiewer")

        #make the first column -> editor textbox and import file button
        self.editor_text_box = ct.CTkTextbox(self.root, height=300, width=300)
        self.editor_text_box.grid(row=0, column=0, padx=10, pady=10,sticky='n')
        self.importFileButton = ct.CTkButton(self.root, width=300, text="Import File", command=self.chooseInputFile)
        self.importFileButton.grid(row=1, column=0, padx=10, pady=10)


        #make feature buttons -> second column
        # Create a frame for the second column buttons
        self.frame_buttons = ct.CTkFrame(self.root)
        self.frame_buttons.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky='n')
        self.minifyButton = ct.CTkButton(self.frame_buttons, text="Minify")
        self.minifyButton.grid(row=0, column=1, padx=10, pady=5)
        self.prettifyButton = ct.CTkButton(self.frame_buttons, text="Prettify")
        self.prettifyButton.grid(row=1, column=1, padx=10, pady=5)
        self.convertToJsonButton = ct.CTkButton(self.frame_buttons, text="Convert to Json")
        self.convertToJsonButton.grid(row=2, column=1, padx=10, pady=5)
        self.compressButton = ct.CTkButton(self.frame_buttons, text="Compress")
        self.compressButton.grid(row=3, column=1, padx=10, pady=5)
        self.correctButton = ct.CTkButton(self.frame_buttons, text="Correct Xml")
        self.correctButton.grid(row=4, column=1, padx=10, pady=5)
        self.showErrorsButton = ct.CTkButton(self.frame_buttons, text="Show Xml Errors")
        self.showErrorsButton.grid(row=5, column=1, padx=10, pady=5)


        #make third column -> output textbox and save file
        output_text_box = ct.CTkTextbox(self.root, height=300, width=300, state='disabled')
        output_text_box.grid(row=0, column=2, padx=10, pady=10, sticky='n')
        saveFileButton = ct.CTkButton(self.root,  width=300, text="Save File")
        saveFileButton.grid(row=1, column=2, padx=10, pady=10)


        self.makeResponsive()

        #main event loop
        self.root.mainloop()

    def makeResponsive (self):
        # Configure row and column weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def chooseInputFile (self):
        file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("text files", "*.txt"), ("xml files", "*.xml"), ("All Files", "*.*")))
        if file_path:
            # Do something with the selected file path (e.g., display it in a label)
            # self.inputFileNameLabel.configure(text=f"{os.path.basename(file_path)}")
            self.inputPath = file_path
        else:
            self.inputPath = ""
        #display in text box
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.editor_text_box.delete(1.0, tk.END)  # Clear existing content
                self.editor_text_box.insert(tk.END, content)
        
    
#start app
Ui()
#for UI
import customtkinter as ct
#file dialog
import tkinter as tk
from tkinter import filedialog
#for getting the file name from path
import os
#for program features
from formatting import minify, prettify
from xml2json import xml2json
from correct_xml import correct_xml
from xml_error_detector import XML_error_detector
# Social Network
from build_graph_network_from_xml import *
# Compression
from BPE import BPE
bpe = BPE()

ct.set_appearance_mode("system")  # Modes: system (default), light, dark
ct.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

class Ui :

    def __init__(self):
        self.root = ct.CTk()

        #init members
        self.inputPath = ""

        #init window dimensions + title
        self.root.geometry("950x470")
        self.root.title("XML Parsiewer")

        #make the first column -> editor textbox and import file button
        self.editor_text_box = ct.CTkTextbox(self.root, height=400, width=270, wrap='none', undo=True, autoseparators=True)
        self.editor_text_box.grid(row=0, column=0, padx=10, pady=10,sticky='n')
        self.importFileButton = ct.CTkButton(self.root, width=270, text="Import File", command=self.chooseInputFile)
        self.importFileButton.grid(row=1, column=0, padx=10, pady=10)


        #make feature buttons -> second column
        self.frame_of_frames = ct.CTkFrame(self.root)
        self.frame_of_frames.grid(row=0, column=1, padx=10, pady=15, sticky='n')

        self.out_to_in_button = ct.CTkButton(self.frame_of_frames, text="Copy Output to Input for Modifications", command=self.copy_inout)
        self.out_to_in_button.grid(row=2, column=0, padx=10, pady=5, sticky='n', columnspan = 2)
        self.in_to_out_button = ct.CTkButton(self.frame_of_frames, text="Copy Input to Output for Compression", command=self.copy_outin)
        self.in_to_out_button.grid(row=1, column=0, padx=10, pady=5, sticky='n', columnspan = 2)

        # Create a frame for the second column buttons
        self.frame_buttons1 = ct.CTkFrame(self.frame_of_frames)
        self.frame_buttons1.grid(row=0, column=0, padx=10, pady=5, sticky='n')
        self.minifyButton = ct.CTkButton(self.frame_buttons1, text="Minify", command=self.minify)
        self.minifyButton.grid(row=0, column=0, padx=10, pady=5, columnspan=2)
        self.prettifyButton = ct.CTkButton(self.frame_buttons1, text="Prettify", command=self.prettify)
        self.prettifyButton.grid(row=1, column=0, padx=10, pady=5, columnspan=2)
        self.convertToJsonButton = ct.CTkButton(self.frame_buttons1, text="Convert to JSON", command=self.xml2json)
        self.convertToJsonButton.grid(row=2, column=0, padx=10, pady=5, columnspan=2)
        self.compressButton = ct.CTkButton(self.frame_buttons1, text="Compress Output", command=self.compress)
        self.compressButton.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

        # Add entry widgets for user IDs
        self.iterations = ct.CTkEntry(self.frame_buttons1, width=50)
        self.iterations.grid(row=4, column=1, padx=10, pady=5)
        self.iterationsText = ct.CTkLabel(self.frame_buttons1, text ="Max iters.", padx = 5, pady = 5)
        self.iterationsText.grid(row=4, column=0, padx=10, pady=5)

        self.decompressButton = ct.CTkButton(self.frame_buttons1, text="Decompress", command=self.decompress)
        self.decompressButton.grid(row=5, column=0, padx=10, pady=5, columnspan=2)
        self.correctButton = ct.CTkButton(self.frame_buttons1, text="Correct XML", command=self.correct_xml)
        self.correctButton.grid(row=6, column=0, padx=10, pady=5, columnspan=2)
        self.showErrorsButton = ct.CTkButton(self.frame_buttons1, text="Show XML Errors",command=self.show_xml_errors)
        self.showErrorsButton.grid(row=7, column=0, padx=10, pady=5, columnspan=2)



        self.frame_buttons2 = ct.CTkFrame(self.frame_of_frames)
        self.frame_buttons2.grid(row=0, column=1, padx=10, pady=5, sticky='n')
        # Add a button to parse XML and build the social graph
        self.buildGraphButton = ct.CTkButton(self.frame_buttons2, text="Build Social Graph", command=self.build_social_graph)
        self.buildGraphButton.grid(row=0, column=0, padx=10, pady=5, columnspan=2)

        # Add a button to visualize the social graph
        self.visualizeGraphButton = ct.CTkButton(self.frame_buttons2, text="Visualize Social Graph", command=self.visualize_social_graph)
        self.visualizeGraphButton.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        # Add a button to search for posts by topic
        self.searchPostsButton = ct.CTkButton(self.frame_buttons2, text="Search Posts by Topic", command=self.search_posts_by_topic)
        self.searchPostsButton.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

        # Add an entry widget for the topic
        self.topicEntry = ct.CTkEntry(self.frame_buttons2, width=100)
        self.topicEntry.grid(row=3, column=0, padx=10, pady=5, columnspan=2)

        # Add a button to print the network analysis report
        self.networkAnalysisButton = ct.CTkButton(self.frame_buttons2, text="Network Analysis", command=self.show_network_analysis)
        self.networkAnalysisButton.grid(row=4, column=0, padx=10, pady=5, columnspan=2)

        # Add entry widgets for user IDs
        self.user1Entry = ct.CTkEntry(self.frame_buttons2, width=50)
        self.user1Entry.grid(row=5, column=1, padx=10, pady=5)
        self.user1ID = ct.CTkLabel(self.frame_buttons2, text ="User1 ID:", padx = 5, pady = 5)
        self.user1ID.grid(row=5, column=0, padx=10, pady=5)

        self.user2Entry = ct.CTkEntry(self.frame_buttons2, width=50)
        self.user2Entry.grid(row=6, column=1, padx=10, pady=5)
        self.user2ID = ct.CTkLabel(self.frame_buttons2, text ="User2 ID:", padx = 5, pady = 5)
        self.user2ID.grid(row=6, column=0, padx=10, pady=5)

        # Attributes used to build and maintain the social graph
        self.content_that_built_the_graph = None
        self.social_graph = None


        self.undo_button = ct.CTkButton(self.frame_buttons2, width=50, text="Undo", command=self.undo)
        self.undo_button.grid(row=7, column=0, padx=5, pady=5)
        self.redo_button = ct.CTkButton(self.frame_buttons2, width=50, text="Redo", command=self.redo)
        self.redo_button.grid(row=7, column=1, padx=5, pady=5)

        #make third column -> output textbox and save file
        self.output_text_box = ct.CTkTextbox(self.root, height=400, width=270, state='disabled', wrap='none')
        self.output_text_box.grid(row=0, column=3, padx=10, pady=10, sticky='n')
        self.saveFileButton = ct.CTkButton(self.root,  width=270, text="Save File", command=self.choose_output_file)
        self.saveFileButton.grid(row=1, column=3, padx=10, pady=10)
        self.last_function_performed_output_extension = ".txt"
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

    # These still need buttons
    def undo(self):
        try:
            self.editor_text_box.edit_undo()
        except:
            pass
    def redo(self):
        try:
            self.editor_text_box.edit_redo()
        except:
            pass

    def copy_inout(self):
        content = self.output_text_box.get(1.0, tk.END)
        self.editor_text_box.delete(1.0, tk.END)
        self.editor_text_box.insert(tk.END, content)

    def copy_outin(self):
        content = self.editor_text_box.get(1.0, tk.END)
        self.show_output(content)
        self.last_function_performed_output_extension = ".xml"

    def chooseInputFile (self):
        file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=(("xml files", "*.xml"), ("text files", "*.txt"), ("All Files", "*.*")))
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

    def choose_output_file(self):
        file_path = filedialog.asksaveasfilename(
        title="Save File",
        defaultextension=self.last_function_performed_output_extension,
        filetypes=[("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                text_content = self.output_text_box.get(1.0, tk.END)
                file.write(text_content)

    def compress(self):
        text_content = self.output_text_box.get(1.0, tk.END)
        self.show_output("Compressing file, this might\ntake a moment..")
        file_path = filedialog.asksaveasfilename(
        title="Compress File",
        defaultextension=".xip",
        filetypes=[("All files", "*.xip")])
        if file_path:
            bpe.compress(text_content, file_path[:len(file_path)-4], self.iterations.get())
            self.show_output("Compression done!")

    def decompress(self):
        self.show_output("Decompressing file, this might\ntake a moment..")
        file_path = filedialog.askopenfilename(
        title="Decompress File",
        filetypes=[("All files", "*.xip")])
        if file_path:
            content = bpe.decompress(file_path)
            self.show_output(content)
            self.last_function_performed_output_extension = ".xml"

    def minify(self):
        content = self.editor_text_box.get(1.0, tk.END)
        content = minify(content)
        self.show_output(content)
        self.last_function_performed_output_extension = ".xml"

    def xml2json(self):
        content = self.editor_text_box.get(1.0, tk.END)
        content = xml2json(content)
        self.show_output(content)
        self.last_function_performed_output_extension = ".json"

    def prettify(self):
        content = self.editor_text_box.get(1.0, tk.END)
        content = prettify(content)
        self.show_output(content)
        self.last_function_performed_output_extension = ".xml"

    def correct_xml(self):
        content = self.editor_text_box.get(1.0, tk.END)
        try:
            content = correct_xml(content)
            self.show_output(content)
            self.last_function_performed_output_extension = ".xml"
        except:
            self.show_error("Input is not a syntax-error-free XML file.")

    def show_xml_errors(self):
        content=self.editor_text_box.get(1.0,tk.END)
        content = XML_error_detector(content)
        self.show_output(content)
        self.last_function_performed_output_extension = ".txt"

    def build_social_graph(self):
        xml_content = self.editor_text_box.get(1.0, tk.END)
        try:
            self.social_graph = build_graph_netowrk_from_xml(xml_content)
            self.show_output("Social graph built successfully.")
            self.content_that_built_the_graph = xml_content
        except:
            self.show_error("The entered file is not a valid\nsocial graph representation. Try again\nwith a different file.")

    def visualize_social_graph(self):
        xml_content = self.editor_text_box.get(1.0, tk.END)
        if (xml_content == self.content_that_built_the_graph):
            self.social_graph.visualize_graph()
        else:
            self.show_error("Please build the social graph first.")

    def search_posts_by_topic(self):
        # Get the topic from the entry widget
        topic = self.topicEntry.get()
        xml_content = self.editor_text_box.get(1.0, tk.END)
        if topic:
            if (xml_content == self.content_that_built_the_graph):
                posts_by_topic = self.social_graph.search_posts_by_topic(topic)
                self.output_text_box.configure(state='normal')
                self.output_text_box.delete(1.0, tk.END)
                for post in posts_by_topic:
                    self.output_text_box.insert(tk.END, post + '\n')
                if (len(posts_by_topic) == 0):
                    self.output_text_box.insert(tk.END, "No posts with this topic were found.")
                self.output_text_box.configure(state='disabled')

                self.last_function_performed_output_extension = ".txt"
            else:
                self.show_error("Please build the social graph first.")
        else:
            self.show_error("Please enter a topic to search for.")

    def show_network_analysis(self):
        xml_content = self.editor_text_box.get(1.0, tk.END)
        if (xml_content != self.content_that_built_the_graph):
            self.show_error("Please build the social graph first.")
        else:
            # Get user-specified parameters
            user1_id = self.user1Entry.get()
            user2_id = self.user2Entry.get()
            topic = self.topicEntry.get()

            # Perform network analysis with user-specified parameters
            result = self.social_graph.print_network_analysis(user1_id, user2_id, topic)

            # Display the result in the output text box
            self.show_result("Network Analysis", result)
            self.last_function_performed_output_extension = ".txt"


    def show_result(self, title, result):
        self.output_text_box.configure(state='normal')
        self.output_text_box.delete(1.0, tk.END)
        self.output_text_box.insert(tk.END, f"{title}:\n")
        if result:
            for item in result:
                self.output_text_box.insert(tk.END, f"{item}\n")
        else:
            self.output_text_box.insert(tk.END, "No result found.")
        self.output_text_box.configure(state='disabled')


    # The two functions below are almost identical, but the different names are for clarity
    def show_error(self, message):
        # Show error messages in the output text box
        self.output_text_box.configure(state='normal')
        self.output_text_box.delete(1.0, tk.END)
        self.output_text_box.insert(tk.END, message)
        self.output_text_box.configure(state='disabled')
        self.last_function_performed_output_extension = ".txt"

    def show_output(self, message):
        self.output_text_box.configure(state='normal')
        self.output_text_box.delete(1.0, tk.END)
        self.output_text_box.insert(tk.END, message)
        self.output_text_box.configure(state='disabled')

#start app
Ui()

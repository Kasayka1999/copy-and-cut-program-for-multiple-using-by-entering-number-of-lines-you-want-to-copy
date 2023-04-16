import ctypes as ct
from tkinter import *
import tkinter as tk
from tkinter import ttk
import pyperclip
import tkinter.font as TkFont
import tkinter.messagebox as messagebox
from _tkinter import TclError
import sv_ttk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import darkdetect
import tkinter.font as TkFont
from tkinter.filedialog import askdirectory
from tkinter import filedialog

class App(ttk.Frame, ttk.Label):
    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self)

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Define check_frame attribute
        self.check_frame = ttk.LabelFrame(self, text="Action", padding=(20, 10))

        # Create widgets :)
        self.setup_widgets()

    def copy_first_4900_asins(self):
        """
        A method that extracts the first n ASINs (where n is the number entered in the input field),
        from the Text widget, deletes them, and copies them to the clipboard.
        """
        input_number = int(self.number_input.get())
        text = textarea.get("1.0", "end-1c")
        asins = text.split("\n")[:input_number]
        textarea.delete("1.0", f"{len(asins)+1}.0")
        update_line_count(None)
        pyperclip.copy("\n".join(asins))

    def setup_widgets(self):
        
        # Create a Frame for input widgets
        self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(
            row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)
        
        # Entry
        self.entry = ttk.Entry(self.widgets_frame)
        self.entry.insert(0, "Selects .txt file")
        self.entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")
        
        
        # Button Functionold
        def open_file_dialog():
            """
            A function that opens a file dialog and returns the selected file path.
            """
            file_path = filedialog.askopenfilename(title="Select .txt file", filetypes=[("Text files", "*.txt")])
            return file_path

        def Funcbutton():
            global last_file_path
            path = open_file_dialog()
            if not path:
                return
            textarea.delete("1.0", "end")
            with open(path, "r") as f:
                asins = f.read().split("\n")
            textarea.insert("1.0", "\n".join(asins))
            # Update the text of the entry widget
            self.entry.delete(0, tk.END)
            self.entry.insert(0, path)
            # Save the file path for later use in the save function
            last_file_path = path
            update_line_count(None)

        def save_file():
            global last_file_path
            # If the last file path is not set, ask the user to select a file to save
            if not last_file_path:
                last_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            # If the user didn't select any file, return
            if not last_file_path:
                return
            text = textarea.get("1.0", "end-1c")
            with open(last_file_path, "w") as f:
                f.write(text)
            # Update the text of the entry widget
            self.entry.delete(0, tk.END)
            self.entry.insert(0, last_file_path)

        def undo():
            """
            A function that undoes the last change in the textarea.
            """
            if textarea.edit_modified():
                textarea.edit_undo()
                update_line_count(None)

        def redo():
            """
            A function that redoes the last undone change in the textarea.
            """
            try:
                textarea.edit_redo()
                update_line_count(None)
            except TclError:
                pass

        def remove_duplicates():
            """
            A function that removes duplicate lines from the textarea.
            """
            text = textarea.get("1.0", "end-1c")
            lines = text.split("\n")
            unique_lines = list(set(lines))
            textarea.delete("1.0", "end")
            textarea.insert("1.0", "\n".join(unique_lines))
            update_line_count(None)

       
        # Button
        self.button = ttk.Button(self.widgets_frame, text="Select", command = Funcbutton)
        self.button.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="ew")


        # Create the Save button
        save_icon = tk.PhotoImage(file="icons/save-icon-new.png")
        save_button = ttk.Button(
            self.widgets_frame,
            text="",
            image=save_icon,
            compound="center",
            command=save_file,
            width=0
        )
        save_button.image = save_icon
        save_button.grid(row=0, column=2, padx=5, pady=(0, 10), sticky="ew")
            
        
        # Create a Frame for the input field
        self.input_frame = ttk.LabelFrame(self, text="Enter a number", padding=(20, 10))
        self.input_frame.grid(
            row=2, column=0, padx=(20, 10), pady=(140, 10), sticky="nsew"
        )

        # Input field for entering a number
        self.number_entry = ttk.Entry(self.input_frame)
        self.number_entry.grid(row=0, column=0, padx=1, pady=5, sticky="nsew")

        # Create a Frame for the Input & Copy Paste
        self.check_frame = ttk.LabelFrame(self, text=" Enter number of lines you want to copy & cut ", padding=(20, 10))
        self.check_frame.grid(
            row=2, column=0, padx=(20, 10), pady=(140, 10), sticky="nsew"
        )

        # Prompt the user to enter a number
        self.number_label = ttk.Label(
            self.check_frame, text="Number Line:", padding=(5, 0)
        )
        self.number_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        # Entry widget for entering a number
        self.number_input = ttk.Entry(self.check_frame)
        self.number_input.insert(0, "10")  # set a default value of 10
        self.number_input.grid(row=0, column=1, padx=5, pady=10, sticky="ew")


       # Create the Copy & Cut button
        start_button = ttk.Button(
            self.check_frame, text="Copy & Cut", style="Accent.TButton", 
            command=self.copy_first_4900_asins
        )
        start_button.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

        # Create a Frame for the Optimize button
        self.optimize_frame = ttk.LabelFrame(self, text="", padding=(10, 10), borderwidth=0, relief="flat")
        self.optimize_frame.grid(row=3, column=0, padx=(35, 10), pady=(10, 0), sticky="nsew")
        
        # Create the Undo
        optimize_icon = tk.PhotoImage(file="icons/undo-icon.png")
        optimize_button = ttk.Button(
            self.optimize_frame,
            text="Undo",
            image=optimize_icon,
            compound="left",
            command=undo,
            width=5
        )
        optimize_button.image = optimize_icon
        optimize_button.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        # Create the Redo
        optimize_icon2 = tk.PhotoImage(file="icons/redo-icon.png")
        optimize_button = ttk.Button(
            self.optimize_frame,
            text="Redo",
            image=optimize_icon2,
            compound="left",
            command=redo,
            width=5
        )
        optimize_button.image = optimize_icon2
        optimize_button.grid(row=0, column=3, padx=5, pady=10, sticky="nsew")

        # Create the Remove Duplicates
        optimize_button = ttk.Button(
            self.optimize_frame,
            text="Remove Duplicate",
            command=remove_duplicates,
            width=20
        )
        optimize_button.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
        # Set background color to match parent widget
        self.optimize_frame.configure(style="TFrame")

    

#NEW CLASS       
class Gauge(ttk.Label, ttk.Frame):           
    def setup(self):
        """Setup routine"""      
# Start Progress

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Copy & Cut By UXELL")
    root.resizable(False,False)
    
    # Start Progress
    gauge = Gauge(root, padding=20)
    gauge.grid(row=1, column=0)
    # Simply set the theme
    if darkdetect.theme() == "Light":
        sv_ttk.use_light_theme()
    else:
        sv_ttk.use_dark_theme()

    app = App(root)
    app.grid(row=0, column=0)
    
    # End Progress
    # Start ListBox 

    # Create a Frame for the Checkbuttons
    check_frame = ttk.LabelFrame(text="Text Area", padding=(15, 10))
    check_frame.grid(
        row=0, column=1, rowspan=2, padx=(20, 10), pady=(20, 10), sticky="nsew"
    )

    sf = TkFont.Font(family='Courier', size=10, weight='normal')
    textarea = tk.Text(check_frame, undo=True, font=sf, borderwidth=0)

    # Create the Label widget to show line count
    line_count_label = ttk.Label(check_frame, text="Lines: 1")
    line_count_label.pack(side="bottom", pady=(5, 0))

    # Insert the default text
    default_text = "Text here..."
    textarea.insert("1.0", default_text)

    # Bind the FocusIn event to remove the default text
    def remove_default_text(event):
        if textarea.get("1.0", "end-1c") == default_text:
            textarea.delete("1.0", "end")

    textarea.bind("<FocusIn>", remove_default_text)

    textarea.pack(side="left", expand=1, fill=tk.BOTH)
    scrollbar = ttk.Scrollbar(check_frame, command=textarea.yview)
    scrollbar.pack(side="right", fill="y")
    textarea.configure(yscrollcommand=scrollbar.set)


    # Update the line count when the Text widget is modified or keys are pressed
    def update_line_count(event):
        lines = textarea.get("1.0", "end-1c").split("\n")
        line_count_label.configure(text="Lines: {}".format(len(lines)))

    textarea.bind("<KeyRelease>", update_line_count)

    # End ListBox


    
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate))
    

    root.mainloop()
    

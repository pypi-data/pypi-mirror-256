import customtkinter
import tkinter as tk
from PIL import Image, ImageTk
import os
import platform
import subprocess

def create_tab(self, tab):
    
    def open_graph_in_browser():
        # Open the file in the default program
        info = self.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = os.path.join(folder, self.selected_graph_name + ".html")
        
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", file_path])
        else:
            subprocess.Popen(["xdg-open", file_path])
    
    def _resize_image(event):
        self.graph_label.update_idletasks()
        new_width = self.graph_label.winfo_width()
        new_height = self.graph_label.winfo_height()
        
        alt_width = new_height * 1.77778
        alt_height = new_width / 1.77778
        
        if (new_width < new_height):
            new_height = alt_height
        else:
            new_width = alt_width
        
        self.image_width = new_width
        self.image_height = new_height
        
        self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(new_width, new_height))
        self.graph_label.configure(image=self.graph_image)
        self.graph_label.update_idletasks()
        
        print("RESIZED")
    
    tab.grid_columnconfigure(1, weight=10)
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_columnconfigure(2, weight=1)
    tab.grid_rowconfigure(1, weight=1)
    
    self.graph_selector_value = tk.StringVar()
    self.graph_selector_value.set("Best Cost Stacked")
    self.graph_selector = customtkinter.CTkOptionMenu(tab, values=["Best Cost Stacked", "Best Cost by Round", "Calibrated Parameters", "Table"], variable=self.graph_selector_value, command=self.update_graph)
    self.graph_selector.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    # Add a button to call open_graph_in_browser
    self.graph_button = customtkinter.CTkButton(tab, text="Open Graph in Browser", command=open_graph_in_browser)
    self.graph_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    self.graph_image_obj = Image.open(os.path.join("./images", "up.png"))
    self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(700, 500))
    self.graph_label = customtkinter.CTkLabel(tab, text=None, image=self.graph_image)
    self.graph_label.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
    #window = customtkinter.CTk()
    self.graph_label.bind('<Configure>', _resize_image)
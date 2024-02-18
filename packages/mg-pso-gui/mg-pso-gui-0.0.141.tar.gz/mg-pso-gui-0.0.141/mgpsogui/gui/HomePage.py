#!/usr/local/bin/python3.9

import os 
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print(dir_path)

# minikube kubectl -- create -f ../start.yaml ; sleep 60 ; minikube service pf8087-csu-csip-oms -n csip

import tkinter as tk
import tkinter.messagebox
import customtkinter
import json
import os
from PIL import Image, ImageTk
import traceback
from multiprocessing import Process
from multiprocessing import Queue
import re
import pandas as pd
import numpy as np
import ast
import platform
import time

from ..util import PSORunner
from ..util import GraphGenerator

import subprocess
import plotly.express as px
import plotly.graph_objs as go

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

from . import OptionManager as om

from .SetupTab import SetupTab as st
from .PlatformTab import PlatformTab as pt
from .RunTab import RunTab as rt

from ..util.CTkToolTip import CTkToolTip as ctt

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.option_manager = om.OptionManager()
        
        self.running_config = None
        self.selected_graph_name = None

        self.train_process = None
        self.minikube_process = None
        self.data_x = [0]
        self.data_y = [0]
        
        self.image_width = 1280
        self.image_height = 720

        # configure window
        self.title("CSIP PSO")
        self.geometry(f"{1920}x{1080}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_padding_x = (5, 5)
        header_padding_y = (10, 10)
        
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CSIP PSO", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(20, 5), pady=header_padding_y)
        self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Save", width=60, command=self.save_project)
        self.save_button.grid(row=0, column=1, padx=header_padding_x, pady=header_padding_y)
        self.load_button = customtkinter.CTkButton(self.sidebar_frame, text="Load", width=60, command=self.load_project)
        self.load_button.grid(row=0, column=2, padx=header_padding_x, pady=header_padding_y)
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scale:", anchor="w")
        self.scaling_label.grid(row=0, column=7, padx=header_padding_x, pady=header_padding_y)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["50%", "75%", "100%", "125%", "150%", "175%", "200%"], width=60,
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=0, column=8, padx=header_padding_x, pady=header_padding_y)
        self.scaling_optionemenu.set("100%")
        
        expand_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "expand.png")), size=(20, 20))
        self.new_window = customtkinter.CTkButton(self.sidebar_frame, text=None, width=30, image=expand_image, command=self.new_window)
        self.new_window.grid(row=0, column=9, padx=header_padding_x, pady=header_padding_y)
        
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=(60, 60), pady=(10, 10), sticky="nsew")
        tab1 = "Platform"
        tab2 = "Setup"
        tab3 = "Run"
        tab4 = "Visualize"
        tab5 = "Results"
        
        self.tabview.add(tab1)
        self.tabview.add(tab2)
        self.tabview.add(tab3)
        self.tabview.add(tab4)
        self.tabview.add(tab5)
        
        self.tabview.configure(state="disabled")
        
        
        pt.create_tab(self, self.tabview.tab(tab1))
        st.create_tab(self, self.tabview.tab(tab2))
        rt.create_tab(self, self.tabview.tab(tab3))
        
        self.tabview.tab(tab4).grid_columnconfigure(1, weight=10)
        self.tabview.tab(tab4).grid_columnconfigure(0, weight=1)
        self.tabview.tab(tab4).grid_columnconfigure(2, weight=1)
        self.tabview.tab(tab4).grid_rowconfigure(1, weight=1)
        
        self.graph_selector_value = tk.StringVar()
        self.graph_selector_value.set("Best Cost Stacked")
        self.graph_selector = customtkinter.CTkOptionMenu(self.tabview.tab(tab4), values=["Best Cost Stacked", "Best Cost by Round", "Calibrated Parameters", "Table"], variable=self.graph_selector_value, command=self.update_graph)
        self.graph_selector.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Add a button to call open_graph_in_browser
        self.graph_button = customtkinter.CTkButton(self.tabview.tab(tab4), text="Open Graph in Browser", command=self.open_graph_in_browser)
        self.graph_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        #CTkToolTip(self.graph_button, delay=0.5, message="Open graph in browser...")
        
        
        self.graph_image_obj = Image.open(os.path.join("./images", "up.png"))
        self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(700, 500))
        self.graph_label = customtkinter.CTkLabel(self.tabview.tab(tab4), text=None, image=self.graph_image)
        self.graph_label.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        #window = customtkinter.CTk()
        self.graph_label.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
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

    def callback_test(self, *args):
        print("callback_test called")
            
    def update_graph(self, value):
        selected_graph = self.graph_selector_value.get()
        info = self.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        if (selected_graph == "Best Cost Stacked"):
            self.selected_graph_name = "best_cost_stacked"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Best Cost by Round"):
            self.selected_graph_name = "best_cost_by_round"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Table"):
            self.selected_graph_name = "table"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Calibrated Parameters"):
            self.selected_graph_name = "calibrated_params_by_round"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
            
    def save_project(self):
        metrics = self.option_manager.get_metrics()
        filename = asksaveasfilename(filetypes=[("JSON", "*.json")], initialfile="config", defaultextension="json", title="Save Project")
        
        try:
        
            # Convert metrics to json and save to file with proper spacing
            with open(filename, "w") as f:
                f.write(json.dumps(metrics, indent=4))
                
            self.save_button.configure(text="Saved!")
            self.after(3000, lambda: self.save_button.configure(text="Save"))
        except Exception as e:
            self.save_button.configure(text="Error!")
            print(e)
            self.after(3000, lambda: self.save_button.configure(text="Save"))
    
    def new_window(self):
        # Shell out and run ./main.py
        subprocess.Popen(["python3", "../mgpsogui.py"])
    
    def load_project(self):
        
        filename = askopenfilename(filetypes=[("JSON", "*.json")], title="Open Project", multiple=False)
        print(filename)
        
        try:
        
            # Load config.json and convert to metrics
            with open(filename, "r") as f:
                metrics = json.loads(f.read())
            
            self.option_manager.set_path(filename)
            
            if "arguments" in metrics:
                metrics["arguments"]["calibration_parameters"] = metrics["calibration_parameters"]
            
            if "service_parameters" in metrics:
                self.option_manager.set_service_parameters(metrics["service_parameters"])
                self.tabview.configure(state="enabled")
            
            print(metrics)
            
            self.option_manager.clear()
            self.option_manager.add_arguments(metrics["arguments"])
            self.option_manager.add_steps(metrics["steps"])
            
            self.steps_frame.clear()
            self.steps_frame.render()

            self.static_param_frame.clear()
            self.static_param_frame.render()
            
            self.calib_param_frame.clear()
            self.calib_param_frame.render()
            
            self.load_button.configure(text="Loaded!")
            self.after(3000, lambda: self.load_button.configure(text="Load"))
            
        except Exception as e:
            print(e)
            self.load_button.configure(text="Error!")
            self.after(3000, lambda: self.load_button.configure(text="Load"))

    def open_graph_in_browser(self):
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

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

def start():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()
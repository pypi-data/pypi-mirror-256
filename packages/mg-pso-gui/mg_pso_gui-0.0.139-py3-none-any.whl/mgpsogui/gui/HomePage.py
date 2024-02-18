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
        
        """self.tabview.tab(tab2).grid_columnconfigure(0, weight=8)
        self.tabview.tab(tab2).grid_columnconfigure(1, weight=1)
        self.tabview.tab(tab2).grid_rowconfigure(0, weight=1)
        self.tabview.tab(tab2).grid_rowconfigure(1, weight=1)
        
        self.steps_frame = sv.StepView(self.tabview.tab(tab2), label_text="Group Editor", option_manager=self.option_manager)
        self.steps_frame.grid(row=0, rowspan=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.steps_frame.grid_columnconfigure(0, weight=1)
        self.steps_frame.grid_rowconfigure(0, weight=1)
        
        self.static_param_frame = spv.StaticParameterView(self.tabview.tab(tab2), label_text="Static Parameters", option_manager=self.option_manager)
        self.static_param_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.static_param_frame.grid_columnconfigure(0, weight=1)
        self.static_param_frame.grid_rowconfigure(0, weight=1)
        
        self.calib_param_frame = cpv.CalibrationParametersView(self.tabview.tab(tab2), label_text="Calibration Parameters", option_manager=self.option_manager)
        self.calib_param_frame.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.calib_param_frame.grid_columnconfigure(0, weight=1)
        self.calib_param_frame.grid_rowconfigure(0, weight=1)
        """
        
        # URL
        
        self.tabview.tab(tab3).grid_columnconfigure(0, weight=1)
        self.tabview.tab(tab3).grid_rowconfigure(0, weight=1)
        self.tabview.tab(tab3).grid_rowconfigure(1, weight=1)
        self.tabview.tab(tab3).grid_rowconfigure(2, weight=200)
        self.url = customtkinter.CTkEntry(self.tabview.tab(tab3), textvariable=self.option_manager.get_arguments()['url'])
        self.url.grid(row=0, column=0, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.run_button = customtkinter.CTkButton(self.tabview.tab(tab3), text="Run", command=self.run)
        self.run_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        ctt(self.run_button, delay=0.5, message="Start calibration...")
        
        
        self.stop_button = customtkinter.CTkButton(self.tabview.tab(tab3), text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        ctt(self.stop_button, delay=0.5, message="Stop calibration...")
        
        self.progress_container = customtkinter.CTkFrame(self.tabview.tab(tab3))
        self.progress_container.grid_columnconfigure(0, weight=1)
        self.progress_container.grid_columnconfigure(1, weight=1)
        self.progress_container.grid_columnconfigure(2, weight=1)
        self.progress_container.grid(row=1, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Add progress bar to progress container
        self.progress_message_left = customtkinter.CTkLabel(self.progress_container, text="")
        self.progress_message_left.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
        
        self.progress_message_middle = customtkinter.CTkLabel(self.progress_container, text="Calibration not running...")
        self.progress_message_middle.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        
        self.progress_message_right = customtkinter.CTkLabel(self.progress_container, text="")
        self.progress_message_right.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="e")
        
        self.progress_bar = customtkinter.CTkProgressBar(self.progress_container)
        self.progress_bar.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.progress_bar.set(0)
        ctt(self.progress_bar, delay=0.5, message="Current calibration progress")
        
        self.textbox = customtkinter.CTkTextbox(self.tabview.tab(tab3))
        self.textbox.grid(row=2, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0", "Welcome to the CSIP PSO Calibration Tool!\n\nUse the Calibration tab to define steps and calibration parameters. Use this tab to run and observe calibration progress. Once finished, use the Visualization tab to generate figures and graphs.")
        
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
            

    def run(self):
        metrics = self.option_manager.get_metrics()
        self.running_config = metrics
        
        self.progress_bar.configure(mode="indeterminnate")
        self.progress_bar.start()
        
        self.data_x = [0]
        self.data_y = [0]
        
        self.progress_message_middle.configure(text="Calibration starting...")
        
        self.textbox.insert("0.0", "Starting calibration...\n\n")
        self.textbox.insert("0.0", "Calibration Parameters:\n")
        self.textbox.insert("0.0", json.dumps(metrics, indent=4) + "\n\n")
        try:
            info = self.option_manager.get_project_data()
            folder = os.path.join(info['path'], info['name'])
            
            
            self.train_process = Process(target=PSORunner.run_process, args=(metrics, folder))
            self.train_process.daemon = True
            self.train_process.start()
            self.after(1000, self.watch_loop)
            self.string_cache = ""
            self.data_cache = ""
            
        except Exception as e:
            self.textbox.insert("0.0", "An exception occurred!\n Exception: " + str(e) + "\n\n")
            self.textbox.insert("0.0", "Stack trace:\n")
            self.textbox.insert("0.0", traceback.format_exc())
            self.textbox.insert("0.0", "\n\n")
            self.textbox.insert("0.0", "Calibration failed!")
            self.progress_message_left.configure(text="")
            self.progress_message_middle.configure(text="Calibration failed! See error log below.")
            self.progress_message_right.configure(text="")
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.set(0)
            
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
        
            
    def watch_loop(self):
        # Check if file exists:
        
        info = self.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
            
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        if (os.path.exists(os.path.join(folder, 'output.txt'))):
            with open(os.path.join(folder, 'output.txt'), 'r') as f:
                lines = f.readlines()
                lines_string = "".join(lines)
                
                new_characters = lines_string.replace(self.string_cache, "")
                # Update the textbox with characters not in self.string_cache
                self.textbox.insert('0.0', new_characters)
                self.string_cache = lines_string
                print(new_characters, end="")
                
            try:
                with open(os.path.join(folder, "output.txt"), "r") as f:
                    text = f.read()

                calibrated_params_pattern = r"calibrated params: ({.*?})"
                best_particle_values_pattern = r"best particle values: (\[.*?\])"
                progress_pattern = r"Progress -  best_round_cost:(.*?), rel_round_tol:(.*?), rtol:(.*?)\n"

                calibrated_params = re.findall(calibrated_params_pattern, text)
                best_particle_values = re.findall(best_particle_values_pattern, text)
                progress_values = re.findall(progress_pattern, text)

                for index, pp in enumerate(best_particle_values):
                    pp = pp.strip()
                    pp = pp.replace('[ ', '[')
                    pp = pp.replace('  ', ',')
                    pp = pp.replace(' ', ',')
                    best_particle_values[index] = pp

                calibrated_params = [ast.literal_eval(i) for i in calibrated_params]
                best_particle_values = [ast.literal_eval(i) for i in best_particle_values]
                progress_values = [tuple(map(float, i)) for i in progress_values]
                
                print(calibrated_params)
                
                GraphGenerator.calibrated_params_by_round(self.running_config['steps'], calibrated_params, self.option_manager)
                self.update_graph("")
            except Exception as e:
                # Print stack trace
                traceback.print_exc()
                
                print(e)
                
        if (os.path.exists(os.path.join(folder, 'error.txt'))):
            with open(os.path.join(folder, 'error.txt'), 'r') as f:
                lines = f.readlines()
                lines_string = "".join(lines)
                self.data_cache = lines_string
                
                pattern = r'(\d+)%\|.*\|(\d+)/(\d+)(?:,\sbest_cost=(\d+\.\d+))?' # The magic of AI
                matches = re.findall(pattern, self.data_cache)
                filtered_matches = [match for match in matches if match[3] != '']
                matches = filtered_matches

                if len(matches) > 0:
                    df = pd.DataFrame(matches, columns=['percent', 'completed_rounds', 'total_rounds', 'best_cost'], dtype=float)
                    df = df[df['best_cost'] != '']
                    df = df.dropna()
                    df = df.drop_duplicates()
                    df['round_step'] = (df['completed_rounds'].diff() < 0).cumsum()
                    df = df.drop_duplicates(subset=['completed_rounds', 'round_step'])

                    GraphGenerator.best_cost_stacked(self.running_config['steps'], df, self.option_manager)
                    GraphGenerator.best_cost_by_round(self.running_config['steps'], df, self.option_manager)
                    GraphGenerator.table(self.running_config['steps'], df, self.option_manager)
                    self.update_graph("")

                    match = matches[-1]
                    percent = int(match[0])
                    completed_rounds = int(match[1])
                    total_rounds = int(match[2])
                    best_cost = float(match[3]) if match[3] else None
                    
                    if (percent > 0):
                        self.progress_bar.stop()
                        self.progress_bar.configure(mode="determinate")
                        self.progress_bar.set(percent/100)
                        self.progress_message_left.configure(text="Percent Complete: " + str(percent) + "%")
                        self.progress_message_middle.configure(text=str(completed_rounds) + "/" + str(total_rounds))
                        self.progress_message_right.configure(text="Best Cost: " + str(best_cost))
                    else:
                        self.progress_bar.configure(mode="indeterminate")
                        self.progress_bar.start()
                        self.progress_message_left.configure(text="")
                        self.progress_message_middle.configure(text="Starting new round...")
                        self.progress_message_right.configure(text="")
                
                
                
        if self.train_process.is_alive():
            self.after(1000, self.watch_loop)
        else:
            self.progress_bar.stop()
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
            self.progress_message_left.configure(text="")
            self.progress_message_middle.configure(text="Calibration finished!")
            self.progress_message_right.configure(text="")
            self.textbox.insert("0.0", "\nCalibration finished!\n")

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

    def stop(self):
        print("Stopping...")
        self.train_process.terminate()
        
        info = self.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
            
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Stop the process
        if (os.path.exists(os.path.join(folder, 'output.txt'))):
            os.remove(os.path.join(folder, 'output.txt'))
        
        if (os.path.exists(os.path.join(folder, 'error.txt'))):
            os.remove(os.path.join(folder, 'error.txt'))
            
        self.textbox.insert("0.0", "\nCalibration terminated!\n")
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(0)
        self.progress_message_left.configure(text="")
        self.progress_message_middle.configure(text="Calibration stopped!")
        self.progress_message_right.configure(text="")


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
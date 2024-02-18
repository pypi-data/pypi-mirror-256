
import customtkinter
import json
import os
from multiprocessing import Process
import traceback
import re
import ast
import pandas as pd
import numpy as np

from ...util import PSORunner
from ...util import GraphGenerator
from ...util.CTkToolTip import CTkToolTip as ctt

def create_tab(self, tab):
    
    def run():
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
            self.after(1000, watch_loop)
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
            
    def stop():
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
        
    def watch_loop():
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
            self.after(1000, watch_loop)
        else:
            self.progress_bar.stop()
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
            self.progress_message_left.configure(text="")
            self.progress_message_middle.configure(text="Calibration finished!")
            self.progress_message_right.configure(text="")
            self.textbox.insert("0.0", "\nCalibration finished!\n")
    
    # URL
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_rowconfigure(0, weight=1)
    tab.grid_rowconfigure(1, weight=1)
    tab.grid_rowconfigure(2, weight=200)
    self.url = customtkinter.CTkEntry(tab, textvariable=self.option_manager.get_arguments()['url'])
    self.url.grid(row=0, column=0, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

    self.run_button = customtkinter.CTkButton(tab, text="Run", command=run)
    self.run_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    ctt(self.run_button, delay=0.5, message="Start calibration...")
    
    
    self.stop_button = customtkinter.CTkButton(tab, text="Stop", command=stop)
    self.stop_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    ctt(self.stop_button, delay=0.5, message="Stop calibration...")
    
    self.progress_container = customtkinter.CTkFrame(tab)
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
    
    self.textbox = customtkinter.CTkTextbox(tab)
    self.textbox.grid(row=2, column=0, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.textbox.insert("0.0", "Welcome to the CSIP PSO Calibration Tool!\n\nUse the Calibration tab to define steps and calibration parameters. Use this tab to run and observe calibration progress. Once finished, use the Visualization tab to generate figures and graphs.")
        
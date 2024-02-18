from . import StepView as sv
from . import StaticParameterView as spv
from . import CalibrationParametersView as cpv

import customtkinter

def create_tab(self, tab, option_manager):
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(1, weight=1)
    
    self.top_bar_container = customtkinter.CTkFrame(tab)
    self.top_bar_container.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.top_bar_container.grid_columnconfigure(1, weight=1)
    
    cl = customtkinter.CTkLabel(self.top_bar_container, text="Service URL:", anchor="w")
    cl.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="ew")
    
    self.service_url = customtkinter.CTkEntry(self.top_bar_container, textvariable=option_manager.get_arguments()['url'])
    self.service_url.grid(row=0, column=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    self.load_parameters = customtkinter.CTkButton(self.top_bar_container, text="Connect", command=self.load)
    self.load_parameters.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
            
    self.service_editor = customtkinter.CTkScrollableFrame(tab, label_text="Service Editor")
    self.service_editor.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.service_editor.grid_columnconfigure(0, weight=1)
    self.service_editor.grid_rowconfigure(0, weight=1)
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Status:", anchor="w")
    cl.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_status = customtkinter.CTkTextbox(self.service_editor, height=32)
    self.service_status.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Name:", anchor="w")
    cl.grid(row=3, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_name = customtkinter.CTkTextbox(self.service_editor, height=32)
    self.service_name.grid(row=4, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Description:", anchor="w")
    cl.grid(row=5, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_description = customtkinter.CTkTextbox(self.service_editor, height=32)
    self.service_description.grid(row=6, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.service_editor, text="Service Details:", anchor="w")
    cl.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.service_details = customtkinter.CTkTextbox(self.service_editor, height=480)
    self.service_details.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.environment_editor = customtkinter.CTkScrollableFrame(tab, label_text="Environment Editor")
    self.environment_editor.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.environment_editor.grid_columnconfigure(0, weight=1)
    self.environment_editor.grid_rowconfigure(0, weight=1)
    
    cl = customtkinter.CTkLabel(self.environment_editor, text="Cluster Preset:", anchor="w")
    cl.grid(row=0, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.preset_selector = customtkinter.CTkOptionMenu(self.environment_editor, values=["Local", "Other"])
    self.preset_selector.grid(row=1, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.environment_editor, text="Controls:", anchor="w")
    cl.grid(row=2, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.start_cluster_button = customtkinter.CTkButton(self.environment_editor, text="Start Minikube", command=self.start_cluster)
    self.start_cluster_button.grid(row=3, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
    
    # Check if the os is MacOS
    if (platform.system() == "Darwin"):
        self.create_environment_button = customtkinter.CTkButton(self.environment_editor, text="Create Environment", command=self.open_terminal_and_run_cluster)
    else:
        self.create_environment_button = customtkinter.CTkButton(self.environment_editor, text="Copy Command", command=self.deploy_cluster)
        
    self.create_environment_button.grid(row=4, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
    
    self.get_status = customtkinter.CTkButton(self.environment_editor, text="Minikube Status", command=self.cluster_status)
    self.get_status.grid(row=5, column=0, padx=(20, 20), pady=(5, 10), sticky="ew")
    
    self.destroy_environment_button = customtkinter.CTkButton(self.environment_editor, text="Stop Minikube", command=self.stop_cluster)
    self.destroy_environment_button.grid(row=6, column=0, padx=(20, 20), pady=(5,10), sticky="ew")
    
    cl = customtkinter.CTkLabel(self.environment_editor, text="Minikube Status:", anchor="w")
    cl.grid(row=7, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
    self.custer_details = customtkinter.CTkTextbox(self.environment_editor, height=480)
    self.custer_details.grid(row=8, column=0, padx=(20, 20), pady=(5, 5), sticky="ew")
    
def load(self):
    # Make HTTP request to service_url and save the result to bounds.json
    self.load_parameters.configure(text="Loading...")
    self.after(10, self.make_request)
    self.after(3000, lambda: self.load_parameters.configure(text="Connect"))
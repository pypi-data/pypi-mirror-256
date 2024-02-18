

from . import StepView as sv
from . import StaticParameterView as spv
from . import CalibrationParametersView as cpv

def create_tab(self, tab):
    
    tab.grid_columnconfigure(0, weight=8)
    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(0, weight=1)
    tab.grid_rowconfigure(1, weight=1)
    
    self.steps_frame = sv.StepView(tab, label_text="Group Editor", option_manager=self.option_manager)
    self.steps_frame.grid(row=0, rowspan=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
    self.steps_frame.grid_columnconfigure(0, weight=1)
    self.steps_frame.grid_rowconfigure(0, weight=1)
    
    self.static_param_frame = spv.StaticParameterView(tab, label_text="Static Parameters", option_manager=self.option_manager)
    self.static_param_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
    self.static_param_frame.grid_columnconfigure(0, weight=1)
    self.static_param_frame.grid_rowconfigure(0, weight=1)
    
    self.calib_param_frame = cpv.CalibrationParametersView(tab, label_text="Calibration Parameters", option_manager=self.option_manager)
    self.calib_param_frame.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
    self.calib_param_frame.grid_columnconfigure(0, weight=1)
    self.calib_param_frame.grid_rowconfigure(0, weight=1)
    
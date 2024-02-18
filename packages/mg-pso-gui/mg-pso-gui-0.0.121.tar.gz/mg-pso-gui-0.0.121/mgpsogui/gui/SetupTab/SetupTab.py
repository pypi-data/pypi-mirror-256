

from . import StepView as sv
from . import StaticParameterView as spv
from . import CalibrationParametersView as cpv
from . import OptionManager as om

def create_tab(root, tab, option_manager):
    
    tab.grid_columnconfigure(0, weight=8)
    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(0, weight=1)
    tab.grid_rowconfigure(1, weight=1)
    
    root.steps_frame = sv.StepView(tab, label_text="Group Editor", option_manager=option_manager)
    root.steps_frame.grid(row=0, rowspan=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
    root.steps_frame.grid_columnconfigure(0, weight=1)
    root.steps_frame.grid_rowconfigure(0, weight=1)
    
    root.static_param_frame = spv.StaticParameterView(tab, label_text="Static Parameters", option_manager=option_manager)
    root.static_param_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
    root.static_param_frame.grid_columnconfigure(0, weight=1)
    root.static_param_frame.grid_rowconfigure(0, weight=1)
    
    root.calib_param_frame = cpv.CalibrationParametersView(tab, label_text="Calibration Parameters", option_manager=option_manager)
    root.calib_param_frame.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
    root.calib_param_frame.grid_columnconfigure(0, weight=1)
    root.calib_param_frame.grid_rowconfigure(0, weight=1)
    
#

import tkinter as tk
import threading

from vision_oslo_extension.shared_contents import SharedVariables, Local_Shared, SharedMethods
from vision_oslo_extension.base_frame import BasePage

# Basic Information Summary
class C01(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        SharedVariables.main_option = "1"

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 1: Basic Information Summary',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce various summary reports inlcuding branch list, supply point list, transformer list and errors or warnings summary. This process should be fairly quick.',aspect = 1200, font = controller.text_font)
        explain.pack()

        button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_model_check(),width = 20, height =2)
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row = 0, column = 1)

    def run_model_check(self):
        try:
            # so that sim_name is updated when clicked
            sim_name = SharedVariables.sim_variable.get() # call variables saved in a shared places.
            main_option = SharedVariables.main_option
            time_start = Local_Shared.time_start
            time_end = Local_Shared.time_end
            option_select = Local_Shared.option_select
            text_input = Local_Shared.text_input
            low_v = Local_Shared.low_threshold
            high_v = Local_Shared.high_threshold
            time_step = Local_Shared.time_step

            # Run the batch processing function in a separate thread
            thread = threading.Thread(target=SharedMethods.common_thread_run, 
                                      args=("model_check.py",sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step))
            thread.start()
        
        except Exception as e:
            print("Error in threading...Contact Support / Do not carry out multiple tasking at the same time. ", e)

# Low Voltage Analysis Report
class C02(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        SharedVariables.main_option = "2"

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 2: Connection Report',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'This will produce two tables. One showing the connection of all nodes. One showing all connected nodes from the supply points.',aspect = 1200, font = controller.text_font)
        explain.pack()

        button = tk.Button(master=self.excuteframe, text="RUN!", command = lambda: self.run_model_check(),width = 20, height =2)
        button.pack()


        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row = 0, column = 1)


    def run_model_check(self):
        try:
            # so that sim_name is updated when clicked
            sim_name = SharedVariables.sim_variable.get() # call variables saved in a shared places.
            main_option = SharedVariables.main_option
            time_start = Local_Shared.time_start
            time_end = Local_Shared.time_end
            option_select = Local_Shared.option_select
            text_input = Local_Shared.text_input
            low_v = Local_Shared.low_threshold
            high_v = Local_Shared.high_threshold
            time_step = Local_Shared.time_step

            # Run the batch processing function in a separate thread
            thread = threading.Thread(target=SharedMethods.common_thread_run, 
                                      args=("model_check.py",sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step))
            thread.start()
        
        except Exception as e:
            print("Error in threading...Contact Support / Do not carry out multiple tasking at the same time. ", e)

# One stop AC power prepare
class C03(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        SharedVariables.main_option = "3"

        self.headframe = self.create_frame(fill=tk.BOTH)
        
        self.optionframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1))
        self.inputframe = self.create_frame(fill=tk.BOTH, row_weights=(1, 1, 1, 1), column_weights=(1, 1, 1, 1))

        self.excuteframe = self.create_frame(fill=tk.BOTH)

        self.infoframe = self.create_frame(fill=tk.BOTH, column_weights=(1, 1))

        # add widgets here
        head = tk.Label(master=self.headframe, text = 'Page 3: Development in Progress',font = controller.sub_title_font)
        head.pack()

        explain = tk.Message(master=self.headframe, text = 'Pending',aspect = 1200, font = controller.text_font)
        explain.pack()
        button = tk.Button(master=self.excuteframe, text="RUN!", command=lambda: controller.show_frame("PageTwo"),width = 20, height =2)
        button.pack()

        button1 = tk.Button(master=self.infoframe, text="Back to Home", command=lambda: controller.show_frame("StartPage"))
        button1.grid(row = 0, column = 0)
        button2 = tk.Button(master=self.infoframe, text="Back to Processing", command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row = 0, column = 1)


    def run_model_check(self):
        try:
            # so that sim_name is updated when clicked
            sim_name = SharedVariables.sim_variable.get() # call variables saved in a shared places.
            main_option = SharedVariables.main_option
            time_start = Local_Shared.time_start
            time_end = Local_Shared.time_end
            option_select = Local_Shared.option_select
            text_input = Local_Shared.text_input
            low_v = Local_Shared.low_threshold
            high_v = Local_Shared.high_threshold
            time_step = Local_Shared.time_step

            # Run the batch processing function in a separate thread
            thread = threading.Thread(target=SharedMethods.common_thread_run, 
                                      args=("model_check.py",sim_name, main_option, time_start, time_end, option_select, text_input, low_v, high_v, time_step))
            thread.start()
        
        except Exception as e:
            print("Error in threading...Contact Support / Do not carry out multiple tasking at the same time. ", e)


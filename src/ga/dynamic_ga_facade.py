from utils.wcet_data import WcetData
from utils.intermediate_values import IntermediateValues
from utils.user_project import UserProject

from inputs.input_manager import InputManager
from interface_target.interface_target import InterfaceTarget

from ga.dynamic_ga import *
from evt.evt_method import Evt, evt_running
import os
import pandas as pd
from progress.bar import Bar


class DynamicGaFacade:
    """
    Class for estimating the Worst-Case Execution Time (WCET) of a program.

    This class encapsulates the logic for calculating WCET using the Genetic Algorithm with dynamic measurements.


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    project : UserProject
        Contain all information about project


    wcet : WcetData
        Contain all information about wcet
    """

    def __init__(self, project: UserProject, wcet: WcetData) -> None:
        self.project = project
        self.wcet = wcet

    def run(self) -> None:
        '''
        Dynamic GA pipeline for calculate pWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        inter_values = IntermediateValues()
        interface_target = InterfaceTarget(
            project=self.project, inter_values=inter_values)
        input_manager = InputManager(project=self.project,
                                     inter_values=inter_values)

        ga = GA(project=self.project, input_manager=input_manager,
                interface_target=interface_target, inter_values=inter_values)

        if self.project.board == False:
            interface_target.set_ga_filenames()
            interface_target.compile_io_ports()
            interface_target.compile_tick_counter()
            interface_target.compile_to_ir()
            interface_target.link()
            interface_target.compile_to_obj()
            interface_target.compile_to_asm()
            interface_target.backend_compile()

        if self.project.get_flash_board():
            pass
        else:
            interface_target.flash()

        ga.instanciate_dynamic_ga()
        ga.run()
        solution = ga.best_solution()

        results_exec = evt_running(self.project, self.wcet, interface_target, solution)
        if results_exec is None:
            return
        
        # Save the list with all runs results to a csv file.
        csv_filename = os.path.join(
            self.project.output_directory,
            f"{self.project.main_file_name}_{self.project.number_exec}.csv")

        
        results_exec = pd.DataFrame(results_exec)
        results_exec.to_csv(csv_filename, index=False, header=False)

        # EVT Method Instantiation and call
        evt = Evt(self.project, csv_filename)

        try:
            pwcet_list, iid_flag, rawdata_df = Evt.run(evt)
        except Exception as e:
            print(
                f"\n\33[41mError running EVT! {e}\33[0m")
            exit(-1)

        # Transmits the results to the report
        self.wcet.set_pwcet(pwcet_list)
        self.wcet.set_hwm(rawdata_df.valuesx.max())
        self.wcet.set_iid_flag(iid_flag)
        self.wcet.set_histogram(rawdata_df)

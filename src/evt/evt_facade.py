from utils.user_project import UserProject
from utils.wcet_data import WcetData
from pprint import pprint
from interface_target.interface_target import InterfaceTarget
from utils.intermediate_values import IntermediateValues
from inputs.input_manager import InputManager
import pandas as pd
import os.path
from evt.evt_method import Evt, evt_running



class EvtFacade:
    """
    Class for estimating the Probabilistic Worst-Case Execution Time (pWCET) of a program using EVT.


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
        pprint(vars(project))

    def run(self) -> None:
        """
        Method that instantiate the EVT runs with the target interface and later EVT analysis.


        Parameters
        ----------
            None


        Returns
        ----------
            None
        """

        inter_values = IntermediateValues()

        input_manager = InputManager(project=self.project,
                                     inter_values=inter_values)

        interface_target = InterfaceTarget(
            project=self.project, inter_values=inter_values)

        # Decides the input generation or use of a previous one already defined
        if input_manager.generator:
            inter_values.test_cases = input_manager.generate_inputs()
        else:
            inter_values.test_cases = [self.project.chosen_input]

        # If runnig in the simulator target does the necessary compilation, otherwise runnig on real targets, does not compile.
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

        # Selects the first(which should be unique) test case to run and sends it to the interface target
        # Captures the output filtering the line that starts with #cycles.
        # Adds result to the output list with the execution time obtained

        args = inter_values.test_cases[0]
        results_exec = evt_running(self.project, self.wcet, interface_target, args)
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


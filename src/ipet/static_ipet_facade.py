from utils.wcet_data import WcetData
from utils.intermediate_values import IntermediateValues
from utils.user_project import UserProject
from utils.create_files import *
from cfg.graph_generator import *
from cfg.pre_processor import *
from cfg.graph_weight import *
from ipet.ipet import *


class StaticIpetFacade:
    """
    Class for estimating the Worst-Case Execution Time (WCET) of a program.

    This class encapsulates the logic for calculating WCET using the IPET with all analyzes statically.


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
        Fully Static IPET pipeline for calculate sWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        intermediate_values = IntermediateValues()
        create_ir(self.project, intermediate_values)
        create_call_graph(self.project, intermediate_values)
        loop_mapping(intermediate_values)
        loop_bounding(intermediate_values)
        functions_mapping(intermediate_values)
        create_call_graph_in_post_order(intermediate_values)
        graph = {}
        graph_generator_post_order(intermediate_values, graph)
        ipet = Ipet(graph, self.project)
        self.wcet.set_swcet(ipet.run_ipet_static())

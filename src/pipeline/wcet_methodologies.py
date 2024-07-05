from abc import ABC, abstractmethod

from utils.user_project import UserProject
from utils.wcet_data import WcetData
from report_generator.report import Report

from ipet.static_ipet_facade import StaticIpetFacade
from ipet.hybrid_ipet_facade import HybridIpetFacade
from constraint_solver.wpevt_facade import WpevtFacade
from ga.dynamic_ga_facade import DynamicGaFacade
from evt.evt_facade import EvtFacade


# ----------------------------------#
#           BUILDER                 #
# ----------------------------------#

class WcetBuilder(ABC):
    """
    Create the same interface for all methodologies.


    Parameters
    ----------
        None


    Attributes
    ----------
        None
    """
    @abstractmethod
    def __init__(self, user_project: UserProject) -> None:
        raise NotImplementedError

    @abstractmethod
    def run_procedure(self):
        '''
        All Methodologies must implement run_procedure method. This method is used to execute the methodology pipeline.

        If one concrete class not implement this interface, raise "NotImplementedError" exception.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        raise NotImplementedError

    def generate_results(self):
        '''
        All Methodologies must implement generate_results method. This method is used to generate report file.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        reportes_created = 0
        report = Report(self.user_project, self.wcet)
        if ("pdf" in self.user_project.get_report_format()):
            report.create_pdf_report()
            reportes_created += 1

        if ("json" in self.user_project.get_report_format()):
            report.create_json_report()
            reportes_created += 1

        # Raises warning if report wasn't created
        if (reportes_created == 0):
            print("\33[43mWarning! No report was created!\33[0m")
            print("The WCET calculated was:")
            print("iWCET: ", self.wcet.get_swcet())
            print("pWCET: ", self.wcet.get_pwcet())
            print("High Water-Mark: ", self.wcet.get_hwm())
        print("\33[42mAnalysis completed!\33[0m")


# ----------------------------------#
#      CONCRETE CLASSES             #
# ----------------------------------#
class StaticIpet(WcetBuilder):
    """
    Class for organize the pipeline of methodology Static IPET.


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    project : UserProject
        Contain all information about project


    wcet : WcetData
        Contain all information about WCET
    """

    def __init__(self, user_project: UserProject) -> None:
        self.user_project = user_project
        self.wcet = WcetData("Static IPET")

    def run_procedure(self):
        '''
        Execute the pipeline of Static IPET and calculate the sWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        run_ipet = StaticIpetFacade(self.user_project, self.wcet)
        run_ipet.run()




##########################################################################################################


class HybridIpet(WcetBuilder):
    """
    Class for organize the pipeline of methodology Hybrid IPET.


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    project : UserProject
        Contain all information about project


    wcet : WcetData
        Contain all information about WCET
    """

    def __init__(self, user_project: UserProject) -> None:
        self.user_project = user_project
        self.wcet = WcetData("Hybrid IPET")

    def run_procedure(self):
        '''
        Execute the pipeline of Hybrid IPET and calculate the sWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        run_ipet = HybridIpetFacade(self.user_project, self.wcet)
        run_ipet.run()




##########################################################################################################


class Wpevt(WcetBuilder):
    """
    Class for organize the pipeline of methodology Worst Path EVT.


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    project : UserProject
        Contain all information about project


    wcet : WcetData
        Contain all information about WCET
    """

    def __init__(self, user_project: UserProject) -> None:
        self.user_project = user_project
        self.wcet = WcetData("WPEVT")

    def run_procedure(self):
        '''
        Execute the pipeline of Worst Path EVT and calculate the sWCET and pWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        worst_path = WpevtFacade(self.user_project, self.wcet)
        worst_path.run()




##########################################################################################################


class DynamicGa(WcetBuilder):
    """
    Class for organize the pipeline of methodology Dynamic Ga.


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    project : UserProject
        Contain all information about project


    wcet : WcetData
        Contain all information about WCET
    """

    def __init__(self, user_project: UserProject) -> None:
        self.user_project = user_project
        self.wcet = WcetData("Dynamic GA")

    def run_procedure(self):
        '''
        Execute the pipeline of Dynamic Ga and calculate the pWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        ga_facade = DynamicGaFacade(self.user_project, self.wcet)
        ga_facade.run()




##########################################################################################################


class Evt(WcetBuilder):
    """
    Class for organize the pipeline of methodology EVT.


    Parameters
    ----------
    project : UserProject
        Contain all information about project


    Attributes
    ----------
    project : UserProject
        Contain all information about project


    wcet : WcetData
        Contain all information about WCET
    """

    def __init__(self, user_project: UserProject) -> None:
        self.user_project = user_project
        self.wcet = WcetData("EVT")

    def run_procedure(self):
        '''
        Execute the pipeline of EVT and calculate the pWCET.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        evt_concrete = EvtFacade(self.user_project, self.wcet)  
        evt_concrete.run()
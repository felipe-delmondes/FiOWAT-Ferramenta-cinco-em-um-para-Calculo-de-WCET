from datetime import datetime
from pandas import DataFrame

class WcetData():
    """
    DTO of WCET calculated by methodology.

    
    Parameters
    ----------
        None

        
    Attributes
    ----------
    technique_name : str
        Technique name used to calculate WCET. This name is used to report

        Example: Static IPET

    swcet : float
        Time in cycles of Static WCET (sWCET). This WCET was calculated by analyzing the code (source code or IR)

    pwcet : list
        Time in cycles of Probabilistic WCET (pWCET). This WCET was calculated by executing the program.

        This value is a tuple with probability of exceedance and its respective pWCET.

        Example: [(1E-9, 75000), (1E-10, 100000)]

    hwm : float
        Time in cycles of High-Water Mark. The largest measurement observed during analyzes
    
    iid_flag : str
        Independency and identically distribution of data (IID) tests warning. 
        
        Options: Ok, passed | Failed, review data set. (LJung-box not passed)
    
    histogram : Dataframe
        Cycles histogram, from EVT methodology runs. To access this histogram: dataframe.values
    
    worst_input : list
        Input set that generate the WCET

        Example: [10, 9, 8]

    analysis_start_time : str
        Date when analysis start. Example: 2023/07/12 - 20:15
    """
    def __init__(self, method_name) -> None:
        self.technique_name = method_name
        self.swcet = 0.0
        self.pwcet = []
        self.hwm = 0
        self.iid_flag = ""
        self.histogram = None
        self.worst_input = None
        self.analysis_start_time = datetime.now().strftime("%Y/%m/%d - %H:%M:%S.%f")
    

    def __str__(self) -> str:
        return "*** WCET result ***" + \
                "\nTechnique: " + self.technique_name + \
                "\nAnalysis start time: " + self.analysis_start_time + \
                "\nStatic WCET: " + str(self.swcet) + \
                "\nProbabilistic WCET: " + str(self.pwcet) + \
                "\nHigh-Water Mark: " + str(self.hwm) + \
                "\nIID flag: " + self.iid_flag + \
                "\Worst Input: " + str(self.worst_input)


    #Getters
    def get_technique_name(self) -> str:
        return self.technique_name

    def get_swcet(self) -> float:
        return self.swcet

    def get_pwcet(self) -> list:
        return self.pwcet
    
    def get_hwm(self) -> float:
        return self.hwm

    def get_iid_flag(self) -> str:
        return self.iid_flag
    
    def get_histogram(self) -> DataFrame:
        return self.histogram

    def get_worst_input(self) -> list:
        return self.worst_input

    def get_analysis_start_time(self) -> str:
        return self.analysis_start_time



    #Setters
    def set_swcet(self, swcet: float) -> None:
        self.swcet = swcet
    
    def set_pwcet(self, pwcet: list) -> None:
        self.pwcet = pwcet
    
    def set_hwm(self, hwm: float) -> None:
        self.hwm = hwm

    def set_iid_flag(self, iid_flag : str) -> None:
        self.iid_flag = iid_flag
    
    def set_histogram(self, histogram : DataFrame) -> None:
        self.histogram = histogram

    def set_worst_input(self, worst_input: list) -> None:
        self.worst_input = worst_input




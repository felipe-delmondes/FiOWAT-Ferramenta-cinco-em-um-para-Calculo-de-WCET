from pipeline.wcet_methodologies import *
from pipeline.config_parser import ConfigParser


class Director():
    '''
    Control the instantiation process of specific methodology

    
    Parameters
    ----------
    config_path : str
        Absolute directory of config.yaml file. Example: C:\\Users\\Mario\\Desktop\\config.yaml

        
    Attributes
    ----------
    __config_parser : ConfigParser
        Object responsible to reading and check the config.yaml file

    methodology_facade : WcetBuilder
        Pointer to an object that represent specific methodology
    '''
    def __init__(self, config_path : str) -> None:
        print("Reading the config.yaml...", sep=" ")
        self.__config_parser = ConfigParser(config_path)
        self.__config_parser.run_config_parser()
        self.methodology_facade = {"static_ipet":   StaticIpet,
                                   "hybrid_ipet":   HybridIpet,
                                   "wpevt":         Wpevt,
                                   "dynamic_ga":    DynamicGa,
                                   "evt":           Evt}
        print("\33[42mDone\33[0m")


    def run_pipeline(self):
        '''
        Façade to run the pipeline of selected methodology.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Choose the class of selected methodology, after that create an object using the UserProject object like argument in constructor
        try:
            selected_methodology = self.methodology_facade[self.__config_parser.methodology](self.__config_parser.user_project)
        except Exception:
            print("\33[41mError! It's impossible to instantiate " + self.__config_parser.methodology + ".\33[0m")
            exit(1)

        #Execute the pipeline of specific methodology
        selected_methodology.run_procedure()
        selected_methodology.generate_results()
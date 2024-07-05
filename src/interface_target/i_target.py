from abc import ABC, abstractmethod


class ITarget(ABC):
    '''
    Define Interface for all boards and simulators used in InterfaceTarget class.

    If one concrete class not implement this interface, raise "NotImplementedError" exception.


    Parameters
    ----------
        None


    Attributes
    ----------
        None
    '''
    @abstractmethod
    def flash():
        '''
        All targets must implement flash method. This method is for load the program in board.
        
        If simulator not needs this method, just use "pass" instruction.


        Parameters
        ----------
            None

            
        Returns
        -------
            None
        '''
        raise NotImplementedError

    @abstractmethod
    def compile():
        '''
        All targets must implement compile method. This method is for compile this source code to architecture target.


        Parameters
        ----------
            None

            
        Returns
        -------
            None
        '''
        raise NotImplementedError

    @abstractmethod
    def run():
        '''
        All targets must implement run method. This method is for execute the program in target.


        Parameters
        ----------
            None

            
        Returns
        -------
            None
        '''
        raise NotImplementedError
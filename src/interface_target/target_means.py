import serial


class Board():
    """
    Communicate with board


    Parameters
    ----------
    serial_port : str
        Serial port where board is connected


    Attributes
    ----------
    serial_port : str
        Serial port where board is connected
    """

    def __init__(self, serial_port: str) -> None:
        self.serial_port = serial_port

    def run(self, args: list = []) -> list:
        '''
        Execute the program in a board


        Parameters
        ----------
        args : list, default = []
            Input set to execute the program


        Returns
        -------
        output : list
            Set of prints, with response of execution
        '''
        with serial.Serial(self.serial_port, 9600, timeout=1) as ser:
            index = 0
            input_receive = ""
            output = []

            ser.write('start\n'.encode())
            while 1:
                while ser.in_waiting:
                    data_in = ser.readline()
                    input_receive = data_in.strip().decode()

                    if input_receive:
                        output.append(input_receive)

                    if input_receive == "Input":
                        if index >= len(args):
                            print(
                                "\33[41 Error! The executing program is trying to read more arguments than there are in args list.\33[0m")
                            exit(-1)
                        ser.write(f'{args[index]}\n'.encode())
                        index += 1
                        input_receive = ""

                    if input_receive == "Bye Bye!":
                        if index < len(args)-1:
                            print(
                                "\33[43 Warning! The lenght of args list is {} but only {} args were read by the program.\33[0m",
                                len(args),
                                index+1)
                        ser.close()
                        return output


class Simulator():
    """
    Communicate with simulator


    Parameters
    ----------
        None


    Attributes
    ----------
        None
    """

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        '''
        Execute the program in a simulator


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        pass

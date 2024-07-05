import math
import json
from datetime import date
from datetime import datetime
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from utils.wcet_data import WcetData
from utils.user_project import UserProject
import pandas as pd
import numpy as np


class Report():
    """
    Class responsible for generating reports, in PDF file or JSON file.


    Parameters
    ----------
    project : UserProject
        Object contains all user project information (e.g.: Directory input, main file name)

    wcet : WcetData
        Object contains all results about WCET


    Attributes
    ----------
    project : UserProject
        Object contains all user project information (e.g.: Directory input, main file name)

    wcet : WcetData
        Object contains all results about WCET
    """

    def __init__(self, project: UserProject, wcet: WcetData) -> None:
        self.user_project = project
        self.wcet = wcet

        # Constants where the page starts and the distance between lines
        self.current_y_position = 260
        self.distance_between_lines = 8
        self.center_x = self.mm2p(210/2.0)  # Center of page in x axis
        self.paragraph = self.mm2p(25)  # Distance of left margin

        # PDF object
        self.pdf_file = None

    def wcet_graphic(self) -> None:
        '''
        Create histogram to visualizate measurements distributions, deadline and calculated WCET.

        This function generate a PNG file in same output directory.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Check if there are histogram
        if (self.wcet.get_histogram().empty):
            print(
                "\n\33[41mError! There are not measurements for plot the histogram\33[0m")
            print("Please, contact development team to fix this error")
            print("The WCET calculated was:")
            print("iWCET: ", self.wcet.get_swcet())
            print("pWCET: ", self.wcet.get_pwcet())
            print("High Water-Mark: ", self.wcet.get_hwm())
            exit(1)

        # Easier names
        deadline = self.user_project.get_deadline()
        iwcet = self.wcet.get_swcet()
        pwcet = self.wcet.get_pwcet()
        hwm = self.wcet.get_hwm()
        histogram_data = self.wcet.get_histogram()

        # If some WCET not appear in histogram
        show_all_wcet = True



        ###########################################################################





        # Maximum x value (Just consider HWM and deadline, because other values can be much greater than)
        temp = []
        if (hwm > 0):
            temp.append(hwm)
            temp.append(deadline)
            x_max = int(max(temp, key=int))
        else:
            temp.append(iwcet)
            temp.append(deadline)
            x_max = int(max(temp, key=int))


        #Minimun x value
        temp = []
        if (hwm > 0):
            if(deadline > 0 and deadline < x_max):
                temp.append(deadline)
            temp.append(histogram_data.valuesx.min())
            x_min = int(min(temp, key=int))
        #How hasn't histogram distribution, so it's possible show of start
        else:
            x_min = 0


        ###########################################################################




        # Difference between x ticks
        diff_x_ticks = x_max - x_min
        if(diff_x_ticks == 0):
            diff_x_ticks = int(x_max / 25)
        else:
            diff_x_ticks = int(diff_x_ticks / 25)

        
        # Maximum vertical line
        y_max = int(histogram_data.valuesx.mode().iloc[0])
        y_max = math.log(y_max)*100



        ###########################################################################



        # Create all informations in histogram
        plt.figure(figsize=(19, 8))
        plt.title('WCET analysis of ' +
                  self.user_project.get_main_file_name() + ".c",
                  fontsize=20)
        plt.xlabel('Cycles', fontsize=14)
        plt.ylabel('Frequency', fontsize=16)
        plt.xticks(range(x_min,
                         x_max + 1,
                         diff_x_ticks),
                   rotation=90,
                   fontsize=10)
    

        # Create vertical lines
        if (deadline > 0):
            plt.vlines(deadline, 0, y_max, colors='r')
            plt.text(deadline, y_max, s="Deadline",
                     rotation='vertical', fontsize=12, color='r')

        if (iwcet > 0):
            if (iwcet <= x_max and iwcet >= x_min):
                plt.vlines(iwcet, 0, y_max, colors='b')
                plt.text(iwcet, y_max, s="iWCET",
                         rotation='vertical', fontsize=12, color='b')
            else:
                show_all_wcet = False

        if (pwcet != []):
            for probability in pwcet:
                if (probability[1] <= x_max and probability[1] >= x_min):
                    plt.vlines(probability[1], 0, y_max, colors='g')
                    plt.text(
                        probability[1],
                        y_max, s="pWCET " + str(probability[0]),
                        rotation='vertical', fontsize=12, color='g')
                else:
                    show_all_wcet = False

        if (hwm > 0):
            plt.vlines(hwm, 0, y_max, colors='k')
            plt.text(hwm, y_max, s="HWM",
                     rotation='vertical', fontsize=12, color='k')

        if (show_all_wcet == False):
            plt.legend(handles=[mpatches.Patch(
                color='green', label='Some pWCET did not appear')])

        plt.hist(histogram_data.valuesx, bins=250, color='m', log=True)
        plt.savefig(self.user_project.get_output_directory() + "wcet_" +
                    self.user_project.get_main_file_name() + "_histogram.png",
                    format='png')





    def mm2p(self, milimiters: float) -> float:
        '''
        Convert milimiters to points units. ReportLab use point units.


        Parameters
        ----------
        milimiters : int 
            Distance in milimiters


        Returns
        -------
        points : int
            Distance in points
        '''
        return milimiters / 0.352777

    def compliance_do178(self, paragraph: int, loose: float) -> None:
        '''
        Create line in PDF file with information about if calculated WCET complies with standard DO-178 and percentage in relation to deadline.


        Parameters
        ----------     
        paragraph : int
            Distance of left margin to start the comment

        loose : float
            Ratio between calculated value and deadline (Usually with range between 0 to a little more than 1)


        Returns
        -------
            None
        '''
        x_position = self.mm2p(paragraph)
        y_position = self.mm2p(self.current_y_position)
        common_text = str(round(loose * 100, 3)) + "% --- "

        # 90% or more of deadline is unsafe
        if (loose > 0.9):
            # Red text
            self.pdf_file.setFillColorRGB(1, 0, 0)
            self.pdf_file.drawString(
                x_position, y_position, common_text +
                "Does not comply with the DO-178 standard")

        # Between 80% and 90% of deadline is necessary careful
        elif (loose > 0.8):
            # Yellow text
            self.pdf_file.setFillColorRGB(1, 1, 0)
            self.pdf_file.drawString(
                x_position, y_position, common_text +
                "The program must be analyzed with caution")

        # Below 80% of deadline is safe
        else:
            # Green text
            self.pdf_file.setFillColorRGB(0, 1, 0)
            self.pdf_file.drawString(x_position,
                                     y_position,
                                     common_text + "The program is safe")

    def setup_pdf(self):
        '''
        Initialize the setup for PDF file.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        # Set initial configuration of PDF file
        self.pdf_file = canvas.Canvas(self.user_project.get_output_directory() +
                                      "WCET Report " + self.user_project.get_main_file_name() +
                                      " - " + str(date.today()) + ".pdf",
                                      pagesize=A4)

        # Metadata in PDF file. It's show in Properties
        self.pdf_file.setCreator("FioWAT")

        # self.pdf_file.setEncrypt(senha : str)

        # Text color black
        self.pdf_file.setFillColorRGB(0, 0, 0)

        # Font family and font size of title
        self.pdf_file.setFont('Times-Roman', 20)

        # Title
        self.pdf_file.drawCentredString(
            self.center_x, self.mm2p(272),
            self.user_project.get_main_file_name() + ".c program WCET report")

        # Font family and font size of the body of the text
        self.pdf_file.setFont('Times-Roman', 12)

    def show_loose(self, message: str, result: any) -> None:
        '''
        Write the line that show the loose.


        Parameters
        ----------
        message : str
            Message to show on line.

        result : any
            WCET calculated. They can be iWCET (float), pWCET (list of tuples), HWM (int).


        Returns
        -------
            None
        '''
        # PWCET uses tuple (probability, pWCET)
        if (type(result) is tuple):
            # Use just the pWCET element
            result = result[1]
            paragraph = 68
        else:
            paragraph = 57

        if (result == 0):
            self.pdf_file.drawString(self.paragraph,
                                     self.mm2p(self.current_y_position),
                                     "Loose of " + message + ": --- ")
        else:
            self.pdf_file.drawString(self.paragraph,
                                     self.mm2p(self.current_y_position),
                                     "Loose of " + message + ": ")
            self.compliance_do178(
                paragraph, result / self.user_project.get_deadline())

        self.current_y_position -= self.distance_between_lines
        self.pdf_file.setFillColorRGB(0, 0, 0)

    def create_line(self, message: str, result: any) -> None:
        '''
        Write the line to show the relevant variables on the report.


        Parameters
        ----------
        message : str
            Message to name the variable.

        variable : any
            Value of WcetData or UserProject.


        Returns
        -------
            None
        '''
        # Prevent many decimal numbers
        if (type(result) in [float, np.float64, np.float32]):
            result = round(result, 3)
        elif (type(result) is list):
            result = str(result).replace("[", "").replace("]", "")

        self.pdf_file.drawString(self.paragraph,
                                 self.mm2p(self.current_y_position),
                                 message + ": " + str(result))
        self.current_y_position -= self.distance_between_lines

    def error_print_report(self) -> None:
        '''
        Show report data in print, because cannot create report file.


        Parameters
        ----------
            None

        Returns
        -------
            None
        '''
        print(
            "\n\33[41mError! The FioWAT don't has permission to create file.\33[0m")
        print("Please, if you have the PDF file opened, close it.")
        print("Another reason is if the image file was not created.")
        print("The WCET calculated was:")
        print("iWCET: ", self.wcet.get_swcet())
        print("pWCET: ", self.wcet.get_pwcet())
        print("High Water-Mark: ", self.wcet.get_hwm())
        exit(1)

    def save_pdf_file(self) -> None:
        '''
        Save the PDF report file on hard disk.


        Parameters
        ----------
            None

        Returns
        -------
            None
        '''
        # Create PDF file on disk and close canvas (The PDF file must is closed)
        try:
            self.pdf_file.save()
        except Exception as e:
            print(e)
            self.error_print_report()

        print("\33[42mDone\33[0m")

    def create_pdf_report(self):
        '''
        Create report in PDF format in output directory.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Creating PDF report file...", end=" ")
        self.setup_pdf()

        # *** FIRST PAGE ***
        if (self.user_project.get_deadline() > 0):
            self.show_loose("iWCET", self.wcet.get_swcet())  # Line 1

            # Line 2 -> ??
            if (self.wcet.get_pwcet() == []):
                self.show_loose("pWCET", 0)
            else:
                for probability in self.wcet.get_pwcet():
                    self.show_loose(
                        "pWCET " + str(probability[0]), probability)

            self.show_loose("HiWaM", self.wcet.get_hwm())  # Line 3

        # Line 4
        if (self.wcet.get_swcet() > 0):
            self.create_line("iWCET", self.wcet.get_swcet())
        else:
            self.create_line("iWCET", "---")

        # Restrict the number of elements until 3 by line
        # Line 5
        if (len(self.wcet.get_pwcet()) == 0):
            self.create_line("pWCET", "---")
        elif (len(self.wcet.get_pwcet()) <= 3):
            self.create_line("pWCET", self.wcet.get_pwcet())
        else:
            # Show the first 3 elements
            self.create_line("pWCET", self.wcet.get_pwcet()[0:3])
            # There is 4 or 5 elements (5 is the maximum number of elements, the filter check this)
            if (len(self.wcet.get_pwcet()) == 4):
                self.create_line("pWCET", self.wcet.get_pwcet()[3])
            else:
                self.create_line("pWCET", self.wcet.get_pwcet()[3:5])

        # Line 6
        if (self.wcet.get_hwm() > 0):
            self.create_line("High-Water Mark", self.wcet.get_hwm())
        else:
            self.create_line("High-Water Mark", "---")

        # Line 7
        if (self.user_project.get_deadline() > 0):
            self.create_line("Deadline", self.user_project.get_deadline())
        else:
            self.create_line("Deadline", "---")

        self.create_line("Function target",
                         self.user_project.get_function_target())  # Line 8
        self.create_line("Technique", self.wcet.get_technique_name())  # Line 9
        self.create_line(
            "Triple Target", self.user_project.get_triple_target())  # Line 10

        # Only EVT techniques need use IID flag
        # Line 11
        if (self.wcet.get_technique_name() in ["WPEVT", "Dynamic GA", "EVT"]):
            self.create_line("IID result", self.wcet.get_iid_flag())

        self.create_line("Start of analysis",
                         self.wcet.get_analysis_start_time())  # Line 12
        self.create_line("Creation of report", datetime.now().strftime(
            "%Y/%m/%d - %H:%M:%S.%f"))  # Line 13
        

        # Only hybrid or dynamic techniques can create histogram
        if (self.wcet.get_technique_name() in ["WPEVT", "Dynamic GA", "EVT"]):
            # Create histogram
            self.wcet_graphic()
            # Original dimensions
            width = 1900.0
            height = 800.0
            scale = 0.1125  # Scale to height has 85. Example: 85/400 = 0.2125
            try:
                self.pdf_file.drawImage(self.user_project.get_output_directory() + "wcet_" +
                                        self.user_project.get_main_file_name() + "_histogram.png",
                                        self.mm2p(5),
                                        self.mm2p(25),
                                        self.mm2p(width*scale),
                                        self.mm2p(height*scale))
            except Exception as e:
                print(e)
                self.error_print_report()

        # Only EVT can create more plots
        if (self.wcet.get_technique_name() in ["WPEVT", "Dynamic GA", "EVT"]):
            # If EVT runned
            if (len(self.wcet.get_histogram().valuesx) >= 5000):
                # Create new Page
                self.pdf_file.showPage()
                # *** SECOND PAGE ***
                try:
                    # pWCET plot
                    # Original dimensions
                    width = 600.0
                    height = 400.0
                    scale = 0.2125  # Scale to height has 85. Example: 85/400 = 0.2125
                    self.pdf_file.drawImage(self.user_project.get_output_directory() + "wcet_" +
                                            self.user_project.get_main_file_name() + "_pwcet.png",
                                            self.mm2p(45),
                                            self.mm2p(205),
                                            self.mm2p(width*scale),
                                            self.mm2p(height*scale))

                    # QQ plot and PP plot
                    width = 1000.0
                    height = 400.0
                    scale = 0.2125
                    self.pdf_file.drawImage(self.user_project.get_output_directory() + "wcet_" +
                                            self.user_project.get_main_file_name() + "_qq_pp.png",
                                            self.mm2p(15),
                                            self.mm2p(115),
                                            self.mm2p(width*scale),
                                            self.mm2p(height*scale))

                    # Statistical Summary
                    width = 600.0
                    height = 400.0
                    scale = 0.2125
                    self.pdf_file.drawImage(self.user_project.get_output_directory() + "wcet_" +
                                            self.user_project.get_main_file_name() + "_stat.png",
                                            self.mm2p(45),
                                            self.mm2p(25),
                                            self.mm2p(width*scale),
                                            self.mm2p(height*scale))
                except Exception as e:
                    print(
                        "\n\33[41mError! The EVT figures were not generated\33[0m")
                    print("Error code: ", e)
                    print("The WCET calculated was:")
                    print("iWCET: ", self.wcet.get_swcet())
                    print("pWCET: ", self.wcet.get_pwcet())
                    print("High Water-Mark: ", self.wcet.get_hwm())
                    exit(1)

        self.save_pdf_file()

    def create_json_report(self) -> None:
        '''
        Create report in JSON format in output directory.


        Parameters
        ----------
            None


        Returns
        -------
            None
        '''
        print("Creating JSON report file...", end=" ")

        # Create temporary dictionary to store all relevant values about project
        temporary_json = {}
        temporary_json['Main File Name'] = self.user_project.get_main_file_name()
        temporary_json['Function Target'] = self.user_project.get_function_target()
        temporary_json['iWCET'] = self.wcet.get_swcet()
        temporary_json['pWCET'] = self.wcet.get_pwcet()
        temporary_json['HWM'] = self.wcet.get_hwm()
        temporary_json['Deadline'] = self.user_project.get_deadline()
        temporary_json['Technique Name'] = self.wcet.get_technique_name()
        temporary_json['Triple Target'] = self.user_project.get_triple_target()
        temporary_json['Analysis Start Time'] = self.wcet.get_analysis_start_time()
        temporary_json['Report Creation'] = datetime.now().strftime(
            "%Y/%m/%d - %H:%M:%S.%f")
        temporary_json['IID result'] = self.wcet.get_iid_flag()

        # Convert dictionary to JSON format (JavaScript Object Format)
        json_object = json.dumps(
            temporary_json, indent=4, separators=("", ":"))

        # Create JSON file
        with open(self.user_project.get_output_directory() + "WCET Report " +
                  self.user_project.get_main_file_name() +
                  " - " + str(date.today()) + ".json", "w") as outfile:
            outfile.write(json_object)

        print("\33[42mDone\33[0m")
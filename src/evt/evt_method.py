# Initialization and Imports
import scipy.stats as st
import statsmodels.api as sm
import statsmodels.sandbox as sm_box
from random import sample
import numpy as np
import random
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from utils.user_project import UserProject
from typing import Tuple
from progress.bar import Bar


class Evt():
    """
    Implements the Evt methodology for WCET estimation based in the probabilistc analysis. 
    The method contain several steps taken in order to achieve best curve fitting based on the data provided.
    Method pipeline follows as: data aquisition and import, method selection,
    curve fitting, iid testing, Pwcet estimation and results plot 


    Parameters
    ----------
    project : UserProject
        All informations about user project.

    csv_filename : str
        Name of the csv file containing runs cycles count.


    Attributes
    ----------
    pwcet_bounds : list
        Desired values of exceedance of probability to be obatined.

    csv_filename : str
        Name of the csv file containing runs cycles count.
    """

    def __init__(self, project: UserProject, csv_filename: str) -> None:
        self.pwcet_bounds = project.pwcet_bounds
        self.csv_filename = csv_filename
        self.directory = project.output_directory
        self.main_filename = project.main_file_name

    class Fit(object):
        """
        Fitted Distribution Object


        Attributes
        ---------- 
        dist : st.rv.frozen
           Distribution object  

        shape : float
           Distribution parameter

        loc : float
           Distribution parameters

        scale : float
           Distribution parameters   

        cvonmises : CramerVonMisesResult
           Goodness of fit parameter, Cramer Von Mises   

        ks_fit : KstestResult
           Goodness of fit parameter, Kolmogorov Smirnov


        Returns
        ----------
            None 
        """
        @classmethod
        def __init__(self, dist: object, shape: float, loc: float, scale: float, cvonmises: object, ks_fit: object) -> None:
            self.dist = dist
            self.shape = shape
            self.loc = loc
            self.scale = scale
            self.cvonmises = cvonmises
            self.ks_fit = ks_fit

    # Data acquisition
    def dataimport(filename_a: str = "", header_a: int = 0, usecols_a: int = 0, clock_freq: int = 1) -> pd.DataFrame:
        """
        Imports the data set values from a .csv file.


        Parameters
        ----------
        filename : str
            File name, default ='fibcall_30_10000.csv'

        header : int, default = 0
            Header line

        usecols : int, default = 0
            Data Column

        clock_freq : int, default = 1 
            Conversion factor from ms to cycles


        Returns
        ----------
        rawdata_df : pd.DataFrame
            Data set containg the cycle counts of all runs.
        """
        # .csv file reading - single collumn, header #1 row
        rawdata_df = pd.read_csv(filepath_or_buffer=filename_a, header=header_a, usecols=[
                                 usecols_a], names=["valuesx"])

        # AVR ATMEGA328 clock - 1MHz #[Hz]Converts cycle time to cycles
        rawdata_df.valuesx = rawdata_df.valuesx*clock_freq
        return rawdata_df

    # Peaks of Threshold - POT - Sel_extremos
    # Extracts extreme values above the threshold
    def sel_extremos_pot(data: pd.DataFrame, threshold: int, export: bool = False) -> Tuple[pd.DataFrame, int]:
        """
        Peaks over Threshold method of filtering maximum values.


        Parameters
        ----------
        data : pd.DataFrame
            Data set

        threshold : int
            Threshold value

        export : bool, default = False.
            Exports the output as a .csv file. This argument is optional.

        clock_freq : int, default = 1. 
            Conversion factor from ms to cycles


        Returns
        ----------
        extremos : pd.DataFrame
            derived maximum valuesfrom data set.

        len_ext : int
            Number of maximum values found.
        """

        extremos = data.loc[data.values > threshold]
        len_ext = len(extremos)
        print(len(extremos), "extreme values over",
              threshold, "were found, using POT method")

        if len(extremos) == 0:
            warnings.warn("None extreme value was found")

        if (export) == True:
            extremos.to_csv('out.zip', index=False)  # Export the peaks - .csv

        return extremos, len_ext

    # Block Maxima - BM - Sel_extremos
    # Extracts extreme values from the block
    def sel_extremos_bm(data: pd.DataFrame, blocksize: int) -> Tuple[pd.DataFrame, int]:
        """
        Block maxima method of filtering maximum values.


        Parameters
        ----------
        data : pd.DataFrame
            Data set

        blocksize : int
            Block size value


        Returns
        ----------
        extremos : pd.DataFrame
            derived maximum valuesfrom data set.

        len_ext : int
            Number of maximum values found.
        """

        periods = int((data.index.max() - data.index.min()
                       )/blocksize)+1  # Number of Intervals
        intervalos = pd.interval_range(
            start=data.index[0],
            freq=blocksize, periods=periods, closed="left")

        # Extreme values filtering
        empty_intervals = 0
        extremos_i, extremos_values = [], []

        for i in intervalos:
            data_slice = data.loc[(data.index >= i.left) &
                                  (data.index < i.right)]
            if len(data_slice) > 0:
                extremos_i.append(data_slice.idxmax())
                extremos_values.append(
                    data_slice.loc[extremos_i[-1]['valuesx']])
            else:
                empty_intervals += 1

        if empty_intervals > 0:
            warnings.warn(message=f"{empty_intervals} blocks with no value",)

        len_ext = len(extremos_values)
        print(len_ext, "extreme values were found using BM method")

        if len_ext == 0:
            warnings.warn("None extreme value was found")

        extremos = pd.DataFrame(list(zip(extremos_values[:], extremos_i[:])), columns=[
                                'valuesx', 'indice'], dtype='float64')
        return extremos, len_ext

    # Curve Fitting
    def fitting(values: pd.DataFrame, method: str) -> Tuple[st.rv_continuous, float, float, float, object, object]:
        """
        Curve fitting method.


        Parameters
        ----------
        values : pd.DataFrame
            Data set

        method : str
            Maximum extraction method name.


        Returns
        ----------
        dist : st.rv.frozen
           Distribution object. 

        shape : float
           Distribution parameter.

        loc : float
           Distribution parameter.

        scale : float
           Distribution parameter. 

        cvonmises : CramerVonMisesResult
           Goodness of fit parameter, Cramer Von Mises   

        ks_fit : KstestResult
           Goodness of fit parameter, Kolmogorov Smirnov 
        """

        if method == 'pot':
            shape, loc, scale = st.genpareto.fit(
                values)  # Generalized Pareto Distribution
            dist = st.genpareto(shape, loc, scale)  # Fitted Curve

        elif method == 'bm':
            shape, loc, scale = st.genextreme.fit(
                values)  # Generalized Extreme Distribution
            dist = st.genextreme(shape, loc, scale)  # Fitted Curve

        # Goodness of Fit summary
        cvonmises = st.cramervonmises(
            values, dist.cdf, args=())  # Cramer Von Mises test
        ks_fit = st.kstest(values, dist.cdf)  # Kolmogorov Smirnov test(KS)
        # chi_fit=st.chisquare(st.ecdf(values), dist.cdf) #Chi-square test
        print(type, cvonmises)
        return dist, shape, loc, scale, cvonmises, ks_fit

    # Independency Data Tests
    def stats_validation(rawdata_df: pd.DataFrame, seg: int = 1000, rep: int = 100,
                         alpha: float = 0.05) -> Tuple[list, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
        """
        Perform a series of statiscal tests in order to validate IID assumptions.


        Parameters
        ----------
        rawdata_df : pd.DataFrame
            Original data set.

        seg : int, default = 1000
            Segment size for statistical methods. This argument is optional.

        rep : int, default = 100
            Number of runs for statistical methods. This argument is optional.

        alpha : float, default = 0.05
            Confidence level. This argument is optional.


        Returns
        ----------
        ww : pd.DataFrame
            Wald Wolfowitz test results.

        lb_[2,5,10,20,50]:pd.DataFrame
            Ljung-box tests, where 2,5,10,20,50, are the lags tested.
        """

        data_set = rawdata_df.valuesx.tolist()  # list conversion
        a = str()
        ww = []
        # LJUNG BOX LISTS
        lb_2 = pd.DataFrame()
        lb_5 = pd.DataFrame()
        lb_10 = pd.DataFrame()
        lb_20 = pd.DataFrame()
        lb_50 = pd.DataFrame()

        for i in range(rep):
            datasrt = sample(data_set, seg)  # 1st Sample
            # _single_sample tests_#
            # Mesurements Independence Tests
            # Wald Wolfowitz (WW)
            ww.append(sm_box.stats.runs.runstest_1samp(
                datasrt, cutoff='median', correction=True))
            # Ljung-Box (LB)
            lb_2 = pd.concat(
                [sm.stats.diagnostic.acorr_ljungbox(
                    datasrt, lags=2, boxpierce=False, model_df=0, period=None,
                    return_df=True, auto_lag=False),
                 lb_2],
                ignore_index=True, sort=False)
            lb_5 = pd.concat(
                [sm.stats.diagnostic.acorr_ljungbox(
                    datasrt, lags=5, boxpierce=False, model_df=0, period=None,
                    return_df=True, auto_lag=False),
                 lb_5],
                ignore_index=True, sort=False)
            lb_10 = pd.concat(
                [sm.stats.diagnostic.acorr_ljungbox(
                    datasrt, lags=10, boxpierce=False, model_df=0, period=None,
                    return_df=True, auto_lag=False),
                 lb_10],
                ignore_index=True, sort=False)
            lb_20 = pd.concat(
                [sm.stats.diagnostic.acorr_ljungbox(
                    datasrt, lags=20, boxpierce=False, model_df=0, period=None,
                    return_df=True, auto_lag=False),
                 lb_20],
                ignore_index=True, sort=False)
            lb_50 = pd.concat(
                [sm.stats.diagnostic.acorr_ljungbox(
                    datasrt, lags=50, boxpierce=False, model_df=0, period=None,
                    return_df=True, auto_lag=False),
                 lb_50],
                ignore_index=True, sort=False)

        # Independency and indentically distribution of data(IID) tests warning. Ok- passed, Failed - Review data set. (LJung-box not passed)
        for i in ww[1]:
            if i >= (1-alpha):
                ww_flag = True
            else:
                ww_flag = False

        lb_2_flag = (lb_2.lb_pvalue <= alpha).any()
        lb_5_flag = (lb_5.lb_pvalue <= alpha).any()
        lb_10_flag = (lb_10.lb_pvalue <= alpha).any()
        lb_20_flag = (lb_20.lb_pvalue <= alpha).any()
        lb_50_flag = (lb_50.lb_pvalue <= alpha).any()

        if (lb_2_flag or lb_5_flag or lb_10_flag or lb_20_flag or lb_50_flag) == True:
            lb_flag = True
        else:
            lb_flag = False

        if ww_flag or lb_flag == True:
            if ww_flag and lb_flag == True:
                iid_flag = "Failed - Review data set. (WW and LbJung-box not passed)"
            elif ww_flag == True:
                iid_flag = "Failed - Review data set. ( WW not passed)"
            elif lb_flag == True:
                iid_flag = "Failed - Review data set. (LbJung-box not passed)"
        else:
            iid_flag = "OK - Pass"

        return ww, lb_2, lb_5, lb_10, lb_20, lb_50, iid_flag

    # Fitted Data Stats Tests
    def stats_fit_validation(b: np.array, FIT: st.rv_continuous, exceed_prob_ecdf: sm.distributions.empirical_distribution.ECDF) -> Tuple[list, list]:
        """
        Perform paired samples statiscal tests in order to validate the fitting of data set and fitted distribution.


        Parameters
        ----------
        rawdata_df : pd.DataFrame
            Original data set. 

        seg : int, default = 1000
            Segment size for statistical methods. This argument is optional.

        rep : int, default = 100
            Number of runs for statistical methods. This argument is optional.

        alpha : float, default = 0.05
            Confidence level. This argument is optional.


        Returns
        ----------
        ks : list
            Komolgorov-Smirnov test results.

        ad : list
            Anderson Darling test results, where the AD adjusts for differnte sample sizes.
        """

        ks, ad1 = ([]for i in range(2))
        rep = 100
        for i in range(rep):
            seg = random.randint(10, len(b))  # random size sample
            values = sample(list(b), seg)
            values_tail = sample(list(b[-seg:len(b)]), seg)

            datasrt = FIT[0].cdf(values)  # 1st Sample - Fit dist.
            datasrt2 = exceed_prob_ecdf(values)  # 2nd Sample - Empirical dist.

            # Similarity of Distribution Tests
            # Kolmogorov Smirnov (KS)
            ks.append(st.ks_2samp(datasrt, datasrt2, method='auto'))

            # AndersonDarling ksamples (AD1)
            warnings.filterwarnings("ignore")
            # AD1 - Adjusts for possibly different sample sizes
            ad1.append(st.anderson_ksamp([datasrt, datasrt2]))
            warnings.filterwarnings("default")

        return ks, ad1

    # Pwcet Calculation- Evt Projection
    def pwcet(exec_values: list, dist: st.rv_continuous) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates pWCET from the exceedance probability desired.


        Parameters
        ----------
        exec_values : float
            Exceedance probability values desired. 

        dist : st.rv_continuous
            Continuos distribution; scypy.stats.rv_continuous.


        Returns
        ----------
        pwcet_proj : ndarray.float
            pWCET values of outputs.

        exceed_prob : ndarray.float
            Exceedance of probability array.

        cycles_pwcet : ndarray.float
            pWCET values of exceed_prob array.
        """

        pwcet_proj = dist.isf(exec_values)
        print("pwcet de", exec_values, ":", np.ceil(pwcet_proj))
        exceed_prob = np.logspace(-13, 0, num=100, base=10)
        cycles_pwcet = dist.isf(((exceed_prob)))

        return pwcet_proj, exceed_prob, cycles_pwcet

    # Evt main Pipeline
    def run(self) -> Tuple[list, str, pd.DataFrame]:
        """
        Main program pipeline for the EVT methodology.


        Parameters
        ----------
        Evt : EVT (self)
            Object of EVT


        Returns
        ----------
        pwcet_proj : list
            pWCET values for each exceedance of probabilty in pWCET bounds.

        iid_flag : str
            IID flag of statistical tests.

        rawdata_df : pd.DataFrame
            Dataframe cotaining the full data set used in the analysis.
        """

        def __init__(self, project, csv_filename) -> None:
            self.pwcet_bounds = project.pwcet_bounds
            self.csv_filename = csv_filename
            self.directory = project.output_directory
            self.main_filename = project.main_file_name

        print("EVT Calculation...", end=" ")
        print("\33[42mStarted\33[0m")

        # Reads data from .csv -self.project.filename(filename:str='fibcall_30_10000.csv',header:int=0,usecols:int=0,clock_freq:int=1)
        rawdata_df = Evt.dataimport(self.csv_filename, 0, 0, 1)

        # Limit value, threshold for POT (em Cycles) - Using Quantile strategy
        threshold = int(rawdata_df['valuesx'].quantile(q=[0.98]))
        # Peaks of Threshold - POT - DataFrame w/ extremes
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(
            rawdata_df, threshold, False)

        # Block Maxima - BM - Using % of ex
        bm = int(len(rawdata_df)*0.01)  # Block size
        extre_max_bm, len_ext_bm = Evt.sel_extremos_bm(rawdata_df, bm)
        POT_FIT = Evt.fitting(extre_max_pot.valuesx,
                              "pot")  # POT Curve Fitting
        BM_FIT = Evt.fitting(extre_max_bm.valuesx, "bm")   # BM Curve Fitting
        print("The KS value for the POT method is: ",
              POT_FIT[5], "and for the BM method is: ", BM_FIT[5])
        if POT_FIT[5] <= BM_FIT[5]:  # Selects the best Fit result and pass it to the object FIT
            FIT = POT_FIT
            extre_max = extre_max_pot
            len_ext = len_ext_pot
            print("The distribution choosen for fitting is the Generalized Pareto Dist., using the POT method for extremes selection")
        else:
            FIT = BM_FIT
            extre_max = extre_max_bm
            len_ext = len_ext_bm
            print("The distribution choosen for fitting is the Generalized Extreme Dist., using the BM method for extremes selection")

        iid_rep = 100  # Segment counts for Stats Test
        iid_segsize = 1000  # Segment Size
        confidence = 0.05  # Null Hypotheses Confidence Level
        # Independency Data Tests
        ww, lb_2, lb_5, lb_10, lb_20, lb_50, iid_flag = Evt.stats_validation(
            rawdata_df, iid_rep, iid_rep, confidence)
        # Pwcet Calculation- Evt Projection
        self.pwcet_bounds = np.array(self.pwcet_bounds, dtype=float)
        pwcet_proj, exceed_prob, cycles_pwcet = Evt.pwcet(
            self.pwcet_bounds, FIT[0])

        # pWCET tuple exhibition
        pwcet_proj2 = (np.ceil(pwcet_proj)).astype(int)
        # pwcet_proj=np.int_(pwcet_proj)
        pwcet_proj3 = []
        for element in pwcet_proj2:
            pwcet_proj3.append(int(element))
        pwcet_proj4 = [(self.pwcet_bounds[i], pwcet_proj3[i])
                       for i in range(0, len(pwcet_proj3))]

        b = np.linspace(
            (extre_max.valuesx).min(),
            (extre_max.valuesx).max(),
            len_ext)
        fit_pdf = FIT[0].pdf(b)  # Probability density Function
        fit_cdf = FIT[0].cdf(b)  # Cumulative distribution Function
        exceed_prob_ecdf = sm.distributions.empirical_distribution.ECDF(
            extre_max.valuesx)  # Cumulative Empirical Distribution Function
        exceed_prob_ecdf_y = exceed_prob_ecdf(b)  # Empiric CDF

        ks, ad1 = Evt.stats_fit_validation(b, FIT, exceed_prob_ecdf)

        ww = pd.DataFrame(ww, columns=['statistic', 'pvalue'], dtype=float)
        ks = pd.DataFrame(ks, columns=['statistic', 'pvalue'], dtype=float)
        ad1 = pd.DataFrame(ad1)

     # __________________________Plot_______________________________#
        # RawData
        fig1, ax1 = plt.subplots(1, 1, figsize=(6, 4))
        ax1.plot(rawdata_df.index, rawdata_df.values)
        ax1.axhline(threshold, color='r')
        ax1.title.set_text("Raw data")
        fig1.savefig(self.directory + "wcet_" +
                     self.main_filename + "_dataset.png", format='png')
        # fig1.savefig("wcet_" + "_dataset.png", format='png')

        # Tail and Fitting
        fig2, ax2 = plt.subplots(1, 1, figsize=(6, 4))
        ax2.plot(b[1:], fit_pdf[1:])
        ax2.hist(extre_max.valuesx, bins=30, density=True)
        ax2.set_xlim(min(extre_max.valuesx),max(extre_max.valuesx))
        ax2.title.set_text("Tail Distribution")
        fig2.savefig(self.directory + "wcet_" +
                     self.main_filename + "_tail_fit.png", format='png')
        # fig2.savefig("wcet_" + "_tail_fit.png", format='png')

        # STATS - Box Plot
        fig3, ax3 = plt.subplots(1, 1, figsize=(6, 4))
        ax3.boxplot((ww.pvalue, (ks.statistic), abs((ad1.statistic))/abs(ad1.statistic.max()-ad1.statistic.min()), lb_2.lb_pvalue,
                     lb_5.lb_pvalue, lb_10.lb_pvalue, lb_20.lb_pvalue, lb_50.lb_pvalue), 0, '')
        ax3.set_xticks([1, 2, 3, 4, 5, 6, 7, 8], labels=[
            'ww', 'ks', 'ad', 'LB02', 'LB05', 'LB10', 'LB20', 'LB50'])
        ax3.title.set_text("Statistics Summary")
        fig3.savefig(self.directory + "wcet_" +
                     self.main_filename + "_stat.png", format='png')
        # fig3.savefig("wcet_" + "_stat.png", format='png')

        # QQ-PLOT
        fig4, axs = plt.subplots(1, 2, figsize=(10, 4))
        QQ = st.probplot(
            extre_max.valuesx, dist=FIT[0],
            plot=axs[0])  # quantils evaluation ( CDF^-1)
        axs[0].title.set_text("QQ plot")
        axs[0].set_ylabel("Sample quantiles")
        # PP-PLOT
        axs[1].scatter(exceed_prob_ecdf_y, fit_cdf, marker='o', c='b')
        axs[1].axline([0, 0], [1, 1], c='r')
        axs[1].set_ylabel("Sample percentiles")
        axs[1].set_xlabel("Theoretical percentiles")
        axs[1].title.set_text("PP plot")
        fig4.savefig(self.directory + "wcet_" +
                     self.main_filename + "_qq_pp.png", format='png')
        # fig4.savefig("wcet_" + "_qq_pp.png", format='png')

        # PWCET PROJECTION PLOT
        fig5, ax5 = plt.subplots(1, 1, figsize=(6, 4))
        ax5.plot(cycles_pwcet, exceed_prob)  # Probabilistc model
        ax5.scatter(b, (1-fit_cdf), marker='o', c='r', s=1)
        ax5.set_yscale("log")
        ax5.set_xscale("linear")
        ax5.set_ylabel("Exceedance Probability")
        ax5.set_xlabel("pWCET[cycles]")
        ax5.legend(["projection", "measurements"])
        ax5.ticklabel_format(style='sci', axis='x')
        ax5.title.set_text("PWCET_Projection")
        ax5.set_xlim(min(extre_max.valuesx),1*max(cycles_pwcet))
        fig5.savefig(self.directory + "wcet_" +
                     self.main_filename + "_pwcet.png", format='png')
        # fig5.savefig("wcet_" + "_pwcet.png", format='png')

        print("\33[42mCompleted\33[0m")

        return (pwcet_proj4, iid_flag, rawdata_df)


def evt_running(project: UserProject, wcet: object, interface_target: object, args: list) -> list:
    '''
    Execute N times the same input, used by EVT for generate sample.

    If haven't variability in measurements, so abort the execution and generate report without pWCET.


     Parameters
    ----------
    project : UserProject
        DTO with all information about user project

    wcet : WcetData
        DTO with all information about WCET results

    interface_target : InterfaceTarget
        Object to adapter FioWAT with many boards or simulators

    args : list
        Input set used by EVT


    Returns
    ----------
    results_exec : list
        All cycles executed. If return None, so it's problem to execute this program in EVT
    '''
    results_exec = []

    # Create progress bar to show the progress of run to user
    bar = Bar('Running tests', max=project.number_exec)
    bar.start()

    # Run N times to EVT calculate pWCET
    for i in range(project.number_exec):
        # If not have variability, so interrupt the execution and generate the Report
        if i == 50 and len(set(results_exec)) == 1:
            print(
                f"\n\33[43mWarning! Executions with no variability. EVT cannot run with unique value in sample.\33[0m")
            wcet.set_hwm(results_exec[0])
            histogram = pd.DataFrame(results_exec, columns=['valuesx'])
            wcet.set_histogram(histogram)
            return None

        # Store the measurement
        output = interface_target.run(args)
        cycles = int([line.split(" ")[-1]
                      for line in output if line and line[:2] == "#c"][0])
        results_exec.append(cycles)
        bar.next()
    bar.finish()
    return results_exec


if __name__ == '__main__':
    Evt.run(Evt)

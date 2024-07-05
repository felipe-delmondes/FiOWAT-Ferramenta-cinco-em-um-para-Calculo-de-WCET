from setup_test import *
import random
from pandas import DataFrame, read_csv
import warnings
import scipy.stats as st
import statsmodels.api as sm
import numpy as np

from src.evt.evt_method import Evt, evt_running
from src.evt.evt_facade import EvtFacade
from src.utils.user_project import UserProject
from src.utils.wcet_data import WcetData


def aux(args):
    return ["EVT", "Main", "Function" + str(args[0]), "#cycles " + str(random.randrange(0, 1000)), "Bye Bye"]

class Test_evt_running(unittest.TestCase):

    #VC-420 - The {EVT} method must exhibit a warning if the cycles values remains constant after 50 executions.
    @patch('src.evt.evt_method.Bar')
    def test_01_zero_variability_measurements(self, mocked_bar):
        project = Mock()
        project.number_exec = 100

        wcet = Mock()

        interface_target = Mock()
        interface_target.run.return_value = ["EVT", "Main", "Function", "#cycles 500", "Bye Bye"]

        args = [1, 2, 3]

        result = evt_running(project, wcet, interface_target, args)

        self.assertIsNone(result)
        wcet.set_hwm.assert_called_once()
        wcet.set_histogram.assert_called_once()

    #VC-419 -The {EVT} method must exhibit a progress bar during the process of running the interface_ target.run
    @patch('src.evt.evt_method.Bar')
    def test_02_normal_situation(self, mocked_bar):
        project = Mock()
        project.number_exec = 100

        wcet = Mock()

        interface_target = Mock()
        interface_target.run.side_effect = aux

        args = [1, 2, 3]

        result = evt_running(project, wcet, interface_target, args)

        self.assertNotEqual(result, None)

class Test_evt(unittest.TestCase):

    #VC-421 The {EVT} facade must save a .csv file in the output folder containing the execution cycles of each run.
    @patch('src.evt.evt_facade.Evt')
    @patch('src.evt.evt_facade.IntermediateValues')
    @patch('src.evt.evt_facade.InputManager')
    @patch('src.evt.evt_facade.InterfaceTarget')
    @patch('src.evt.evt_facade.evt_running')
    def test_04_csv_export_normal_situtation(self, mock_evt_running, mock_interface_target, mock_manager, mock_inter_values, mock_evt):
        wcet = WcetData("EVT")

        project = UserProject(sys._getframe(0).f_code.co_name,
                              "",
                              OUTPUT_DIRECTORY,
                              "avr",
                              "atmel",
                              "none",
                              "atmega328",
                              "Main",
                              ["json"],
                              0)
        project.set_target(False, 'COM1', True)
        project.set_evt(10, [1E-9, 1E-10, 1E-11, 1E-12])
        project.set_inputs([4, 3, 2, 1, 3], ["int", "float", "int(10)"], [
                           1, 0.0, -1], [10, 1.0, 100], "none", 5)

        mock_manager().generator = False

        mock_evt_running.return_value = [10, 10, 110]

        mock_histogram = Mock()
        mock_histogram.valuesx.max.return_value = 45

        mock_evt.run.return_value = ([(1E-9, 20000)], "Ok - Passed", mock_histogram)

        EvtFacade(project, wcet).run()

        file = open(OUTPUT_DIRECTORY + sys._getframe(0).f_code.co_name + "_" + str(project.number_exec) + ".csv", 'r')
        hash_json = hashlib.sha256(file.read().encode('utf-8')).hexdigest()
        file.close()

        self.assertEqual(hash_json,
                         "3192caaa96da373c60d7c63448c03f19619cc350e3872941b10a943a7dd9e32b")

    #VC-422 - The {EVT} facade must throw an exception containing a warning in case of Error while running {EVT} class.
    @patch('src.evt.evt_facade.Evt')
    @patch('src.evt.evt_facade.IntermediateValues')
    @patch('src.evt.evt_facade.InputManager')
    @patch('src.evt.evt_facade.InterfaceTarget')
    @patch('src.evt.evt_facade.evt_running')
    def test_05_facade_evt_warn_normal_situtation(self, mock_evt_running, mock_interface_target, mock_manager, mock_inter_values, mock_evt):
        wcet = WcetData("EVT")

        project = UserProject(sys._getframe(0).f_code.co_name,
                                "",
                                OUTPUT_DIRECTORY,
                                "avr",
                                "atmel",
                                "none",
                                "atmega328",
                                "Main",
                                ["json"],
                                0)
        project.set_target(False, 'COM1', True)
        project.set_evt(10, [1E-9, 1E-10, 1E-11, 1E-12])
        project.set_inputs([4, 3, 2, 1, 3], ["int", "float", "int(10)"], [
                            1, 0.0, -1], [10, 1.0, 100], "none", 5)

        mock_manager().generator = False

        mock_evt_running.return_value = [10, 10, 110]

        mock_histogram = Mock()
        mock_histogram.valuesx.max.return_value = 45
        mock_evt.run_return_value ([], "Not OK", mock_histogram)
     
        with self.assertRaises(SystemExit) as cm:
            EvtFacade(project, wcet).run()

        self.assertEqual(cm.exception.code, -1)

    #VC-423 - The {EVT} facade must return the {pwcet}, the {hwm}, the {iid_flag} and the {dataset} obtained after the {EVT} methodology to the wcet object.
    @patch('src.evt.evt_facade.Evt')
    @patch('src.evt.evt_facade.IntermediateValues')
    @patch('src.evt.evt_facade.InputManager')
    @patch('src.evt.evt_facade.InterfaceTarget')
    @patch('src.evt.evt_facade.evt_running')
    def test_06_facade_return_normal_situtation(self, mock_evt_running, mock_interface_target, mock_manager, mock_inter_values, mock_evt):
        wcet = WcetData("EVT")

        project = UserProject(sys._getframe(0).f_code.co_name,
                              "",
                              OUTPUT_DIRECTORY,
                              "avr",
                              "atmel",
                              "none",
                              "atmega328",
                              "Main",
                              ["json"],
                              0)
        project.set_target(False, 'COM1', True)
        project.set_evt(10, [1E-9, 1E-10, 1E-11, 1E-12])
        project.set_inputs([4, 3, 2, 1, 3], ["int", "float", "int(10)"], [
                           1, 0.0, -1], [10, 1.0, 100], "none", 5)

        mock_manager().generator = False

        mock_evt_running.return_value = [10, 10, 110]

        mock_histogram = Mock()
        mock_histogram.valuesx = DataFrame(data=[1,2,3,4,5,6,7,8,45])

        mock_evt.run.return_value = ([(1E-9, 20000)], "Ok - Passed", mock_histogram)

        self.evt=EvtFacade(project, wcet).run()
        
        if wcet.pwcet == [(1E-9, 20000)]:a= True
        else: a=False
        if wcet.iid_flag =='Ok - Passed':b=True
        else: b=False
        if wcet.hwm[0] == 45:c=True
        else: c=False
        d=wcet.histogram.valuesx.equals(DataFrame(data=[1,2,3,4,5,6,7,8,45]))
        
        self.assertTrue(a and b and c and d)

    #VC-424 - The {EVT} method must read the data set from a .csv and use it as a Dataframe.
    def test_07_csv_read_normal(self):

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1)

        data_2 = read_csv(os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv"),
            header=0, usecols=[0],
            names=["valuesx"])

        self.assertEqual((DataFrame.equals(data,data_2)),True)

    #VC-425 - The {EVT} method must compute the threshold of the {POT} method by calculating the 0.98 quantile of the dataset.
    def test_08_threshold_normal(self):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))

        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        data_2 = read_csv(os.path.join(INPUT_DIRECTORY, "fibcall_30_10000_pot.csv"),
             header=0, usecols=[0],
             names=["valuesx"])

        self.assertEqual((DataFrame.equals(extre_max_pot,data_2)),True)

    #VC-426 -The {EVT} method must log the quantity of values are above the threshold of the {POT} method.
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_09_Log_POT_normal(self,mock_stdout):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))

        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)

        self.assertEqual(mock_stdout.getvalue(),"202 extreme values over 42974 were found, using POT method\n")

    #VC-427 -The {EVT} method must warn if none values above the threshold were found using the {POT} method.
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_010_Log_POT_normal(self,mock_stdout):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1)
        threshold_a = 1000

        with warnings.catch_warnings(record=True) as cm:
            extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
            self.assertEqual(cm[0].message.args[0],'None extreme value was found')

    #VC-428 -The {EVT} method must compute the blocksize of the {BM} method as 0.01 of the dataset length.
    def test_11_blocksize_normal(self):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        bm = int(len(data)*0.01)

        extre_max_bm, len_ext_bm = Evt.sel_extremos_bm(data, bm)

        self.assertEqual(len_ext_bm,bm,True)

    #VC-429 -The {EVT} method must log the quantity of values found using the {BM} method.
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_12_log_bm_normal(self,mock_stdout):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        bm = int(len(data)*0.01)
        extre_max_bm, len_ext_bm = Evt.sel_extremos_bm(data, bm)

        self.assertEqual(mock_stdout.getvalue(),"100 extreme values were found using BM method\n")

    #VC-430 -The {EVT} method must use a generalized pareto distribution to fit the extremes found using the {POT} method.
    def test_14_GP_POT_normal(self):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        POT_FIT = Evt.fitting(extre_max_pot.valuesx,"pot")

        self.assertEqual(POT_FIT[0].dist.name,'genpareto')

    #VC-431 - The {EVT} method must use a generalized extreme value distribution to fit the extremes found using the {BM} method.
    def test_15_GEV_BM_normal(self):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        bm = int(len(data)*0.01)
        extre_max_bm, len_ext_bm = Evt.sel_extremos_bm(data, bm)
        BM_FIT = Evt.fitting(extre_max_bm.valuesx,"bm")

        self.assertEqual(BM_FIT[0].dist.name,'genextreme')

    #VC-432 - The {EVT} method must calculate the statistic value of the Cramer Von Mises test to evaluate the goodness of fit.
    def test_16_cvmises_fit_normal(self):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        POT_FIT = Evt.fitting(extre_max_pot.valuesx,"pot")
        cvonmises2 = st.cramervonmises(extre_max_pot.valuesx,POT_FIT[0].cdf, args=())

        self.assertEqual(POT_FIT[4].pvalue,cvonmises2.pvalue)

    #VC-433 -The {EVT} method must calculate the statistic value of the {KS} test to evaluate the goodness of fit.
    def test_17_ks_fit_normal(self):
        project = Mock()
        project.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        project.output_directory=OUTPUT_DIRECTORY
        project.main_file_name=''

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        POT_FIT = Evt.fitting(extre_max_pot.valuesx,"pot")
        ks2 = st.kstest(extre_max_pot.valuesx,POT_FIT[0].cdf)

        self.assertEqual(POT_FIT[5].pvalue,ks2.pvalue)

    #VC-434 -The {EVT} method must choose between {POT} and {BM} method using the lowest value of {KS} statistic to proceed in the analysis.
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_18_method_choosen_fit_normal(self,mock_stdout):
        #project = Mock()
        self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        self.directory=OUTPUT_DIRECTORY
        self.main_filename=''

        self.csv_filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")

        Evt.run(self)
        a=mock_stdout.getvalue()

        if ('The KS value for the POT method is:  KstestResult(statistic=0.17978697509847563' in a):
            if('for the BM method is:  KstestResult(statistic=0.11923938329788575' in a):
                if('using the BM method for extremes selection' in a):
                    cm=True
        else:
            cm=False

        self.assertTrue(cm)

    #VC-435 -The {EVT} method must perform the {WW} and {LB} independency tests of the dataset.
    def test_19_idpendence_test_normal(self):

        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        ww, lb_2, lb_5, lb_10, lb_20, lb_50, iid_flag = Evt.stats_validation(
            data, 100, 1000, 0.05)
        if(len(ww)!=0):a=True
        b=not(lb_2.empty)
        c=not(lb_5.empty)
        d=not(lb_10.empty)
        e=not(lb_20.empty)
        f=not(lb_50.empty)

        self.assertTrue(a and b and c and d and e and f)

    #VC-436 -The {EVT} method must perform the {LB} tests using lags for 2, 5, 10, 20, and 50 samples of the dataset.
    def test_20_LB_lags_normal(self):
        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        ww, lb_2, lb_5, lb_10, lb_20, lb_50, iid_flag = Evt.stats_validation(
            data, 100, 1000, 0.05)

        if (len(lb_2.index)==2000):b=True
        if (len(lb_5.index)==5000):c=True
        if (len(lb_10.index)==10000):d=True
        if (len(lb_20.index)==20000):e=True
        if (len(lb_50.index)==50000):f=True

        self.assertTrue(b and c and d and e and f)

    #VC-437 -The {EVT} method must warn when the {WW} or {LB} independency tests statistic results are lower than a 95% of the.
    def test_21_ww_lb_flag_normal(self):
        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        ww, lb_2, lb_5, lb_10, lb_20, lb_50, iid_flag = Evt.stats_validation(
            data, 100, 1000,0.98)

        self.assertEqual(iid_flag,"Failed - Review data set. (WW and LbJung-box not passed)")

    #VC-438 - The {EVT} method must perform the independency tests a 100 times using a sample of 100 random elements from the dataset.
    def test_22_ww_lb_test_count_normal(self):
        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)

        ww, lb_2, lb_5, lb_10, lb_20, lb_50, iid_flag = Evt.stats_validation(
            data, 1000, 100,0.98)
        a=len(ww) #tests a 100 times
        if a== 100:b=True
        ww2, lb_2_2, lb_5_2, lb_10_2, lb_20_2, lb_50_2, iid_flag_2 = Evt.stats_validation(
            data, 1000, 100,0.98)
        c=self.assertnotEqual=(ww,ww2)  #using a sample of 100 random elements
        d= b and c
        self.assertTrue(d)

    #VC-439 - The {EVT} methodology must perform the {AD} and {KS} similarity of distribution tests using the dataset and fitted distribution.
    def test_23_ad_ks_run_normal(self):
        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        FIT = Evt.fitting(extre_max_pot.valuesx,"pot")

        b = np.linspace((extre_max_pot.valuesx).min(),(extre_max_pot.valuesx).max(),len_ext_pot)
        fit_pdf = FIT[0].pdf(b)  # Probability density Function
        fit_cdf = FIT[0].cdf(b)  # Cumulative distribution Function
        exceed_prob_ecdf = sm.distributions.empirical_distribution.ECDF(
            extre_max_pot.valuesx)  # Cumulative Empirical Distribution Function

        ad,ks= Evt.stats_fit_validation(b, FIT, exceed_prob_ecdf)
        if(len(ad)!=0):a=True
        if(len(ks)!=0):b=True
        self.assertTrue(a and b)

    #VC-440 - The {EVT} method must perform the similarity of distribution tests a 100 times using random sizes of elements from the dataset.
    def test_24_ad_ks_count_normal(self):
        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        FIT = Evt.fitting(extre_max_pot.valuesx,"pot")

        b = np.linspace((extre_max_pot.valuesx).min(),(extre_max_pot.valuesx).max(),len_ext_pot)
        fit_pdf = FIT[0].pdf(b)  # Probability density Function
        fit_cdf = FIT[0].cdf(b)  # Cumulative distribution Function
        exceed_prob_ecdf = sm.distributions.empirical_distribution.ECDF(
            extre_max_pot.valuesx)  # Cumulative Empirical Distribution Function

        ad,ks= Evt.stats_fit_validation(b, FIT, exceed_prob_ecdf)
        if(len(ad)==100):a=True
        if(len(ks)==100):b=True
        self.assertTrue(a and b)

    #VC-441 - The {EVT} method must calculate the {pWCET} for the desired exceedance atributed pwcet_bounds of the class EVT.
    def test_25_pwcet_normal(self):
        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        FIT = Evt.fitting(extre_max_pot.valuesx,"pot")
        pwcet_bounds= [1e-9, 1e-10, 1e-11]

        pwcet_bounds = np.array(pwcet_bounds, dtype=float)
        pwcet_proj, exceed_prob, cycles_pwcet = Evt.pwcet(
            pwcet_bounds, FIT[0])
        pwcet_proj2 = (np.ceil(pwcet_proj)).astype(int)

        result=[8093070, 13081834, 21119946]
        result_bool = all(x == y for x, y in zip(pwcet_proj2, result))

        self.assertTrue(result_bool)

    #VC-442 - The {EVT} method must calculate pWECT using the inverse value of the cumulative distribution of probability of the fitted distribution.
    def test_26_pwcet_ISF_normal(self):
        filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000.csv")
        data=Evt.dataimport(filename,0,0,1000000)
        threshold_a = int(data['valuesx'].quantile(q=[0.98]))
        extre_max_pot, len_ext_pot = Evt.sel_extremos_pot(data, threshold_a, False)
        FIT = Evt.fitting(extre_max_pot.valuesx,"pot")
        pwcet_bounds= [1e-9, 1e-10, 1e-11]

        pwcet_bounds = np.array(pwcet_bounds, dtype=float)
        pwcet_proj, exceed_prob, cycles_pwcet = Evt.pwcet(
            pwcet_bounds, FIT[0])

        pwcet_proj2 = FIT[0].isf(pwcet_bounds)

        result_bool = all(x == y for x, y in zip(pwcet_proj2,pwcet_proj))
        self.assertTrue(result_bool)

    #VC-443 - The {EVT} method must generate a figure containing a plot of the dataset series read from the csv file.
    def test_27_fig_1_normal(self):

        self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        self.directory=OUTPUT_DIRECTORY
        self.main_filename=''
        self.csv_filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000_1.csv")

        self_fig_ref=os.path.join(INPUT_DIRECTORY, "wcet__dataset.png")
        self_fig_out=os.path.join(OUTPUT_DIRECTORY, "wcet__dataset.png")

        Evt.run(self)
        file = open(self_fig_out,'r', encoding='utf8',errors="ignore")

        png_json = (hashlib.sha256(file.read().encode('utf-8'))).hexdigest()
        file.close()

        self.assertEqual(png_json,
                         "379c39c314f0d718b1c2be79172ab25bf049a4391024ef33b68d69ef6873d8f1")

    #VC-444 - The {EVT} method must generate a figure containing the histogram of the extremes found after the {POT} or {BM} methods and the fitted distribution superposed.
    def test_28_fig_2_normal(self):

        self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        self.directory=OUTPUT_DIRECTORY
        self.main_filename=''
        self.csv_filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000_1.csv")

        self_fig_ref=os.path.join(INPUT_DIRECTORY, "wcet__tail_fit.png")
        self_fig_out=os.path.join(OUTPUT_DIRECTORY, "wcet__tail_fit.png")

        Evt.run(self)
        file = open(self_fig_out,'r', encoding='utf8',errors="ignore")
        png_json = (hashlib.sha256(file.read().encode('utf-8'))).hexdigest()
        file.close()

        self.assertEqual(png_json,
                         "2b7c7051ee2190f55a0c8f383f6ea2dbbea530b2961168e79dbd53eedc0c5d52")   
         
    #VC-445 - The {EVT} method must generate a figure containing a boxplot containing the distribution of the {AD}, [KS}, {LB} and {WW} statistical tests.
    def test_29_fig_3_normal(self):

        self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        self.directory=OUTPUT_DIRECTORY
        self.main_filename=''
        self.csv_filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000_1.csv")

        self_fig_out=os.path.join(OUTPUT_DIRECTORY, "wcet__stat.png")

        Evt.run(self)

        check_file = os.path.isfile(self_fig_out)
        self.assertTrue(check_file)

    #VC-446 - The {EVT} method must generate a figure containing a {qq-plot} and a {pp-plot} of the distribution fitting.
    def test_30_fig_4_normal(self):

        self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        self.directory=OUTPUT_DIRECTORY
        self.main_filename=''
        self.csv_filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000_1.csv")

        self_fig_ref=os.path.join(INPUT_DIRECTORY, "wcet__qq_pp.png")
        self_fig_out=os.path.join(OUTPUT_DIRECTORY, "wcet__qq_pp.png")

        Evt.run(self)
        file = open(self_fig_out,'r', encoding='utf8',errors="ignore")

        png_json = (hashlib.sha256(file.read().encode('utf-8'))).hexdigest()
        file.close()

        self.assertEqual(png_json,
                         "1be9ba45a4730f771851831e216b072bb81d85616e214b0a91b35cb8f8a4470b")        

    #VC-447 - The {EVT} method must generate a figure containing a plot of the dataset series read from the csv file.
    def test_31_fig_5_normal(self):

        self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
        self.directory=OUTPUT_DIRECTORY
        self.main_filename=''
        self.csv_filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000_1.csv")

        self_fig_ref=os.path.join(INPUT_DIRECTORY, "wcet__pwcet.png")
        self_fig_out=os.path.join(OUTPUT_DIRECTORY, "wcet__pwcet.png")

        Evt.run(self)
        file = open(self_fig_out,'r', encoding='utf8',errors="ignore")

        png_json = (hashlib.sha256(file.read().encode('utf-8'))).hexdigest()
        file.close()

        self.assertEqual(png_json,
                         "d82767054f7f5b0d983cc940f5e4367d5bc138dcbd6473868c28474a9bc32ca2")

    #VC-448 - The {EVT} method must save all the figures generated during the evt methodology in the output folder.
    def test_32_figures_output_normal(self):

      self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
      self.directory=OUTPUT_DIRECTORY
      self.main_filename=''
      self.csv_filename=os.path.join(INPUT_DIRECTORY, "fibcall_30_10000_1.csv")

      Evt.run(self)
      check_file_1 = os.path.isfile(os.path.join(OUTPUT_DIRECTORY, "wcet__dataset.png"))
      check_file_2 = os.path.isfile(os.path.join(OUTPUT_DIRECTORY, "wcet__tail_fit.png"))
      check_file_3 = os.path.isfile(os.path.join(OUTPUT_DIRECTORY, "wcet__stat.png"))
      check_file_4 = os.path.isfile(os.path.join(OUTPUT_DIRECTORY, "wcet__qq_pp.png"))
      check_file_5 = os.path.isfile(os.path.join(OUTPUT_DIRECTORY, "wcet__pwcet.png"))
      self.assertTrue(check_file_1 and check_file_2 and check_file_3 and check_file_4 and check_file_5)

    #VC-449 - The {EVT} Method must receive the number of executions to run in from the project class.
    def test_33_exec_facade_output_normal(self):
        project = UserProject(sys._getframe(0).f_code.co_name,
                                "",
                                OUTPUT_DIRECTORY,
                                "avr",
                                "avr",
                                "",
                                "unknown",
                                "main",

                                    )
        project.number_exec = 20
        wcet = Mock()
        interface_target = Mock()
        interface_target.run.return_value = ["EVT", "Main", "Function", "#cycles 500", "Bye Bye"]
        args = [1, 2, 3]

        result_exec = evt_running(project, wcet, interface_target, args)

        if len(result_exec)==project.number_exec:result_bool=True
        self.assertTrue(result_bool)

    # def test_Tool_EVT_method(self):
    #     self.pwcet_bounds = [1e-9, 1e-10, 1e-11]
    #     self.directory=OUTPUT_DIRECTORY
    #     self.main_filename=''
    #     self.csv_filename=os.path.join(INPUT_DIRECTORY, "bsort1000_xtensa_evt_30000.csv")

    #     Evt.run(self)

if __name__ == '__main__':
    unittest.main()

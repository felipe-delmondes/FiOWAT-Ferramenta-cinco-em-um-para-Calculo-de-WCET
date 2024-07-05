import json
from cfg.timeMeter_aux import *
from progress.bar import Bar
import os
from os.path import join


class TimeMeter():
    """
    Class to obtain the execution time of the basic blocks of a program.
    Responsible for running the instrumented executable using an InterfaceTarget object 
    and extracting times from the execution output.


    Parameters
    ----------
    project : UserProject
        Contain all information about project

    inter_values : IntermediateValues
        All intermediate information obtained by pre processing

    interface_target : InterfaceTarget
        Coordenates the communication with the target hardware.

    Attributes
    ----------
    project : UserProject
        Contain all information about project

    inter_values : IntermediateValues
        All intermediate information obtained by pre processing

    interface_target : InterfaceTarget
        Coordenates the communication with the target hardware.

    partial_times : dict of dict
        Basic block times for each function in the program. Used
        to store values after each run.

    final_times : dict of dict
        Basic block times for each function in the program. Used
        to integrate the results obtained after each run.

    output : str
        The execution output returned by InterfaceTarget run method.
    """

    def __init__(self, project, inter_values, interface_target):
        self.project = project
        self.inter_values = inter_values
        self.interface_target = interface_target

        self.partial_times = {}
        self.final_times = {}

    def run_test_cases(self):
        """
        Calls the InterfaceTarget object to execute the underlying program.
        In each call, passes a test case from IntermediateValues as input arguments.
        After each call, extracts basic block times and integrates them in the final times dictionary.
        """
        try:
            bar = Bar('Running tests', max=len(self.inter_values.test_cases))
            bar.start()
            for args in self.inter_values.test_cases:
                self.output = self.interface_target.run(args)
                self.extract_times()
                self.integrate_times()
                bar.next()
            bar.finish()
        except Exception as e:
            print(
                f"\n\33[41mError running test case! {e}\33[0m")
            exit(-1)

    def extract_times(self):
        """
        Extracts basic block times from the execution output of an instrumented program.
        """
        try:
            time_marks = []
            for mark in [line for line in self.output
                         if line and line[0] == '#']:
                time_marks.append(Mark(mark))

            time_marks.append(Mark("#;@End;x;0"))

            self.partial_times['instrumentation'] = [time_marks[1].time]
            discount = self.partial_times['instrumentation'][0]

            stack = Stack()
            ctx = Context(last_mark=time_marks[1], block_time=0)
            for mark in time_marks[1:]:
                if mark.func == "@End":
                    insert_in_dict(self.partial_times, ctx.last_mark.func,
                                   ctx.last_mark.block, ctx.block_time)
                    return
                if mark.func == ctx.last_mark.func:
                    if mark.block != ctx.last_mark.block:
                        ctx.inc_block_time(mark.time - discount)
                        insert_in_dict(self.partial_times, ctx.last_mark.func,
                                       ctx.last_mark.block, ctx.block_time)
                        inc_in_dict(
                            self.partial_times, ctx.last_mark.func, "_total",
                            ctx.block_time)
                        ctx.block_time = 0

                        ctx.update_last_mark(mark)
                    else:
                        ctx.inc_block_time(mark.time - discount)
                        ctx.update_last_mark(mark)

                else:
                    found_ctx = stack.pop_if_matches(mark.func)
                    if found_ctx:
                        ctx.inc_block_time(mark.time - discount)
                        insert_in_dict(self.partial_times, ctx.last_mark.func,
                                       ctx.last_mark.block, ctx.block_time)
                        inc_in_dict(
                            self.partial_times, ctx.last_mark.func, "_total",
                            ctx.block_time)
                        ctx = found_ctx
                        ctx.update_last_mark(mark)
                    else:
                        stack.push(ctx)
                        new_ctx = Context(last_mark=mark,
                                          block_time=mark.time - discount)
                        ctx = new_ctx
        except Exception as e:
            print(
                f"\n\33[41mError extracting times after an execution: {e}\33[0m")
            exit(-1)
        return

    def integrate_times(self):
        """
        Integrates partial execution times into the dictionary with final times.

        The integration takes the two values for a given block and 
        choose the higher one to stay in the final dictionary.
        """
        try:
            if not self.final_times:
                self.final_times = self.partial_times
            else:
                for func in self.partial_times:
                    if func == "instrumentation":
                        continue
                    if func in self.final_times:
                        for block in self.partial_times[func]:
                            if block in self.final_times[func]:
                                self.final_times[func][block] = max(
                                    self.partial_times[func][block],
                                    self.final_times[func][block])
                            else:
                                self.final_times[func][block] = self.partial_times[func][block]
                    else:
                        self.final_times[func] = self.partial_times[func]
        except Exception as e:
            print(
                f"\n\33[41mError integrating times after an execution: {e}\33[0m")
            exit(-1)

    def save_times(self):
        """
        Saves the dictionary with basic block times to a JSON file.
        """
        output_file = self.project.output_directory+self.project.main_file_name+"_block_times.json"
        try:
            with open(f"{output_file}", "w") as report:
                json.dump(self.final_times, report, indent=4)
        except Exception as e:
            print(
                f"\n\33[41mError saving times after an execution: {e}\33[0m")
            exit(-1)

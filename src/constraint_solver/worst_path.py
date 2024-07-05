from utils.intermediate_values import IntermediateValues


def worst_path_match(
        intermediate_values: IntermediateValues, coverage_code: dict) -> float:
    '''
    Calculate the percentage match between calculated worst path and concrete execution


    Parameters
    ----------
    intermediate_values : IntermediateValues
        DTO with worst path

    coverage_code : dict
        Dictionary with number of executions of all basic blocks (Except main function).

        Basic blocks with 0 executions times not appear here.


    Returns
    -------
    match_percentage : float
        How many the execution match with calculated worst path.
        This value range is between 0 and 1
    '''
    difference = 0
    # Compare worst path with coverage test
    # Sum the difference between expected number of executions and real number of executions
    path_dict = intermediate_values.get_all_worst_path_basic_block()
    for function, value in path_dict.items():
        for basic_block in value:
            # If found the basic block, calculate the difference
            if (basic_block[0] in coverage_code[function]):
                difference += basic_block[1] - \
                    coverage_code[function][basic_block[0]]
            # Else, it's means the basic block was executed 0 times, so the subtraction is with 0
            else:
                difference += basic_block[1]

    # Return the percentagem of match
    return 1 - (difference / intermediate_values.get_number_executions_worst_path())

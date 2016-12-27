#!/usr/bin/python3

import random
import re
import sys
import auxiliar_functions as auxf
# import pdb

class RollInputError(Exception):
    '''    raised if the input syntax is wrong, tells the use how it should be done'''
    def __init__(self):
        self.msg = 'Try "!r n" (n>0) or "!r help" to find more roll options...'

class SuccessConditionError(Exception):
    '''raised if the success condition is greater than the dice size'''
    def __init__(self):
        self.msg = 'Success condition value should not be greater than the dice size...'

class ExplodingDiceError(Exception):
    '''raised if the explode value is greater than the dice size'''
    def __init__(self):
        self.msg = 'Exploding value should not be greater than dice size'

class ExplodingDiceTooSmallError(Exception):
    '''raised if the explode value is 1 or 2 (avoids long loops)'''
    def __init__(self):
        self.msg = 'Exploding value should be greater than 2'


def dice_input_verification(input_command, default_mode = 'wod'):
    '''
    checks the input command, match0 provides a link to the documentation
    matches 01 and 02 set the default roll mode (!r n)
    match1 is the default roll mode
    matches 2, 22, 3 and 32 are the arbitrary roll modes
    '''
    match0 = re.match('!r help$', input_command)
    match01 = re.match('!r set wod$', input_command)
    match02 = re.match('!r set simple$', input_command)
    match1 = re.match('!r (\d+)$', input_command)
    match2 = re.match('!r (\d+)d(\d+)$', input_command)
    match22 = re.match('!r (\d+)d(\d+)\?(\d+)$', input_command)      
    match3 = re.match('!r (\d+)d(\d+)x(\d+)$', input_command)
    match32 = re.match('!r (\d+)d(\d+)x(\d+)\?(\d+)$', input_command)
    
    if match0 != None:
        auxiliar_message = 'Find the documentation at:\nhttps://github.com/brmedeiros/dicey9000/blob/master/README.md'    
        return 0, 0, 0, 0, None, None, auxiliar_message
        
    elif match01 != None:
        mode_message = 'Default mode (!r n) set to World of Darksness (WoD)'
        return 0, 0, 0, 0, 'wod', mode_message, None

    elif match02 != None:
        mode_message = 'Default mode (!r n) set to simple (nd6)'
        return 0, 0, 0, 0, 'simple', mode_message, None
    
    elif match1 != None and default_mode == 'wod':
        return int(match1.group(1)), 10, 10, 7, 'wod', None, None

    elif match1 != None and default_mode == 'simple':
        return int(match1.group(1)), 6, 0, 0, 'simple', None, None
    
    elif match2 != None:
        return int(match2.group(1)), int(match2.group(2)), 0, 0, None, None, None

    elif match22 != None:
        if int(match22.group(3)) > int(match22.group(2)):
            raise SuccessConditionError
            return 0, 0, 0, 0, None, None, None
        else: 
            return int(match22.group(1)), int(match22.group(2)), 0, int(match22.group(3)), None, None, None
    
    elif match3 != None:
        if int(match3.group(3)) > int(match3.group(2)):
            raise ExplodingDiceError
            return 0, 0, 0, 0, None, None, None
        elif int(match3.group(3)) < 3:
            raise ExplodingDiceTooSmallError
            return 0, 0, 0, 0, None, None, None
        else:
            return int(match3.group(1)), int(match3.group(2)), int(match3.group(3)), 0, None, None, None
                
    elif match32 != None:
        if int(match32.group(3)) > int(match32.group(2)):
            raise ExplodingDiceError
            return 0, 0, 0, 0, None, None, None
        elif int(match32.group(3)) < 3:
            raise ExplodingDiceTooSmallError
            return 0, 0, 0, 0, None, None, None
        elif int(match32.group(4)) > int(match32.group(2)):
            raise SuccessConditionError
            return 0, 0, 0, 0, None, None, None
        else:
            return int(match32.group(1)), int(match32.group(2)), int(match32.group(3)), int(match32.group(4)), None, None, None
        
    else:
        raise RollInputError
        return 0, 0, 0, 0, None, None, None
       

def results_recorder(results_list, single_result, formated_results, format_option = False):
    ''' 
    creates 2 lists of the results, one formated for printing
    no exploding dice: format_option = False
    exploding dice: format_option = True
    '''
    results_list.append(single_result)
    if format_option == False:
        formated_results.append('{0}'.format(single_result))
    else:
        formated_results.append('x.{0}'.format(single_result))


def exploding_dice_check(explode_value, dice_type, results_list, single_result, formated_results):
    '''
    checks if there is an exploding dice condition
    if so the dice is rerolled if its result exceeds the explode value
    '''
    if explode_value > 0:
        while single_result >= explode_value:
            single_result = random.randint(1,dice_type)
            # auxf.sp_print('x.{}'.format(single_result))
            results_recorder(results_list, single_result, formated_results, 1)


def count_resuts_success(results_list, success_condition):
    '''
    counts the number of successes and informs the user about it
    '''
    if success_condition > 0:
        success_counter = 0
        for single_result in results_list:
            if single_result >= success_condition:
                success_counter += 1
        
        if success_counter == 0:
            success_msg = 'Failure...'
        elif success_counter == 1:
            success_msg = '1 success!'
        elif success_counter > 1:
            success_msg = '{} successes!'.format(success_counter)
        return success_msg
            

def dice_roll(number_of_dice, dice_type = 10, explode = 0, success_condition = 0):
    '''
    rolls the dice...
    the results list saves the dice rolls if there is a success condition > 0
    formated_results saves the information about exploded dice
    '''
    results = []
    formated_results = []
    for i in range(number_of_dice):
        result = random.randint(1,dice_type)
        # auxf.sp_print('{0:2}.'.format(i+1), result) # for printing in a 2-ish column table
        # auxf.sp_print(result) # for printing in a single line
        results_recorder(results, result, formated_results)
        exploding_dice_check(explode, dice_type, results, result, formated_results)
        # print() # for printing in a 2-ish column table
    # print() # for printing in a single line
    
    success_msg = count_resuts_success(results, success_condition)
    return results, formated_results, success_msg
    

def dice_exception_msg(exception, exception_message):
    '''
    returns the exception message and returns False
    (later used to decide if the roll will be made)
    '''
    s1 = 'An exception of type {0} occurred.'.format(type(exception).__name__)
    s2 = '------\n{0}'.format(exception_message)
    msg_string = '\n'.join([s1, s2])
    return msg_string, False


def should_it_roll(input_command, exception_tuple):
    '''
    Makes a dice roll if no dice exception occurs
    If an exception happens, the exception message
    is printed to the user
    '''
    pass


def main():
    try:
        will_roll = True
        n, d, x, s, mode, mode_msg, aux_msg = dice_input_verification(input('Type the roll you want to make...\n'))
        
        # while mode_msg != None:
        #     print(mode_msg)
        #     n, d, x, s, mode, mode_msg, aux_msg = dice_input_verification(input('Ready...\n'), mode)

        # while aux_msg != None:
        #     print(aux_msg)
        #     n, d, x, s, mode, mode_msg, aux_msg = dice_input_verification(input('Ready...\n'), mode)

    except (SuccessConditionError, ExplodingDiceError, ExplodingDiceTooSmallError, RollInputError) as ex:
        exception_msg_string, will_roll = dice_exception_msg(ex, ex.msg)
        print(exception_msg_string)        


    if will_roll == True: 
        res, formated_results, r_msg = dice_roll(n, d, x, s)
        results_string = ' '.join(formated_results)
        print(results_string)
        if r_msg != None: 
            print(r_msg)


if __name__ == '__main__':
    main()
    
    

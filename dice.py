#!/usr/bin/python3

import re
import random
import aux_functions as auxf

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
    checks the input command, roll_match checks dice roll input
    options_match checks help and default mode settings input
    '''
    roll_match = re.match(r'!r (?P<number_of_dice>\d+)(d(?P<dice_type>\d+))?'\
                          r'(x(?P<explode_value>\d+))?(\?(?P<success_condition>\d+))?$', input_command)

    option_match = re.match(r'!r (?P<help>help)?(set (?P<mode>wod|simple))?$', input_command)

    number_of_dice, dice_type, explode_value, success_condition, default_mode, mode_message, aux_message\
    = 0, 0, 0, 0, default_mode, None, None

    if roll_match:
        number_of_dice = int(roll_match.group('number_of_dice'))

        if not roll_match.group('dice_type'):
            if default_mode == 'wod':
                return number_of_dice, 10, 10, 8, 'wod', None, None
            if default_mode == 'simple':
                return number_of_dice, 6, 0, 0, 'simple', None, None
        else:
            dice_type = int(roll_match.group('dice_type'))
            if roll_match.group('explode_value'):
                explode_value = int(roll_match.group('explode_value'))
                if explode_value > dice_type:
                    raise ExplodingDiceError
                    return 0, 0, 0, 0, None, None, None
                elif explode_value < 3:
                    raise ExplodingDiceTooSmallError
                    return 0, 0, 0, 0, None, None, None
            if roll_match.group('success_condition'):
                 success_condition = int(roll_match.group('success_condition'))
                 if success_condition > dice_type:
                     raise SuccessConditionError
                     return 0, 0, 0, 0, None, None, None

        return number_of_dice, dice_type, explode_value, success_condition, default_mode, None, None

    elif option_match:
        if option_match.group('help'):
            aux_message = 'Find the documentation at:\nhttps://github.com/brmedeiros/dicey9000/blob/master/README.md'
            return 0, 0, 0, 0, None, None, aux_message
        if option_match.group('mode') == 'wod':
            mode_message = 'Default mode (!r n) set to World of Darksness (WoD)'
            return 0, 0, 0, 0, 'wod', mode_message, None
        if option_match.group('mode') == 'simple':
            mode_message = 'Default mode (!r n) set to simple (nd6)'
            return 0, 0, 0, 0, 'simple', mode_message, None

    else:
        raise RollInputError
        return 0, 0, 0, 0, None, None, None


def results_recorder(results_list, single_result, formated_results, success_condition, format_option = False):
    ''' 
    creates 2 lists of the results, one formated for printing...
    no exploding dice: format_option = False; exploding dice: format_option = True
    '''
    results_list.append(single_result)
    if not format_option:
        if single_result < success_condition and success_condition > 0 or success_condition == 0:
            formated_results.append('{0}'.format(single_result))
        elif single_result >= success_condition and success_condition > 0:
            formated_results.append('**{0}**'.format(single_result))
    else:
        if single_result < success_condition and success_condition > 0 or success_condition == 0:
            formated_results.append('x.{0}'.format(single_result))
        elif single_result >= success_condition and success_condition > 0:
            formated_results.append('x.**{0}**'.format(single_result))


def exploding_dice_check(explode_value, dice_type, results_list, single_result, formated_results, success_condition):
    '''
    checks if there is an exploding dice condition
    if so the dice is rerolled if its result exceeds the explode value
    '''
    if explode_value > 0:
        while single_result >= explode_value:
            single_result = random.randint(1,dice_type)
            # auxf.sp_print('x.{}'.format(single_result))
            results_recorder(results_list, single_result, formated_results, success_condition, True)


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
            success_msg = '**Failure...**'
        elif success_counter == 1:
            success_msg = '**1** success!'
        elif success_counter > 1:
            success_msg = '**{}** successes!'.format(success_counter)
        return success_msg
            

def dice_roll(number_of_dice, dice_type = 10, explode = 0, success_condition = 0):
    '''
    rolls the dice...
    the results list saves the dice rolls if success_condition > 0
    formated_results saves the information about exploded dice
    '''
    results = []
    formated_results = []
    for i in range(number_of_dice):
        result = random.randint(1,dice_type)
        results_recorder(results, result, formated_results, success_condition)
        exploding_dice_check(explode, dice_type, results, result, formated_results, success_condition)
    
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
    Makes a dice roll if no dice exception occurs.
    If an exception happens, the exception message is printed to the user
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
    
    

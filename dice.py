#!/usr/bin/python3

import re
import random
import dice_config as dcfg
import dice_exceptions as dexc

def dice_input_verification(input_command, mode = 'wod'):
    '''
    checks the input command, roll_match checks dice roll input
    options_match checks help and default mode (!r n) settings input
    '''
    roll_match = re.match(r'!r (?P<number_of_dice>\d+)(d(?P<dice_type>\d+))?'
                          r'(x(?P<explode_value>\d+))?(\?(?P<success_condition>\d+))?$', input_command)

    option_match = re.match(r'!r ((?P<help>help)|(set (?P<mode>wod|simple)))$', input_command)

    explode_value, success_condition = 0, 0

    if roll_match:
        number_of_dice = int(roll_match.group('number_of_dice'))

        if not roll_match.group('dice_type'):
            if mode == 'wod':
                return number_of_dice, 10, 10, 8, 'wod', None
            if mode == 'simple':
                return number_of_dice, 6, 0, 0, 'simple', None
        else:
            dice_type = int(roll_match.group('dice_type'))
            if roll_match.group('explode_value'):
                explode_value = int(roll_match.group('explode_value'))
                if explode_value > dice_type:
                    raise dexc.ExplodingDiceError
                elif explode_value < 3:
                    raise dexc.ExplodingDiceTooSmallError
            if roll_match.group('success_condition'):
                success_condition = int(roll_match.group('success_condition'))
                if success_condition > dice_type:
                    raise dexc.SuccessConditionError

        return number_of_dice, dice_type, explode_value, success_condition, mode, None

    elif option_match:
        if option_match.group('help'):
            cmd_msg = 'Find all available commands at:\nhttps://github.com/brmedeiros/dicey9000/blob/master/README.md'
            return 0, 0, 0, 0, mode, cmd_msg
        if option_match.group('mode') == 'wod':
            cmd_msg = 'Default mode (!r n) set to World of Darksness (WoD)'
            return 0, 0, 0, 0, 'wod', cmd_msg
        if option_match.group('mode') == 'simple':
            cmd_msg = 'Default mode (!r n) set to simple (nd6)'
            return 0, 0, 0, 0, 'simple', cmd_msg

    else:
        raise dexc.RollInputError


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
    '''checks if there is an exploding dice condition and rerolls the dice if it explodes'''
    if explode_value > 0:
        while single_result >= explode_value:
            single_result = random.randint(1,dice_type)
            results_recorder(results_list, single_result, formated_results, success_condition, True)


def count_resuts_success(results_list, success_condition):
    '''counts the number of successes and informs the user about it'''
    if success_condition > 0:
        success_counter = 0
        for single_result in results_list:
            if single_result >= success_condition:
                success_counter += 1

        if success_counter == 0:
            success_msg = 'Failure...'
        elif success_counter == 1:
            success_msg = '**1** success!'
        elif success_counter > 1:
            success_msg = '**{}** successes!'.format(success_counter)
        return success_msg


def dice_roll(number_of_dice, dice_type = 10, explode = 0, success_condition = 0):
    '''rolls the dice... results are saved if success_condition > 0'''
    results = []
    formated_results = []
    for i in range(number_of_dice):
        result = random.randint(1,dice_type)
        results_recorder(results, result, formated_results, success_condition)
        exploding_dice_check(explode, dice_type, results, result, formated_results, success_condition)

    success_msg = count_resuts_success(results, success_condition)
    return results, formated_results, success_msg


def should_it_roll(input_command, exception_tuple):
    '''Makes a dice roll if no dice exception occurs. If it happens, the exception message is printed'''
    pass


def main():
    try:
        will_roll = True
        n, d, x, s, mode, msg = dice_input_verification(input('Type the roll you want to make...\n'), dcfg.default_mode)
        while msg != None:
            print(msg)
            if dcfg.default_mode != mode: dcfg.default_mode = mode
            n, d, x, s, mode, msg = dice_input_verification(input('Ready...\n'), dcfg.default_mode)

    except (dexc.SuccessConditionError, dexc.ExplodingDiceError, dexc.ExplodingDiceTooSmallError, dexc.RollInputError) as ex:
        print(dexc.dice_exception_msg(ex, ex.msg))
        will_roll = False

    if will_roll == True:
        res, formated_results, r_msg = dice_roll(n, d, x, s)
        results_string = ' '.join(formated_results)
        print(results_string)
        if r_msg != None:
            print(r_msg)

if __name__ == '__main__':
    main()

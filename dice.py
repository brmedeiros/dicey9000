#!/usr/bin/python3

import re
import random
import dice_config as dcfg
import dice_exceptions as dexc

class DiceRoll():

    def __init__(self, number_of_dice, dice_type, roll_modifier, explode_value, success_condition):
        self.number_of_dice = number_of_dice
        self.dice_type = dice_type
        self.roll_modifier = roll_modifier
        self.explode_value = explode_value
        self.success_condition = success_condition
        self.successes = 0
        self.results = []
        self.formated_results = []

    def roll_dice(self):
        if self.number_of_dice != None:
            self.results = [random.randint(1, self.dice_type) for i in range(self.number_of_dice)]
            self.formated_results = ['{}'.format(result) for result in self.results]
            return self.results

    @property
    def total(self):
        if self.roll_modifier != None:
            return sum(self.results) + self.roll_modifier

    def explode_dice(self):
        if self.explode_value != None:
            for i, result in enumerate(self.results):
                if result >= self.explode_value:
                    self.results[i+1:i+1] = [random.randint(1, self.dice_type)]
                    self.formated_results[i+1:i+1] = ['x.{}'.format(self.results[i+1])]
        return self.results

    def success_counter(self):
        if self.success_condition != None:
            self.successes = 0
            for i, result in enumerate(self.results):
                if result >= self.success_condition:
                    self.successes += 1
                    self.formated_results[i] = '**{}**'.format(self.formated_results[i])
        return self.successes

    def output(self):
        success_msg = ''
        if self.success_condition != None:
            if self.successes == 0:
                success_msg = '\nFailure...'
            elif self.successes == 1:
                success_msg = '\n**1** success!'
            elif self.successes > 1:
                success_msg = '\n**{}** successes!'.format(self.successes)
        if self.roll_modifier != None:
            if self.roll_modifier > 0:
                return ' + '.join(self.formated_results) + ' + {} = {}'.format(self.roll_modifier, self.total) + success_msg
            elif self.roll_modifier < 0:
                return ' + '.join(self.formated_results) + ' + ({}) = {}'.format(self.roll_modifier, self.total) + success_msg
            else:
                return ' + '.join(self.formated_results) + ' = {}'.format(self.total) + success_msg
        else:
            return '  '.join(self.formated_results) + success_msg


def dice_input_verification(input_command, mode = 'wod'):
    '''
    checks the input command, roll_match checks dice roll input
    options_match checks help and default mode (!r n) settings input
    '''
    roll_match = re.match(r'!r (?P<number_of_dice>\d+)(d(?P<dice_type>\d+))?'
                          r'((?P<total>\+)(?P<add_mod>\d+)?|(-(?P<sub_mod>\d+)))?'
                          r'(x(?P<explode_value>\d+))?(\?(?P<success_condition>\d+))?$', input_command)

    option_match = re.match(r'!r ((?P<help>help)|(set (?P<mode>wod|simple))|(?P<status>status))$', input_command)

    modifier, explode_value, success_condition = None, None, None

    if roll_match:
        number_of_dice = int(roll_match.group('number_of_dice'))
        if not any(roll_match.group('dice_type', 'total', 'sub_mod', 'explode_value', 'success_condition')):
            if mode == 'wod':
                return number_of_dice, 10, None, 10, 8, 'wod', None
            if mode == 'simple':
                return number_of_dice, 6, 0, None, None, 'simple', None

        elif roll_match.group('dice_type'):
            dice_type = int(roll_match.group('dice_type'))
            if dice_type == 0:
                raise dexc.DiceTypeError
            if roll_match.group('add_mod'):
                modifier = int(roll_match.group('add_mod'))
            elif roll_match.group('sub_mod'):
                modifier = -int(roll_match.group('sub_mod'))
            elif roll_match.group('total'):
                modifier = 0
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
        else:
            raise dexc.RollInputError
        return number_of_dice, dice_type, modifier, explode_value, success_condition, mode, None

    elif option_match:
        if option_match.group('help'):
            cmd_msg = 'Find all available commands at:\nhttps://github.com/brmedeiros/dicey9000/blob/master/README.md'
            return None, None, None, None, None, mode, cmd_msg
        if option_match.group('mode') == 'wod':
            cmd_msg = 'Default mode (!r n) set to World of Darksness (WoD)'
            return None, None, None, None, None, 'wod', cmd_msg
        if option_match.group('mode') == 'simple':
            cmd_msg = 'Default mode (!r n) set to simple (nd6)'
            return None, None, None, None, None, 'simple', cmd_msg
        if option_match.group('status'):
            cmd_msg = 'Default mode is currently {}.'.format(dcfg.mode)
            return None, None, None, None, None, mode, cmd_msg
    else:
        raise dexc.RollInputError


def main():
    try:
        while True:
            try:
                will_roll = True
                n, d, m, x, s, dcfg.mode, msg = dice_input_verification(input('\nType the roll you want to make...\n'),
                                                                        dcfg.mode)
                while msg != None:
                    print(msg)
                    n, d, m, x, s, dcfg.mode, msg = dice_input_verification(input('Ready...\n'), dcfg.mode)

            except (dexc.SuccessConditionError, dexc.ExplodingDiceError, dexc.DiceTypeError,
                    dexc.ExplodingDiceTooSmallError, dexc.RollInputError) as ex:
                print(dexc.dice_exception_msg(ex, ex.msg))
                will_roll = False

            if will_roll == True:
                my_roll = DiceRoll(n, d, m, x, s)
                my_roll.roll_dice()
                my_roll.explode_dice()
                my_roll.success_counter()
                print(my_roll.output())

    except KeyboardInterrupt:
        print('\nbye!')

if __name__ == '__main__':
    main()

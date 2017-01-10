#!/usr/bin/python3

import re
import random
import dice_config as dcfg
import dice_exceptions as dexc

class DiceRollClass():
    
    def __init__(self, number_of_dice, dice_type, roll_modifier, explode_value, success_condition):
        self.number_of_dice = number_of_dice
        self.dice_type = dice_type
        self.roll_modifier = roll_modifier
        self.explode_value = explode_value
        self.success_condition = success_condition
        self.results = []
        self.successes = 0
        self.formated_results = []
                
    def roll_dice(self):
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
            if self.roll_modifier >= 0:
                return ' + '.join(self.formated_results) + ' + {} = {}'.format(self.roll_modifier, self.total) + success_msg
            else:
                return ' + '.join(self.formated_results) + ' + ({}) = {}'.format(self.roll_modifier, self.total) + success_msg
        else:
            return '  '.join(self.formated_results) + success_msg

        
def main():
    for i in range(5):
        roll = DiceRollClass(5, 10, None, 10, 8)
        # print(roll.roll_dice(), roll.successes, roll.total)
        roll.roll_dice()
        print(roll.explode_dice(), roll.success_counter())
        # print(roll.formated_results)
        print(roll.output())
        print()

if __name__ == '__main__':
    main()







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

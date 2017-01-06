import unittest
import dice
import dice_config as dcfg
import dice_exceptions as dexc

class DiceInputVerificationTest(unittest.TestCase):
    def test_dice_roll_input_wod(self):
        examples = {'!r 5':[5, 10, 10, 8, 'wod', None],
                    '!r 2000':[2000, 10, 10, 8, 'wod', None],
                    '!r 2d8':[2, 8, 0, 0, 'wod', None],
                    '!r 7d6x4':[7, 6, 4, 0, 'wod', None],
                    '!r 5000d700x700':[5000, 700, 700, 0, 'wod', None],
                    '!r 15d20?20':[15, 20, 0, 20, 'wod', None],
                    '!r 39d10x5?8':[39, 10, 5, 8, 'wod', None],
                    '!r 1d4x4?4':[1, 4, 4, 4, 'wod', None]}
        for example, value in examples.items():
            n, d, x, s, mode, cmd_msg  = dice.dice_input_verification(example)
            self.assertEqual([n, d, x, s, mode, cmd_msg], value)

    def test_dice_roll_input_simple(self):
        examples = {'!r 7':[7, 6, 0, 0, 'simple', None],
                    '!r 2000':[2000, 6, 0, 0, 'simple', None],
                    '!r 2d8':[2, 8, 0, 0, 'simple', None],
                    '!r 7d6x4':[7, 6, 4, 0, 'simple', None],
                    '!r 8000d899x899':[8000, 899, 899, 0, 'simple', None],
                    '!r 15d20?20':[15, 20, 0, 20, 'simple', None],
                    '!r 39d10x5?8':[39, 10, 5, 8, 'simple', None],
                    '!r 1d4x4?4':[1, 4, 4, 4, 'simple', None]}
        for example, value in examples.items():
             n, d, x, s, mode, cmd_msg = dice.dice_input_verification(example, 'simple')
             self.assertEqual([n, d, x, s, mode, cmd_msg], value)

    def test_dice_options_help(self):
        examples = {'!r help': [0, 0, 0, 0, dcfg.mode, 'Find all available commands at:'
                                '\nhttps://github.com/brmedeiros/dicey9000/blob/master/README.md']}
        for example, value in examples.items():
            n, d, x, s, mode, cmd_msg  = dice.dice_input_verification(example, dcfg.mode)
            self.assertEqual([n, d, x, s, mode, cmd_msg], value)

    def test_dice_options_mode(self):
        examples = {'!r set wod': [0, 0, 0, 0, 'wod', 'Default mode (!r n) set to World of Darksness (WoD)'],
                    '!r set simple': [0, 0, 0, 0, 'simple', 'Default mode (!r n) set to simple (nd6)']}
        for dmode in ['wod', 'simple']:
            for example, value in examples.items():
                n, d, x, s, mode, cmd_msg  = dice.dice_input_verification(example, dmode)
                self.assertEqual([n, d, x, s, mode, cmd_msg], value)

    def test_dice_input_exception(self):
        examples = ['!r ', '!r dmeoamdef', '!r kelf laij', '!r 2 3', '!r 6dz','!r 30dx', '!r 5d7x7?', '!r 9d10?',
                    '!r -10', '!r -6d8', '!r 6d8x?10', '!r 12d12x18?', '!r set ', '!r set help', '!r set akneoi',
                    '!r 3d6 help', '!r set 6d8?4 wod']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.RollInputError, dice.dice_input_verification, example, mode)

    def test_eploding_dice_exception(self):
        examples = ['!r 5d8x9', '!r 12d60x100', '!r 1d6x9?4']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.ExplodingDiceError, dice.dice_input_verification, example, mode)

    def test_eploding_dice_too_small_exception(self):
        examples = ['!r 5d8x1', '!r 8d6x2', '!r 3d70x1?10', '!r 10d2x2?2']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.ExplodingDiceTooSmallError, dice.dice_input_verification, example, mode)

    def test_success_condition_exception(self):
        examples = ['!r 2d8?9', '!r 2d15?55', '!r 65d10x6?11', '!r 32d5x5?100']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.SuccessConditionError, dice.dice_input_verification, example, mode)

class ResultsRecorderTest(unittest.TestCase):
    def test_results_recorder(self):
        examples = [
            [[7, 12, 1, 6, 10, 25, 555, 2], 10, ['7', '**12**', '1', '6', '**10**', '**25**', '**555**', '2'], False],
            [[2, 5, 87, 6, 4, 65], 50, ['2', '5', '**87**', '6', '4', '**65**'], False],
            [[6, 8, 9, 1, 1, 2], 0, ['x.6', 'x.8', 'x.9', 'x.1', 'x.1', 'x.2'], True],
            [[6, 8, 9, 1, 1, 2], 5, ['x.**6**', 'x.**8**', 'x.**9**', 'x.1', 'x.1', 'x.2'], True]
        ]
        for example in examples:
            list1, list2 = [], []
            for result in example[0]:
                dice.results_recorder(list1, result, list2, example[1], example[3])
            self.assertEqual([list1, list2], [example[0], example[2]])

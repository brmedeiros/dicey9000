import unittest
import unittest.mock as mock
import dice
import dice_config as dcfg
import dice_exceptions as dexc

class DiceInputVerificationTest(unittest.TestCase):
    def test_dice_roll_input_wod(self):
        examples = {'!r 5':[5, 10, None, 10, 8, 'wod', None],
                    '!r 2000':[2000, 10, None, 10, 8, 'wod', None],
                    '!r 2d8':[2, 8, None, None, None, 'wod', None],
                    '!r 7d6x4':[7, 6, None, 4, None, 'wod', None],
                    '!r 5000d700x700':[5000, 700, None, 700, None, 'wod', None],
                    '!r 15d20?20':[15, 20, None, None, 20, 'wod', None],
                    '!r 39d10x5?8':[39, 10, None, 5, 8, 'wod', None],
                    '!r 1d4x4?4':[1, 4, None, 4, 4, 'wod', None],
                    '!r 6d6+':[6, 6, 0, None, None, 'wod', None],
                    '!r 5d32+5':[5, 32, 5, None, None, 'wod', None],
                    '!r 17d4-12':[17, 4, -12, None, None, 'wod', None],
                    '!r 3d12+x12':[3, 12, 0, 12, None, 'wod', None],
                    '!r 10d20-7?15':[10, 20, -7, None, 15, 'wod', None],
                    '!r 768d37+33x5?23':[768, 37, 33, 5, 23, 'wod', None]}
        for example, value in examples.items():
            n, d, m, x, s, mode, cmd_msg  = dice.dice_input_verification(example)
            self.assertEqual([n, d, m, x, s, mode, cmd_msg], value)

    def test_dice_roll_input_simple(self):
        examples = {'!r 7':[7, 6, 0, None, None, 'simple', None],
                    '!r 2000':[2000, 6, 0, None, None, 'simple', None],
                    '!r 2d8':[2, 8, None, None, None, 'simple', None],
                    '!r 7d6x4':[7, 6, None, 4, None, 'simple', None],
                    '!r 8000d899x899':[8000, 899, None, 899, None, 'simple', None],
                    '!r 15d20?20':[15, 20, None, None, 20, 'simple', None],
                    '!r 39d10x5?8':[39, 10, None, 5, 8, 'simple', None],
                    '!r 1d4x4?4':[1, 4, None, 4, 4, 'simple', None],
                    '!r 6d6+':[6, 6, 0, None, None, 'simple', None],
                    '!r 5d32+5':[5, 32, 5, None, None, 'simple', None],
                    '!r 17d4-12':[17, 4, -12, None, None, 'simple', None],
                    '!r 3d12+x12':[3, 12, 0, 12, None, 'simple', None],
                    '!r 10d20-7?15':[10, 20, -7, None, 15, 'simple', None],
                    '!r 768d37+33x5?23':[768, 37, 33, 5, 23, 'simple', None]}
        for example, value in examples.items():
             n, d, m, x, s, mode, cmd_msg = dice.dice_input_verification(example, 'simple')
             self.assertEqual([n, d, m, x, s, mode, cmd_msg], value)

    def test_dice_options_help(self):
        examples = {'!r help': [None, None, None, None, None, dcfg.mode, 'Find all available commands at:'
                                '\nhttps://github.com/brmedeiros/dicey9000/blob/master/README.md']}
        for example, value in examples.items():
            n, d, m, x, s, mode, cmd_msg  = dice.dice_input_verification(example, dcfg.mode)
            self.assertEqual([n, d, m, x, s, mode, cmd_msg], value)

    def test_dice_options_mode(self):
        examples = {'!r set wod': [None, None, None, None, None,
                                   'wod', 'Default mode (!r n) set to World of Darksness (WoD)'],
                    '!r set simple': [None, None, None, None, None,
                                      'simple', 'Default mode (!r n) set to simple (nd6)']}
        for dmode in ['wod', 'simple']:
            for example, value in examples.items():
                n, d, m, x, s, mode, cmd_msg  = dice.dice_input_verification(example, dmode)
                self.assertEqual([n, d, m, x, s, mode, cmd_msg], value)

    def test_dice_input_exception(self):
        examples = ['!r ', '!r dmeoamdef', '!r kelf laij', '!r 2 3', '!r 6dz','!r 30dx', '!r 5d7x7?', '!r 9d10?',
                    '!r -10', '!r -6d8', '!r 6d8x?10', '!r 12d12x18?', '!r set ', '!r set help', '!r set akneoi',
                    '!r 3d6 help', '!r set 6d8?4 wod', '!r 6d12-', '!r 8d4-45?+', '!r 12d6+8-9', '!r 8d20-923+1x10?15',
                    '!r 6+','!r 5+2', '!r 7-', '!r 12-3', '!r 20x4', '!r 25?12', '!r 2+7x4?4', '!r 5-12x15?20']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.RollInputError, dice.dice_input_verification, example, mode)

    def test_exploding_dice_exception(self):
        examples = ['!r 5d8x9', '!r 12d60x100', '!r 1d6x9?4', '!r 78d5+x43', '!r 6d12-10x15', '!r 8d20+1x22?20']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.ExplodingDiceError, dice.dice_input_verification, example, mode)

    def test_exploding_dice_too_small_exception(self):
        examples = ['!r 5d8x1', '!r 8d6x2', '!r 3d70x1?10', '!r 10d2x2?2', '!r 78d5+x2', '!r 6d12-10x1',
                    '!r 8d20+1x2?20']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.ExplodingDiceTooSmallError, dice.dice_input_verification, example, mode)

    def test_success_condition_exception(self):
        examples = ['!r 2d8?9', '!r 2d15?55', '!r 65d10x6?11', '!r 32d5x5?100', '!r 78d5+?6', '!r 6d12-10?45',
                    '!r 8d20+1x18?200']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.SuccessConditionError, dice.dice_input_verification, example, mode)

    def test_dice_type_exception(self):
        examples = ['!r 2d0', '!r 50d0?55', '!r 6d0x6?11', '!r 32d0x5?100', '!r 78d0+?6', '!r 6d0-10?45',
                    '!r 8d0+1x18?200']
        for mode in ['wod', 'simple']:
            for example in examples:
                self.assertRaises(dexc.DiceTypeError, dice.dice_input_verification, example, mode)

class DiceRollTest(unittest.TestCase):
    @mock.patch('random.randint')
    def test_roll_dice(self, random_call):
        results = [1, 4, 6, 6, 2, 3, 5]
        random_call.side_effect = results
        target = dice.DiceRoll(7, 6, None, None, None)
        target.roll_dice()
        self.assertEqual(7, target.number_of_dice)
        self.assertEqual(7, len(target.results))
        for i, result in enumerate(results):
            self.assertEqual(result, target.results[i])
            self.assertEqual(str(result), target.formated_results[i])

    @mock.patch('random.randint')
    def test_total(self, random_call):
        results = [1, 10, 5, 4, 10]
        random_call.side_effect = results
        examples = [0, 5, -10, 22, -50]
        for example in examples:
            target = dice.DiceRoll(5, 10, example, None, None)
            target.roll_dice()
            self.assertEqual(example, target.roll_modifier)
            self.assertEqual(sum(results) + example, target.total)
        
    @mock.patch('random.randint')
    def test_explode(self, random_call):
        results = [1, 12, 5, 4, 7, 6]
        random_call.side_effect = results
        target = dice.DiceRoll(6, 12, None, 12, None)
        target.roll_dice()
        self.assertEqual(12, target.explode_value)
        self.assertEqual(len(results)+1, len(target.results)) 

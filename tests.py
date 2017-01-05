#!/usr/bin/python3

import unittest
import dice
from dice_exceptions import *

class DiceInputVerificationTest(unittest.TestCase):
    def test_dice_roll_input(self):
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 5')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [5, 10, 10, 8, 'wod', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 2000')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [2000, 10, 10, 8, 'wod', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 77', 'simple')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [77, 6, 0, 0, 'simple', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 2d8')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [2, 8, 0, 0, 'wod', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 7d6x4')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [7, 6, 4, 0, 'wod', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 5000d700x700')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [5000, 700, 700, 0, 'wod', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 15d20?20')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [15, 20, 0, 20, 'wod', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 39d10x5?8')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [39, 10, 5, 8, 'wod', None, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r 1d4x4?4')
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [1, 4, 4, 4, 'wod', None, None])
        
    def test_dice_options_input(self):
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r help')
        help_string = 'Find all available commands at:\nhttps://github.com/brmedeiros/dicey9000/blob/master/README.md'
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [0, 0, 0, 0, None, None, help_string])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r set wod')
        mode_string = 'Default mode (!r n) set to World of Darksness (WoD)'
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [0, 0, 0, 0, 'wod', mode_string, None])
        n, d, x, s, mode, mode_msg, aux_msg = dice.dice_input_verification('!r set simple')
        mode_string = 'Default mode (!r n) set to simple (nd6)'
        self.assertEqual([n, d, x, s, mode, mode_msg, aux_msg], [0, 0, 0, 0, 'simple', mode_string, None])

    def test_dice_input_exception(self):
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r ')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r dmeoamdef')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r kelf laij')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r 2 3')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r 6dz')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r 30dx')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r 5d7x7?')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r 9d10?')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r 6d8x?10')
        self.assertRaises(RollInputError, dice.dice_input_verification, '!r 12d12x18?')

    def test_eploding_dice_exception(self):
        self.assertRaises(ExplodingDiceError, dice.dice_input_verification, '!r 5d8x9')
        self.assertRaises(ExplodingDiceError, dice.dice_input_verification, '!r 12d60x100')
        self.assertRaises(ExplodingDiceError, dice.dice_input_verification, '!r 1d6x9?4')

    def test_eploding_dice_too_small_exception(self):
        self.assertRaises(ExplodingDiceTooSmallError, dice.dice_input_verification, '!r 5d8x1')
        self.assertRaises(ExplodingDiceTooSmallError, dice.dice_input_verification, '!r 8d6x2')
        self.assertRaises(ExplodingDiceTooSmallError, dice.dice_input_verification, '!r 3d70x1?10')
        self.assertRaises(ExplodingDiceTooSmallError, dice.dice_input_verification, '!r 10d2x2?2')
    
    def test_success_condition_exception(self):
        self.assertRaises(SuccessConditionError, dice.dice_input_verification, '!r 2d8?9')
        self.assertRaises(SuccessConditionError, dice.dice_input_verification, '!r 2d15?55')
        self.assertRaises(SuccessConditionError, dice.dice_input_verification, '!r 65d10x6?11')
        self.assertRaises(SuccessConditionError, dice.dice_input_verification, '!r 32d5x5?100')

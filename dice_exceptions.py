class RollInputError(Exception):
    '''raised if the input syntax is wrong, tells the use how it should be done'''
    def __init__(self):
        self.msg = 'Try "!r n" (n>0) or "!r help" to find more roll options.'

class SuccessConditionError(Exception):
    '''raised if the success condition is greater than the dice size'''
    def __init__(self):
        self.msg = 'Success condition value should not be greater than the dice size.'

class ExplodingDiceError(Exception):
    '''raised if the explode value is greater than the dice size'''
    def __init__(self):
        self.msg = 'Exploding value should not be greater than dice size.'

class ExplodingDiceTooSmallError(Exception):
    '''raised if the explode value is 1 or 2 (avoids long loops)'''
    def __init__(self):
        self.msg = 'Exploding value should be greater than 2.'

class GlitchValueError(Exception):
    '''raised if the glitch value is greater than the dice size'''
    def __init__(self):
        self.msg = 'Glitch value should be greater than 0 and less than dice size'

class DiceTypeError(Exception):
    '''raised if a zero-sided die is chosen by the user'''
    def __init__(self):
        self.msg = 'Dice type should be greater than 0.'

def dice_exception_msg(exception, exception_msg):
    '''returns the exception message'''
    msg_string = 'An exception of type {0} occurred.\n------\n{1}'.format(type(exception).__name__, exception_msg)
    return msg_string

#!/usr/bin/python3

import os
import discord
import asyncio
import random
import datetime as dt
import dice
import dice_config as dcfg
import dice_exceptions as dexc
import aux_functions as auxf

def main():

    client = discord.Client()

    @client.async_event # equivalent to @client.event\n@asyncio.courotine
    def on_ready():
        '''
        this function represents the event 'being ready'...
        it should not be called anywhere and it is defined in the discord module
        '''
        print('DICEY9000 v.2.0\n------\nLogged in as {0}, id: {1}'.format(client.user, client.user.id))
        auxf.sp_print('Server(s) joined:')
        for server in client.servers:
            auxf.sp_print('{0}'.format(server))
        print('\n------')

    @client.async_event
    def on_message(message):
        '''
        this function represents a 'message event' in any of the channels...
        it should not be called anywhere and it is defined in the discord module
        '''
        if message.author == client.user:
            print('{:%d/%m/%y %H:%M} @{} {}: {}'
                  .format(dt.datetime.now(), message.channel, message.author.name, message.content))

        if message.content.startswith('!r'):
            print('{:%d/%m/%y %H:%M} @{} user: {}'
                  .format(dt.datetime.now(), message.channel, message.content))
            try:
                will_roll = True
                number_of_dice, dice_type, modifier, explode, success, dcfg.mode, cmd_msg\
                = dice.dice_input_verification(message.content, dcfg.mode)

                if cmd_msg != None:
                    yield from client.send_message(message.channel, cmd_msg)
                    will_roll = False

            except (dexc.SuccessConditionError, dexc.ExplodingDiceError, dexc.DiceTypeError,
                    dexc.ExplodingDiceTooSmallError, dexc.RollInputError) as ex:
                yield from client.send_message(message.channel, dexc.dice_exception_msg(ex, ex.msg))
                will_roll = False

            if will_roll == True:
                my_roll = dice.DiceRoll(number_of_dice, dice_type, modifier, explode, success)
                my_roll.roll_dice()
                my_roll.explode_dice()
                my_roll.success_counter()
                yield from client.send_message(message.channel, my_roll.output())                

    token = os.environ['DICEY9000_TOKEN']
    client.run(token)

if __name__ == '__main__':
    main()

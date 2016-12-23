#!/usr/bin/python3

import discord
import asyncio
import random
from datetime import datetime

import dice
import dicey9000_login_info as info
from auxiliar_functions import sp_print

def main():

    client = discord.Client()
    
    @client.async_event
    def on_error():
        pass
    
    @client.async_event # equivalent to @client.event \n @asyncio.courotine
    def on_ready():
        '''
        this function represents the event 'being ready'...
        it should not be called anywhere
        it is defined in the discord module
        '''
        print('------')
        print('Logged in as {}, id: {}'.format(client.user, client.user.id))
        sp_print('Server(s) joined:')
        for server in client.servers:
            sp_print('{}'.format(server))
        print()
        print('------')
        global default_mode
        default_mode = 'wod' #starts dicey9000 with WoD default mode


    @client.async_event    
    def on_message(message):
        '''
        this function represents a 'message event' in any of the channels...
        it should not be called anywhere
        it is defined in the discord module
        '''
        # print messages written in the channels (from all servers?) to the terminal screen 
        print('{:%d/%m/%y %H:%M} @{} {}: {}'.format(datetime.now(), message.channel, message.author.name, message.content))
        
        if message.content.startswith('!r'):
            global default_mode
            try:
                will_roll = True
                number_of_dice, dice_type, explode, success, mode, mode_msg = dice.dice_input_verification(message.content, default_mode)
                if mode_msg != None:
                    yield from client.send_message(message.channel, mode_msg)
                    default_mode = mode
            except dice.SuccessConditionError as ex:
                exception_msg_string, will_roll = dice.dice_exception_msg(ex, ex.msg)
                yield from client.send_message(message.channel, exception_msg_string)
            except dice.ExplodingDiceError as ex:
                exception_msg_string, will_roll = dice.dice_exception_msg(ex, ex.msg)
                yield from client.send_message(message.channel, exception_msg_string)
            except dice.ExplodingDiceTooSmallError as ex:
                exception_msg_string, will_roll = dice.dice_exception_msg(ex, ex.msg)
                yield from client.send_message(message.channel, exception_msg_string)
            except dice.RollInputError as ex:
                exception_msg_string, will_roll = dice.dice_exception_msg(ex, ex.msg)
                yield from client.send_message(message.channel, exception_msg_string)


            if will_roll == True: 
                results, formated_results, success_msg  = dice.dice_roll(number_of_dice, dice_type, explode, success)
                results_string = '  '.join(formated_results)
                yield from client.send_message(message.channel, results_string)
                if success_msg != None:
                    yield from client.send_message(message.channel, success_msg)

    
    client.run(info.token)

if __name__ == '__main__':
    main()

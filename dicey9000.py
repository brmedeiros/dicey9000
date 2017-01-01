#!/usr/bin/python3

import os
import discord
import asyncio
import random
import datetime as dt

import dice
import aux_functions as auxf

def main():

    client = discord.Client()
    
        
    @client.async_event # equivalent to @client.event\n@asyncio.courotine
    def on_ready():
        '''
        this function represents the event 'being ready'...
        it should not be called anywhere
        it is defined in the discord module
        '''
        print('DICEY9000 v.1.3\n------\nLogged in as {0}, id: {1}'.format(client.user, client.user.id))
        auxf.sp_print('Server(s) joined:')
        for server in client.servers:
            auxf.sp_print('{0}'.format(server))
        print('\n------')
        
        global default_mode
        default_mode = 'wod'


    @client.async_event    
    def on_message(message):
        '''
        this function represents a 'message event' in any of the channels...
        it should not be called anywhere
        it is defined in the discord module
        '''

        if message.author == client.user:
            print('{:%d/%m/%y %H:%M} @{} {}: {}'
                  .format(dt.datetime.now(), message.channel, message.author.name, message.content))
        
        
        if message.content.startswith('!r'):
            global default_mode

            print('{:%d/%m/%y %H:%M} @{} user: {}'
                  .format(dt.datetime.now(), message.channel, message.content))
            
            try:
                will_roll = True
                number_of_dice, dice_type, explode, success, mode, mode_msg, aux_msg\
                = dice.dice_input_verification(message.content, default_mode)

                if mode_msg != None:
                    yield from client.send_message(message.channel, mode_msg)
                    default_mode = mode
                    will_roll = False
                
                if aux_msg != None:
                    yield from client.send_message(message.channel, aux_msg)
                    will_roll = False

            except (dice.SuccessConditionError, dice.ExplodingDiceError,
                    dice.ExplodingDiceTooSmallError, dice.RollInputError) as ex:
                exception_msg_string, will_roll = dice.dice_exception_msg(ex, ex.msg)
                yield from client.send_message(message.channel, exception_msg_string)


            if will_roll == True: 
                results, formated_results, success_msg  = dice.dice_roll(number_of_dice, dice_type, explode, success)
                results_string = '  '.join(formated_results)
                yield from client.send_message(message.channel, results_string)
                if success_msg != None:
                    yield from client.send_message(message.channel, success_msg)
    
    
    token = os.environ['DICEY9000_TOKEN']
    client.run(token)

if __name__ == '__main__':
    main()

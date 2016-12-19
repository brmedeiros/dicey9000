DICEY9000

v1.0

dicey9000 is a bot for discord that makes dice rolls.
It takes commands from users messages starting with '!r'

---Default mode - World of Darkness (WoD)

Call it by typing: 

   !r n

where n is the number of 10 sided dice to be rolled.
A dice explodes (gets rolled again) if its result is
equal to 10. A result list is printed and the number 
f success is shown.

---Arbitrary roll 

An arbitrary roll can be made with the following syntax:
   
   !r (number_of_dices)d(dice_type)x(explode_value)?(success_condition)
   	
All entries should be greater than 0.
If the dice result is equal or greater than the explode_value
it gets rolled again.
If the dice result is equal or greater than the success_condition
a success is added to the total number of successes.
Both x(explode_value) and ?(success_condition) are optional. 


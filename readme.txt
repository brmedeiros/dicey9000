# dicey9000

*v1.3*

dicey9000 is a bot for discord that makes dice rolls.
It takes commands from users messages starting with `!r`

#### Default mode

Activate the default roll mode by typing

   `!r n`

where `n` is the number of dices to be rolled.

#### Choose default mode

You can choose the default roll mode by typing

   `!r set mode_name`

There are currently two possible `mode_name` choices:

- `wod`

World of Darkness (WoD) (chosen by default)

Uses the WoD rules to count successes and explode dices. A successes
happens if the dice scores 7 of higher. A dice explodes (gets rolled
again) if its result is equal to 10. A result list is printed and the
number of successes is shown.

- `simple`

Rolls n 6 sided dices and a list of the results are shown.

#### Arbitrary roll 

An arbitrary roll can be made with the following syntax:
   
   `!r (number_of_dices)d(dice_type)x(explode_value)?(success_condition)`
   	
  * All entries should be greater than 0. 
  * If the dice result is equal or greater than the explode_value it gets
    rolled again.
  * If the dice result is equal or greater than the success_condition a
    success is added to the total number of successes.
  * Both x(explode_value) and ?(success_condition) are optional.

#### Help

Get the link to this page by typing

   `!r help`

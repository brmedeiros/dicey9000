# dicey9000

*v2.1*

dicey9000 is a bot for discord that makes dice rolls.
It takes commands from users messages starting with `!r`

#### Default mode

Activate the default roll mode by typing

  `!r n`

where `n` is the number of dice to be rolled.

#### Choose default mode

You can choose the default roll mode by typing

  `!r set mode_name`

There are currently two possible `mode_name` choices:

- `wod`

World of Darkness (WoD) (chosen by default)

Uses the WoD rules to count successes and explode dice. A success
happens if a die scores 7 of higher. A die explodes (is rolled again)
if its result is equal to 10. A result list is printed and the number
of successes is shown.

- `simple`

Rolls n 6 sided dice and adds the results.

#### Check default mode

You can check which mode is currently active by typing

  `!r status`

#### Arbitrary roll

An arbitrary roll can be made with the following syntax:

  `!r (number_of_dice)d(dice_type)+(roll_modifier)x(explode_value)?(success_condition)`

  * All entries should be greater than 0.
  * If roll_modifier is present, the results are added and modified
    by roll_modifier.
    - A negative modfier can be applied to the roll by exchanging '+' with '-'.
    - Alternatively, if only '+' is present (without a roll_modifier value)
      the results will be added with no modidier.
  * If the roll result is equal or greater than the explode_value, the
    die is rolled again.
  * If the roll result is equal or greater than the success_condition, a
    success is added to the total number of successes.
  * x(explode_value), +(roll_modifier) and ?(success_condition)
    are optional entries.

#### Help

Get the link to this page by typing

  `!r help`

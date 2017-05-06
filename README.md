# dicey9000

*v2.2*

dicey9000 is a bot for discord that makes dice rolls.
It takes commands from users messages starting with `!r`

#### Default mode

Activate the default roll mode by typing

  `!r n`

where `n` is the number of dice to be rolled.

#### Choose default mode

You can choose the default roll mode by typing

  `!r set mode_name`

There are currently three possible `mode_name` choices:

- `wod`

World of Darkness (WoD) (chosen by default)

Rolls n 10 sided dice and uses the WoD rules to count successes and
explode dice. A success happens if a die scores 8 or higher. A die
explodes (is rolled again) if its result is equal to 10. A result list
is printed and the number of successes is shown.

- `sr`

Shadowrun (SR)

Rolls n 6 sided dice and uses SR4 rules to count successes and account
for glitches or critical glitches. A success happens if a die scores 5
or higher. A glitch happens if half (rounded up) of the dice score 1
and at least one success is scored. A critical glitch happens if half
(rounded up) of the dice score 1 and no successes are scored.

- `simple`

Rolls n 6 sided dice and adds the results.

#### Check default mode

You can check which mode is currently active by typing

  `!r status`

#### Arbitrary roll

An arbitrary roll can be made with the following syntax:

  `!r (number_of_dice)d(dice_type)+(roll_modifier)x(explode_value)?(success_condition)g(glitch_value)`

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
  * If the roll result is less or equal than the glitch_value the glitch counter
    increases by one (see the Shadowrun mode above).
  * x(explode_value), +(roll_modifier), ?(success_condition) and g(glitch_value)
    are optional entries.

#### Help

Get the link to this page by typing

  `!r help`
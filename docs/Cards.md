# Commands and Features

## HiLo

HiLo is a game in which two unique cards are randomly generated. You are then told the value of one of these cards, and must guess if the other value of the other card is either higher, or lower then the valuevof the first card.

If you are correct, you win and may either take your money, or go for double or nothing!

Values from least to greatest: `Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King`

Command:
> <prefix>game hilo bet_amount

Example:
> <prefix>game hilo 100

# Code Walkthrough

```Python
import random
```

Import [random](https://docs.python.org/3/library/random.html).

Used to generate random cards.

```Python
from discord.ext import commands
```

Import [`commands`](https://github.com/Rapptz/discord.py/tree/async/discord/ext/commands) from the `discord.ext` directory.

Used to create the bot with our description and command prefix.

```Python
playing_users = {}
```

The UserID-GameInstance key-value dictionary.

```Python
class Cards:
    def __init__(self, bot):
        self.bot = bot
```

Create the Cards cog class.

```Python
    @commands.group(pass_context=True)
    async def game(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.pm_help(ctx)
```

Create a group command with a name of `game`. If no subcommand is invoked, the user is PMed help.

```Python
    @game.command(pass_context=True)
    async def hilo(self, ctx):
        arguments = ctx.message.content.lower().split(" ")
```

Create a subcommand of the `game` command named `hilo`. This command will be used to manage a HiLo game.

Obtains all the arguments of the command the old-fashioned way, by splitting the message by spaces.

```Python
        if len(arguments) != 3:
            await self.bot.say("```Command: game hilo bet_amount\n"
                               "Example: game hilo 10```")
            return
```

Returns if there are not three arguments.

```Python
        if not arguments[2].isdecimal():
            await self.bot.say("```Bet amount needs to be a number.```")
            return
```

Returns if the second argument is not a integer.

```Python
        hilo_game_instance = HiLo_Game(ctx.message.author, arguments[2])
```

Create the HiLo game instance with the message author as the player, and the 2nd (read third) argument as the bet amount.

```Python
        await self.bot.say(hilo_game_instance.logic())
```

Perform the game logic and say the returned message from the logic. It is known that there is a responding message, so there is no checking for `None`

```Python
        playing_users[ctx.message.author.id] = hilo_game_instance
```

Add this game instance to the global `playing_users` dictionary.

*****

```Python
    async def receive_message(self, message):
        if (message.author.id == self.bot.user.id or
                message.author.id not in playing_users):
            return
```

Create a `on_message` listener to listen for game responces. Returns if the message author is the bot or if the message author is not a user playing a registered game.

```Python
        game = playing_users[message.author.id]
```

Gets the game being the user is a player in.

```Python
        if isinstance(game, HiLo_Game):
            response = game.logic(message)
            if response is not None:
                await self.bot.send_message(message.channel, response)
```

If the game the user is playing is a instance of `HiLo` game, perform logic and get any possible response.

If the responce from the game is not None, then have the bot speak the message.

*****

```Python
class Card:
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
```

Class to store representation of a Card.

```Python
    def __init__(self, value_rules, value, suit):
        self.value_rules = value_rules
        self.value = value
        self.suit = suit
```

The chosen method to store card representation is not straight-forward. `value_rules` is a Value(int)-Rank(str) key-value dictionary. `value` is the value of this card. `suit` is straight-forward, the suit of the card.

The string rank of the card is determined by the given value of the card.

```Python
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.rank == other.rank and
                self.suit == other.suit and
                self.value == other.value)
```

Allows cards to be compared with the `==` operator.

```Python
    @property
    def rank(self):
        return self.value_rules[self.value]
```

Return the string rank of the card.

```Python
    def __str__(self):
        if self.suit == "":
            return self.rank
        return "{} of {}".format(self.rank, self.suit)
```

String representation of cards. If there is no suit, rank alone is returnd - such as if the card is a Joker.

```Python
    def __repr__(self):
        return "Card({},{},{})".format(self.rank, self.suit, self.value)
```

Data representation of a card, including `rank`, `suit`, and `value`.

```Python
    @staticmethod
    def random(value_rules):
        return Card(value_rules, random.choice(list(value_rules.keys())),
                    random.choice(["Clubs", "Diamonds", "Hearts", "Spades"]))
```

A static method that can be used to generate a random card from the card value-ranks in the `value_rules` dictionary.

```Python
class HiLo_Game:
    value_rules = {
        1: "Ace",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "Jack",
        12: "Queen",
        13: "King"
    }
```

The HiLo game class. The value rules are as shown, with `Ace` having the lowest value and `King` having the highest.

```Python
    responses = {"start": [None],
                 "guess": ["higher", "lower"],
                 "choose": ["double", "pass"]}
```

A dictionary of valid responces for each state the game has. If a value of a stage is None, then there is no response for that stage.

```Python
    def __init__(self, user, bet_amount):
        self.user = user
        self.bet_amount = int(bet_amount)
        self.stage = "start"
        self.card_hidden = None
        self.card_visible = None
        self._new_cards()
```

Create a HiLo game. Requires the User and the amount bet.

Saves the user and bet amount.

Sets the stage to start, along with setting both `card_hidden` and `card_visible` to `None`.

Executes the private `_new_cards()` method, which assigns each card to a uniquely-valued card.

```Python
    def _new_cards(self):
        self.card_hidden = Card.random(self.value_rules)
        self.card_visible = Card.random(self.value_rules)
        while self.card_hidden.value == self.card_visible.value:
            self.card_hidden = Card.random(self.value_rules)
```

Makes sure both `card_hidden` and `card_visible` have a unique value.

```Python
    def logic(self, message=None):
        if message is not None:
            message.content = message.content.lower()
            if message.content not in self.responses[self.stage]:
                return
        else:
            if message not in self.responses[self.stage]:
                return
```

The logic function for the game.

Starts by normalizing the obtained message, and making sure said message is valid for the current state.

```Python
        if self.stage == "start":
            self.stage = "guess"
            return ("So, do you think the face-down card is `higher` or "
                    "`lower` then the **{}**?".format(self.card_visible))
```

The `start` stage if branch.

Only used when the game is first started. Sets the current stage to `guess` and return the message asking the player to either choose `higher` or `lower`.

```Python
        if self.stage == "guess":
            response = ""
            if ((message.content == "higher" and
                 self.card_hidden.value > self.card_visible.value) or
                    (message.content == "lower" and
                     self.card_hidden.value < self.card_visible.value)):
                response += ("You Won $**{}**!\nDo you wish to go for "
                             "`double` or nothing, or will you take your"
                             "winnings and `pass`?"
                             .format(self.bet_amount * 2))
                is_or_is_not = "is"
                self.stage = "choose"
            else:
                response += ("You Lost $**{}**!\nBetter luck next time!"
                             .format(self.bet_amount))
                is_or_is_not = "is not"
                del playing_users[message.author.id]
            response = ("The **{}** {} {} then the **{}**\n"
                        .format(self.card_hidden,
                                is_or_is_not,
                                message.content,
                                self.card_visible)) + response
            return response
```

The `guess` stage if branch.

First sees if the players guess was correct based on what their choice was. If the player was correct, then set the next stage to `choose` and set `is_or_is_not` to `is`. This is used to say if the visible card was `higher` or `lower` then the hidden card.

If the player was incorrect, then the response is how you lose, and the player is deleated from the global `playing_users` dictionary.

No matter if the player was correct or not, the player is told the rank of the hidden card.

```Python
        elif self.stage == "choose":
            if message.content == "double":
                self._new_cards()
                response = ("So, do you think the face-down card is "
                            "`higher` or `lower` then the **{}**?"
                            .format(self.card_visible))
                self.bet_amount *= 2
                self.stage = "guess"
            if message.content == "pass":
                response = ("Thanks for playing!\n$**{}** has been added to "
                            "your account!".format(self.bet_amount * 2))
                del playing_users[message.author.id]
            return response
```

The `choose` stage if branch.

If the choice is double, then generates new cards, set the stage to `guess`, and increase the `bet_amount`.

If the choice is `pass`, then the game is deleted.

```Python
def generate_deck(value_rules, jokers=0, joker_value=0):
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    deck = [Card(value_rules, value, suit)
            for value in value_rules for suit in suits]
    deck.extend([Card({joker_value: "Joker"}, joker_value, "")
                 for _ in range(jokers)])
    return deck
```

The `generate_deck` method, used to generate a deck of cards.

Creates a card of every value in the passed `value_rules`.

Then adds a `Joker` for every `joker`.

Lastly returns the `deck`.

```Python
def setup(bot):
    cards = Cards(bot)
    bot.add_listener(cards.on_receive_message, "on_message")
    bot.add_cog(cards)
```

Add the `on_receive_message` listener and the cog to the bot.
"""Cards cog.

Will contain many card playable card games.

"""
from discord.ext import commands
import random

playing_users = {}


def generate_deck(jokers=False, value_rules="default"):
    """Create a new 52-54 Card Deck.

    Keyword Arguments:
    jokers -- If two Jokers should be added to the Deck. (default False)
    value_rules -- Rank-Value Dictionary for each Card generated. (default: incremental) (example {"Ace": 14})

    Returns:
    list -- List of Cards, each being unique asside from possible Jokers.
    """
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    deck = [Card(rank, suit, value_rules) for rank in ranks for suit in suits]
    if jokers:
        deck.extend([Card("Joker", None) for _ in range(2)])
    return deck


class Card:
    """A playing Card."""

    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, rank, suit, value_rules="default"):
        """Create a new Card with the supplied rank and suit.

        Keyword Arguments:
        rank -- Rank of the Card [Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King]
        suit -- Suite of the Card [Clubs, Diamonds, Hearts, Spades]
        value_rules -- Rank-Value Dictionary (default: incremental) (example {"Ace": 14})

        """
        if rank == "random":
            self.rank = random.choice(self.ranks)
        else:
            self.rank = rank

        if suit == "random":
            self.suit = random.choice(self.suits)
        else:
            self.suit = suit

        if value_rules != "default" and self.rank in value_rules:
            self.value = value_rules[self.rank]
        else:
            self.value = self.ranks.index(self.rank) + 1

    def __gt__(self, other):
        """Return true if this card is greater than supplied other card.

        Allows Card to be compated to other with the > comparison operator.

        Keyword Arguments:
        other -- Card to compare to.

        Returns:
        bool -- True this Card is greater then the other card, False otherwise.

        """
        return self.value > other.value

    def __lt__(self, other):
        """Return true if this card is less than supplied other card.

        Allows Card to be compated to other with the < comparison operator.

        Keyword Arguments:
        other -- Card to compare to.

        Returns:
        bool -- True this Card is less then 'other' card, False otherwise.

        """
        return self.value < other.value

    def __eq__(self, other):
        """Allow Card to be compared to other Card with the == operator.

        Keyword Arguments:
        other -- Card to see if this card is equal to.

        Returns:
        bool -- True if this Card and 'other' Card are equal, False otherwise.

        """
        return self.__class__ == other.__class__ and self.rank == other.rank and self.suit == other.suit and self.value == other.value

    def __str__(self):
        """Return string representation of Card."""
        if self.suit is None:
            return self.rank
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        """Return data representation of Card."""
        return "Card({},{},{})".format(self.rank, self.suit, self.value)


class HiLo_Game:
    """HiLo Game instance."""

    def __init__(self, user, bet_amount):
        """Create a new HiLo game with the supplied player.

        Keyword Arguments:
        user -- User to play HiLo.
        bet_amount -- Amount of money bet.

        """
        self.user = user
        self.bet_amount = int(bet_amount)
        self.card_hidden = Card("random", "random")
        self.card_visiable = Card("random", "random")
        while self.card_hidden == self.card_visiable:
            self.card_hidden = Card("random", "random")

    def guess(self, guess):
        """Guess weather the hidden card is higher or lower than the hidden card.

        Returns:
        bool -- True if the user was correct, False otherwise.

        """
        if guess.lower() == "higher"and self.card_hidden.value > self.card_visiable.value:
            return True
        elif guess.lower() == "lower" and self.card_hidden.value < self.card_visiable.value:
            return True
        else:
            return False


class Cards:
    """Card cog."""

    def __init__(self, bot):
        """Initalization function."""
        self.bot = bot

    @commands.command(pass_context=True)
    async def game(self, ctx):
        """Base command for playing card games.

        Keyword arguments:
        ctx -- Command context.

        """
        arguments = ctx.message.content.split(" ")
        game_name = arguments[1]
        if game_name.lower() == "hilo":
            if len(arguments) != 3:
                await self.bot.say("Correct command: 'game hilo bet_amount'\nExample: 'game hilo 10'")
                return
            if not arguments[2].isdecimal():
                await self.bot.say("Bet amount needs to be a number.")
                return
            if False:  # TODO: Replace with not enough money economy check.
                await self.bot.say("You don't have ${}!".format(arguments[2]))
                return
            hilo_game_instance = HiLo_Game(ctx.message.author, arguments[2])
            await self.bot.say("So, do you think the face-down card is *higher* or *lower* then the **{}**?".format(hilo_game_instance.card_visiable))
            playing_users[ctx.message.author.id] = hilo_game_instance
#                   FIX: Above error messages are only placeholders at the moment.

    async def receive_message(self, message):
        """Called whenever any player sends a message."""
        if message.author.id == self.bot.user.id or message.author.id not in playing_users:
            return
        game = playing_users[message.author.id]
        if isinstance(game, HiLo_Game):
            if message.content.lower() != "higher" and message.content.lower() != "lower":
                return
            win = game.guess(message.content.lower())
            responce_message = "The **{}** {}{} then the **{}**".format(game.card_hidden, "is " if win else "is not ", message.content, game.card_visiable)
            # The card_hidden (is/is not) (higher/lower) then the card_visiable.
            if win:
                responce_message += "\nYou won **${}**!".format(game.bet_amount * 2)
            else:
                responce_message += "\nYou lost **${}**, Better luck next time!".format(game.bet_amount)
            await self.bot.send_message(message.channel, responce_message)
            del playing_users[message.author.id]


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    cards = Cards(bot)
    bot.add_listener(cards.receive_message, "on_message")
    bot.add_cog(cards)

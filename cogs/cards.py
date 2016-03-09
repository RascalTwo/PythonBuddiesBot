"""Cards cog.

Will contain many card playable card games.

"""
from discord.ext import commands
import random

hilo_games = []


class Deck:
    """Contains 52 unique Cards."""

    def __init__(self):
        """Create, populate, and shuffle a new Deck of Cards."""
        self.deck = self.generate_deck()
        random.shuffle(self.deck)

    def draw_cards(self, amount):
        """Remove card(s) from Deck.

        Keyword arguments:
        amount -- Number of Cards to remove and return from Deck.

        Returns:
        list -- Cards removed from Deck.

        """
        cards = []
        for _ in range(amount):
            cards.append(self.deck.pop())
        return cards

    def get_deck(self):
        """Get the current Deck of Cards.

        Returns:
        list -- Cards within the Deck.

        """
        return self.deck

    @staticmethod
    def generate_deck():
        """Create a new Deck."""
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Joker", "Queen", "King"]
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        return [Card(rank, suit) for rank in ranks for suit in suits]


class Card:
    """A playing Card.

    Supports the following operators: ==, +, -, <, >.

    """

    def __init__(self, rank="random", suit="random"):
        """Create a new Card with the supplied rank and suit.

        Keyword Arguments:
        rank -- Rank of the Card [Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Joker, Queen, King] (default random)
        suit -- Suite of the Card [Clubs, Diamonds, Hearts, Spades] (default random)

        """
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Joker", "Queen", "King"]
        if rank == "random":
            self.rank = random.choice(ranks)
        else:
            self.rank = rank

        if suit == "random":
            self.suit = random.choice(["Clubs", "Diamonds", "Hearts", "Spades"])
        else:
            self.suit = suit
        self.value = ranks.index(self.rank) + 1

    def get_rank(self):
        """Return rank of Card."""
        return self.rank

    def get_suit(self):
        """Return suit of Card."""
        return self.suit

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

    def __add__(self, other):
        """Allow Card to be added to another card with the + operator.

        Keyword Arguments:
        other -- Card to add to this card.

        Returns:
        int -- Result of adding the two card values.

        """
        return self.value + other.value

    def __sub__(self, other):
        """Allow Card to be subtracted from another card with the - operator.

        Keyword Arguments:
        other -- Card to subtract from this card.

        Returns:
        int -- Result of subtracting the two card values, may be negative.

        """
        return self.value - other.value

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
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        """Return data representation of Card."""
        return "Card({},{})".format(self.rank, self.suit)


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
        self.card_hidden = Card()
        self.card_visable = Card()
        while (self.card_hidden == self.card_visable):
            self.card_hidden = Card()

    def guess(self, guess):
        """Guess weather the hidden card is higher or lower than the hidden card.

        Returns:
        bool -- True if the user was correct, False otherwise.

        """
        if guess == "higher"and self.card_hidden > self.card_visable:
            return True
        elif guess == "lower" and self.card_hidden < self.card_visable:
            return True
        else:
            return False

    def get_hidden_card(self):
        """Return the hidden (face-down) card."""
        return self.card_hidden

    def get_visable_card(self):
        """Return the visable (face-up) card."""
        return self.card_visable

    def get_user(self):
        """Return the user playing."""
        return self.user

    def get_bet_amount(self):
        """Return the amount bet."""
        return self.bet_amount


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
            if len(arguments) == 3:
                if arguments[2].isdecimal():
                    if True:  # TODO: Replace with economy check.
                        hilo_game_instance = HiLo_Game(ctx.message.author, arguments[2])
                        await self.bot.say("So, do you think the face-down card is *higher* or *lower* then the **{}**?".format(hilo_game_instance.get_visable_card()))
                        hilo_games.append(hilo_game_instance)
                    else:
                        await self.bot.say("You don't have ${}!".format(arguments[2]))
                else:
                    await self.bot.say("Bet amount needs to be a number.")
            else:
                await self.bot.say("Correct command: 'game hilo bet_amount'\nExample: 'game hilo 10'")
#                   FIX: Above error messages are only placeholders at the moment.

    async def receive_message(self, message):
        """Called whenever any player sends a message."""
        if message.author.id == self.bot.user.id:
            return
        hilo_game_instance = [hilo_game for hilo_game in hilo_games if hilo_game.get_user() == message.author]
        if hilo_game_instance != []:
            hilo_game_instance = hilo_game_instance[0]
            if message.content.lower() == "higher" or message.content.lower() == "lower":
                win = hilo_game_instance.guess(message.content)
                responce_message = "The **{}** {}{} then the **{}**".format(hilo_game_instance.get_hidden_card(), "is " if win else "is not ", message.content, hilo_game_instance.get_visable_card())
                # The hidden_card (is/is not) (higher/lower) then the visable_card
                if win:
                    responce_message += "\nYou won **${}**!".format(hilo_game_instance.get_bet_amount() * 2)
                else:
                    responce_message += "\nYou lost **${}**, Better luck next time!".format(hilo_game_instance.get_bet_amount())
                await self.bot.send_message(message.channel, responce_message)
                hilo_games.pop(hilo_games.index(hilo_game_instance))


def setup(bot):
    """Called when cog is loaded via load_extension()."""
    cards = Cards(bot)
    bot.add_listener(cards.receive_message, "on_message")
    bot.add_cog(cards)

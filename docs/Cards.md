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

## Card

Card storing class.

## HiLo_Game

The HiLo game class.

## Cards

The actual cog class.

## Generate Deck

Method to generate an entire deck of unique cards, with or without jokers.


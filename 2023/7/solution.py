import os
import pdb
import re
from dataclasses import dataclass, field
from enum import Enum

FILE = os.path.join(os.path.dirname(__file__), "input.txt")


class Card:
    label: str
    value: int

    def __init__(self, label: str, value: int):
        self.label = label
        self.value = value

    def __lt__(self, other: "Card"):
        return self.value < other.value

    def __eq__(self, other: "Card"):
        return self.label == other.label

    def __repr__(self):
        return f"<Card {self.label}>"


CARD_TYPES = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_TYPES.reverse()
CARDS_MAP = {label: Card(label, value) for value, label in enumerate(CARD_TYPES)}


class WildCard(Card):
    def __init__(self):
        self.label = "W"
        self.value = -1


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    @classmethod
    def type_for_cards(cls, cards: list[Card]) -> "HandType":
        counts = {}
        for card in cards:
            counts[card.label] = counts.get(card.label, 0) + 1
        if "W" not in counts:
            unique_cards = len(counts)
            if unique_cards == 1:
                return cls.FIVE_OF_A_KIND
            elif unique_cards == 2:
                return cls.FOUR_OF_A_KIND if 4 in counts.values() else cls.FULL_HOUSE
            elif unique_cards == 3:
                return cls.THREE_OF_A_KIND if 3 in counts.values() else cls.TWO_PAIR
            elif unique_cards == 4:
                return cls.ONE_PAIR

            return cls.HIGH_CARD

        wild_count = counts.pop("W")
        if wild_count == 5:
            return cls.FIVE_OF_A_KIND

        unique_cards = len(counts)
        if unique_cards == 1:
            return cls.FIVE_OF_A_KIND
        elif unique_cards == 2:
            if 1 in counts.values():
                return cls.FOUR_OF_A_KIND
            return cls.FULL_HOUSE
        elif unique_cards == 3:
            return cls.THREE_OF_A_KIND
        elif unique_cards == 4:
            return cls.ONE_PAIR

        raise Exception(f"Should not get here -> {cards}")


@dataclass
class Hand:
    cards: list[Card]
    bid: int
    type: HandType

    @classmethod
    def create(cls, line: str, jacks_are_wild=False):
        cards_line, bid = line.split(" ")
        cards = []
        for card_label in cards_line:
            if card_label == "J" and jacks_are_wild:
                cards.append(WildCard())
            else:
                cards.append(CARDS_MAP[card_label])
        return cls(cards=cards, bid=int(bid), type=HandType.type_for_cards(cards))

    def __lt__(self, other: "Hand"):
        if self.type.value != other.type.value:
            return self.type.value < other.type.value

        for self_card, other_card in zip(self.cards, other.cards):
            if self_card == other_card:
                continue
            return self_card < other_card


def do_solution(lines: list[str]):
    result = 0
    for idx, hand in enumerate(sorted(Hand.create(line) for line in lines)):
        rank = idx + 1
        result += rank * hand.bid

    return result


def do_solution_2(lines: list[str]):
    result = 0
    for idx, hand in enumerate(sorted(Hand.create(line, jacks_are_wild=True) for line in lines)):
        rank = idx + 1
        result += rank * hand.bid

    return result


if __name__ == "__main__":
    with open(FILE, "r") as file:
        lines = list(file.readlines())

        total = do_solution(lines)
        print("TOTAL: ", total)

        total2 = do_solution_2(lines)
        print("TOTAL2: ", total2)

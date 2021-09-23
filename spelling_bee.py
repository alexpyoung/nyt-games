#!/usr/bin/env python3

from argparse import Action, ArgumentParser
from urllib.request import urlopen

MINIMUM_CHARACTER_COUNT = 4
HIVE_CHARACTER_COUNT = 6


class ValidateCenter(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) > 1:
            raise ValueError("'center' must only be 1 character")
        setattr(namespace, self.dest, values)

class ValidateHive(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) != HIVE_CHARACTER_COUNT:
            raise ValueError(f"Expected {HIVE_CHARACTER_COUNT} hive characters")
        setattr(namespace, self.dest, values)

def main(required, optional):
    source = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'
    with urlopen(source) as content:
        words = map(lambda w: w.decode('utf-8'), set(content.read().split()))
        candidates = filter(lambda w: validate(w, required, optional), words)
        for word in sorted(candidates, key=lambda w: sort_value(w, list(optional) + [required])):
            print(word)

def validate(word, required_letter, optional_letters):
    if required_letter not in word:
        return False
    inclusions = list(optional_letters) + [required_letter]
    for letter in list(word):
        if letter not in inclusions:
            return False
    return len(word) >= MINIMUM_CHARACTER_COUNT

def sort_value(word, letters):
    for letter in letters:
        if letter not in word:
            return len(word)
    return 50 # Longer than any dictionary word

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('center', action=ValidateCenter, help='Required character')
    arg_parser.add_argument('hive', action=ValidateHive, help='Remaining characters')
    args = arg_parser.parse_args()
    main(args.center, args.hive)

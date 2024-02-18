import os
import re
from collections import Counter

class SpellCheckMate:
    def __init__(self):
        file_path = os.path.join(os.path.dirname(__file__), 'big.txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        self.word_dictionary = dict(Counter(self.__words(text)))
    
    def correct(self, word):
        candidates_set = self.__candidates(word)
        probabilities = [self.__word_probability(candidate, sum(self.word_dictionary.values())) for candidate in candidates_set]
        candidates_list = list(candidates_set)
        return candidates_list[probabilities.index(max(probabilities))]

    def alternatives(self, word):
        candidates_set = self.__candidates(word)
        return list(candidates_set)

    def print_alternatives(self, word):
        alternatives = self.alternatives(word)
        for w in alternatives:
            print(w)

    def check(self, text):
        letters_and_space = 'abcdefghijklmnopqrstuvwxyz '
        lowercase_text = text.lower()
        for sentence in lowercase_text.split('.'):
            clean_sentence = ''.join(filter(letters_and_space.__contains__, sentence))
            self.__check_sentence(clean_sentence)

    def __check_sentence(self, sentence):
        corrected_sentence = ""
        corrected_word = ""
        wrong_word_position = 0

        words = sentence.split()
        for word in words:
            corrected_word = self.correct(word.lower())
            if corrected_word != word:
                wrong_word_position = self.__find_word_position(word, sentence)
                print(sentence)
                self.__print_spaces_and_position_at(wrong_word_position)
                self.print_alternatives(word)
                corrected_word = input("> ")
                corrected_sentence += corrected_word + " "
            else:
                corrected_sentence += word + " "

        print(sentence)
        print(corrected_sentence)

    def __print_spaces_and_position_at(self, n):
        print(" " * n + "^")

    def __find_word_position(self, word_to_find, sentence):
        position = sentence.find(word_to_find)
        return position

    def __words(self, text):
        return re.findall(r'\w+', text.lower())

    def __word_probability(self, word, N):
        if word in self.word_dictionary:
            return self.word_dictionary[word] / N if N else 0
        else:
            return 0

    def __candidates(self, word):
        known_words_set = self.__known({word})
        if known_words_set:
            return known_words_set

        one_edit_away_set = self.__known(self.__one_edit_away(word))
        if one_edit_away_set:
            return one_edit_away_set

        two_edits_away_set = self.__known(self.__two_edits_away(word))
        if two_edits_away_set:
            return two_edits_away_set

        return {'404'}

    def __known(self, words):
        return {w for w in words if w in self.word_dictionary}

    def __one_edit_away(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]

        return set(deletes + transposes + replaces + inserts)

    def __two_edits_away(self, word):
        return {e2 for e1 in self.__one_edit_away(word) for e2 in self.__one_edit_away(e1)}

# Import necessary modules
import re
from collections import Counter

# Define Cython types for optimization
ctypedef list WordsList
ctypedef set WordsSet
ctypedef tuple SplitsTuple

# Define the SpellCheckMate class
cdef class SpellCheckMate:
    cdef dict word_dictionary

    # Constructor to initialize the WORDS Counter
    def __cinit__(self):
        with open('big.txt') as f:
            text = f.read()
        self.word_dictionary = dict(Counter(self.__words(text)))

    # Function to get the most probable spelling correction for a word
    cpdef str correct(self, str word):
        # Generate candidates
        cdef WordsSet candidates_set = self.__candidates(word)

        # Calculate probability values for each candidate
        cdef list probabilities = [self.__word_probability(candidate, sum(self.word_dictionary.values())) for candidate in candidates_set]

        # Return the candidate with the maximum probability
        candidates_list = list(candidates_set)
        return candidates_list[probabilities.index(max(probabilities))]

    cpdef WordsList alternatives(self, str word):
        cdef WordsSet candidates_set = self.__candidates(word)
        return list(candidates_set)

    cpdef print_alternatives(self, str word):
        cdef WordsList alternatives = self.alternatives(word)
        for word in alternatives:
            print(word)

    cpdef check(self, str text):
        letters_and_space = 'abcdefghijklmnopqrstuvwxyz '
        lowercase_text = text.lower()
        for sentence in lowercase_text.split('.'):
            clean_sentence = ''.join(filter(letters_and_space.__contains__, sentence))
            self.__check_sentence(clean_sentence)

    cpdef __check_sentence(self, str sentence):
        words = sentence.split()
        cdef str corrected_sentence = ""
        for word in words:
            # print("word is:" + word)
            corrected_word = self.correct(word.lower())
            if (corrected_word != word):
                # print("corrected word is:" + corrected_word)                
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

    cpdef __print_spaces_and_position_at(self, int n):
        # print("number of spaces to print: " + str(n))
        print(" " * n + "^")

    cpdef int __find_word_position(self, str word_to_find, str sentence):
        position = sentence.find(word_to_find)
        return position

    cpdef WordsList __words(self, str text):
        return re.findall(r'\w+', text.lower())

    cpdef float __word_probability(self, str word, int N):
        if word in self.word_dictionary.keys():
            return self.word_dictionary[word] / N if N else 0
        else:
            return 0

    # Function to generate possible spelling corrections for a word
    cpdef WordsSet __candidates(self, str word):
        cdef WordsSet known_words_set = self.__known({word})
        if known_words_set:
            return known_words_set

        cdef WordsSet one_edit_away_set = self.__known(self.__one_edit_away(word))
        if one_edit_away_set:
            return one_edit_away_set

        cdef WordsSet two_edits_away_set = self.__known(self.__two_edits_away(word))
        if two_edits_away_set:
            return two_edits_away_set

        # If none of the above conditions are met, return 404
        return { '404' }

    cpdef WordsSet __known(self, WordsSet words):
        return {w for w in words if w in self.word_dictionary}

    cpdef WordsSet __one_edit_away(self, str word):
        cdef int i
        cdef str L, R, c
        cdef list splits, deletes, transposes, replaces, inserts

        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]

        return set(deletes + transposes + replaces + inserts)

    cpdef WordsSet __two_edits_away(self, str word):
        return {e2 for e1 in self.__one_edit_away(word) for e2 in self.__one_edit_away(e1)}
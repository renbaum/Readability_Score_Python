# Write your code here
# put your python code here
# from nltk import TreebankWordTokenizer as TWT
import re
import string
import sys
from math import ceil

from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

readability = {1: ["5-6", "Kindergarten"],
             2: ["6-7", "First Grade"],
             3: ["7-8", "Second Grade"],
             4: ["8-9", "Third Grade"],
             5: ["9-10", "Fourth Grade"],
             6: ["10-11", "Fifth Grade"],
             7: ["11-12", "Sixth Grade"],
             8: ["12-13", "Seventh Grade"],
             9: ["13-14", "Eighth Grade"],
             10: ["14-15", "Ninth Grade"],
             11: ["15-16", "Tenth Grade"],
             12: ["16-17", "Eleventh Grade"],
             13: ["17-18", "Twelfth Grade"],
             14: ["18-22", "College student"]}


class TextAnalyzer:
    def __init__(self, text, longmanfile):
        self.text = text
        self.sentences = sent_tokenize(text)
        self.longman = self.get_longmanfile(longmanfile)

    def get_longmanfile(self, longmanfile):
        with open(longmanfile, "r") as file:
            longman = file.read()
        return longman.split("\n")

    def count_words(self):
        return self.count_words_in_text(self.text)

    def count_words_in_text(self, text):
        filtered_lst = self.get_filtered_word_list(text)
        return len(filtered_lst)

    def get_word_list(self, text):
        return word_tokenize(text)

    def get_filtered_word_list(self, text):
        lst = word_tokenize(text)
        filtered_lst = [word for word in lst if word not in string.punctuation]
        return filtered_lst

    def count_characters(self):
        lst1 = self.get_word_list(self.text)
        sum = 0
        for i in lst1:
            sum += len(i)
        return sum


    def count_size(self):
        return len(self.text)

    def count_sentences(self):
        return len(self.sentences)

    def average_words(self):
        words_words_per_sentence = [word_tokenize(sentence) for sentence in self.sentences]
        filtered_words_per_sentence = [[word for word in sentence if word not in string.punctuation] for sentence in words_words_per_sentence]
        num_words_per_sentence = [len(sentence) for sentence in filtered_words_per_sentence]
        return sum(num_words_per_sentence) / len(num_words_per_sentence)

    def is_it_easy(self):
        return self.average_words() <= 10

    def count_syllables_in_word(self, word):
        syllables = 0
        l = re.findall(r"[AEIOUYaeiouy]+", word)
        for i in l:
            if len(i) <=2: syllables += 1
            elif len(i) == 3: syllables += 2

        if re.search(r"[AEIOUYaeiouy]$", word): syllables -= 1
        if syllables == 0: syllables = 1

        return syllables

    def count_syllables(self):
        list = self.get_filtered_word_list(self.text)
        syllables = 0
        for word in list:
            syllables += self.count_syllables_in_word(word)

        return syllables

    def extract_age(self, text):
        l = re.findall(r"\d{1,2}", text)
        for i in l:
            yield int(i)

    def get_average_age(self, list_age):
        count = 0
        total_age = 0
        for i in list_age:
            for age in self.extract_age(i):
                total_age += age
                count += 1

        return total_age / count

    def get_dificult_words(self):
        list = self.get_filtered_word_list(self.text)
        dificult_words = [diffword for diffword in list if diffword not in self.longman]
        return len(dificult_words)


    def calculate_score(self):
        word_count = self.count_words()
        sentence_count = self.count_sentences()
        characters = self.count_characters()
        dificult_words = self.get_dificult_words()
        syllables = self.count_syllables()

        score = 4.71 * characters / word_count + 0.5 * word_count / sentence_count - 21.43
        score = ceil(score)
        fk = 0.39 * word_count / sentence_count + 11.8 * syllables / word_count - 15.59
        fk = ceil(fk)
        dale = 0.1579 * (dificult_words / word_count) * 100 + 0.0496 * (word_count / sentence_count)
        if (dificult_words / word_count) * 100 >= 5: dale += 3.6365
        dale = ceil(dale)

        age_score = readability[score][0]
        age_fk = readability[fk][0]
        age_dale = readability[dale][0]

        print(f"Characters: {characters}")
        print(f"Sentences: {sentence_count}")
        print(f"Words: {word_count}")
        print(f"Difficult words: {dificult_words}")
        print(f"Syllables: {syllables}")
        print()
        print(f"Automated Readability Index: {score} (about {age_score} year olds).")
        print(f"Flesch-Kincaid Readability Test: {fk} (about {age_fk} year olds).")
        print(f"Dale-Chall Readability Index: {dale}. The text can be understood by {age_dale} year olds.")
        print(f"This text should be understood in average by {self.get_average_age([age_score, age_fk, age_dale]):.1f} year olds.")



if __name__ == "__main__":
    text = ""


    if len(sys.argv) == 3:
        filename = sys.argv[1]
        longmanfile = sys.argv[2]
        with open(filename, "r") as file:
            text = file.read()
            print(f"Text: {text}")
    else:
        text = input()
        longmanfile = "word.txt"

    result = "HARD"
    analyzer = TextAnalyzer(text, longmanfile)
    analyzer.calculate_score()


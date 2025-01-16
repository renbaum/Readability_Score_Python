# Write your code here
# put your python code here
# from nltk import TreebankWordTokenizer as TWT
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
    def __init__(self, text):
        self.text = text
        self.sentences = sent_tokenize(text)

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

    def calculate_score(self):
        word_count = self.count_words()
        sentence_count = self.count_sentences()
        characters = self.count_characters()

        score = 4.71 * characters / word_count + 0.5 * word_count / sentence_count - 21.43
        score = ceil(score)
        print(f"Characters: {characters}")
        print(f"Sentences: {sentence_count}")
        print(f"Words: {word_count}")
        print(f"Automated Readability Index: {score} (this text should be understood by {readability[score][0]} year olds).")


        return self.average_words()


if __name__ == "__main__":
    text = ""

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        with open(filename, "r") as file:
            text = file.read()
            print(f"Text: {text}")
    else:
        text = input()

    result = "HARD"
    analyzer = TextAnalyzer(text)
    analyzer.calculate_score()


# Write your code here
# put your python code here
# from nltk import TreebankWordTokenizer as TWT
from nltk.tokenize import sent_tokenize

text = input()

x = TWT()

#nltk.download('punkt_tab')
lst = sent_tokenize(text)
#lst = x.tokenize(text, True)
# print(f"Sentences: {len(lst)}, Characters: {len(text)}")
result = "EASY"
if len(lst) > 3:
    result = "HARD"
elif len(text) > 100:
    result = "HARD"

print(f"Difficulty: {result}")
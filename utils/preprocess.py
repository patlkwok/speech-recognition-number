import re

def split_sentence(article):
    # Split the article into words, group by sentences
    words_by_sentences = []
    sentences = re.split("[,;.!?:]+", article)
    for s in sentences:
        words = re.split("[ \-\'\"]+", s)
        words_by_sentences.append(words)
    return words_by_sentences

def get_number_words(article):
    number_words = []
    words_by_sentences = split_sentence(article.lower())
    number_basic = {"zero", "one", "two", "three", "four",\
                    "five", "six", "seven", "eight", "nine"}
    number_teens = {"ten", "eleven", "twelve", "thirteen", "fourteen", \
                    "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"}
    number_tens = {"ten", "twenty", "thirty", "forty", "fifty", \
                   "sixty", "seventy", "eighty", "ninty"}
    number_units = {"hundred", "thousand", "million", "billion", "trillion"}
    number_ordinal = {"zeroth", "first", "second", "third", "fourth", \
                       "fifth", "sixth", "seventh", "eighth", "ninth", \
                       "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", \
                       "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth", \
                       "twentieth", "thirtieth", "fortieth", "fiftieth", \
                       "sixtieth", "seventieth", "eightieth", "nintieth", \
                       "hundredth", "thousandth", "millionth", "billionth", "trillionth"}
    for s in words_by_sentences:
        number = ""
        for w in s:
            if w in number_basic or w in number_teens or w in number_tens or w in number_units:
                number = number + w + " "
            else:
                if len(number) > 0:
                    number_words.append(number[:-1])
                number = ""
        if len(number) > 0:
            number_words.append(number[:-1])
    return number_words
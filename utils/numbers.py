ordinals = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", \
            6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth", \
            11: "eleventh", 12: "twelfth", 13: "thirteenth", 14: "fourteenth", \
            15: "fifteenth", 16: "sixteenth", 17: "seventeenth", 18: "eighteenth", \
            19: "nineteenth", 20: "twentieth", 21: "twenty first", \
            22: "twenty second", 23: "twenty third", 24: "twenty fourth", \
            25: "twenty fifth", 26: "twenty sixth", 27: "twenty sevent", \
            28: "twenty eighth", 29: "twenty ninth", 30: "thirtieth", \
            31: "thirty first"}

digits = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", \
          5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

digits_alt = {0: "oh", 1: "one", 2: "two", 3: "three", 4: "four", \
              5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

teens = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", \
         15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"}

tens = {10: "ten", 20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", \
        60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}

def read_as_ordinals(num):
    num = int(num)
    if num <= 0 or num >= 32:
        return {"NA": 1.0}
    return {ordinals[num]: 1.0}

def read_by_digit(num):
    method1 = ""
    method2 = ""
    for d in num:
        if d.isdigit():
            method1 = method1 + digits[int(d)] + " "
            method2 = method2 + digits_alt[int(d)] + " "
        else:
            method1 = method1 + d + " "
            method2 = method2 + d + " "
    method1 = method1[:-1]
    method2 = method2[:-1]
    if method1 == method2:
        return {method1: 1.0}
    return {method1: 0.5, method2: 0.5}

def read_2d(num):
    num = int(num)
    if num == 0:
        return ""
    if num <= 9:
        return digits[num]
    if num <= 19:
        return teens[num]
    if num % 10 == 0:
        return tens[10*(num//10)]
    return tens[10*(num//10)] + " " + digits[num%10]

def read_2d_year(num):
    num = int(num)
    if num == 0:
        return "hundred"
    if num <= 9:
        return "oh " + digits[num]
    if num <= 19:
        return teens[num]
    if num % 10 == 0:
        return tens[10*(num//10)]
    return tens[10*(num//10)] + " " + digits[num%10]

def read_year(num):
    if int(num) >= 10000 or int(num) <= 0:
        return {"NA": 1.0}
    millenium = num[:-3]
    century = num[:-2]
    year = num[-2:]
    if century == "":
        return {read_2d(year): 1.0}
    if millenium != "" and century[-1] == "0":
        if year == "00":
            method1 = digits[int(millenium)] + " thousand"
            method2 = read_2d(century) + " " + read_2d_year(year)
            return {method1: 0.9, method2: 0.1}
        else:
            method1 = digits[int(millenium)] + " thousand " + read_2d(year)
            method2 = digits[int(millenium)] + " thousand and " + read_2d(year)
            method3 = read_2d(century) + " " + read_2d_year(year)
            return {method1: 0.5, method2: 0.3, method3: 0.2}
    method = read_2d(century) + " " + read_2d_year(year)
    return {method: 1.0}
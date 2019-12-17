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

multiples = {100: "hundred", 1000: "thousand", 10 ** 6: "million", \
             10 ** 9: "billion", 10 ** 12: "trillion"}

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

def int2words_3d(n):
    if n == 0:
        return []
    res_arr = []
    hundreds = n // 100
    rem = n % 100
    if hundreds >= 1:
        res_arr = res_arr + [digits[hundreds], "hundred"]
    ts = (rem // 10) * 10
    ones = rem % 10
    if rem == 0:
        return res_arr
    if rem <= 9:
        res_arr = res_arr + [digits[rem]]
        return res_arr
    if rem <= 19:
        res_arr = res_arr + [teens[rem]]
        return res_arr
    if ones == 0:
        res_arr = res_arr + [tens[ts]]
        return res_arr
    res_arr = res_arr + [tens[ts], digits[ones]]
    return res_arr

def int2words(num):
    n = int(num)
    if n == 0:
        return "zero"
    part_tn = n // (10 ** 12)
    rem_tn = n % (10 ** 12)
    part_bn = rem_tn // (10 ** 9)
    rem_bn = rem_tn % (10 ** 9)
    part_mn = rem_bn // (10 ** 6)
    rem_mn = rem_bn % (10 ** 6)
    part_ts = rem_mn // 1000
    rem_ts = rem_mn % 1000
    res_arr = []
    if part_tn >= 1:
        res_arr = res_arr + int2words_3d(part_tn) + ["trillion"]
    if part_bn >= 1:
        res_arr = res_arr + int2words_3d(part_bn) + ["billion"]
    if part_mn >= 1:
        res_arr = res_arr + int2words_3d(part_mn) + ["million"]
    if part_ts >= 1:
        res_arr = res_arr + int2words_3d(part_ts) + ["thousand"]
    res_arr = res_arr + int2words_3d(rem_ts)
    return res_arr

def read_by_dig(num):
    res_arr = []
    for d in num:
        if d.isdigit():
            res_arr = res_arr + [digits[int(d)]]
        else:
            res_arr = res_arr + [d]
    return res_arr

def float2words(num):
    res_arr = []
    if num[0] == "-":
        res_arr = res_arr + ["minus"]
        num = num[1:]
    num_parts = num.split(".")
    if len(num_parts) == 1:
        int_part = num_parts[0]
    else:
        int_part, frac_part = num_parts[0], num_parts[1]
    int_part = "".join(int_part.split(","))
    res_arr = res_arr + int2words(int_part)
    if len(num_parts) >= 2:
        res_arr = res_arr + ["point"] + read_by_dig(frac_part)
    return res_arr

def num2words(num):
    res_arr = []
    num_parts = num.split("/")
    if len(num_parts) == 1:
        numer = num_parts[0]
    else:
        numer, denom = num_parts[0], num_parts[1]
    res_arr = res_arr + float2words(numer)
    if len(num_parts) >= 2:
        res_arr = res_arr + ["over"] + float2words(denom)
    return " ".join(res_arr)
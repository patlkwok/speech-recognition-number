import copy

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

ordinals = {"one": "first", "two": "second", "three": "third", "five": "fifth", \
            "eight": "eighth", "nine": "ninth", "twelve": "twelfth", "twenty": "twentieth", \
            "thirty": "thirtieth", "forty": "fortieth", "fifty": "fiftieth", \
            "sixty": "sixtieth", "seventy": "seventieth", "eighty": "eightieth", \
            "ninety": "ninetieth"}

def read_by_digit(num):
    # Read a number digit by digit
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
    # Read an integer with at most 2 digits
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
    # Helper for reading years
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
    # Read a year number (can have at most 2 letters at beginning or end)
    bl = ""
    el = ""
    if num[0].isalpha() and not num[1].isalpha():
        bl = num[0] + " "
        num = num[1:]
    elif num[0].isalpha() and num[1].isalpha() and not num[2].isalpha():
        bl = num[0] + " " + num[1] + " "
        num = num[2:]
    if num[-1].isalpha() and not num[-2].isalpha():
        el = " " + num[-1]
        num = num[:-1]
    elif num[-1].isalpha() and num[-2].isalpha() and not num[-3].isalpha():
        el = " " + num[-2] + " " + num[-1]
        num = num[:-2]
    if not num.isdigit():
        return {"NA": 1.0}
    if int(num) >= 10000 or int(num) <= 0:
        return {"NA": 1.0}
    millenium = num[:-3]
    century = num[:-2]
    year = num[-2:]
    if century == "":
        return {bl + read_2d(year) + el: 1.0}
    if millenium != "" and century[-1] == "0":
        if year == "00":
            method1 = digits[int(millenium)] + " thousand"
            method2 = read_2d(century) + " " + read_2d_year(year)
            return {bl + method1 + el: 0.9, bl + method2 + el: 0.1}
        else:
            method1 = digits[int(millenium)] + " thousand " + read_2d(year)
            method2 = digits[int(millenium)] + " thousand and " + read_2d(year)
            method3 = read_2d(century) + " " + read_2d_year(year)
            return {bl + method1 + el: 0.4, bl + method2 + el: 0.2, bl + method3 + el: 0.4}
    method = read_2d(century) + " " + read_2d_year(year)
    return {bl + method + el: 1.0}

def read_time(num):
    num_arr = num.split(":")
    hr, m = num_arr[0], num_arr[1]
    hr_w = read_2d(hr)
    if int(hr) == 0:
        hr_w = "zero"
    if m == "00":
        method1 = hr_w + " " + "o' clock"
        method2 = hr_w
        return {method1: 0.5, method2: 0.5}
    m_w = read_2d(m)
    return {hr_w + " " + m_w: 1.0}

def int2words_3d(n):
    # Read an integer with at most 3 digits (as array of words)
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
    # Read an integer with at most 15 digits (as array of words)
    n = int(num)
    if n == 0:
        return ["zero"]
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
    # Read a number digit by digit (as array of words)
    res_arr = []
    for d in num:
        if d.isdigit():
            res_arr = res_arr + [digits[int(d)]]
        else:
            res_arr = res_arr + [d]
    return res_arr

def float2words(num):
    # Read a number (integer or float, as array of words)
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
    # Read a number (integer, float or fraction)
    res_arr = []
    percent = False
    if num[-1] == "%":
        percent = True
        num = num[:-1]
    num_parts = num.split("/")
    if len(num_parts) == 1:
        numer = num_parts[0]
    else:
        numer, denom = num_parts[0], num_parts[1]
    res_arr = res_arr + float2words(numer)
    if len(num_parts) >= 2:
        res_arr = res_arr + ["over"] + float2words(denom)
    if percent:
        res_arr.append("percent")
    return " ".join(res_arr)

def int2words_4d(num):
    # Alternative way for reading 4-digit integers
    if len(num) != 4:
        return "NA"
    hundreds = num[:2]
    units = num[2:]
    if units[0] == "0":
        units = units[1]
    if units == "0":
        res = num2words(hundreds) + " hundred"
    else:
        res = num2words(hundreds) + " hundred " + num2words(units)
    return res

def ordinal_num(w):
    # Convert a cardinal number into ordinal
    res_arr = w.split(" ")
    last = res_arr[-1]
    if last in ordinals:
        res_arr[-1] = ordinals[last]
    else:
        res_arr[-1] = last + "th"
    return " ".join(res_arr)

def read_num_type(num, t):
    # Read a number based on type
    if t == "s":
        # Serial number, e.g. phone number
        return read_by_digit(num)
    if t == "y":
        # Year number, highway number, house number, room number
        return read_year(num)
    if t == "t":
        # Time
        return read_time(num)
    # General (cardinal) number or ordinal number
    if num[-1] != "%":
        cond1 = (len(num) == 4 and eval(num) >= 1000 and eval(num) < 10000)
        cond2 = (len(num) == 5 and eval(num) <= -1000 and eval(num) > -10000)
    else:
        cond1 = False
        cond2 = False
    if cond1 or cond2:
        form1 = num2words(num)
        if eval(num) < 0:
            form2 = "minus " + int2words_4d(num[1:])
        else:
            form2 = int2words_4d(num)
        if t == "o":
            # Ordinal number
            form1 = ordinal_num(form1)
            form2 = ordinal_num(form2)
        if abs(eval(num)) < 2000:
            return {form1: 0.5, form2: 0.5}
        else:
            return {form1: 0.8, form2: 0.2}
    if t == "o":
        # Ordinal number
        return {ordinal_num(num2words(num)): 1.0}
    return {num2words(num): 1.0}

def read_num_basic(num, types):
    # Read a number based on possible types
    res = {}
    for t in types:
        p = read_num_type(num, t)
        for f in p:
            if f in res:
                res[f] = res[f] + types[t] * p[f]
            else:
                res[f] = types[t] * p[f]
    return res

def split_options(old_p, original, new_option, new_p):
    p = copy.deepcopy(old_p)
    p[original] -= new_p
    if new_option in p:
        p[new_option] += new_p
    else:
        p[new_option] = new_p
    return p

def alternative_one(w):
    mult = {"hundred", "thousand", "million", "billion", "trillion"}
    old_arr = w.split(" ")
    res_arr = []
    for i in range(len(old_arr) - 1):
        if old_arr[i] == "one" and old_arr[i+1] in mult:
            res_arr.append("a")
        else:
            res_arr.append(old_arr[i])
    res_arr.append(old_arr[-1])
    return " ".join(res_arr)

def alternative_neg(w):
    old_arr = w.split(" ")
    res_arr = []
    for i in range(len(old_arr)):
        if old_arr[i] == "minus":
            res_arr.append("negative")
        else:
            res_arr.append(old_arr[i])
    return " ".join(res_arr)

def read_num(num, types):
    res = read_num_basic(num, types)
    for w in res:
        alt_one = alternative_one(w)
        prob = res[w]
        res = split_options(res, w, alt_one, prob / 2)
    for w in res:
        alt_neg = alternative_neg(w)
        prob = res[w]
        res = split_options(res, w, alt_neg, prob / 2)
    return res
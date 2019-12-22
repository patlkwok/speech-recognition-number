import re

def clean_word(w):
    # Clean a word, remove punctuations at beginning or end
    new_w = ""
    for c in w:
        if c in {"'", '"', "(", ")", "[", "]", "{", "}"}:
            continue
        new_w = new_w + c
    if new_w[-1] in {".", ",", "?", "!", ";"}:
        return new_w[:-1]
    return new_w

def contain_num(s):
    # Check if a string contains at least one digit
    return any(c.isdigit() for c in s)

def get_numbers(s):
    # Get the words containing digits from a sentence
    words = s.split(" ")
    words = [clean_word(w).lower() for w in words]
    res = []
    for i in range(len(words)):
        w = words[i]
        if contain_num(w):
            if i == 0 and i == len(words) - 1:
                d = {"num": w, "pos": i, "prev": "", "next": ""}
            elif i == 0:
                d = {"num": w, "pos": i, "prev": "", "next": words[i+1]}
            elif i == len(words) - 1:
                d = {"num": w, "pos": i, "prev": words[i-1], "next": ""}
            else:
                d = {"num": w, "pos": i, "prev": words[i-1], "next": words[i+1]}
            res.append(d)
    return res

def get_type(d):
    # For each type, get the probabilities that the number belongs to it
    months = {"january", "february", "march", "april", "may", "june", \
              "july", "august", "september", "october", "november", "december"}
    num = d["num"]
    digit_only = num.isdigit()
    ordinal = False
    alnum = num.isalnum()
    n_digits = len(num)
    if num[-2:] in {"st", "nd", "rd", "th"} and num[:-2].isdigit():
        ordinal = True
        num = num[:-2]
    """
    elif num[-1] == "d" and num[:-1].isdigit():
        if num[-2] == "2" or num[-2] == "3":
            ordinal = True
            num = num[:-1]
    """
    ana = False
    if alnum and not ordinal:
        if re.match(r"^[A-Za-z]{0,2}\d{1,4}[A-Za-z]{0,2}\Z", num) is not None:
            ana = True
    tod = False
    if re.match(r"^\d{1,2}:\d{2}\Z", num) is not None:
        tod = True
    # Case 1: Very short integers (1-2 digits)
    if digit_only and n_digits <= 2:
        if int(num) <= 31 and (d["prev"] in months or d["next"] in months):
            p = {"o": 0.9, "c": 0.05, "s": 0.05}
        else:
            p = {"c": 0.9, "s": 0.1}
    # Case 2: Short integers (1-4 integers)
    elif digit_only and n_digits <= 4:
        if int(num) >= 1500 and int(num) <= 2500 and d["prev"] in months:
            p = {"y": 0.85, "c": 0.1, "s": 0.05}
        elif int(num) >= 1500 and int(num) <= 2500 and d["prev"] in {"in", "during", "between", "from"}:
            p = {"y": 0.85, "c": 0.1, "s": 0.05}
        elif int(num) >= 1500 and int(num) <= 2500 and d["prev"].isdigit():
            p = {"y": 0.85, "c": 0.1, "s": 0.05}
        elif int(num) >= 1500 and int(num) <= 2500:
            p = {"y": 0.55, "c": 0.35, "s": 0.1}
        else:
            p = {"y": 0.3, "c": 0.6, "s": 0.1}
    # Case 3: Long integers
    elif digit_only:
        if n_digits <= 6:
            p = {"c": 0.6, "s": 0.4}
        elif n_digits <= 9:
            p = {"c": 0.4, "s": 0.6}
        elif n_digits <= 12:
            p = {"c": 0.2, "s": 0.8}
        else:
            p = {"s": 1.0}
    # Case 4: Ordinal numbers
    elif ordinal:
        if n_digits <= 6:
            p = {"o": 0.9, "s": 0.1}
        elif n_digits <= 8:
            p = {"o": 0.7, "s": 0.3}
        else:
            p = {"s": 1.0}
    # Case 5: Letters + numbers + letters
    elif ana:
        p = {"y": 0.7, "s": 0.3}
    # Case 6: Time of day
    elif tod:
        p = {"t": 0.9, "s": 0.1}
    # Case 7: Regular numbers
    else:
        mat = re.match("^\-?\d+\.?\d*([/]\-?\d+\.?\d*)?%?\Z", num)
        if mat is not None and n_digits <= 6:
            p = {"c": 0.9, "s": 0.1}
        elif mat is not None and n_digits <= 10:
            p = {"c": 0.8, "s": 0.2}
        elif mat is not None and n_digits <= 15:
            p = {"c": 0.4, "s": 0.6}
        else:
            p = {"s": 1.0}
    return {"num": num, "pos": d["pos"], "replace": d["num"], "type": p}
# Python program to print a given number in 
# words. The program handles numbers  
# from 0 to 9999  
  
# A function that prints 
# given number in words 

digits = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", \
          5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

teens = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", \
         15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"}

tens = {10: "ten", 20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", \
        60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"}
        
multiples = {100: "hundred", 1000: "thousand", 10 ** 6: "million", \
             10 ** 9: "billion", 10 ** 12: "trillion"}
        
def int2words_3d(n):
    if n == 0:
        return ""
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
    return " ".join(res_arr)

def num2words(num):
    
    

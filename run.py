import itertools
import sys
from get_number_type import *
from read_numbers import *

def get_type_sentence(s):
    # Get the possible types of numbers given a sentence
    nums = get_numbers(s)
    res = []
    for n in nums:
        t = get_type(n)
        res.append(t)
    return res

def read_num_sentence(s):
    # Get the possible way to read numbers given a sentence
    types = get_type_sentence(s)
    res = []
    for t in types:
        num = t["num"]
        pos = t["pos"]
        rep = t["replace"]
        try:
            reads = read_num(num, t["type"])
        except:
            reads = read_num(num, {"s": 1.0})
        d = {"num": num, "pos": pos, "replace": rep, "p": reads}
        res.append(d)
    return res

def get_replaces(reads):
    # Some format conversion
    possible_ways = [list(reads[i]["p"].keys()) for i in range(len(reads))]
    all_replaces = []
    iter_ways = itertools.product(*possible_ways)
    for i in iter_ways:
        this_replaces = []
        for j in range(len(reads)):
            r = reads[j]
            d = {"replace": r["replace"], "pos": r["pos"]}
            d["new"] = i[j]
            d["p"] = r["p"][i[j]]
            this_replaces.append(d)
        all_replaces.append(this_replaces)
    return all_replaces
    
def replace_num(s, replaces):
    # Replace numbers in a sentence with spelt-out forms
    s = s.lower()
    prob = 1.0
    s_arr = s.split(" ")
    for r in replaces:
        old_word = s_arr[r["pos"]]
        new_word = old_word.replace(r["replace"], r["new"])
        s_arr[r["pos"]] = new_word
        prob *= r["p"]
    return " ".join(s_arr), prob

def get_all_possibles(s):
    # Get all possible ways of reading a sentence containing numbers
    possibles = []
    reads = read_num_sentence(s)
    all_replaces = get_replaces(reads)
    for replaces in all_replaces:
        new_s, prob = replace_num(s, replaces)
        d = {"new": new_s, "p": prob}
        possibles.append(d)
    return possibles

if __name__ == "__main__":
    input_file, output_file = sys.argv[1], sys.argv[2]
    with open(input_file) as f:
        contents = f.readlines()
    contents = [s.strip() for s in contents]
    with open(output_file, "w+") as f:
        for s in contents:
            f.write(s)
            f.write("\n")
            possibles = get_all_possibles(s)
            for p in possibles:
                f.write(str(p["p"]))
                f.write(" | ")
                f.write(p["new"])
                f.write("\n")
            f.write("\n\n")
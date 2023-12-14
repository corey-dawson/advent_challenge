import re

# create function to find first digit
def get_num(line, rgx, map, rv=False):
    rgx_rslt = re.search(rgx, line)
    if len(rgx_rslt.group()) == 1:
        return(line[rgx_rslt.start()])
    else:
        if rv:
            grp = str(rgx_rslt.group())[::-1]
        else : 
            grp = rgx_rslt.group()
        return(str(map[grp]))
    

# read file
with open("dec1/ch1_input", "r") as f:
    lines = [l.strip() for l in f]

# map word to value
n_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

# create rgx and reverse rgx
rgx = f"{'|'.join(n_map.keys())}|\d"
rgx_rv = f"{'|'.join([str(k)[::-1] for k in n_map.keys()])}|\d"

# loop and get digits
l_rslt = []
for l in lines:
    l_rslt.append(
        int(f"{get_num(l, rgx, n_map)}{get_num(l[::-1], rgx_rv, n_map, rv=True)}")
    )
rslt = sum(l_rslt)
print(rslt)


# create function to find first digit
def get_num(line):
    for c in line:
        if c.isdigit():
            return(c)

# read file
with open("dec1/ch1_input", "r") as f:
    lines = [l.strip() for l in f]

# loop and get digits
l_rslt = []
for l in lines:
    l_rslt.append(
        int(f"{get_num(l)}{get_num(l[::-1])}")
    )
rslt = sum(l_rslt)
print(rslt)

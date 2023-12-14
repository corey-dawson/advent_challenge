import re

class nm_match:
    def __init__(self, num, inst, x1, x2, y1, y2):
        self.num = num
        self.inst = inst
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    def prnt_rng(self):
        print(f"{self.num} inst{self.inst}: ({self.x1}, {self.y1}) to ({self.x2}, {self.y2})")
        
class nterms:
    def __init__(self, num, row, strt_idx, end_idx, x1,x2):
        self.num = num
        self.row = row
        self.strt_idx = strt_idx
        self.end_idx = end_idx
        self.y1 = row
        self.y2 = row
        self.x1 = x1
        self.x2 = x2
    def prnt_rng(self):
        print(f"{self.num}: row_idx: {self.row}, col_idx: {self.strt_idx} to {self.end_idx}, srch-rg: {self.x1} to {self.x2}")
        
class asterick:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    def prnt_rng(self):
        print(f"({self.x1}, {self.y1}) to ({self.x2}, {self.y2})")

# find all numbers in file and get a (x, y) range
# to search for special characters        
def get_search_idx(lines):
    
    # get index range of each number
    max_col_idx = len(lines[0])
    max_rows_idx = len(lines)
    
    # main func logic
    nums = []
    inst = 0
    for i in range(0, len(lines)):
        y1 = i
        y2 = i
        # if y1 > 0:
        #     y1 = y1 - 1
        # if y2 < max_rows_idx:
        #     y2 = y2 + 1
        l = lines[i]
        # regex search for numbers
        num_match = re.findall("\d+", l)
        # create search index for each found num
        for n in num_match:
            if l[0:len(n)] == n:
                nm_rgx = n + "+\\b"
            else:
                nm_rgx = "(?<=\D)" + n + "+\\b"
            x1, x2 = re.search(nm_rgx, l).span()
            x2 = x2 - 1
            # if x1 > 0:
            #     x1 = x1 - 1
            # if x2 < max_col_idx:
            #     x2 = x2
            nums.append(nm_match(
                num = int(n),
                inst = inst,
                x1 = x1,
                x2 = x2,
                y1 = y1,
                y2 = y2
            ))
            inst += 1
    return(nums)

# read in filee
with open("dec3/input", "r") as f:
    lines = [l.strip() for l in f]

# find all non period symbols
# create rgx from all symbols
syms = []
for l in lines:
    line_syms = re.sub("\d|\\.", "", l)
    if len(line_syms) > 0:
        for c in line_syms:
            syms.append(c)
syms = list(set(syms))
sym_rgx = "|\\".join([str(x) for x in syms])
sym_rgx = "\\" + sym_rgx

# get list of nums with a search area
# lines = [lines[55]]
nums = get_search_idx(lines[0:8])

# for each found number, see if a sym is in the 
# sub matrix defined by the search area indexes
# sym_rgx = r"[^\.^\d]"
terms = []
for m in nums:
    search = [x[m.x1:m.x2] for x in lines[m.y1:m.y2+1]]
    srch_str = "".join(search)
    # print("===============")
    # m.prnt_rng()
    # print(f"search str: {srch_str}")
    if bool(re.search(sym_rgx, srch_str)):
        terms.append(m.num)
print(f"the sum of nums with adjacent symbols = {sum(terms)}")

# part 2
# find all * with serch areas

def find_idx2(lines):
    # get index range of each number
    max_col_idx = len(lines[0]) - 1
    max_rows_idx = len(lines) - 1
    ast = []
    # loop through to find *
    for y in range(0, len(lines)):
        l = lines[y]
        for x in range(0, len(l)):
            if "*" == l[x]:
                x1 = x-1
                x2 = x+1
                y1 = y-1
                y2 = y+1
                if x1 < 0:
                    x1 = x
                if x2 > max_col_idx:
                    x2 = x
                if y1 < 0 :
                    y1 = y
                if y2 > max_rows_idx:
                    y2 = y
                ast.append(asterick(
                    x1 = x1,
                    x2 = x2,
                    y1 = y1,
                    y2 = y2
                ))
    return(ast)
                

ast = find_idx2(lines)

def find_matches(ast, nums):
    matches = []
    for i in ast:
        print("")
        print("===============================")
        print(f"({i.x1}, {i.y1}) to ({i.x2}, {i.y2})")
        tmp = []
        for n in nums:
            cond = [
                n.end_idx < i.x1,
                n.strt_idx > i.x2,
                n.row < i.y1,
                n.row > i.y2,
            ]
            if all([not x for x in cond]):
                print(f"match: {n.num}")
                tmp.append(n.num)
        if len(tmp) == 2:
            # print("=================================")
            # print("asterick range: ")
            # i.prnt_rng()
            # ms = ", ".join([str(x) for x in tmp])
            # print(f"matches for asteric: {ms}")
            matches.append(tmp)
    return(matches)

matches = find_matches(ast, nums)
p = [m[0] * m[1] for m in matches]
s = sum(p)


# linr 7 (idx = 6). missing 372, 89

strt = None
end = None
nums = []
for r in range(0, len(lines)):
    l = lines[r]
    for i in range(0, len(l)):
        if l[i].isdigit():
            if strt == None:
                strt = i
            if (strt != None and i+1 == len(l)):
                end = i
                x1 = strt
                x2 = end
                if strt > 0:
                    x1 = strt - 1
                print(f"{l[strt:end+1]}: {strt}-{end}")
                nums.append(
                    nterms(
                        int(l[strt:end+1]),
                        row = r,
                        strt_idx=strt,
                        end_idx=end,
                        x1 = x1,
                        x2 = x2
                    )             
                )
                strt = None
                end = None
        elif (strt != None and end == None):
                end = i
                x1 = strt
                x2 = end
                if strt > 0:
                    x1 = strt - 1
                if end == len(l):
                    x2 = end - 1
                print(f"{l[strt:end]}: {strt}-{end}")
                nums.append(
                    nterms(
                        int(l[strt:end]),
                        row = r,
                        strt_idx=strt,
                        end_idx=end - 1,
                        x1 = x1,
                        x2 = x2
                    )             
                )
                strt = None
                end = None
            
for itm in nums:
    itm.prnt_rng()
    
for a in ast:
    a.prnt_rng()
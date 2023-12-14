import numpy as np
import pandas as pd

class smaps:
    def __init__(self, prt, rng_lst):
        prts = prt.strip().split("\n")[1:]
        d = {}
        for i in np.arange(min(seeds), max(seeds)+1, 1):
            d[i] = i
        for r in prts:
            vals = [int(x) for x in r.split()]
            for i, j in zip(range(vals[1], vals[1]+vals[2]), range(vals[0], vals[0]+vals[2])):
                d[i] = j
        
        # create class map object
        self.map_nm = prt.split(":")[0].replace("-to", "")[:-4]
        self.map = d
        

# read in filee
file = "dec5/input"
with open(file, "r") as f:
    content = f.read()

# isoloate each section of file    
prts = content.split("\n\n")


# get the seeds as a dataframe
seeds = [int(x) for x in prts[0].split(":")[1].strip().split()]
df = pd.DataFrame({"seed": seeds})

# create map and a map name:
maps = []
conv_nm = []
for p in prts[1:]:
    conv_nm.append(p.split(":")[0].replace("-to", "")[:-4])
    if conv_nm[-1] == "seed-soil":
        maps.append(smaps(p, seeds))
    else:
        src_col = conv_nm[-1].split("-")[0]
        mp = [x for x in maps if x.map_nm.split("-")[1] == src_col][0]
        maps.append(smaps(p, mp.map.values())) 

# walk through map tranformation
for c in conv_nm:
    # get map
    m = [x.map for x in maps if x.map_nm == c][0]
    # get new dataframe col name
    src_nm = c.split("-")[0]
    trg_nm = c.split("-")[1]
    # run map
    df[trg_nm] = df[src_nm].map(m)

# part 1 try 2
# =============================================

class smaps2:
    def __init__(self, prt):
        prts = prt.strip().split("\n")[1:]
        mps = []

        for r in prts:
            vals = [int(x) for x in r.split()]
            mps.append(vals)
        
        # create class map object
        self.map_nm = prt.split(":")[0].replace("-to", "")[:-4]
        self.maps = mps

# read in filee
file = "dec5/input"
with open(file, "r") as f:
    content = f.read()

# isoloate each section of file    
prts = content.split("\n\n")


# get the seeds as a dataframe
seeds = [int(x) for x in prts[0].split(":")[1].strip().split()]
df = pd.DataFrame({"seed": seeds})

# create maps
maps = []
conv_nm = []
for p in prts[1:]:
    conv_nm.append(p.split(":")[0].replace("-to", "")[:-4])
    maps.append(smaps2(p))

for c in conv_nm:

    # get new dataframe col name
    src_nm = c.split("-")[0]
    trg_nm = c.split("-")[1]
    
    # create new col
    df[trg_nm] = df[src_nm]
    
    # get map
    mps = [x.maps for x in maps if x.map_nm == c][0]
    
    # create map calc
    for dest, src, lngth in mps:
        uppr_bnd = src + lngth
        offset = dest - src
        df.loc[(df[src_nm] >= src) & (df[src_nm] < uppr_bnd),  trg_nm] = df.loc[(df[src_nm] >= src) & (df[src_nm] < uppr_bnd),  src_nm]  + offset

print(f"min of seeds: {df.location.min()}")

# part 2: big fail for big data
# =============================================

upd_seeds = []

# spit into groups of 2
seed_iter = iter(seeds)
b = zip(seed_iter,seed_iter)
for x, y in b:
    tmp_seeds = list(np.arange(x,x+y,1))
    upd_seeds.extend(tmp_seeds)

df = pd.DataFrame({"seed": upd_seeds})

# create maps
maps = []
conv_nm = []
for p in prts[1:]:
    conv_nm.append(p.split(":")[0].replace("-to", "")[:-4])
    maps.append(smaps2(p))

for c in conv_nm:

    # get new dataframe col name
    src_nm = c.split("-")[0]
    trg_nm = c.split("-")[1]
    
    # create new col
    df[trg_nm] = df[src_nm]
    
    # get map
    mps = [x.maps for x in maps if x.map_nm == c][0]
    
    # create map calc
    for dest, src, lngth in mps:
        uppr_bnd = src + lngth
        offset = dest - src
        df.loc[(df[src_nm] >= src) & (df[src_nm] < uppr_bnd),  trg_nm] = df.loc[(df[src_nm] >= src) & (df[src_nm] < uppr_bnd),  src_nm]  + offset

print(f"min of seeds: {df.location.min()}")

# part 2 try 2
# ===================================================================

class obj:
    def __init__(self, obj_nm):
        self.name = obj_nm
        self.range = []
    def add_range(self, strt, end, offset = 0):
        self.range.append([strt, end, offset])
    def print(self):
        print(f"{self.name}")
        print("===========================")
        for s, e, o in self.range:
            print(f"[start = {s}, end = {e}, offset = {o}]")
        print("")
        
        
class maps:
    def __init__(self, prt):
        transf = []
        src_dest = prt.split(":")[0].replace("-to", "")[:-4].strip().split("-")
        rngs = [int(x) for x in prt.split(":")[1].strip().split()]
        rng_iter = iter(rngs)
        for offset, strt, lngth in zip(rng_iter, rng_iter, rng_iter):
            o = offset - strt
            s = strt
            e = strt + lngth - 1
            transf.append([s, e, o])
        self.input = src_dest[0]
        self.output  = src_dest[1]
        self.trans = transf
    def print(self):
        print(f"map input: {self.input}")
        print(f"map output: {self.output}")
        print("===========================")
        for s, e, o in self.trans:
            print(f"[start = {s}, end = {e}, offset = {o}]")
        print("")
        
def transform(map_nm, mps, obj_rngs):
    # this is the function
    # set initial 0
    mp_input = map_nm.split("-")[0]
    m = [x for x in mps if x.input == mp_input][0] # map
    o = [x for x in obj_rngs if x.name == mp_input][0] # range data to map
    r_all = [x for x in o.range]

    for t in m.trans:
        # get all initial obj ranges to consider (with 0 offset)
        r_flt = [x for x in r_all if x[2] == 0 ]
        
        for r in r_flt:
            # see if transformation intersects with range
            logic = [t[0] > r[1], t[1] < r[0]]
            if any(logic):
                new_rng = [r]
            else:
                # 4 cases. 
                # trans range withinh obj range
                # t lower is within obj range & t upper is outside
                # t upper is within obj range and t lower is outside
                # obj range is within trans range
                if t[0] <= r[0] and t[1] >= r[1]:
                    new_rng = [[r[0], r[1], t[2]]]
                elif t[0] > r[0] and t[1] < r[1]:
                    new_rng = [
                        [r[0], t[0]-1, 0],
                        [t[0], t[1], t[2]],
                        [t[1]+1, r[1], 0]
                    ]
                elif t[0] <= r[0] and t[1] < r[1]:
                    new_rng = [
                        [r[0], t[1], t[2]],
                        [t[1]+1, r[1], 0]
                    ]
                elif t[0] > r[0] and t[1] >= r[1]:
                    new_rng = [
                        [r[0], t[0]-1, 0],
                        [t[0], r[1], t[2]]
                    ]
                # remove old range and add in new range
                r_all = [x for x in r_all if x[0] != r[0] and x[1] != r[1]]
                r_all.extend(new_rng)
    # create a new r all class
    out = obj(map_nm)
    for x in r_all:
        out.add_range(x[0], x[1], x[2])
    return(out)

# read in filee
file = "dec5/input"
with open(file, "r") as f:
    content = f.read()

# isoloate each section of file    
prts = content.split("\n\n")

# get the seeds as a dataframe
seeds = [int(x) for x in prts[0].split(":")[1].strip().split()]

# spit into groups of 2 and seed as a class
obj_rngs = [obj("seed")]
seed_iter = iter(seeds)
b = zip(seed_iter,seed_iter)
for x, y in b:
    obj_rngs[0].add_range(x, x+y-1)

# create transformation map classes
mps = []
conv_nm = []
for p in prts[1:]:
    conv_nm.append(p.split(":")[0].replace("-to", "")[:-4])
    mps.append(maps(p))

# apply transform
for nm in conv_nm:
    obj_rngs.append(
        transform(nm, mps, obj_rngs)
    )
    # apply offset
    new_obj_nm = nm.split("-")[-1]
    new_obj = obj(new_obj_nm)
    last = obj_rngs[-1]
    for x in last.range:
        new_obj.add_range(x[0]+x[2], x[1]+x[2], 0)
    obj_rngs.append(new_obj)

# print transformations
[x.print() for x in obj_rngs]
# print transmformations without intermediates
[x.print() for x in obj_rngs if "-" not in x.name]

# get list of locations
loc = [x for x in  obj_rngs if x.name == "location"][0]
loc_min = min([x[0] for x in loc.range])
print(f"min of seeds: {loc_min}")

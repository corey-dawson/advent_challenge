import pandas as pd

# object for each reveal
class reveal:   
    def __init__(self, game_nb, reveal):
        self.game_nb = game_nb
        self.red = 0
        self.blue = 0
        self.green = 0
        for r in reveal.split(","):
            cnt, color = r.strip().split(" ")
            match color:
                case "red":
                    self.red = int(cnt)
                case "blue":
                    self.blue = int(cnt)
                case "green":
                    self.green = int(cnt)       

def find_removals(data: list[any], red: int, green: int, blue: int):
    # filter down to constraints
    rm_nb = []
    rm_nb.extend([x.game_nb for x in rvl if x.red  > red])
    rm_nb.extend([x.game_nb for x in rvl if x.blue  > blue])
    rm_nb.extend([x.game_nb for x in rvl if x.green  > green])
    rm_nb = list(set(rm_nb))
    return(rm_nb)

def rvl_to_df(data):
    data_dict = {
        "game_nb": [x.game_nb for x in data],
        "red": [x.red for x in data],
        "blue": [x.blue for x in data],
        "green": [x.green for x in data]
    }
    df = pd.DataFrame.from_dict(data_dict)
    return df

# read in filee
with open("dec2/input", "r") as f:
    lines = [l.strip() for l in f]

# parser file to create a list of reveals
rvl = []
for l in lines:
    game, reveals = l.split(":")
    game_nb = int(game.split(" ")[1])
    for r in reveals.split(";"):
        rvl.append(reveal(game_nb, r))

# find games that dont meet constraints
rm_nums = find_removals(
    data = rvl,
    red = 12,
    green = 13,
    blue = 14)

# filter and sum up games
valid_nb = {x.game_nb for x in rvl if x.game_nb not in rm_nums}
valid_sum = sum(valid_nb)
print(f"Sum of valid games is {valid_sum}")

# challenge 2
# find max per group_nm for red, green, blue
df = rvl_to_df(rvl)
grp = df.groupby("game_nb").max().reset_index()
grp["prod"] = grp.red * grp.blue * grp.green
rslt = grp["prod"].sum()
print(f"the sum of the products is {rslt}")

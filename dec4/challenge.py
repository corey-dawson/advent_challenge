from math import pow

class card:
    def __init__(self, card):
        card_vals = [x.strip() for x in card.split(":")[-1].split(" | ")]
        self.card_num = int(card.split(":")[0].split()[-1])
        self.wins = [int(x) for x in card_vals[0].split()]
        self.nums = [int(x) for x in card_vals[1].split()]

# read in filee
file = "dec4/input"
with open(file, "r") as f:
    lines = [l.strip() for l in f]

# create a collection of cards    
cards = [card(l) for l in lines]

# for each card, findnumber of matches to winning numbers
match = [sum([True if x in c.wins else False for x in c.nums]) for c in cards]
score = [pow(2, x-1) if x > 0 else 0 for x in match]
rslt = int(sum(score))
print(f"total score: {rslt}")

# part 2
# ===============================================================

# duplicate card object
copies = cards.copy()

# get disctinct card numbers
uniq_cards = [x.card_num for x in copies]

# loop through
for i in uniq_cards:
    n_cards = len([x for x in copies if x.card_num == i])
    # crnt card
    c = cards[i-1]
    # crnt card matches
    matches = sum([True if x in c.wins else False for x in c.nums])
    copy = cards[i:i+matches]
    for i in range(0, n_cards):
        copies.extend(copy)
    #copies.sort(key = lambda x: x.card_num)

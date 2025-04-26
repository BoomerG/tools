import pandas as pd
from itertools import combinations

df8 = pd.read_csv('team_8_stats.csv')
df9 = pd.read_csv('team_9_stats.csv')
handicap = 23
sl8 = {}
sl9 = {}

for i, row in df8.iterrows():
    name = row['Player Name']
    sl8[name] = row['Skill Level']
    
for i, row in df9.iterrows():
    name = row['Player Name']
    sl9[name] = row['Skill Level']
    

def opt_team():
    valid_combos8 = [combo for combo in combinations(sl8.items(), 5) if sum(sl for name, sl in combo) == handicap]
    sorted_combos8 = [sorted(combo, key=lambda item: item[1], reverse=True) for combo in valid_combos8]
    valid_combos9 = [combo for combo in combinations(sl9.items(), 5) if sum(sl for name, sl in combo) == handicap]
    sorted_combos9 = [sorted(combo, key=lambda item: item[1], reverse=True) for combo in valid_combos9]
    
    tm8_formatted = ["<br>Team: " + ", ".join(name for name, skill in combo) + "<br>Skills: " + ", ".join(str(skill) for name, skill in combo) for combo in sorted_combos8]
    tm9_formatted = ["<br>Team: " + ", ".join(name for name, skill in combo) + "<br>Skills: " + ", ".join(str(skill) for name, skill in combo) for combo in sorted_combos9]
    
    return tm8_formatted, tm9_formatted

# combos8, combos9 = opt_team()
# print(combos8)
# print(combos9)

if __name__ == "__main__":
    combos8, combos9 = str(opt_team())
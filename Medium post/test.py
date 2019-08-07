import urllib, json
import pandas as pd
import re
from itertools import permutations
from pulp import *


LATEST_URL = "https://api.draftkings.com/draftgroups/v1/draftgroups/21434/draftables?format=json"
response = urllib.request.urlopen(LATEST_URL)
data = json.loads(response.read())
current = pd.DataFrame.from_dict(data["draftables"])

# Remove players that are out or questionable
current = current[current.status == "None"]

# Add flex position
flex = current[current.position.isin(["RB","WR","TE"])].copy()
flex.position = "FLEX"
current = pd.concat([current, flex])

def get_float(l, key):
    """ Returns first float value from a list of dictionaries based on key. Defaults to 0.0 """
    for d in l:
        try:
            return float(d.get(key))
        except:
            pass
    return 0.0

points = [get_float(x, "value") for x in
  current.draftStatAttributes]
current["points"] = points


availables = current[["position", "displayName", "salary",
  "points"]].groupby(["position", "displayName", "salary",
  "points"]).agg("count")
availables = availables.reset_index()

salaries = {}
points = {}
for pos in availables.position.unique(): #Returns the sorted unique elements of an array
    available_pos = availables[availables.position == pos]
    salary = list(available_pos[["displayName","salary"]].set_index("displayName").to_dict().values())[0]
    point = list(available_pos[["displayName","points"]].set_index("displayName").to_dict().values())[0]
    salaries[pos] = salary
    points[pos] = point

pos_num_available = {
    "QB": 1,
    "RB": 2,
    "WR": 3,
    "TE": 1,
    "FLEX": 1,
    "DST": 1
}

# Constraint
SALARY_CAP = 50000

#  _vars is a dictionary of position and an LpVariable
_vars = {k: LpVariable.dict(k, v, cat="Binary") for k, v in points.items()}

# Setup of the problem

prob = LpProblem("Fantasy", LpMaximize)
rewards = []
costs = []
position_constraints = []

# Setting up the reward
for k, v in _vars.items():
    costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])
    rewards += lpSum([points[k][i] * _vars[k][i] for i in v])
    prob += lpSum([_vars[k][i] for i in v]) <= pos_num_available[k]

prob += lpSum(rewards)
prob += lpSum(costs) <= SALARY_CAP

prob.solve()
def summary(prob):
    div = '---------------------------------------\n'
    print("Variables:\n")
    score = str(prob.objective)
    constraints = [str(const) for const in prob.constraints.values()]
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))
        constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
        if v.varValue != 0:
            print(v.name, "=", v.varValue)
    print(div)
    print("Constraints:")
    for constraint in constraints:
        constraint_pretty = " + ".join(re.findall("[0-9\.]*\*1.0", constraint))
        if constraint_pretty != "":
            print("{} = {}".format(constraint_pretty, eval(constraint_pretty)))
    print(div)
    print("Score:")
    score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
    print("{} = {}".format(score_pretty, eval(score)))


summary(prob)

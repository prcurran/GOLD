from ccdc import io
import numpy as np
import pandas as pd


def activity(identifier):
    if "ZINC" in identifier:
        return 0
    else:
        return 1


entries = io.EntryReader("hotspot_scored.sdf")

idents = [entry.identifier for entry in entries]
act = [activity(entry.identifier) for entry in entries]

hs1 = [float(np.sum([float(entry.attributes["acceptor"]),
                float(entry.attributes["donor"]),
                float(entry.attributes["apolar"])
                ]))
        for entry in entries]

# hs2 = [entry.attributes["hs2_total"] for entry in entries]
hs2 = [float(np.sum([float(entry.attributes["hs2_acceptor"]),
                float(entry.attributes["hs2_donor"]),
                float(entry.attributes["hs2_apolar"])
                ]))
        for entry in entries]

df1 = pd.DataFrame({"identifier": idents,
                    "score": hs1,
                    "activity": act,
                    "scheme": ["hs1"] * len(idents)})

df1 = df1.sort_values(by="score", ascending=False)

df2 = pd.DataFrame({"identifier": idents,
                    "score": hs2,
                    "activity": act,
                    "scheme": ["hs2"] * len(idents)})

df2 = df2.sort_values(by="score", ascending=False)

df1.to_csv("df1.csv")
df2.to_csv("df2.csv")
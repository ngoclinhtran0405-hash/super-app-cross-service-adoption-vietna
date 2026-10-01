"""Sanity check: recompute AVE and composite reliability (rho_c) from the final outer
loadings and compare with the values reported by SmartPLS.
Loadings are rounded to 3 decimals, so small differences (<= 0.005) are expected."""
import pandas as pd, numpy as np

load = pd.read_csv("results/outer_loadings_final.csv")
rep = pd.read_csv("results/reliability_validity.csv").set_index("construct")
rows = []
for c, g in load.groupby("construct"):
    l = g["outer_loading"].to_numpy()
    ave = np.mean(l**2)
    rho_c = l.sum()**2 / (l.sum()**2 + np.sum(1 - l**2))
    rows.append((c, len(l), round(ave,3), rep.loc[c,"ave"], round(rho_c,3), rep.loc[c,"rho_c"]))
df = pd.DataFrame(rows, columns=["construct","n_items","ave_calc","ave_reported","rho_c_calc","rho_c_reported"])
df["ok"] = ((df.ave_calc-df.ave_reported).abs()<=0.005) & ((df.rho_c_calc-df.rho_c_reported).abs()<=0.005)
print(df.to_string(index=False))
print("\nTotal retained items:", len(load))

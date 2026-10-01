"""Re-create the main figures from the CSV files in results/."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

# 1) Path coefficients
p = pd.read_csv("results/path_coefficients.csv")
p["label"] = p["from"] + " → " + p["to"]
p = p.sort_values("original_sample")
colors = np.where(p.p_value < 0.05, "#1f6feb", "#b0b7c3")
fig, ax = plt.subplots(figsize=(7, 9))
ax.barh(p.label, p.original_sample, color=colors)
ax.axvline(0, color="black", lw=0.8)
ax.set_xlabel("Path coefficient (β)")
ax.set_title("Structural model: path coefficients\n(blue = significant at p < 0.05, grey = not supported)")
fig.tight_layout(); fig.savefig("figures/path_coefficients.png", dpi=200); plt.close(fig)

# 2) HTMT heatmap
h = pd.read_csv("results/htmt.csv")
names = sorted(set(h.construct_a) | set(h.construct_b))
m = pd.DataFrame(np.nan, index=names, columns=names)
for _, r in h.iterrows():
    m.loc[r.construct_a, r.construct_b] = r.htmt
    m.loc[r.construct_b, r.construct_a] = r.htmt
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(m.values.astype(float), cmap="Blues", vmin=0.3, vmax=1.0)
ax.set_xticks(range(len(names)), names); ax.set_yticks(range(len(names)), names)
for i in range(len(names)):
    for j in range(len(names)):
        if i != j: ax.text(j, i, f"{m.iloc[i,j]:.2f}", ha="center", va="center", fontsize=7,
                           color="white" if m.iloc[i,j] > 0.75 else "black")
ax.set_title("Discriminant validity: HTMT (threshold 0.90)")
fig.colorbar(im, ax=ax, shrink=0.8); fig.tight_layout()
fig.savefig("figures/htmt_heatmap.png", dpi=200); plt.close(fig)

# 3) R-squared
r = pd.read_csv("results/r_squared.csv").sort_values("r2")
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.barh(r.construct, r.r2, color="#1f6feb")
for y, v in enumerate(r.r2): ax.text(v + 0.01, y, f"{v:.3f}", va="center")
ax.set_xlim(0, 0.75); ax.set_xlabel("R²"); ax.set_title("Explained variance of endogenous constructs")
fig.tight_layout(); fig.savefig("figures/r_squared.png", dpi=200); plt.close(fig)

# 4) Outer loadings
l = pd.read_csv("results/outer_loadings_final.csv")
fig, ax = plt.subplots(figsize=(7, 8))
ax.scatter(l.outer_loading, range(len(l)), color="#1f6feb", s=18)
ax.set_yticks(range(len(l)), l.item, fontsize=6)
ax.axvline(0.7, color="red", ls="--", lw=1); ax.invert_yaxis()
ax.set_xlabel("Outer loading"); ax.set_title("Final outer loadings (48 retained items; threshold 0.70)")
fig.tight_layout(); fig.savefig("figures/outer_loadings.png", dpi=200); plt.close(fig)
print("figures written")

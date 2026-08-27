import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/spotify_tracks.csv")
df = df[df["popularity"] > 0]

lo, hi = df["popularity"].quantile([0.25, 0.75])
top = df[df["popularity"] >= hi]
bottom = df[df["popularity"] <= lo]

FEATURES = ["danceability", "energy", "loudness", "valence",
            "acousticness", "speechiness", "tempo", "duration_ms"]

gap = ((top[FEATURES].mean() - bottom[FEATURES].mean())
       / df[FEATURES].std()).sort_values()

fig, ax = plt.subplots(figsize=(8, 4.5))
colors = ["#e34948" if v < 0 else "#2a78d6" for v in gap]
ax.barh(gap.index, gap.values, color=colors, height=0.6)
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_xlim(-1, 1)
ax.set_xlabel("gap between hits and ignored tracks (standard deviations)")
ax.set_title("Hits sound like misses")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("charts/01_hits_vs_misses.png", dpi=160)

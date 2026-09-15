import matplotlib.pyplot as plt

from signals import FEATURES, drop_missing_popularity, load_tracks, standardized_gap

tracks = drop_missing_popularity(load_tracks("data/spotify_tracks.csv"))
gap = standardized_gap(tracks, FEATURES).sort_values()

fig, ax = plt.subplots(figsize=(8, 4.5))
colors = ["#e34948" if v < 0 else "#2a78d6" for v in gap]
ax.barh(gap.index, gap.to_numpy(), color=colors, height=0.6)
ax.axvline(0, color="#52514e", linewidth=1)
ax.set_xlim(-1, 1)
ax.set_xlabel("gap between hits and ignored tracks (standard deviations)")
ax.set_title("Hits sound like misses")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("charts/01_hits_vs_misses.png", dpi=160)

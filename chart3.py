import pandas as pd
import matplotlib.pyplot as plt

from signals import FEATURES, drop_missing_popularity, load_tracks, standardized_gap

tracks = drop_missing_popularity(load_tracks("data/spotify_tracks.csv"))

def mean_abs_gap(tracks: pd.DataFrame) -> float:
    return standardized_gap(tracks, FEATURES).abs().mean()

by_genre = pd.Series({g: mean_abs_gap(sub)
                      for g, sub in tracks.groupby("track_genre")}).sort_values()
catalogue = mean_abs_gap(tracks)

low = by_genre.head(10)
high = by_genre.tail(10)
low_slots = list(range(0, 10))
high_slots = list(range(11, 21))

fig, ax = plt.subplots(figsize=(8, 7))
ax.barh(low_slots, low.to_numpy(), height=0.65, color="#2a78d6")
ax.barh(high_slots, high.to_numpy(), height=0.65, color="#2a78d6")
ax.set_yticks(low_slots + high_slots, list(low.index) + list(high.index))
ax.text(0.005, 10, "⋮ 94 genres in between", va="center", fontsize=9, color="#52514e")

ax.axvline(catalogue, color="#52514e", linestyle="--", linewidth=1.2)
ax.text(catalogue + 0.01, -1.1, f"whole catalogue {catalogue:.2f}",
        color="#52514e", fontsize=9)
ax.set_xlabel("average size of the hits-vs-ignored gap, across 8 audio features "
              "(standard deviations)")
ax.set_title("In some genres the sound decides. In others it says nothing.")
ax.text(0.02, -0.13, "10 highest and 10 lowest of 114 genres; 94 omitted",
        transform=ax.transAxes, fontsize=8, color="#52514e")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("charts/03_sound_matters_by_genre.png", dpi=160)

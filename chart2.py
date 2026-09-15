import pandas as pd
import matplotlib.pyplot as plt

from signals import drop_missing_popularity, load_tracks, standardized_gap

tracks = drop_missing_popularity(load_tracks("data/spotify_tracks.csv"))

GENRES = ["edm", "metal", "reggaeton", "country", "jazz", "acoustic"]

def loudness_gap(tracks: pd.DataFrame) -> float:
    return standardized_gap(tracks, ["loudness"])["loudness"]

loud = pd.Series({g: loudness_gap(tracks[tracks["track_genre"] == g])
                  for g in GENRES}).sort_values()
catalogue = loudness_gap(tracks)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(loud.index, loud.to_numpy(), height=0.6,
        color=["#e34948" if v < 0 else "#2a78d6" for v in loud])
ax.axvline(0, color="#52514e", linewidth=1)
ax.axvline(catalogue, color="#52514e", linestyle="--", linewidth=1.2)
ax.text(catalogue + 0.02, 5.35, f"catalogue average {catalogue:+.2f}",
        color="#52514e", fontsize=9, va="center")
ax.set_xlim(-0.8, 0.8)
ax.set_xlabel("loudness gap between hits and ignored tracks, within genre "
              "(standard deviations)")
ax.set_title("The catalogue average points the wrong way for half of them")
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("charts/02_loudness_by_genre.png", dpi=160)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/spotify_tracks.csv")
df = df[df["popularity"] > 0]

FEATURES = ["danceability", "energy", "loudness", "valence",
            "acousticness", "speechiness", "tempo", "duration_ms"]

def mean_abs_gap(frame):
    lo, hi = frame["popularity"].quantile([0.25, 0.75])
    top = frame[frame["popularity"] >= hi]
    bottom = frame[frame["popularity"] <= lo]
    return ((top[FEATURES].mean() - bottom[FEATURES].mean())
            / frame[FEATURES].std()).abs().mean()

by_genre = pd.Series({g: mean_abs_gap(sub)
                      for g, sub in df.groupby("track_genre")}).sort_values()
catalogue = mean_abs_gap(df)

shown = pd.concat([by_genre.head(10), by_genre.tail(10)])

fig, ax = plt.subplots(figsize=(8, 7))
ax.barh(shown.index, shown.values, height=0.65, color="#2a78d6")
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

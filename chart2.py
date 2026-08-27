import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/spotify_tracks.csv")
df = df[df["popularity"] > 0]

GENRES = ["edm", "metal", "reggaeton", "country", "jazz", "acoustic"]

def gap(frame, feature):
    lo, hi = frame["popularity"].quantile([0.25, 0.75])
    top = frame[frame["popularity"] >= hi]
    bottom = frame[frame["popularity"] <= lo]
    return (top[feature].mean() - bottom[feature].mean()) / frame[feature].std()

loud = pd.Series({g: gap(df[df["track_genre"] == g], "loudness")
                  for g in GENRES}).sort_values()
catalogue = gap(df, "loudness")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(loud.index, loud.values, height=0.6,
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

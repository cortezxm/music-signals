import pandas as pd

df = pd.read_csv("data/spotify_tracks.csv")
df = df[df["popularity"] > 0]

low, high = df["popularity"].quantile([0.25, 0.75])

print("cuts:", low, high)

top = df[df["popularity"] >= high]
bottom = df[df["popularity"] <= low]
print("top:", len(top), "bottom:", len(bottom))

FEATURES = ["danceability", "energy", "loudness", "valence",
            "acousticness", "speechiness", "tempo", "duration_ms"]

print(pd.DataFrame({"top": top[FEATURES].mean(),
                    "bottom": bottom[FEATURES].mean()}))

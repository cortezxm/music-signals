import pandas as pd

df = pd.read_csv("data/spotify_tracks.csv")
# print(df.shape)
# print(df.columns.tolist())

print(df["popularity"].describe())
print(df["popularity"].value_counts().head(10))

zeros = df[df["popularity"] == 0]
print(zeros[["artists", "track_name", "track_genre"]].sample(12, random_state=7))
print(zeros["track_genre"].value_counts().head(8))

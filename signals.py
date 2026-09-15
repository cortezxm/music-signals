import pandas as pd

FEATURES: list[str] = ["danceability", "energy", "loudness", "valence", "acousticness", "speechiness", "tempo", "duration_ms"]

def load_tracks(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def drop_missing_popularity(tracks: pd.DataFrame) -> pd.DataFrame:
    return tracks[tracks["popularity"] > 0]

def split_hits_ignored(tracks: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    low_cut, high_cut = tracks["popularity"].quantile([0.25, 0.75])
    hits = tracks[tracks["popularity"] >= high_cut]
    ignored = tracks[tracks["popularity"] <= low_cut]
    return hits, ignored

def standardized_gap(tracks: pd.DataFrame, features: list[str]) -> pd.Series:
    hits, ignored = split_hits_ignored(tracks)
    return (hits[features].mean() - ignored[features].mean()) / tracks[features].std()



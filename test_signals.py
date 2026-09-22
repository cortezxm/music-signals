import pandas as pd 
from signals import drop_missing_popularity

def test_drop_missing_popularity_removes_zero_rows():
	tracks = pd.DataFrame({"popularity": [0, 40, 0, 70]})
	result = drop_missing_popularity(tracks)
	assert list(result["popularity"]) == [40, 70]

def test_drop_missing_popularity_all_zeros_returns_empty():
	tracks = pd.DataFrame({"popularity": [0, 0, 0, 0]})
	result = drop_missing_popularity(tracks)
	assert list(result["popularity"]) == []


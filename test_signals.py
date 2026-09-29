import pandas as pd 
import pytest
from signals import drop_missing_popularity, split_hits_ignored, standardized_gap

def test_drop_missing_popularity_removes_zero_rows():
	tracks = pd.DataFrame({"popularity": [0, 40, 0, 70]})
	result = drop_missing_popularity(tracks)
	assert list(result["popularity"]) == [40, 70]

def test_drop_missing_popularity_all_zeros_returns_empty():
	tracks = pd.DataFrame({"popularity": [0, 0, 0, 0]})
	result = drop_missing_popularity(tracks)
	assert list(result["popularity"]) == []

def test_split_hits_ignored_keeps_top_and_bottom_quarters():
	tracks = pd.DataFrame({"popularity": [10, 20, 30, 40, 50, 60, 70, 80]})
	hits, ignored = split_hits_ignored(tracks)
	assert list(hits["popularity"]) == [70, 80]
	assert list(ignored["popularity"]) == [10, 20]

def test_split_hits_ignored_all_equal_lands_in_both():
	tracks = pd.DataFrame({"popularity": [50, 50, 50, 50, 50]})
	hits, ignored = split_hits_ignored(tracks)
	assert list(hits["popularity"]) == [50, 50, 50, 50, 50]
	assert list(ignored["popularity"]) == [50, 50, 50, 50, 50]

def test_standardized_gap_hits_vs_ignored_in_std_units():
	tracks = pd.DataFrame({
			"popularity": [10, 20, 30, 40, 50],
			"energy": [0, 0, 1, 2, 2],
		})
	result = standardized_gap(tracks, ["energy"])
	assert result["energy"] == pytest.approx(2.0)

def test_standardized_gap_no_spread_returns_nan():
	tracks = pd.DataFrame({
			"popularity": [10, 20, 30, 40, 50],
			"energy": [10, 10, 10, 10, 10]
		})
	result = standardized_gap(tracks, ["energy"])
	assert pd.isna(result["energy"])
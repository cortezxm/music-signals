# music-signals

> Does what a song *sounds like* decide whether it gets played?

![The catalogue average points the wrong way for half of them](charts/02_loudness_by_genre.png)

## The story

**The question.** Does what a song *sounds like* decide whether it gets played?

**What I found.** Across 98,000 tracks, almost nothing — no audio feature separates a hit
from an ignored track by even a third of a standard deviation. But that emptiness is an
artifact of averaging 114 genres together. Split them apart and real effects appear,
pointing in **opposite directions**: popular EDM and metal tracks are louder than their
peers, while popular jazz and acoustic tracks are **quieter**. The catalogue-wide figure
says "louder," and it is wrong in direction for half the genres it was computed from.

The size of the effect varies just as wildly. In hardcore the gap averages **0.69 standard
deviations**; in j-idol, **0.055**. That is a twelvefold spread around a catalogue figure of
0.13 that describes neither end of it.

**Why it matters.** "Master it louder" is the most common piece of production advice there
is, and the catalogue-wide numbers appear to support it. For a jazz or acoustic artist, this
data says the opposite. And in genres like j-idol, metal and reggaeton the audio features
carry almost no signal at all — whatever decides a hit there is not in this dataset, which
is worth knowing before spending a month chasing it in the mix.

---

## The three charts

**1 — Across the whole catalogue, hits sound like misses.**
No audio feature separates the top popularity quartile from the bottom by even a third of a
standard deviation. The axis is fixed to ±1 on purpose: auto-scaling would zoom in and make
these stubs look like skyscrapers.

![Hits sound like misses](charts/01_hits_vs_misses.png)

**2 — Loud sells in EDM and metal and costs you in jazz and acoustic**, so "master it
louder" — the advice the catalogue-wide numbers support — is backwards for half the shelf.
The dashed line is chart 1's catalogue figure, sitting on the wrong side of zero for three
of these six genres.

![The catalogue average points the wrong way for half of them](charts/02_loudness_by_genre.png)

**3 — In some genres the sound decides; in others it says nothing.**
Averaged across all eight features, the hits-vs-ignored gap runs from 0.69 standard
deviations in hardcore down to 0.055 in j-idol.

![In some genres the sound decides](charts/03_sound_matters_by_genre.png)

---

## What this analysis cannot do

Written down deliberately, because a number that is not questioned is not a finding.

- **Popularity may be measuring the metric, not the music.** Popular tracks are ~18 seconds
  shorter than ignored ones. If popularity is built on play counts, a three-minute track
  accumulates more plays per hour of listening than a five-minute one, by arithmetic alone.
  This dataset cannot separate "listeners prefer short songs" from "a play-count metric
  rewards short songs," and the second explanation is not ruled out.

- **There is no release date in this data.** Every "songs changed over time" story is
  unanswerable here, and none is claimed.

- **Chart 3's summary is crude.** Averaging the gap across eight different features mashes
  loudness, tempo and duration into one number. It is a ranking device, not a measurement.

- **Some "genres" are buckets.** `world-music`, `german` and `iranian` each hold several real
  genres under one label. If one sub-genre inside a bucket is both more popular and sonically
  distinct, the metric reads that as "sound decides" when it has actually found two genres
  wearing one name. Normalising by each genre's own spread handles the homogeneity objection;
  it does not handle this one. It is testable, and untested here.

- **16,020 tracks (14%) carry `popularity = 0`** — a sentinel for missing data, not a score.
  They include artists with hundreds of millions of plays. Dropped before any analysis.

- **Extreme-groups design.** Comparisons are top popularity quartile vs bottom quartile,
  within genre; the middle 50% is discarded. This sharpens the contrast and is disclosed
  rather than hidden. A median split was rejected because near-identical borderline tracks
  would land in opposite groups and dilute any real effect.

---

## The engineering

**Stack.** Python 3.14 · pandas 3.0 · matplotlib 3.11. No notebook — three scripts that run
top to bottom and write a PNG.

**Data.** [Spotify Tracks Dataset](https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset)
— 114,000 tracks, 114 genres, CC0. Not committed (19 MB); fetched by the command below.

**Run it.**

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt

mkdir -p data charts
curl -sSL -o data/spotify_tracks.csv \
  "https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset/resolve/main/dataset.csv"

./.venv/bin/python chart1.py
./.venv/bin/python chart2.py
./.venv/bin/python chart3.py
```

**How it's built.** Three steps, one per chart.

1. `explore.py` — profiles the raw columns. This is where the `popularity = 0` sentinel was
   found, and where the absence of a release date killed the first version of the question.
2. `analysis.py` — drops the sentinel, cuts the top and bottom popularity quartiles, and
   compares the group means across eight audio features.
3. `chart1/2/3.py` — the three figures. Each expresses its gap as a **standardized
   difference** (group gap ÷ that feature's own standard deviation), so decibels,
   milliseconds and 0-to-1 ratios can share one axis.

**Why standardized differences.** Raw means across mixed units are not comparable and will
fool you in both directions: a 0.03 gap on a 0-to-1 scale looks trivial next to 18,457
milliseconds, and both turn out to be about a sixth of a standard deviation.

**Tests.** None yet — v0 ships first. `B.2`/`B.3` extract these scripts into a typed module
with `pytest` coverage; this README will be updated in place rather than replaced.

---

## License

Code MIT. The dataset is CC0, from the source linked above.

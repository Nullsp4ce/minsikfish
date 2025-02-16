# Test Match Results

### Rating List

_Calculated with [BayesElo](https://www.remi-coulom.fr/Bayesian-Elo/)_

_Ratings are flucutating in wide range due to low number of rounds. Currently setting up new positions._

| Rank | Version                      |   Elo |          CI |
| ---- | ---------------------------- | ----: | ----------: |
|      | _Monchester 1.0 (reference)_ | _544_ |   619 ~ 480 |
| 1    | v0.5                         |   266 |   312 ~ 221 |
| 2    | v0.4                         |   221 |   266 ~ 176 |
| 3    | v0.4 -3p                     |   221 |   266 ~ 176 |
| 4    | v0.3 -1p                     |    33 |    82 ~ -18 |
| 5    | v0.2.1 -take8                |  -223 | -155 ~ -306 |

#### Feature Comparison

| Feature \ Avg. Depth |                          1 |                      3 |                      5 |
| -------------------- | -------------------------: | ---------------------: | ---------------------: |
| Random               | -223<br><small>v0.2 -take8 |                        |                        |
| Minimax              |      33<br><small>v0.3 -1p | 221<br><small>v0.4 -3p |                        |
| + Time Management    |                            |     221<br><small>v0.4 |                        |
| Alpha-Beta Pruning   |                            |                        | **266<br><small>v0.5** |

### Pentanomial

| Version                      | Mo  |    Mi     |    Mi     |     Mi     |     Mi     |     Mi     |
| ---------------------------- | :-: | :-------: | :-------: | :--------: | :--------: | :--------: |
| _Monchester 1.0 (reference)_ |  x  | 4-4-3-1-0 | 9-3-0-0-0 | 9-3-0-0-0  | 12-0-0-0-0 | 12-0-0-0-0 |
| v0.5                         |  -  |     x     | 0-4-8-0-0 | 0-5-7-0-0  | 4-3-5-0-0  | 11-1-0-0-0 |
| v0.4                         |  -  |     -     |     x     | 0-0-12-0-0 | 4-5-3-0-0  | 12-0-0-0-0 |
| v0.4 -3p                     |  -  |     -     |     -     |     x      | 5-4-3-0-0  | 12-0-0-0-0 |
| v0.3 -1p                     |  -  |     -     |     -     |     -      |     x      | 3-6-3-0-0  |
| v0.2.1 -take8                |  -  |     -     |     -     |     -      |     -      |     x      |

### LOS Matrix

LOS (_likelihood of superiority_) denotes how likely is one engine significantly strong than another engine.

| LOS, Row vs Column           |  Mo |  Mi |  Mi |  Mi |  Mi |  Mi |
| ---------------------------- | --: | --: | --: | --: | --: | --: |
| _Monchester 1.0 (reference)_ |     |  99 |  99 |  99 | 100 | 100 |
| v0.5                         |   0 |     |  90 |  90 |  99 | 100 |
| v0.4                         |   0 |   9 |     |  49 |  99 | 100 |
| v0.4 -3p                     |   0 |   9 |  50 |     |  99 | 100 |
| v0.3 -1p                     |   0 |   0 |   0 |   0 |     |  99 |
| v0.2.1 -take8                |   0 |   0 |   0 |   0 |   0 |     |

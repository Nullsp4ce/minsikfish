# Test Match Results

### Rating List

_Calculated with [BayesElo](https://www.remi-coulom.fr/Bayesian-Elo/)_

_Ratings are flucutating in wide range due to low number of rounds. Currently setting up new positions._

| Rank | Version                      | Elo   | CI          |
| ---- | ---------------------------- | ----- | ----------- |
|      | _Monchester 1.0 (reference)_ | _544_ | 650 ~ 458   |
| 1    | v0.5                         | 312   | 381 ~ 245   |
| 2    | v0.4                         | 237   | 302 ~ 172   |
| 3    | v0.4 -3p                     | 232   | 298 ~ 166   |
| 4    | v0.3 -1p                     | 0     | 75 ~ -81    |
| 5    | v0.2.1 -take8                | -269  | -166 ~ -409 |

#### Feature Comparison

| Feature \ Avg. Depth |                          1 |                      3 |                      5 |
| -------------------- | -------------------------: | ---------------------: | ---------------------: |
| Random               | -269<br><small>v0.2 -take8 |                        |                        |
| Minimax              |       0<br><small>v0.3 -1p | 232<br><small>v0.4 -3p |                        |
| + Time Management    |                            |     237<br><small>v0.4 |                        |
| Alpha-Beta Pruning   |                            |                        | **312<br><small>v0.5** |

### Pentanomial

| Version                      | Mo  |      Mi       |    Mi     |    Mi     |    Mi     |    Mi     |
| ---------------------------- | :-: | :-----------: | :-------: | :-------: | :-------: | :-------: |
| _Monchester 1.0 (reference)_ |  x  | 2-2-1-**1**-0 | 4-2-0-0-0 | 5-1-0-0-0 | 6-0-0-0-0 | 6-0-0-0-0 |
| v0.5                         |  -  |       x       | 0-3-3-0-0 | 0-4-2-0-0 | 3-2-1-0-0 | 6-0-0-0-0 |
| v0.4                         |  -  |       -       |     x     | 0-0-6-0-0 | 2-4-0-0-0 | 6-0-0-0-0 |
| v0.4 -3p                     |  -  |       -       |     -     |     x     | 3-3-0-0-0 | 6-0-0-0-0 |
| v0.3 -1p                     |  -  |       -       |     -     |     -     |     x     | 3-2-1-0-0 |
| v0.2.1 -take8                |  -  |       -       |     -     |     -     |     -     |     x     |

### LOS Matrix

LOS (_likelihood of superiority_) denotes how likely is one engine significantly strong than another engine.

| LOS, Row vs Column           |  Mo |  Mi |  Mi |  Mi |  Mi |  Mi |
| ---------------------------- | --: | --: | --: | --: | --: | --: |
| _Monchester 1.0 (reference)_ |     |  99 |  99 |  99 |  99 | 100 |
| v0.5                         |   0 |     |  93 |  94 |  99 |  99 |
| v0.4                         |   0 |   6 |     |  54 |  99 |  99 |
| v0.4 -3p                     |   0 |   5 |  45 |     |  99 |  99 |
| v0.3 -1p                     |   0 |   0 |   0 |   0 |     |  99 |
| v0.2.1 -take8                |   0 |   0 |   0 |   0 |   0 |     |

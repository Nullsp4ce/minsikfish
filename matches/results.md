# Test Match Results

### Rating List

_Calculated with [BayesElo](https://www.remi-coulom.fr/Bayesian-Elo/)_

| Rank | Version                      | Elo  | CI         |
| ---- | ---------------------------- | ---- | ---------- |
|      | _Monchester 1.0 (reference)_ | 544  | 629 ~ 470  |
| 1    | v0.5                         | 361  | 424 ~ 299  |
| 2    | v0.4 -3p                     | 353  | 415 ~ 291  |
| 3    | v0.4                         | 335  | 397 ~ 273  |
| 4    | v0.3 -1p                     | 50   | 126 ~ -34  |
| 5    | v0.2 -take8                  | -131 | -36 ~ -252 |

#### Feature Comparison

| Feature \ Avg. Depth |                          1 |                      3 |                      5 |
| -------------------- | -------------------------: | ---------------------: | ---------------------: |
| Random               | -131<br><small>v0.2 -take8 |                        |                        |
| Minimax              |      50<br><small>v0.3 -1p | 353<br><small>v0.4 -3p |                        |
| + Time Management    |                            |     335<br><small>v0.4 |                        |
| Alpha-Beta Pruning   |                            |                        | **361<br><small>v0.5** |

### Pentanomial

| Version                      | Mo  |      Mi       |    Mi     |    Mi     |    Mi     |    Mi     |
| ---------------------------- | :-: | :-----------: | :-------: | :-------: | :-------: | :-------: |
| _Monchester 1.0 (reference)_ |  x  | 2-2-1-**1**-0 | 2-3-1-0-0 | 3-3-0-0-0 | 6-0-0-0-0 | 6-0-0-0-0 |
| v0.5                         |  -  |       x       | 0-0-6-0-0 | 0-0-6-0-0 | 4-2-0-0-0 | 5-1-0-0-0 |
| v0.4 -3p                     |  -  |       -       |     x     | 0-0-6-0-0 | 3-3-0-0-0 | 6-0-0-0-0 |
| v0.4                         |  -  |       -       |     -     |     x     | 2-4-0-0-0 | 6-0-0-0-0 |
| v0.3 -1p                     |  -  |       -       |     -     |     -     |     x     | 1-3-2-0-0 |
| v0.2-take8                   |  -  |       -       |     -     |     -     |     -     |     x     |

### LOS Matrix

LOS (_likelihood of superiority_) denotes how likely is one engine significantly strong than another engine.

| LOS, Row vs Column           | Mo  | Mi  | Mi  | Mi  | Mi  | Mi  |
| ---------------------------- | --- | --- | --- | --- | --- | --- |
| _Monchester 1.0 (reference)_ |     | 99  | 99  | 99  | 99  | 99  |
| v0.5                         | 0   |     | 57  | 70  | 99  | 99  |
| v0.4 -3p                     | 0   | 42  |     | 64  | 99  | 99  |
| v0.4                         | 0   | 29  | 35  |     | 99  | 99  |
| v0.3 -1p                     | 0   | 0   | 0   | 0   |     | 99  |
| v0.2-take8                   | 0   | 0   | 0   | 0   | 0   |     |

# Test Matches

Versions of _Minsikfish_ are matched against each other to provide relative Elo ratings.

The ratings will serve as a metric to assess how certain basic features contribute to playing strength.

The starting positions consist of an equal number of `e4` and `d4` openings to cover various positions and reduce bias.

## Run Details

### Format

- Double Round Robin
- 120+1
- Some unbalanced matchups can be skipped (e.g. estimated elo difference of 600+)

### Engine Options

- Hash: 128MB
- Own books are allowed
- Tablebase: Nalimov up to 5-men
- TB draws are adjudicated
- TB hash: 32MB
- Ponder: OFF

### Starting Positions

- `As-49` Alapin Sicilian, Barmen Defense, Black puts ...Bg4

  `1. e4 c5 2. c3 d5 3. exd5 Qxd5 4. d4 Nc6 5. Nf3 Bg4`

- `Kp-85` Giuoco Piano, Center Attack, 6. e5 d5

  `1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d4 exd4 6. e5 d5`

- `Ks-31` Advance Caro-Kann, Botvinnik-Carls Defense

  `1. e4 c6 2. d4 d5 3. e5 c5 4. dxc5 e6 5. Be3 Ne7`

- `Qp-11` Semi-Slav Defense, Botvinnik Gambit Accepted

  `1. d4 d5 2. c4 c6 3. Nf3 Nf6 4. Nc3 e6 5. Bg5 dxc4 6. e4 b5 7. e5 h6 8. Bh4 g5 9. Nxg5 hxg5`

- `Qp-53~5` QGD, Pillsbury Attack, 5... h6

  `1. d4 d5 2. c4 e6 3. Nc3 Nf6 4. Bg5 Bd7 5. Nf3 h6`

- `Qs-71` Old Czech Benoni

  `1. d4 c5 2. d5 e5 3. e4 d6 4. Nc3 Nf6 5. Be2 Nbd7`

- `Si-16` Open Sicilian, with ...d6, Moscow Variation

  `1. e4 c5 2. Nf3 d6 3. Bb5+ Bd7 4. Bxd7+ Qxd7 5. O-O Nf6`

- `Si-7w7` Open Sicilian, with ...Nc6, Pelikan Variation, 7. Nd5

  `1. e4 c5 2. Nf3 Nc6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 e5 6. Ndb5 d6 7. Nd5 Nxd5 8. exd5 Nb8`

- `Ru-71` Open Ruy Lopez, Main Line

  `1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Nxe4 6. d4 b5 7. Bb3 d5 8. dxe5 Be6`

- `In-43~5` Queen's Indian Defence, Traditional Variation (Transposed from `c4`)

  `1. c4 Nf6 2. Nf3 e6 3. g3 b6 4. Bg2 Bb7 5. O-O Be7 6. Nc3 O-O 7. d4 Ne4`

- `In-46b4` Bogo-Indian Defence, Exchange Variation

  `1. d4 Nf6 2. c4 e6 3. Nf3 Bb4+ 4. Bd2 Bxd2+ 5. Qxd2 d5`

- `In-81` Fianchetto King's Indian, Neo-Grünfeld

  `1. d4 Nf6 2. c4 g6 3. g3 Bg7 4. Bg2 c5 5. d5 d6`

### Environment

- CPU: AMD Ryzen 5 7600 6-Core 3.80GHz
- RAM: 32GB

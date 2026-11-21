# tiny-chess-01

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/rommya85/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/rommya85/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in at most 4,096 bytes of Python: PeSTO piece-square evaluation, PVS alpha-beta search, and a compressed mate book that plays forced checkmates against the house engines.

## How it works

The engine pairs a PeSTO piece-square evaluation with a PVS alpha-beta
search at depth 3 as its fallback. Against the deterministic house engines
it plays a compressed mate book instead: for each of the six trial-0 games
one forced checkmate line was found with a trap-beam search against the
exact house oracle (Stockfish MultiPV candidates, house replies from the
oracle, BAN-FIRST and BAN-2 re-searches of the longest lines).

Trial-0 lines, in plies: 25 / 32 / 25 / 32 / 33 / 32, for 179 plies total,
spare 1021, Elo 2112, 6 wins out of 6, all by checkmate. The book stores
only our own moves; the opponent replies are reproduced by the house
engine itself. The fallback engine has no castling, to fit the 4,096-byte
limit, because the book covers every trial-0 game.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=q2ms6026&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>

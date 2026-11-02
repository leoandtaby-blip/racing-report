# Racing results report

A small Python tool that automates a racing results report.

Every morning, someone on a trading team looks through the results by hand: who won, at what price, did the favourites win, were there any shocks? This tool does that job automatically.

## What it does

You give it a start date and an end date. It then:

1. pulls every race and its winner from a SQLite database, using SQL joins across races, results, horses, jockeys, trainers and courses
2. shows each winner's price, jockey and trainer
3. works out how many favourites won (the favourite is the shortest-priced runner in each race)
4. flags big-priced winners (10.0 or bigger), the shocks a trader would want to know about
5. saves the report as a text file in a `reports` folder

It also handles mistakes, like a date range with no races, without crashing.

## How to run it

You need Python 3. No extra packages are needed.

```
python daily_report.py
```

Then type the dates when it asks:

```
Start date? (e.g. 2026-01-01): 2026-01-01
End date?   (e.g. 2026-01-31): 2026-01-31
```

## Example summary

```
SUMMARY
Races: 10
Favourites won: 4 (40%)
Big-priced winners (10.0 or bigger):
  Duke Of Dorset at 23.1 (Aintree, 2026-01-03)
  Iron Duke at 10.8 (Newmarket, 2026-01-21)
```

## The data

`racing.db` is a made-up practice database of 80 races and 708 runners, built for learning SQL. It is not real racing data.

## Ideas for next steps

- Run it automatically every morning and email the report
- Read real results from a racing data API
- Show strike rates by jockey, trainer, course and going

# Going report
# Type a horse's name to see how it runs on each type of going.

import sqlite3
from pathlib import Path

# Find racing.db next to this script, wherever it's run from
DB_PATH = Path(__file__).parent / "racing.db"

# Fastest ground first, softest last
GOING_ORDER = ["Firm", "Good to Firm", "Good", "Good to Soft", "Soft", "Heavy"]

conn = sqlite3.connect(DB_PATH)

name = input("Which horse? ").strip()

# Match the name whatever capital letters are typed
horse = conn.execute(
    "SELECT horse_id, name FROM horses WHERE LOWER(name) = LOWER(?)", (name,)
).fetchone()

if horse is None:
    print(f"No horse called '{name}' found. Horses in the database:")
    for (horse_name,) in conn.execute("SELECT name FROM horses ORDER BY name"):
        print(f"  {horse_name}")
    raise SystemExit

horse_id, horse_name = horse

rows = conn.execute("""
    SELECT races.going,
           COUNT(*) AS runs,
           SUM(CASE WHEN results.position = 1 THEN 1 ELSE 0 END) AS wins,
           ROUND(AVG(results.position), 1) AS avg_position,
           SUM(CASE WHEN results.position IS NULL THEN 1 ELSE 0 END) AS non_finishes
    FROM results
    JOIN races ON results.race_id = races.race_id
    WHERE results.horse_id = ?
    GROUP BY races.going
""", (horse_id,)).fetchall()

by_going = {row[0]: row[1:] for row in rows}

print()
print(f"{horse_name}: record by going")
print(f"{'Going':<14}{'Runs':>5}{'Wins':>6}{'Win %':>7}{'Avg pos':>9}{'DNF':>5}")
for going in GOING_ORDER:
    if going not in by_going:
        continue
    runs, wins, avg_position, non_finishes = by_going[going]
    avg_text = avg_position if avg_position is not None else "-"
    print(f"{going:<14}{runs:>5}{wins:>6}{wins / runs:>7.0%}{avg_text:>9}{non_finishes:>5}")

print()
print("Avg pos = average finishing position. DNF = did not finish (fell, pulled up, unseated).")

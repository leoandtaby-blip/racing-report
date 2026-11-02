# Racing results report
# Step 5: ask for a date range, show each race's winner and a summary,
# then save the report to a file.

import sqlite3
from pathlib import Path

# Find racing.db next to this script, wherever it's run from
DB_PATH = Path(__file__).parent / "racing.db"

# A winner at this price or bigger counts as a shock
BIG_PRICE = 10.0

START_DATE = input("Start date? (e.g. 2026-01-01): ")
END_DATE = input("End date?   (e.g. 2026-01-31): ")

conn = sqlite3.connect(DB_PATH)

# Every line of the report is kept here, so we can save it at the end
report_lines = []


def report(line=""):
    """Show a line on screen and keep it for the saved report."""
    print(line)
    report_lines.append(line)


races = conn.execute("""
    SELECT races.race_id, races.race_date, courses.name, races.race_name, races.going
    FROM races
    JOIN courses ON races.course_id = courses.course_id
    WHERE races.race_date BETWEEN ? AND ?
    ORDER BY races.race_date
""", (START_DATE, END_DATE)).fetchall()

if not races:
    print(f"No races found between {START_DATE} and {END_DATE}.")
    raise SystemExit

favourites_won = 0
shocks = []

report(f"Results from {START_DATE} to {END_DATE}")
for race_id, race_date, course, race_name, going in races:
    report()
    report(f"{race_date}  {course}: {race_name} ({going})")

    winner = conn.execute("""
        SELECT horses.name, results.sp_decimal, jockeys.name, trainers.name
        FROM results
        JOIN horses ON results.horse_id = horses.horse_id
        JOIN jockeys ON results.jockey_id = jockeys.jockey_id
        JOIN trainers ON horses.trainer_id = trainers.trainer_id
        WHERE results.race_id = ? AND results.position = 1
    """, (race_id,)).fetchone()

    if winner is None:
        report("  No winner recorded.")
        continue

    horse, sp, jockey, trainer = winner
    report(f"  Winner: {horse} at {sp}")
    report(f"  Jockey: {jockey}   Trainer: {trainer}")

    # The favourite is the runner with the shortest price in the race
    fav_price = conn.execute(
        "SELECT MIN(sp_decimal) FROM results WHERE race_id = ?", (race_id,)
    ).fetchone()[0]

    if sp == fav_price:
        favourites_won += 1
        report("  The favourite won.")

    if sp >= BIG_PRICE:
        shocks.append(f"{horse} at {sp} ({course}, {race_date})")

report()
report("=" * 40)
report("SUMMARY")
report(f"Races: {len(races)}")
report(f"Favourites won: {favourites_won} ({favourites_won / len(races):.0%})")
if shocks:
    report(f"Big-priced winners ({BIG_PRICE} or bigger):")
    for shock in shocks:
        report(f"  {shock}")
else:
    report("No big-priced winners.")

# Save the report in a "reports" folder next to this script
reports_folder = Path(__file__).parent / "reports"
reports_folder.mkdir(exist_ok=True)
report_file = reports_folder / f"report_{START_DATE}_to_{END_DATE}.txt"
report_file.write_text("\n".join(report_lines), encoding="utf-8")
print()
print(f"Report saved to {report_file}")

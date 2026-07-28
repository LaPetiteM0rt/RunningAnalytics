import json
from setup_database import setup_database
from sqlalchemy.dialects.postgresql import insert as pg_insert

def populate_database():
    engine, run_table = setup_database()

    with open("data/processed/runs.json", "r") as file:
        runs = json.load(file)

    print(f"Loaded {len(runs)} runs, inserting...")

    with engine.connect() as connection:
        for run in runs:
            insert_stmt = pg_insert(run_table).values(
                id=run["id"],
                start_date=run["start_date"],
                distance=run["distance"],
                duration=run["duration"],
                total_elevation_gain=run.get("total_elevation_gain"),
                average_speed=run["average_speed"],
                max_speed=run["max_speed"],
                average_watts=run.get("average_watts"),
                max_watts=run.get("max_watts"),
                weighted_average_watts=run.get("weighted_average_watts"),
                kilojoules=run.get("kilojoules"),
                average_heartrate=run.get("average_heartrate"),
                max_heartrate=run.get("max_heartrate"),
                elev_high=run.get("elev_high"),
                elev_low=run.get("elev_low"),
                suffer_score=run.get("suffer_score"),
            )
            insert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["id"])
            connection.execute(insert_stmt)

        print("About to commit")
        connection.commit()
import json

def process_raw_data(file_path):
    with open(file_path, 'r') as raw_file, open("data/processed/runs.json", 'w') as processed_file:
        raw_data = json.load(raw_file)
        processed = [transform_runs(activity) for activity in raw_data]
        json.dump(processed, processed_file, indent=2)

def transform_runs(runs):
    return {"id": runs["id"],
            "distance": runs["distance"],
            "duration": runs["moving_time"],
            "total_elevation_gain": runs.get("total_elevation_gain"),
            "start_date": runs["start_date"],
            "average_speed": runs["average_speed"],
            "max_speed": runs["max_speed"],
            "average_watts": runs.get("average_watts"),
            "max_watts": runs.get("max_watts"),
            "weighted_average_watts": runs.get("weighted_average_watts"),
            "kilojoules": runs.get("kilojoules"),
            "average_heartrate": runs.get("average_heartrate"),
            "max_heartrate": runs.get("max_heartrate"),
            "elev_high": runs.get("elev_high"),
            "elev_low": runs.get("elev_low"),
            "suffer_score": runs.get("suffer_score"),
            }

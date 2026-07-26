import json

def process_raw_data(file_path):
    with open(file_path, 'r') as raw_file, open("data/processed/activities.json", 'w') as processed_file:
        raw_data = json.load(raw_file)
        processed = [transform_activity(activity) for activity in raw_data]
        json.dump(processed, processed_file, indent=2)

def transform_activity(activity):
    return {"run_id": activity["id"],
            "distance": activity["distance"],
            "duration": activity["moving_time"],
            "total_elevation_gain": activity.get("total_elevation_gain"),
            "start_date": activity["start_date"],
            "average_speed": activity["average_speed"],
            "max_speed": activity["max_speed"],
            "average_watts": activity.get("average_watts"),
            "max_watts": activity.get("max_watts"),
            "weighted_average_watts": activity.get("weighted_average_watts"),
            "kilojoules": activity.get("kilojoules"),
            "average_heartrate": activity.get("average_heartrate"),
            "max_heartrate": activity.get("max_heartrate"),
            "elev_high": activity.get("elev_high"),
            "elev_low": activity.get("elev_low"),
            "suffer_score": activity.get("suffer_score"),
            }

process_raw_data("data/raw/activities.json")
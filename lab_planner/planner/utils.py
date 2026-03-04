from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician
from lab_planner.models.equipment import Equipment
from pathlib import Path
from datetime import datetime, timedelta
import json

fmt = "%H:%M"


def load_data_as_objects(file: str):
    path = Path(__file__).parent.parent / "data" / file
    with open(path, "r") as f:
        data = json.load(f)
    samples = [
        Sample(
            id=s["id"],
            type=s["type"],
            priority=s["priority"],
            analysisTime=s["analysisTime"],
            arrivalTime=s["arrivalTime"],
            patientId=s["patientId"],
        )
        for s in data.get("samples", [])
    ]
    technicians = [
        Technician(
            id=t["id"],
            name=t.get("name", ""),
            speciality=t["speciality"],
            startTime=t["startTime"],
            endTime=t["endTime"],
        )
        for t in data.get("technicians", [])
    ]
    equipments = [
        Equipment(
            id=e["id"], name=e.get("name", ""), type=e["type"], available=e["available"]
        )
        for e in data.get("equipment", [])
    ]

    return {"samples": samples, "technicians": technicians, "equipment": equipments}


def latest_time(time1: str, time2: str) -> str:
    t1 = datetime.strptime(time1, fmt).time()
    t2 = datetime.strptime(time2, fmt).time()
    return max(t1, t2).strftime(fmt)


def earliest_time(time1: str, time2: str) -> str:
    t1 = datetime.strptime(time1, fmt).time()
    t2 = datetime.strptime(time2, fmt).time()
    return min(t1, t2).strftime(fmt)


def minutes_between(start_time: str, end_time: str) -> int:
    t1 = datetime.strptime(start_time, fmt)
    t2 = datetime.strptime(end_time, fmt)
    delta = t2 - t1
    return int(delta.total_seconds() / 60)


def add_minutes(time_str: str, minutes: int) -> str:
    t = datetime.strptime(time_str, fmt)
    t += timedelta(minutes=minutes)
    return t.strftime(fmt)


def get_full_time(schedule) -> int:
    if len(schedule) == 0:
        return 0
    start = schedule[0]["startTime"]
    end = schedule[0]["endTime"]
    for state in schedule:
        start = earliest_time(start, state["startTime"])
        end = latest_time(end, state["endTime"])
    return minutes_between(start, end)

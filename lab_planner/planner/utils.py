from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician
from lab_planner.models.equipment import Equipment
from pathlib import Path
import json


def load_data_as_objects(file: str):
    path = Path(__file__).parent.parent / "data" / file
    with open(path, "r") as f:
        data = json.load(f)
    samples = [
        Sample(
            id=sample["id"],
            type=sample["type"],
            priority=sample["priority"],
            analysisTime=sample["analysisTime"],
            arrivalTime=sample["arrivalTime"],
            patientId=sample.get("patientId", sample["id"]),
            analysisType=sample.get("analysisType", ""),
        )
        for sample in data.get("samples", [])
    ]
    technicians = [
        Technician(
            id=technician["id"],
            name=technician.get("name", ""),
            speciality=technician.get("speciality")
            or technician.get("specialty")
            or "",
            startTime=technician["startTime"],
            endTime=technician["endTime"],
            efficiency=technician.get("efficiency", 1.0),
        )
        for technician in data.get("technicians", [])
    ]
    equipments = [
        Equipment(
            id=equipement["id"],
            name=equipement.get("name", ""),
            type=equipement["type"],
            available=equipement.get("available", True),
            capacity=equipement.get("capacity", 1),
            cleaningTime=equipement.get("cleaningTime", 1),
        )
        for equipement in data.get("equipment", [])
    ]

    return dict(samples=samples, technicians=technicians, equipment=equipments)


def latest_time(time1: str, time2: str) -> str:
    return max(time1, time2)


def earliest_time(time1: str, time2: str) -> str:
    return min(time1, time2)


def to_minutes(time_str: str) -> int:
    h, m = map(int, time_str.split(":"))
    return h * 60 + m


def to_time_str(total_minutes: int) -> str:
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h:02d}:{m:02d}"


def minutes_between(start_time: str, end_time: str) -> int:
    return to_minutes(end_time) - to_minutes(start_time)


def add_minutes(time_str: str, minutes: int) -> str:
    return to_time_str(to_minutes(time_str) + minutes)


def get_full_time(schedule) -> int:
    if len(schedule) == 0:
        return 0
    start = schedule[0]["startTime"]
    end = schedule[0]["endTime"]
    for state in schedule:
        start = earliest_time(start, state["startTime"])
        end = latest_time(end, state["endTime"])
    return minutes_between(start, end)

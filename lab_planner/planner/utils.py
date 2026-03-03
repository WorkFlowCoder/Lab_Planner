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
    #(self, id: str, type: str, priority: str, analysisTime: int, arrivalTime: str, patientId: str)
    samples = [Sample(
        id=s["id"],
        type=s["type"],
        priority=s["priority"],
        analysisTime=s["analysisTime"],
        arrivalTime=s["arrivalTime"],
        patientId=s["patientId"]
        ) for s in data.get("samples", [])
    ]
    #(self, id: str, name: str, speciality: str, startTime: str, endTime: str)
    technicians = [Technician(
        id=t["id"],
        name=t.get("name",""),
        speciality=t["speciality"],
        startTime=t["startTime"],
        endTime=t["endTime"]
        ) for t in data.get("technicians", [])
    ]
    #(self, id: str, name: str, type: str, available: bool)
    equipments = [Equipment(
        id=e["id"],
        name=e.get("name",""),
        type=e["type"],
        available=e["available"]
        ) for e in data.get("equipment", [])
    ]

    return {
        "samples": samples, 
        "technicians": technicians,
        "equipment": equipments
    }

def sort_samples_by_priority(samples: list) -> list:
    # Séparation en fonction de l'urgence
    stat_samples = [s for s in samples if s.get_priority() == "STAT"]
    urgent_samples = [s for s in samples if s.get_priority() == "URGENT"]
    routine_samples = [s for s in samples if s.get_priority() == "ROUTINE"]
    ## Phase de rangement des liste en fonction de l'heure d'arrvée pour plus tard
    # Concaténation de sortie par ordre d'importande
    return stat_samples + urgent_samples + routine_samples

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

def get_full_time(schedule: list) -> int:
    if len(schedule)==0:
        return 0
    start = schedule[0]["startTime"]
    end = schedule[0]["endTime"]
    sum=0
    for state in schedule:
        start = earliest_time(start,state["startTime"])
        end = latest_time(end,state["endTime"])
    print(start)
    print(end)
    print(minutes_between(start,end))
    return minutes_between(start,end)

def has_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    return start1 < end2 and start2 < end1

def calculate_conflicts(schedule: list) -> int:
    conflicts = 0
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            s1 = schedule[i]
            s2 = schedule[j]
            # Recherche d'un conflit
            if s1["technicianId"] == s2["technicianId"]:
                if has_overlap(s1["startTime"], s1["endTime"],
                               s2["startTime"], s2["endTime"]):
                    # Même technicien sur la même période
                    conflicts += 1
            if s1["equipmentId"] == s2["equipmentId"]:
                if has_overlap(s1["startTime"], s1["endTime"],
                               s2["startTime"], s2["endTime"]):
                    # Même equipement sur la même période
                    conflicts += 1
    return conflicts

def get_technician_available_time(schedule: list, technician_id: str, default_start: str) -> str:
    end_times = [
        s["endTime"]
        for s in schedule
        if s["technicianId"] == technician_id
    ]

    if not end_times:
        return default_start

    return max(end_times)

def get_equipment_available_time(schedule: list, equipment_id: str, default_start: str) -> str:
    end_times = [
        s["endTime"]
        for s in schedule
        if s["equipmentId"] == equipment_id
    ]
    if not end_times:
        return default_start
    return max(end_times)
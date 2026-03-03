from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician
from lab_planner.models.equipment import Equipment
from pathlib import Path
import json

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
    stat_samples = [s for s in samples if s.get_priority() == "STAT"]
    urgent_samples = [s for s in samples if s.get_priority() == "URGENT"]
    routine_samples = [s for s in samples if s.get_priority() == "ROUTINE"]
    # Phase de rangement des liste en fonction de l'heure d'arrvée pour plus tard
    # Concaténation de sortie
    return stat_samples + urgent_samples + routine_samples    
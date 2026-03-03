from lab_planner.planner.utils import sort_samples_by_priority
from lab_planner.planner.utils import latest_time
from lab_planner.planner.utils import add_minutes
from lab_planner.planner.utils import get_full_time
from lab_planner.planner.utils import calculate_conflicts
from lab_planner.planner.utils import get_technician_available_time
from lab_planner.planner.utils import get_equipment_available_time

def planify_lab(data) -> dict:
    # Triage des samples
    sorted_samples = sort_samples_by_priority(data["samples"])
    schedule = []
    for s in sorted_samples:
        # Recherche des ressources
        technician = [t for t in data["technicians"] if (t.get_speciality() == s.get_type() or  t.get_speciality() == "GENERAL")]
        ### Meilleur triage des techniciens à venir
        equipement = [e for e in data["equipment"] if (e.get_type() == s.get_type() and e.get_available())]
        ### Meilleur triage des équipements ?

        # Prendre un créneau avec le premier qui arrive
        s.technician_id = technician[0].get_id()
        horaire_commun = latest_time(s.get_arrivalTime(),technician[0].get_startTime())
        start_for_technicien = get_technician_available_time(schedule,s.technician_id,horaire_commun)
        s.equipment_id = equipement[0].get_id()
        start_moment = get_equipment_available_time(schedule,s.equipment_id,start_for_technicien)
        s.start_time = start_moment
        s.end_time = add_minutes(s.start_time,s.analysisTime)

        schedule.append({
            "sampleId": s.id,
            "technicianId": s.technician_id,
            "equipmentId": s.equipment_id,
            "startTime": s.start_time,
            "endTime": s.end_time,
            "priority": s.priority
        })
    sum_of_time = sum(s.get_analysisTime() for s in sorted_samples)
    full_time = get_full_time(schedule)
    metrics = {
        "total_time": full_time,
        "efficiency": round((sum_of_time/full_time)*100,1),
        "conflicts": calculate_conflicts(schedule)
    }
    res = {
        "schedule": schedule,
        "metrics": metrics
    }
    print(res)
    return res
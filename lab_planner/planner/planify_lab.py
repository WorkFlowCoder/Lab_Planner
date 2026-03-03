from lab_planner.planner.utils import sort_samples_by_priority

def planify_lab(data) -> dict:
    # Triage des samples
    sorted_samples = sort_samples_by_priority(data["samples"])
    for s in sorted_samples:
        print(s.to_string())
    metrics = {
        "total_time": sum(s.get_analysisTime() for s in sorted_samples),
        "efficiency": 0,
        "conflicts": 0
    }
    return {
        "schedule": [],
        "metrics": metrics
    }
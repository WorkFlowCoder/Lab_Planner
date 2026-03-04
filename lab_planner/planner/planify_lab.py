from lab_planner.models.metrics import Metrics
from lab_planner.models.scheduler import Scheduler


def planify_lab(data) -> dict:
    samples = data["samples"]
    technicians = data["technicians"]
    equipements = data["equipment"]
    scheduler = Scheduler(samples, technicians, equipements)
    scheduler.planify()
    metrics = Metrics(scheduler)
    metrics.compute()
    schedule = scheduler.get_schedule()
    metric = metrics.get_metrics()
    result = {"schedule": schedule, "metrics": metric}
    # print(result)
    return result

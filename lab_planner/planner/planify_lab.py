from lab_planner.models.metrics import Metrics
from lab_planner.models.scheduler import Scheduler


def planify_lab(data) -> dict:
    scheduler = Scheduler(data["samples"], data["technicians"], data["equipment"])
    scheduler.planify()
    metrics = Metrics(scheduler)
    metrics.compute()
    res = {"schedule": scheduler.get_schedule(), "metrics": metrics.get_metrics()}
    # print(res)
    return res

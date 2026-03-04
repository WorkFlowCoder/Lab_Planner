from lab_planner.planner.utils import get_full_time
from lab_planner.planner.utils import minutes_between


class Metrics:
    def __init__(self, schedule):
        self.schedule = schedule
        self.total_time = 0
        self.efficiency = 0.0
        self.conflicts = 0
        self.averageWaitTimeSTAT = 0.0
        self.averageWaitTimeURGENT = 0.0
        self.averageWaitTimeROUTINE = 0.0

    def compute(self):
        self.compute_total_time()
        self.compute_efficiency()
        self.compute_conflicts()
        self.compute_averageWaitTime()

    def compute_averageWaitTime(self):
        self.averageWaitTimeSTAT = self.compute_average_type("STAT")
        self.averageWaitTimeURGENT = self.compute_average_type("URGENT")
        self.averageWaitTimeROUTINE = self.compute_average_type("ROUTINE")

    def compute_average_type(self, type: str) -> float:
        samples = self.schedule.get_samples()
        average = 0.0
        samples_type = list(filter(lambda s: s.get_priority() == type, samples))
        if len(samples_type) == 0:
            return average
        for sample in samples_type:
            average += minutes_between(sample.arrivalTime, sample.start_time)
        average /= len(samples_type)
        return average

    def compute_total_time(self):
        self.total_time = get_full_time(self.schedule.get_schedule())

    def compute_efficiency(self):
        samples = self.schedule.get_samples()
        sum_of_time = sum(s.get_analysisTime() for s in samples)
        self.efficiency = round((sum_of_time / self.total_time) * 100, 1)

    def compute_conflicts(self):
        conflicts = 0
        schedule_res = self.schedule.get_schedule()
        for i in range(len(schedule_res)):
            for j in range(i + 1, len(schedule_res)):
                s1 = schedule_res[i]
                s2 = schedule_res[j]
                overlap = (s1["startTime"] < s2["endTime"]) and (
                    s2["startTime"] < s1["endTime"]
                )
                # Recherche d'un conflit
                if s1["technicianId"] == s2["technicianId"] and overlap:
                    # Même technicien sur la même période
                    conflicts += 1
                if s1["equipmentId"] == s2["equipmentId"] and overlap:
                    # Même equipement sur la même période
                    conflicts += 1
        self.conflicts = conflicts

    def get_metrics(self):
        return {
            "total_time": self.total_time,
            "efficiency": self.efficiency,
            "conflicts": self.conflicts,
            "averageWaitTime": {
                "STAT": self.averageWaitTimeSTAT,
                "URNGET": self.averageWaitTimeURGENT,
                "ROUTINE": self.averageWaitTimeROUTINE,
            },
        }

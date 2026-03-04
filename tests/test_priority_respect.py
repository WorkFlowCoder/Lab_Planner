import unittest

from lab_planner.planner.planify_lab import planify_lab
from lab_planner.planner.utils import load_data_as_objects
from lab_planner.models.sample import Sample
from lab_planner.models.scheduler import Scheduler


class TestBasicSheduling(unittest.TestCase):
    def statBeforeUrgent(self):
        path = "example_2.json"
        data = load_data_as_objects(path)
        result = planify_lab(data)
        schedule = result["schedule"]
        self.assertEqual(schedule[0]["sampleId"], "S002")
        self.assertEqual(schedule[0]["priority"], "STAT")

        self.assertEqual(schedule[1]["sampleId"], "S001")
        self.assertEqual(schedule[1]["priority"], "URGENT")

        metrics = result["metrics"]
        # 09:30 à 10:45 = 1h15 = 75 minutes
        self.assertEqual(metrics["total_time"], 75)
        # 00:30 + 00:45 = 1h15 = 75 minutes
        # 75/75*100 = 100.0
        self.assertEqual(metrics["efficiency"], 100.0)
        self.assertEqual(metrics["conflicts"], 0)

    def test_sort_samples_by_priority(self):
        s1 = Sample("S1", "BLOOD", "ROUTINE", 30, "08:00", "P1")
        s2 = Sample("S2", "URINE", "STAT", 20, "08:10", "P2")
        s3 = Sample("S3", "BLOOD", "URGENT", 15, "08:20", "P3")
        scheduler = Scheduler([s1, s2, s3], [], [])
        scheduler.sort_samples_by_priority()
        self.assertEqual([s.id for s in scheduler.samples], ["S2", "S3", "S1"])

    def test_sort_samples_by_priority_2(self):
        s1 = Sample("S1", "BLOOD", "STAT", 30, "08:30", "P1")
        s2 = Sample("S2", "URINE", "STAT", 20, "08:10", "P2")
        s3 = Sample("S3", "BLOOD", "URGENT", 15, "08:20", "P3")
        scheduler = Scheduler([s1, s2, s3], [], [])
        scheduler.sort_samples_by_priority()
        self.assertEqual([s.id for s in scheduler.samples], ["S2", "S1", "S3"])

    def test_sort_samples_by_priority_3(self):
        s1 = Sample("S1", "BLOOD", "STAT", 30, "10:30", "P1")
        s2 = Sample("S2", "URINE", "STAT", 20, "08:30", "P2")
        s3 = Sample("S3", "BLOOD", "STAT", 15, "08:00", "P3")
        scheduler = Scheduler([s1, s2, s3], [], [])
        scheduler.sort_samples_by_priority()
        self.assertEqual([s.id for s in scheduler.samples], ["S3", "S2", "S1"])

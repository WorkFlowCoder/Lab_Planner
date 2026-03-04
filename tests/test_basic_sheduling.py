import unittest

from lab_planner.planner.planify_lab import planify_lab
from lab_planner.planner.utils import load_data_as_objects
from lab_planner.models.scheduler import Scheduler
from lab_planner.models.metrics import Metrics
from lab_planner.models.sample import Sample
from lab_planner.models.equipment import Equipment


class TestBasicSheduling(unittest.TestCase):

    def test_simple_example(self):
        path = "example.json"
        data = load_data_as_objects(path)
        result = planify_lab(data)
        schedule = result["schedule"]
        self.assertEqual(schedule[0]["sampleId"], "S001")
        self.assertEqual(schedule[0]["technicianId"], "T001")
        self.assertEqual(schedule[0]["equipmentId"], "E001")
        self.assertEqual(schedule[0]["startTime"], "09:00")
        self.assertEqual(schedule[0]["endTime"], "09:30")
        metrics = result["metrics"]
        self.assertEqual(metrics["total_time"], 30)
        self.assertEqual(metrics["efficiency"], 100.0)
        self.assertEqual(metrics["conflicts"], 0)

    def test_second_simple_example(self):
        path = "example_2.json"
        data = load_data_as_objects(path)
        result = planify_lab(data)
        schedule = result["schedule"]
        self.assertEqual(schedule[0]["sampleId"], "S002")
        self.assertEqual(schedule[0]["technicianId"], "T001")
        self.assertEqual(schedule[0]["equipmentId"], "E001")
        self.assertEqual(schedule[0]["startTime"], "09:30")
        self.assertEqual(schedule[0]["endTime"], "10:00")
        self.assertEqual(schedule[0]["priority"], "STAT")

        self.assertEqual(schedule[1]["sampleId"], "S001")
        self.assertEqual(schedule[1]["technicianId"], "T001")
        self.assertEqual(schedule[1]["equipmentId"], "E001")
        self.assertEqual(schedule[1]["startTime"], "10:00")
        self.assertEqual(schedule[1]["endTime"], "10:45")
        self.assertEqual(schedule[1]["priority"], "URGENT")

        metrics = result["metrics"]
        # 09:30 à 10:45 = 1h15 = 75 minutes
        self.assertEqual(metrics["total_time"], 75)
        # 00:30 + 00:45 = 1h15 = 75 minutes
        # 75/75*100 = 100.0
        self.assertEqual(metrics["efficiency"], 100.0)
        self.assertEqual(metrics["conflicts"], 0)

    def test_third_simple_example(self):
        path = "example_3.json"
        data = load_data_as_objects(path)
        result = planify_lab(data)
        schedule = result["schedule"]
        self.assertEqual(schedule[0]["sampleId"], "S001")
        self.assertEqual(schedule[0]["technicianId"], "T001")
        self.assertEqual(schedule[0]["equipmentId"], "E001")
        self.assertEqual(schedule[0]["startTime"], "09:00")
        self.assertEqual(schedule[0]["endTime"], "10:00")
        self.assertEqual(schedule[0]["priority"], "URGENT")

        self.assertEqual(schedule[1]["sampleId"], "S002")
        self.assertEqual(schedule[1]["technicianId"], "T002")
        self.assertEqual(schedule[1]["equipmentId"], "E002")
        self.assertEqual(schedule[1]["startTime"], "09:15")
        self.assertEqual(schedule[1]["endTime"], "09:45")
        self.assertEqual(schedule[1]["priority"], "URGENT")

        self.assertEqual(schedule[2]["sampleId"], "S003")
        self.assertEqual(schedule[2]["technicianId"], "T001")
        self.assertEqual(schedule[2]["equipmentId"], "E001")
        self.assertEqual(schedule[2]["startTime"], "10:00")
        self.assertEqual(schedule[2]["endTime"], "10:45")
        self.assertEqual(schedule[2]["priority"], "ROUTINE")

        metrics = result["metrics"]
        # 09:00 à 10:45 = 1h45 = 105 minutes
        self.assertEqual(metrics["total_time"], 105)
        # 01:00 + 00:30 + 00:45 = 2h15 = 135 minutes
        # 135/105*100 = 128.6
        self.assertEqual(metrics["efficiency"], 128.6)
        self.assertEqual(metrics["conflicts"], 0)

    def test_calculate_conflicts(self):
        s1 = Sample("S1", "BLOOD", "ROUTINE", 30, "08:00", "P1")
        s2 = Sample("S2", "URINE", "STAT", 20, "08:10", "P2")
        s3 = Sample("S3", "BLOOD", "URGENT", 15, "08:20", "P3")
        sheduler = Scheduler([s1, s2, s3], [], [])
        sheduler.set_schedule(
            [
                {
                    "technicianId": "T1",
                    "equipmentId": "E1",
                    "startTime": "09:00",
                    "endTime": "10:00",
                },
                {
                    "technicianId": "T1",
                    "equipmentId": "E2",
                    "startTime": "09:30",
                    "endTime": "10:30",
                },  # conflict
                {
                    "technicianId": "T2",
                    "equipmentId": "E1",
                    "startTime": "09:45",
                    "endTime": "10:15",
                },  # conflict
            ]
        )
        metric = Metrics(sheduler)
        metric.compute()
        assert metric.conflicts == 2

    def test_calculate_conflicts_2(self):
        s1 = Sample("S1", "BLOOD", "ROUTINE", 30, "08:00", "P1")
        s2 = Sample("S2", "URINE", "STAT", 20, "08:10", "P2")
        s3 = Sample("S3", "BLOOD", "URGENT", 15, "08:20", "P3")
        sheduler = Scheduler([s1, s2, s3], [], [])
        sheduler.set_schedule(
            [
                {
                    "technicianId": "T1",
                    "equipmentId": "E1",
                    "startTime": "09:00",
                    "endTime": "10:00",
                },
                {
                    "technicianId": "T1",
                    "equipmentId": "E2",
                    "startTime": "10:00",
                    "endTime": "10:30",
                },
                {
                    "technicianId": "T2",
                    "equipmentId": "E1",
                    "startTime": "10:30",
                    "endTime": "10:45",
                },
            ]
        )
        metric = Metrics(sheduler)
        metric.compute()
        assert metric.conflicts == 0

    def test_get_technician_available_time(self):
        scheduler = Scheduler([], [], [])
        scheduler.set_schedule(
            [
                {"technicianId": "T1", "endTime": "09:30"},
                {"technicianId": "T1", "endTime": "10:15"},
                {"technicianId": "T2", "endTime": "09:45"},
            ]
        )
        for tech, time, out in [
            ("T1", "08:00", "10:15"),
            ("T3", "08:00", "08:00"),
        ]:
            assert scheduler.get_technician_available_time(tech, time) == out

    def test_get_equipment_available_time(self):
        equipments = [
            Equipment("E1", "EQUI01", "BLOOD", True, 1, 1),
            Equipment("E2", "EQUI02", "BLOOD", True, 1, 1),
        ]
        scheduler = Scheduler([], [], equipments)
        schedule = [
            {"equipmentId": "E1", "startTime": "08:00", "endTime": "09:30"},
            {"equipmentId": "E1", "startTime": "09:45", "endTime": "10:15"},
            {"equipmentId": "E2", "startTime": "08:00", "endTime": "09:45"},
        ]
        scheduler.set_schedule(schedule)
        duration = 30
        assert (
            scheduler.get_equipment_available_time("E1", "08:00", duration, 1)
            == "10:15"
        )
        assert (
            scheduler.get_equipment_available_time("E2", "08:00", duration, 1)
            == "09:45"
        )

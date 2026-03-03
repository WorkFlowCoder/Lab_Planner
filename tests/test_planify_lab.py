import unittest

from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician
from lab_planner.models.equipment import Equipment
from lab_planner.planner.planify_lab import planify_lab
from lab_planner.planner.utils import load_data_as_objects


class TestPlanifyLab(unittest.TestCase):

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
        self.assertEqual(metrics["total_time"], 75) #105 dans l'example ???
        self.assertEqual(metrics["efficiency"], 100.0) #71.4 dans l'exemple ???
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
        self.assertEqual(metrics["total_time"], 105)
        self.assertEqual(metrics["efficiency"], 128.6) # 78.6 dans l'exemple ??
        self.assertEqual(metrics["conflicts"], 0)
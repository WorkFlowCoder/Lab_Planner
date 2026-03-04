import unittest

from lab_planner.models.scheduler import Scheduler
from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician
from lab_planner.models.equipment import Equipment


class TestParallelExecution(unittest.TestCase):

    def test_parallel_case(self):
        samples = [
            Sample("S1", "BLOOD", "ROUTINE", 30, "08:00", "P1"),
            Sample("S2", "BLOOD", "STAT", 20, "08:10", "P2"),
            Sample("S3", "BLOOD", "URGENT", 15, "08:20", "P3"),
        ]
        technicians = [
            Technician("T001", "TECH01", "BLOOD", "08:00", "18:00", 1.0, ""),
            Technician("T002", "TECH02", "BLOOD", "08:00", "18:00", 1.0, ""),
            Technician("T003", "TECH03", "BLOOD", "08:00", "18:00", 1.0, ""),
        ]
        equipments = [Equipment("E001", "EQUI01", "BLOOD", True, 3, 1)]
        schedule = Scheduler(samples, technicians, equipments)
        schedule.planify()
        result = schedule.get_schedule()

        self.assertEqual(result[0]["sampleId"], "S2")
        self.assertEqual(result[0]["technicianId"], "T001")
        self.assertEqual(result[0]["equipmentId"], "E001")
        self.assertEqual(result[0]["startTime"], "08:10")

        self.assertEqual(result[1]["sampleId"], "S3")
        self.assertEqual(result[1]["technicianId"], "T002")
        self.assertEqual(result[1]["equipmentId"], "E001")
        self.assertEqual(result[1]["startTime"], "08:20")

        self.assertEqual(result[2]["sampleId"], "S1")
        self.assertEqual(result[2]["technicianId"], "T003")
        self.assertEqual(result[2]["equipmentId"], "E001")
        self.assertEqual(result[2]["startTime"], "08:00")

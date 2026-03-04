import unittest

from lab_planner.models.scheduler import Scheduler
from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician


class TestSpecializationMatching(unittest.TestCase):

    def test_specialization_matching(self):
        sample = Sample("S1", "BIOCHIMIE", "ROUTINE", 30, "08:00", "P1")
        t1 = Technician("T1", "Expert", ["HEMATO"], "08:00", "18:00", 1.0)
        t2 = Technician("T2", "Expert", ["BIOCHIMIE"], "08:00", "18:00", 1.0)

        scheduler = Scheduler([sample], [t1, t2], [])
        compatible_techs = scheduler.find_technicians(sample)

        self.assertEqual(len(compatible_techs), 1)
        self.assertEqual(compatible_techs[0].get_id(), "T2")

    def test_general_technician_matching(self):
        sample = Sample("S1", "GENETIQUE", "ROUTINE", 30, "08:00", "P1")
        t1 = Technician("T1", "Poly", ["GENERAL"], "08:00", "18:00", 1.0)

        scheduler = Scheduler([sample], [t1], [])
        compatible_techs = scheduler.find_technicians(sample)

        self.assertEqual(len(compatible_techs), 1)
        self.assertEqual(compatible_techs[0].get_id(), "T1")

    def test_not_compatible(self):
        sample = Sample("S1", "MICROBIO", "ROUTINE", 30, "08:00", "P1")
        t1 = Technician("T1", "Expert", ["HEMATO"], "08:00", "18:00", 1.0)

        scheduler = Scheduler([sample], [t1], [])
        compatible_techs = scheduler.find_technicians(sample)

        self.assertEqual(len(compatible_techs), 0)

import unittest
from lab_planner.planner.utils import latest_time
from lab_planner.planner.utils import add_minutes
from lab_planner.planner.utils import sort_samples_by_priority
from lab_planner.planner.utils import load_data_as_objects
from lab_planner.planner.utils import earliest_time
from lab_planner.planner.utils import minutes_between
from lab_planner.planner.utils import get_full_time
from lab_planner.planner.utils import has_overlap
from lab_planner.planner.utils import calculate_conflicts
from lab_planner.planner.utils import get_technician_available_time
from lab_planner.planner.utils import get_equipment_available_time
from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician
from lab_planner.models.equipment import Equipment
from lab_planner.models.sample import Sample

fmt = "%H:%M"

class TestUtils(unittest.TestCase):

    def test_sort_samples_by_priority(self):
        s1 = Sample("S1", "BLOOD", "ROUTINE", 30, "08:00", "P1")
        s2 = Sample("S2", "URINE", "STAT", 20, "08:10", "P2")
        s3 = Sample("S3", "BLOOD", "URGENT", 15, "08:20", "P3")
        sorted_samples = sort_samples_by_priority([s1, s2, s3])
        self.assertEqual([s.id for s in sorted_samples], ["S2", "S3", "S1"])

    def test_load_data_as_objects(self):
        result = load_data_as_objects("example_2.json")

        # Vérifier que les clés existent
        self.assertIn("samples", result)
        self.assertIn("technicians", result)
        self.assertIn("equipment", result)

        # Vérifier les samples
        samples = result["samples"]
        self.assertEqual(len(samples), 2)
        self.assertIsInstance(samples[0], Sample)
        self.assertEqual(samples[0].get_id(), "S001")
        self.assertEqual(samples[0].get_type(), "BLOOD")
        self.assertEqual(samples[0].get_priority(), "URGENT")
        self.assertIsInstance(samples[1], Sample)
        self.assertEqual(samples[1].get_id(), "S002")
        self.assertEqual(samples[1].get_type(), "BLOOD")
        self.assertEqual(samples[1].get_priority(), "STAT")

        # Vérifier les techniciens
        techs = result["technicians"]
        self.assertEqual(len(techs),1)
        self.assertIsInstance(techs[0], Technician)
        self.assertEqual(techs[0].get_id(), "T001")
        self.assertEqual(techs[0].get_startTime(), "08:00")
        self.assertEqual(techs[0].get_endTime(), "17:00")
        self.assertEqual(techs[0].get_speciality(), "BLOOD")

        # Vérifier les équipements
        equip = result["equipment"]
        self.assertEqual(len(equip), 1)
        self.assertIsInstance(equip[0], Equipment)
        self.assertEqual(equip[0].get_id(), "E001")
        self.assertEqual(equip[0].get_type(), "BLOOD")
        self.assertTrue(equip[0].get_available())

    def test_latest_time(self):
        assert latest_time("09:00", "10:00") == "10:00"
        assert latest_time("15:30", "12:45") == "15:30"

    def test_earliest_time(self):
        assert earliest_time("09:00", "10:00") == "09:00"
        assert earliest_time("15:30", "12:45") == "12:45"

    def test_minutes_between(self):
        assert minutes_between("09:00", "10:00") == 60
        assert minutes_between("08:15", "08:45") == 30

    def test_add_minutes(self):
        assert add_minutes("09:00", 30) == "09:30"
        assert add_minutes("10:45", 60) == "11:45"

    def test_get_full_time(self):
        schedule = [
            {"startTime": "09:00", "endTime": "10:00"},
            {"startTime": "09:30", "endTime": "10:15"}
        ]
        assert get_full_time(schedule) == 75  # 09:00 → 10:15
        assert get_full_time([]) == 0

    def test_has_overlap(self):
        assert has_overlap("09:00", "10:00", "09:30", "10:30") is True
        assert has_overlap("09:00", "10:00", "10:00", "11:00") is False

    def test_calculate_conflicts(self):
        schedule = [
            {"technicianId": "T1", "equipmentId": "E1", "startTime": "09:00", "endTime": "10:00"},
            {"technicianId": "T1", "equipmentId": "E2", "startTime": "09:30", "endTime": "10:30"},  # conflict
            {"technicianId": "T2", "equipmentId": "E1", "startTime": "09:45", "endTime": "10:15"}   # conflict
        ]
        assert calculate_conflicts(schedule) == 2

    def test_get_technician_available_time(self):
        schedule = [
            {"technicianId": "T1", "endTime": "09:30"},
            {"technicianId": "T1", "endTime": "10:15"},
            {"technicianId": "T2", "endTime": "09:45"}
        ]
        assert get_technician_available_time(schedule, "T1", "08:00") == "10:15"
        assert get_technician_available_time(schedule, "T3", "08:00") == "08:00"

    def test_get_equipment_available_time(self):
        schedule = [
            {"equipmentId": "E1", "endTime": "09:30"},
            {"equipmentId": "E1", "endTime": "10:15"},
            {"equipmentId": "E2", "endTime": "09:45"}
        ]
        assert get_equipment_available_time(schedule, "E1", "08:00") == "10:15"
        assert get_equipment_available_time(schedule, "E3", "08:00") == "08:00"
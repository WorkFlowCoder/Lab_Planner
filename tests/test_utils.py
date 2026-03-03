import unittest
from lab_planner.planner.utils import latest_time, add_minutes, sort_samples_by_priority, load_data_as_objects
from lab_planner.models.sample import Sample
from lab_planner.models.technician import Technician
from lab_planner.models.equipment import Equipment
from lab_planner.models.sample import Sample

class TestUtils(unittest.TestCase):

    def test_latest_time(self):
        self.assertEqual(latest_time("09:00", "08:30"), "09:00")
        self.assertEqual(latest_time("07:15", "07:45"), "07:45")

    def test_add_minutes(self):
        self.assertEqual(add_minutes("09:00", 45), "09:45")
        self.assertEqual(add_minutes("23:30", 90), "01:00")  # lendemain

    def test_sort_samples_by_priority(self):
        s1 = Sample("S1", "BLOOD", "ROUTINE", 30, "08:00", "P1")
        s2 = Sample("S2", "URINE", "STAT", 20, "08:10", "P2")
        s3 = Sample("S3", "BLOOD", "URGENT", 15, "08:20", "P3")
        sorted_samples = sort_samples_by_priority([s1, s2, s3])
        self.assertEqual([s.id for s in sorted_samples], ["S2", "S3", "S1"])

class TestLoadData(unittest.TestCase):

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
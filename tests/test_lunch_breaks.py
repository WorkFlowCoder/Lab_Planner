import unittest

from lab_planner.models.scheduler import Scheduler
from lab_planner.models.sample import Sample


class TestLunchBreaks(unittest.TestCase):
    def test_lunch_break(self):
        sample = Sample("S1", "BLOOD", "ROUTINE", 30, "12:05", "P1")

        # On simule un planning où le tech T1 est libre depuis 11h50
        scheduler = Scheduler([sample], [], [])
        scheduler.set_schedule([{"technicianId": "T1", "endTime": "11:50"}])
        sample.technician_id = "T1"
        start_time = scheduler.get_technician_available_time(sample, "12:05")

        # Doit être décalé à 13:00 (fin de pause)
        self.assertEqual(start_time, "13:00")

    def test_lunch_break_stat(self):
        sample = Sample("S1", "BLOOD", "STAT", 20, "12:15", "P2")

        scheduler = Scheduler([sample], [], [])
        scheduler.set_schedule([{"technicianId": "T1", "endTime": "11:00"}])
        sample.technician_id = "T1"
        start_time = scheduler.get_technician_available_time(sample, "12:15")

        # Doit commencer dès son arrivée, cat STAT
        self.assertEqual(start_time, "12:15")

    def test_continuous_work_before_break(self):
        # On simule une tâche qui finit à 12h15
        scheduler = Scheduler([], [], [])
        scheduler.set_schedule([{"technicianId": "T1", "endTime": "12:15"}])
        sample = Sample("S3", "BLOOD", "ROUTINE", 20, "12:15", "P3")
        sample.technician_id = "T1"
        start_time = scheduler.get_technician_available_time(sample, "12:15")
        # Le tech a fini à 12h15, il est en pause, il reprend à 13h00
        self.assertEqual(start_time, "13:00")

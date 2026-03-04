import unittest

from lab_planner.models.scheduler import Scheduler
from lab_planner.models.equipment import Equipment


class TestMaintenance(unittest.TestCase):

    def test_equipment_maintenance(self):
        # Equipment avec maintenance de 06:00 à 07:00
        equipment = Equipment(
            id="EQ001", name="EQUI01", type="BLOOD", available=True, capacity=1
        )
        scheduler = Scheduler([], [], [equipment])
        scheduler.set_schedule([])  # aucun autre créneau
        # On demande un créneau de 30 min à partir de 06:00
        start_time = scheduler.get_equipment_available_time(
            equipment_id="EQ001",
            start_time="06:00",
            duration=30,
            capacity=1,
        )
        assert start_time == "07:00"

    def test_equipment_maintenance_2(self):
        # Equipment avec maintenance de 06:00 à 07:00
        equipment = Equipment(
            id="EQ001", name="EQUI01", type="BLOOD", available=True, capacity=1
        )
        scheduler = Scheduler([], [], [equipment])
        scheduler.set_schedule([])  # aucun autre créneau
        # On demande un créneau de 30 min à partir de 06:20
        start_time = scheduler.get_equipment_available_time(
            equipment_id="EQ001",
            start_time="06:20",
            duration=30,
            capacity=1,
        )
        assert start_time == "07:00"

    def test_equipment_maintenance_3(self):
        # Equipment avec maintenance de 06:00 à 07:00
        equipment = Equipment(
            id="EQ001", name="EQUI01", type="BLOOD", available=True, capacity=1
        )
        scheduler = Scheduler([], [], [equipment])
        scheduler.set_schedule([])  # aucun autre créneau
        # On demande un créneau de 120 min à partir de 05:30
        start_time = scheduler.get_equipment_available_time(
            equipment_id="EQ001",
            start_time="05:30",
            duration=120,
            capacity=1,
        )
        assert start_time == "07:00"

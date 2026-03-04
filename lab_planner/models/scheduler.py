from lab_planner.planner.utils import add_minutes
from lab_planner.planner.utils import latest_time
from datetime import datetime

fmt = "%H:%M"


class Scheduler:

    def __init__(self, samples, technicians, equipment):
        self.samples = samples
        self.technicians = technicians
        self.equipment = equipment
        self.schedule = []

    def planify(self):
        self.sort_samples_by_priority()
        for sample in self.samples:
            self.add_sample_to_schedule(sample)

    def sort_samples_by_priority(self):
        # Triage des samples
        stat_samples = [s for s in self.samples if s.get_priority() == "STAT"]
        urgent_samples = [s for s in self.samples if s.get_priority() == "URGENT"]
        routine_samples = [s for s in self.samples if s.get_priority() == "ROUTINE"]
        list_of_priority = [stat_samples, urgent_samples, routine_samples]
        for case in range(3):
            list_of_priority[case] = sorted(
                list_of_priority[case],
                key=lambda s: datetime.strptime(s.get_arrivalTime(), fmt),
            )
        self.samples = [
            sample for priority_case in list_of_priority for sample in priority_case
        ]

    def get_samples(self):
        return self.samples

    def find_technicians(self, sample) -> list:
        technicians = [
            t
            for t in self.technicians
            if (
                (
                    sample.get_type() in t.get_speciality()
                    or "GENERAL" in t.get_speciality()
                )
            )
        ]
        # Triage des techniciens en fonction de l'heure de disponibilité
        technicians = sorted(
            technicians,
            key=lambda technician: (
                "GENERAL" in technician.get_speciality(),
                datetime.strptime(
                    self.get_technician_available_time(
                        technician.get_id(),
                        latest_time(
                            sample.get_arrivalTime(), technician.get_startTime()
                        ),
                    ),
                    fmt,
                ),
            ),
        )
        return technicians

    def add_sample_to_schedule(self, sample):
        # Recherche des techniciens
        technicians = self.find_technicians(sample)
        sample.technician_id = technicians[0].get_id()
        equipement = [
            e
            for e in self.equipment
            if (e.get_type() == sample.get_type() and e.get_available())
        ]
        sample.equipment_id = equipement[0].get_id()
        ### Meilleur triage des équipements ?

        # Prendre un créneau avec le premier qui arrive
        horaire_commun = latest_time(
            sample.get_arrivalTime(), technicians[0].get_startTime()
        )
        start_for_technicien = self.get_technician_available_time(
            sample.technician_id, horaire_commun
        )
        sample.start_time = self.get_equipment_available_time(
            sample.equipment_id, start_for_technicien
        )
        sample.end_time = add_minutes(sample.start_time, sample.analysisTime)
        self.schedule.append(
            {
                "sampleId": sample.id,
                "technicianId": sample.technician_id,
                "equipmentId": sample.equipment_id,
                "startTime": sample.start_time,
                "endTime": sample.end_time,
                "priority": sample.get_priority(),
                "analysisType": sample.get_analysisType(),
                "efficiency": technicians[0].get_efficiency(),
            }
        )

    def get_technician_available_time(
        self, technician_id: str, default_start: str
    ) -> str:
        end_times = [
            s["endTime"] for s in self.schedule if s["technicianId"] == technician_id
        ]
        if not end_times:
            return default_start
        return max(end_times)

    def get_equipment_available_time(
        self, equipment_id: str, default_start: str
    ) -> str:
        end_times = [
            s["endTime"] for s in self.schedule if s["equipmentId"] == equipment_id
        ]
        if not end_times:
            return default_start
        return max(end_times)

    def get_schedule(self):
        return self.schedule

    def set_schedule(self, schedule: list):
        self.schedule = schedule

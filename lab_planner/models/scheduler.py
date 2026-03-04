from lab_planner.planner.utils import add_minutes
from lab_planner.planner.utils import latest_time


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
        ## Phase de rangement des listes en fonction de l'heures d'arrvée pour plus tard !! (bientôt)
        # Concaténation de sortie par ordre d'importande
        self.samples = stat_samples + urgent_samples + routine_samples

    def get_samples(self):
        return self.samples

    def add_sample_to_schedule(self, sample):
        # Recherche des ressources
        technician = [
            t
            for t in self.technicians
            if (
                t.get_speciality() == sample.get_type()
                or t.get_speciality() == "GENERAL"
            )
        ]
        sample.technician_id = technician[0].get_id()
        ### Meilleur triage des techniciens à venir
        equipement = [
            e
            for e in self.equipment
            if (e.get_type() == sample.get_type() and e.get_available())
        ]
        sample.equipment_id = equipement[0].get_id()
        ### Meilleur triage des équipements ?

        # Prendre un créneau avec le premier qui arrive
        horaire_commun = latest_time(
            sample.get_arrivalTime(), technician[0].get_startTime()
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
                "priority": sample.priority,
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

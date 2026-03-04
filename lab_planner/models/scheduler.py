from lab_planner.planner.utils import add_minutes
from lab_planner.planner.utils import latest_time
from itertools import chain


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
        # On ordonne en fonction de l'heure de début
        self.schedule.sort(key=lambda s: s["startTime"])

    def sort_samples_by_priority(self):
        # Triage des samples
        samples = self.samples
        stat_samples = [s for s in samples if s.get_priority() == "STAT"]
        urgent_samples = [s for s in samples if s.get_priority() == "URGENT"]
        routine_samples = [s for s in samples if s.get_priority() == "ROUTINE"]
        list_priority = [stat_samples, urgent_samples, routine_samples]
        for case in range(3):
            list_priority[case] = sorted(
                list_priority[case],
                key=lambda s: s.get_arrival(),
            )
        self.samples = list(chain.from_iterable(list_priority))

    def get_samples(self) -> list:
        return self.samples

    def find_equipments(self, sample):
        compatibles = [
            e
            for e in self.equipment
            if e.get_type() == sample.get_type() and e.get_available()
        ]

        # Objectif : temps d'attente minimal
        compatibles.sort(
            key=lambda equipment: self.get_equipment_available_time(
                equipment.get_id(),
                sample.get_arrival(),
                sample.analysisTime,
                equipment.capacity,
            )
        )
        return compatibles

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
            key=lambda tech: (
                "GENERAL" in tech.get_speciality(),
                self.get_technician_available_time(
                    tech.get_id(),
                    latest_time(sample.get_arrival(), tech.get_start()),
                ),
            ),
        )
        return technicians

    def add_sample_to_schedule(self, sample):
        # Recherche des techniciens
        technicians = self.find_technicians(sample)
        sample.technician_id = technicians[0].get_id()
        # Sélection de l'équipement compatible
        equipements = self.find_equipments(sample)
        equipment = equipements[0]
        sample.equipment_id = equipment.get_id()

        # Déterminer le créneau de début
        arrival_time = sample.get_arrival()
        technician_arrival = technicians[0].get_start()
        horaire_commun = latest_time(arrival_time, technician_arrival)

        start_tech = self.get_technician_available_time(
            sample.technician_id, horaire_commun
        )
        analysisTime = sample.analysisTime
        capacity = equipment.get_capacity()
        sample.start_time = self.get_equipment_available_time(
            sample.equipment_id, start_tech, analysisTime, capacity
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

    def get_equipment_available_time(
        self, equipment_id: str, start_time: str, duration: int, capacity: int
    ) -> str:
        equipment = next(
            equipment
            for equipment in self.equipment
            if equipment.get_id() == equipment_id
        )

        maintenance_start = equipment.get_maintenance_start()
        maintenance_duration = equipment.get_maintenance_duration()
        maintenance_end = add_minutes(maintenance_start, maintenance_duration)
        start = start_time
        while True:
            end = add_minutes(start, duration)

            # Blocage de la maintenance (chevauchement)
            if (
                maintenance_start
                and start < maintenance_end
                and end > maintenance_start
            ):
                start = maintenance_end
                continue
            # Vérifier capacité (parallèle ou dispo)
            running = sum(
                1
                for s in self.schedule
                if s["equipmentId"] == equipment_id
                and not (s["endTime"] <= start or end <= s["startTime"])
            )
            if running < capacity:
                return start
            start = add_minutes(start, 1)

    def get_technician_available_time(
        self, technician_id: str, default_start: str
    ) -> str:
        key = "technicianId"
        end_times = list(
            map(
                lambda s: s["endTime"],
                filter(lambda s: s[key] == technician_id, self.schedule),
            )
        )
        if not end_times:
            return default_start
        return max(end_times)

    def get_schedule(self):
        return self.schedule

    def set_schedule(self, schedule: list):
        self.schedule = schedule

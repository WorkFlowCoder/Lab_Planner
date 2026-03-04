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
            equip
            for equip in self.equipment
            if equip.get_type() == sample.get_type() and equip.get_available()
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
                    sample, latest_time(sample.get_arrival(), tech.get_start())
                ),
            ),
        )
        return technicians

    def add_sample_to_schedule(self, sample):
        best_start = None
        best_tech = None
        best_equip = None
        # On récupère tous les ressources possibles
        possible_techs = self.find_technicians(sample)
        possible_equips = self.find_equipments(sample)
        # Greedy intelligent
        for tech in possible_techs:
            for equip in possible_equips:
                arrival_time = sample.get_arrival()
                time = latest_time(arrival_time, tech.get_start())
                sample.technician_id = tech.get_id()
                tech_start = self.get_technician_available_time(sample, time)
                equip_start = self.get_equipment_available_time(
                    equip.get_id(),
                    tech_start,
                    sample.get_analysisTime(),
                    equip.get_capacity(),
                )
                # On garde la meilleure option
                if best_start is None or equip_start < best_start:
                    best_start = equip_start
                    best_tech = tech
                    best_equip = equip
                    if best_start == arrival_time:
                        break

        sample.technician_id = best_tech.get_id()
        sample.equipment_id = best_equip.get_id()
        sample.start_time = best_start
        analysisTime = sample.get_analysisTime()

        sample.end_time = add_minutes(sample.start_time, analysisTime)
        self.schedule.append(
            {
                "sampleId": sample.id,
                "technicianId": sample.technician_id,
                "equipmentId": sample.equipment_id,
                "startTime": sample.start_time,
                "endTime": sample.end_time,
                "priority": sample.get_priority(),
                "analysisType": sample.get_analysisType(),
                "efficiency": best_tech.get_efficiency(),
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

    def get_technician_available_time(self, sample, default_start: str) -> str:
        key = "technicianId"
        techId = sample.technician_id
        tasks = [task for task in self.schedule if task[key] == techId]
        current_start = default_start  # Si pas de task
        if tasks:
            # disponibilité après sa dernière task
            current_start = max(s["endTime"] for s in tasks)
        current_start = latest_time(current_start, sample.get_arrival())
        if sample.get_priority() == "STAT":
            return current_start
        current_end = current_start
        while True:
            current_end = add_minutes(current_start, sample.get_analysisTime())
            # Le technicien à pris sa pause ? (simplification 12h à 13h)
            if current_start < "13:00" and current_end > "12:00":
                current_start = "13:00"
                continue  # Vérification creneau

            return current_start

    def get_schedule(self):
        return self.schedule

    def set_schedule(self, schedule: list):
        self.schedule = schedule

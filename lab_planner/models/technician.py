class Technician:
    LUNCH_BREAK_START = "12:00"
    LUNCH_BREAK_END = "15:00"
    LUNCH_DURATION = 60  # 1 heure

    def __init__(
        self,
        id: str,
        name: str,
        speciality: str,
        startTime: str,
        endTime: str,
        efficiency: float = 1.0,
    ):
        self.id = id
        self.name = name
        if isinstance(speciality, str):
            self.speciality = [speciality]
        else:
            self.speciality = speciality
        self.startTime = startTime
        self.endTime = endTime
        self.efficiency = efficiency

    # --- Getters ---

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_speciality(self) -> str:
        return self.speciality

    def get_start(self) -> str:
        return self.startTime

    def get_endTime(self) -> str:
        return self.endTime

    def get_efficiency(self) -> float:
        return self.efficiency

    def has_lunchBreak(self) -> bool:
        return not self.lunchBreak == ""

    def get_lunchBreak(self) -> str:
        return self.lunchBreak

    def to_string(self) -> str:
        return (
            f"[Technician_id={self.id}, name={self.name},"
            f" speciality={self.speciality}, "
            f"startTime={self.startTime}, endTime={self.endTime}]"
        )

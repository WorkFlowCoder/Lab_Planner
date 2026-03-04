class Technician:
    def __init__(
        self, id: str, name: str, speciality: str, startTime: str, endTime: str
    ):
        self.id = id
        self.name = name
        self.speciality = speciality
        self.startTime = startTime
        self.endTime = endTime

    # --- Getters ---

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_speciality(self) -> str:
        return self.speciality

    def get_startTime(self) -> str:
        return self.startTime

    def get_endTime(self) -> str:
        return self.endTime

    def to_string(self) -> str:
        return (
            f"[Technician_id={self.id}, name={self.name}, speciality={self.speciality}, "
            f"startTime={self.startTime}, endTime={self.endTime}]"
        )

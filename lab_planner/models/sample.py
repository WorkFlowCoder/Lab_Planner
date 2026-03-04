class Sample:
    def __init__(
        self,
        id: str,
        type: str,
        priority: str,
        analysisTime: int,
        arrivalTime: str,
        patientId: str,
    ):
        self.id = id
        self.type = type
        self.priority = priority
        self.analysisTime = analysisTime
        self.arrivalTime = arrivalTime
        self.patientId = patientId

        self.technician_id = None
        self.equipment_id = None
        self.start_time = None
        self.end_time = None

    # --- Getters ---

    def get_id(self) -> str:
        return self.id

    def get_type(self) -> str:
        return self.type

    def get_priority(self) -> str:
        return self.priority

    def get_analysisTime(self) -> int:
        return self.analysisTime

    def get_arrivalTime(self) -> str:
        return self.arrivalTime

    def get_patientId(self) -> str:
        return self.patientId

    def to_string(self) -> str:
        return (
            f"[Sample_id={self.id}, type={self.type}, priority={self.priority}, "
            f"analysisTime={self.analysisTime}, arrivalTime={self.arrivalTime}, "
            f"patientId={self.patientId}, technician_id={self.technician_id}, "
            f"equipment_id={self.equipment_id}, start_time={self.start_time}, "
            f"end_time={self.end_time}]"
        )

class Equipment:
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        available: bool,
        capacity: int = 1,
        cleaningTime: int = 1,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.available = available
        self.capacity = capacity
        self.cleaningTime = cleaningTime
        self.init_maintenance()

    def init_maintenance(self):
        match (self.id):
            case "EQ001":  # Hématologie
                self.maintenance_start = "06:00"
                self.maintenance_duration = 60
            case "EQ002":  # Biochimie
                self.maintenance_start = "06:30"
                self.maintenance_duration = 60
            case "EQ003":  # Microbiologie
                self.maintenance_start = "07:00"
                self.maintenance_duration = 60
            case "EQ004":  # Immunologie
                self.maintenance_start = "07:30"
                self.maintenance_duration = 60
            case "EQ005":  # Génétique
                self.maintenance_start = "05:30"
                self.maintenance_duration = 60
            case _:
                self.maintenance_start = "00:00"
                self.maintenance_duration = 0

    # --- Getters ---

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> str:
        return self.type

    def get_available(self) -> bool:
        return self.available

    def get_capacity(self) -> int:
        return self.capacity

    def get_cleaningTime(self) -> int:
        return self.cleaningTime

    def get_maintenance_start(self) -> str:
        return self.maintenance_start

    def get_maintenance_duration(self) -> int:
        return self.maintenance_duration

    def to_string(self) -> str:
        return (
            f"[Equipement_id={self.id}, name={self.name}, type={self.type}, "
            f"available={self.available}]"
        )

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

    def to_string(self) -> str:
        return (
            f"[Equipement_id={self.id}, name={self.name}, type={self.type}, "
            f"available={self.available}]"
        )

class Equipment:
    def __init__(self, id: str, name: str, type: str, available: bool):
        self.id = id
        self.name = name
        self.type = type
        self.available = available

# --- Getters ---

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> str:
        return self.type

    def get_available(self) -> bool:
        return self.available
    
    def to_string(self) -> str:
        return (
            f"[Equipement_id={self.id}, name={self.name}, type={self.type}, "
            f"available={self.available}]"
        )
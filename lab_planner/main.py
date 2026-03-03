from lab_planner.planner.planify_lab import planify_lab
from pathlib import Path
import json

def load_json_data(file: str) -> dict:
    data_path = Path(__file__).parent / "data" / file
    with open(data_path,"r") as f:
        return json.load(f)

def main():

    try:
        data = load_json_data("example.json")
    except FileNotFoundError:
        print("Fichier JSON introuvable.")
        return
    except json.JSONDecodeError:
        print("Erreur : le fichier JSON est mal formé.")
        return

    #print(data)
    result = planify_lab(data)
    print("Schedule")
    print(result)

if __name__ == "__main__":
    main()
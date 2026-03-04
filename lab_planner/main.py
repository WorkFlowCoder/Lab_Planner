from lab_planner.planner.planify_lab import planify_lab
from lab_planner.planner.utils import load_data_as_objects
import json


def main():
    try:
        data = load_data_as_objects("example_inter.json")
    except FileNotFoundError:
        print("Fichier JSON introuvable.")
        return
    except json.JSONDecodeError:
        print("Erreur : le fichier JSON est mal formé.")
        return

    result = planify_lab(data)
    print(result)


if __name__ == "__main__":
    main()

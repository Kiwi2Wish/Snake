def get_last_scores():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "scores.txt")
        with open(file_path, "r") as f:
            lines = f.readlines()

        # Récupérer les 3 derniers scores, sans les dates
        return [line.split(" - ")[0] + " - " + line.split(" - ")[1] for line in lines[-3:]][::-1]  # Inversé pour ordre chrono
    except:
        return []

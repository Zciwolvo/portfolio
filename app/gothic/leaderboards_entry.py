import uuid
from datetime import date
import os
import json


class Entry:
    def __init__(self, user, score, gamemode):
        self.entry_id = str(uuid.uuid4())
        time = date.today()
        self.date = time.strftime("%Y-%m-%d")
        self.user = user
        self.score = score
        self.gamemode = gamemode

    def to_dict(self):
        return {
            "id": self.entry_id,
            "date": self.date,
            "user": self.user,
            "score": self.score,
            "gamemode": self.gamemode,
        }

    @classmethod
    def from_dict(cls, entry):
        return cls(
            id=entry["id"],
            date=entry["date"],
            user=entry["user"],
            score=entry["score"],
            gamemode=entry["gamemode"],
        )

    def save_to_json(self):
        # Define the path to the scores.json file
        scores_file_path = os.path.join("/home/IgorGawlowicz/mysite/scores", "scores.json")

        # Read the existing content of scores.json, or initialize an empty dictionary
        if os.path.exists(scores_file_path):
            with open(scores_file_path, "r") as scores_file:
                scores_data = json.load(scores_file)
        else:
            scores_data = {}

        # Add the new data to the scores dictionary with entry_id as the key
        scores_data[self.entry_id] = self.to_dict()

        # Write the updated dictionary back to scores.json
        with open(scores_file_path, "w") as scores_file:
            json.dump(scores_data, scores_file)

    @classmethod
    def load_from_json(cls, entry_id):
        # Define the path to the scores.json file
        scores_file_path = os.path.join("/home/IgorGawlowicz/mysite/scores", "scores.json")

        if os.path.exists(scores_file_path):
            with open(scores_file_path, "r") as scores_file:
                scores_data = json.load(scores_file)
                if entry_id in scores_data:
                    score_data = scores_data[entry_id]
                    return cls.from_dict(score_data)

        return None

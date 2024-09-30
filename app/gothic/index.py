from flask import render_template, request, jsonify, Blueprint, redirect, url_for, current_app
import random
import os
import jwt
import json

from .custom_map import CustomMap
from .location import Location
from .leaderboards_entry import Entry

from . import gothic

api = ""
@gothic.before_request
def setup_stripe_api_key():
    global api
    api = current_app.config['GOTHIC_API']


score = 0
round_counter = 1


#gothic1_map = CustomMap("gothic1", "https://drive.google.com/uc?id=1mqBhVNb4LErYSNvq9zBo2r-iIgspk79b", 620, 490, 7)
#gothic2_map = CustomMap("gothic2", "https://drive.google.com/uc?id=1D0I3Sp5MNKlJT7WsvNlPbBVAYDCESViL", 2000, 2000, 7)
gothic1_map = CustomMap("gothic1", "/static/maps/g1.png", 620, 490, 7)
gothic2_map = CustomMap("gothic2", "/static/maps/g2.png", 2000, 2000, 7)


def get_random_location(map_pool="gothic1"):
    loc1 = Location(
        "https://drive.google.com/uc?id=1YW-2duV9DiJhiAUp78R23Q8mE3LSTgWe", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc2 = Location(
        "https://drive.google.com/uc?id=19oSQbbsQOJFXC4eQAl4zHwSsxwc-XLJ3", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc3 = Location(
        "https://drive.google.com/uc?id=1ZUcgMr6CX-kugX8mnSs24atWhw9WT9x9", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc4 = Location(
        "https://drive.google.com/uc?id=1uBjQqKOgMz4rIBrPLaFRP74TofUAQ6pq", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc5 = Location(
        "https://drive.google.com/uc?id=1_hZkjYwIb4kFplAmtlqqEcVKO7uw-oab", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    loc6 = Location(
        "https://drive.google.com/uc?id=1u_MYOu8xwylXFocV1AtwC5HuhJYvNVQ3", 2.938957135704084, 3.950195312499991, gothic1_map
    )
    gothic1 = [loc1, loc2, loc3, loc4, loc5, loc6]
    gothic2 = [loc1, loc2, loc3, loc4, loc5, loc6]
    gothic3 = [loc1, loc2, loc3, loc4, loc5, loc6]
    archolos = [loc1, loc2, loc3, loc4, loc5, loc6]
    mixed = [loc1, loc2, loc3, loc4, loc5, loc6]

    chosen = []
    if map_pool == "Gothic1":
        chosen = gothic1
    elif map_pool == "Gothic2":
        chosen = gothic2
    elif map_pool == "Gothic3":
        chosen = gothic3
    elif map_pool == "Archolos":
        chosen = archolos
    else:
        chosen = mixed
    return random.choice(chosen)


@gothic.route("/")
def home():
    global score, round_counter
    round_counter = 1
    score = 0
    access_token = request.cookies.get("access_token")
    if not access_token:
        return render_template(
            "gothic.html",
            message="It looks like you're not logged in, so your score won't be saved to the leaderboards. Log in or create an account to start saving your scores and competing with others.",
        )
    return render_template("gothic.html")


@gothic.route("/start_game", methods=["POST"])
def start_game():
    global score, round_counter, map_pool
    round_counter = 1
    score = 0
    data = request.get_json()
    map_pool = data["selectedGamePool"]
    return jsonify({"message": "Success"})


@gothic.route("/update_score_and_round", methods=["POST"])
def update_score_and_round():
    global score, round_counter, map_pool
    data = request.get_json()
    score += data["score"]
    round_counter += 1
    if round_counter == 6:
        access_token = request.cookies.get("access_token")
        if access_token:
            decoded_token = jwt.decode(
                access_token, key=os.getenv("JWT_SECRET"), algorithms=["HS256"]
            )
            username = decoded_token['sub']['username']
            entry = Entry(username, score, map_pool)
            entry.save_to_json()
    return jsonify({"message": "Success"})

@gothic.route("/leaderboards")
def leaderboards():
    scores_dir = "/scores"
    leaderboards_data = []

    # Define the path to the scores.json file
    scores_file_path = os.path.join(scores_dir, "scores.json")

    if os.path.exists(scores_file_path):
        with open(scores_file_path, "r") as scores_file:
            scores_data = json.load(scores_file)

            # Iterate through all entries in the scores.json file
            for entry_id, score_data in scores_data.items():
                leaderboards_data.append(
                    {
                        "user": score_data["user"],
                        "score": score_data["score"],
                        "gamemode": score_data["gamemode"],
                        "date": score_data["date"],
                    }
                )

    # Sort the leaderboard data by score (you can customize the sorting)
    leaderboards_data.sort(key=lambda x: x["score"], reverse=True)

    return render_template("leaderboards.html", leaderboards_data=leaderboards_data)


@gothic.route("/map")
def map():
    global loc
    try:
        loc = get_random_location(map_pool)
        return render_template(
            "map.html",
            custom_map=loc.map,
            location=loc,
            api=api,
            score=score,
            round=round_counter,
            map_pool=map_pool,
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template("gothic.html")


@gothic.route("/login")
def login():
    return render_template("login.html")


@gothic.route("/register")
def register():
    return render_template("register.html")


from flask import Blueprint, render_template
import json

dataset_blueprint = Blueprint("dataset", __name__)


@dataset_blueprint.route("/dataset")
def display_json():
    try:
        with open("/home/IgorGawlowicz/mysite/static/data/classes_mod.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
        with open("/home/IgorGawlowicz/mysite/static/data/data_bkp.json", "r", encoding="utf-8") as json_file:
            spells = json.load(json_file)
        with open("/home/IgorGawlowicz/mysite/static/data/weapons_mod.json", "r", encoding="utf-8") as json_file:
            weapons = json.load(json_file)
        with open("/home/IgorGawlowicz/mysite/static/data/talents.json", "r", encoding="utf-8") as json_file:
            talents = json.load(json_file)
    except FileNotFoundError:
        classes, spells, weapons, talents = [], [], [], []

    return render_template(
        "dataset.html", classes=classes, spells=spells, weapons=weapons, talents=talents
    )


@dataset_blueprint.route("/classes")
def display_classes():
    try:
        with open("/home/IgorGawlowicz/mysite/static/data/classes_mod.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("classes.html", classes=classes)


@dataset_blueprint.route("/weapons")
def display_weapons():
    try:
        with open("/home/IgorGawlowicz/mysite/static/data/weapons_mod.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("weapons.html", weapons=classes)


@dataset_blueprint.route("/spells")
def display_spells():
    try:
        with open("/home/IgorGawlowicz/mysite/static/data/data_bkp.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("spells.html", spells=classes)


@dataset_blueprint.route("/talents")
def display_talents():
    try:
        with open("/home/IgorGawlowicz/mysite/static/data/talents.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("talents.html", talents=classes)

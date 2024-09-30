from flask import Blueprint, render_template
import json

from . import warhammer

@warhammer.route("/dataset")
def display_json():
    try:
        with open("/static/data/classes_mod.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
        with open("/static/data/data_bkp.json", "r", encoding="utf-8") as json_file:
            spells = json.load(json_file)
        with open("/static/data/weapons_mod.json", "r", encoding="utf-8") as json_file:
            weapons = json.load(json_file)
        with open("/static/data/talents.json", "r", encoding="utf-8") as json_file:
            talents = json.load(json_file)
    except FileNotFoundError:
        classes, spells, weapons, talents = [], [], [], []

    return render_template(
        "dataset.html", classes=classes, spells=spells, weapons=weapons, talents=talents
    )


@warhammer.route("/classes")
def display_classes():
    try:
        with open("/static/data/classes_mod.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("classes.html", classes=classes)


@warhammer.route("/weapons")
def display_weapons():
    try:
        with open("/static/data/weapons_mod.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("weapons.html", weapons=classes)


@warhammer.route("/spells")
def display_spells():
    try:
        with open("/static/data/data_bkp.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("spells.html", spells=classes)


@warhammer.route("/talents")
def display_talents():
    try:
        with open("/static/data/talents.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
    except FileNotFoundError:
        classes = []

    return render_template("talents.html", talents=classes)

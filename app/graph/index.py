from flask import Blueprint, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import ast

from .functions import generate_matrix, create_graph, bfs

from . import graph

socketio = SocketIO()


@graph.route("/")
def index():
    return render_template("graphapp.html")

@graph.route("/generate_circles", methods=["POST"])
def generate_circles():
    data = request.get_json()
    num_circles = data["numCircles"]
    connection_chance = data["connectionChance"]
    start_point = int(data["startPoint"])
    matrix = generate_matrix(num_circles, connection_chance / 100)
    circle_data = create_graph(matrix)
    layers = bfs(matrix, start_point)
    degrees_sum = 0
    degrees: list[int] = []
    for i in range(num_circles):
        degrees_sum += circle_data[i].degrees
        degrees.append(circle_data[i].degrees)
        x = circle_data[i].x
        y = circle_data[i].y
        radius = 40
        connections = circle_data[i].neighbours
        circle_data[i] = {
            "x": x,
            "y": y,
            "radius": radius,
            "connections": connections,
            "matrix": matrix,
        }
    density = (0.5 * degrees_sum) / (0.5 * len(matrix) * (len(matrix) - 1))
    circle_data[len(circle_data)] = layers
    circle_data[0]["density"] = density
    circle_data[0]["degrees"] = sorted(degrees, reverse=True)
    return jsonify(circle_data)


@graph.route("/generate_circles_from_array", methods=["POST"])
def generate_circles_from_array():
    data = request.get_json()
    matrix = data["array"]
    matrix = ast.literal_eval(matrix)
    start_point = 0
    circle_data = create_graph(matrix)
    layers = bfs(matrix, start_point)
    degrees_sum = 0
    degrees: list[int] = []
    for i in range(len(matrix)):
        degrees_sum += circle_data[i].degrees
        degrees.append(circle_data[i].degrees)
        x = circle_data[i].x
        y = circle_data[i].y
        radius = 40
        connections = circle_data[i].neighbours
        circle_data[i] = {
            "x": x,
            "y": y,
            "radius": radius,
            "connections": connections,
            "matrix": matrix,
        }
    density = (0.5 * degrees_sum) / (0.5 * len(matrix) * (len(matrix) - 1))
    circle_data[len(circle_data)] = layers
    circle_data[0]["density"] = density
    circle_data[0]["degrees"] = sorted(degrees, reverse=True)
    return jsonify(circle_data)


@graph.route("/update_circles", methods=["POST"])
def update_circles():
    data = request.get_json()
    start_point = data["startPoint"]
    matrix = data["matrix"]
    layers = bfs(matrix, start_point)
    return jsonify(layers)


@socketio.on("move")
def handle_move(data):
    emit("move", data, broadcast=True)
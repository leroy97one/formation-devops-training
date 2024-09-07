from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, Histogram, generate_latest
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.DEBUG)

# Initialiser l'application Flask
app = Flask(__name__)

# Configuration de la base de données PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle Todo pour la base de données
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Compteur et histogramme pour les métriques Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total number of HTTP requests',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP request latency',
    ['method', 'endpoint']
)

# Route pour exposer les métriques Prometheus
@app.route('/metrics')
def metrics():
    return generate_latest()

# Fonction exécutée avant chaque requête
@app.before_request
def before_request():
    request._start_time = time.time()

# Fonction exécutée après chaque requête pour enregistrer les métriques
@app.after_request
def after_request(response):
    if request.endpoint in ['index', 'add', 'delete', 'update']:
        request_end_time = time.time()
        request_latency = request_end_time - request._start_time
        path = request.path
        REQUEST_COUNT.labels(request.method, path, response.status_code).inc()
        REQUEST_LATENCY.labels(request.method, path).observe(request_latency)
    return response

# Route principale pour afficher la liste des tâches
@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

# Route pour ajouter une nouvelle tâche
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

# Route pour mettre à jour une tâche (inverser l'état "complete")
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

# Route pour supprimer une tâche
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

# Exécution du serveur Flask et création des tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Créer les tables de la base de données si elles n'existent pas
    app.run(host='0.0.0.0', port=5000, debug=True)

# Utilisez une image de base légère
FROM python:3.13-slim
# Créez et définissez le répertoire de travail


WORKDIR /app
# Copiez les fichiers nécessaires dans le conteneur
COPY requirements.txt .
# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt
# Copiez les fichiers nécessaires dans le conteneur
COPY app.py .
COPY test_e2e.py .


RUN mkdir templates
COPY templates/index.html templates/index.html

VOLUME [ "/app/data" ]


# Exposez le port sur lequel l'application sera accessible
EXPOSE 5000
# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]

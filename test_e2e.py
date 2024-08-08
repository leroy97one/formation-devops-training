import pytest
import requests
import re

@pytest.fixture
def base_url():
    return 'http://127.0.0.1:5000' # Mettez l'URL de votre application Flask si différente

def extract_task_ids(response_content):
    # Define a regular expression pattern to match task IDs in the href="/delete/(\d+)" format
    pattern = b'href="/delete/(\d+)"'
    # Use re.findall to extract all task IDs from the response content
    task_ids = re.findall(pattern, response_content)
    # Convertion des task_ids de bytes à int
    return list(map(int, task_ids))


def test_add_and_delete_task(base_url, setup_app):
    # Test d'ajout d'une tâche
    response = requests.post(f'{base_url}/add', data={'title': 'Nouvelle tache'})
    assert response.status_code == 200  # Assurez-vous que la redirection est réussie

    # Vérifier que la tâche a été ajoutée
    response = requests.get(f'{base_url}')
    assert response.status_code == 200
    assert b'Nouvelle tache' in response.content

    # Test de suppression de toutes les tâches
    task_ids = extract_task_ids(response.content)
    for task_id in task_ids:
        # Test de suppression de la tâche
        response = requests.get(f'{base_url}/delete/{task_id}')
        assert response.status_code == 200  # Assurez-vous que la redirection est réussie

    # Vérifier que toutes les tâches ont été supprimées
    response = requests.get(f'{base_url}')
    assert response.status_code == 200
    assert b'Nouvelle tache' not in response.content

def test_index_page(base_url, setup_app):
    # Test de la page d'index
    response = requests.get(f'{base_url}/')
    assert response.status_code == 200  # Assurez-vous que la page est accessible
    assert b'Pense b\xc3\xaate' in response.content  # Vérifiez que le contenu attendu est présent

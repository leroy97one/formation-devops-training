import unittest
from flask_testing import TestCase
from app import app, db, Todo


class YourAppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Testez la création d'une tâche
    def test_add_task(self):
        response = self.client.post('/add', data={'title': 'Nouvelle tache de test'})
        self.assertEqual(response.status_code, 302)

        # Assurez-vous que la tâche a été ajoutée à la base de données
        task = Todo.query.first()
        self.assertIsNotNone(task)
        self.assertEqual(task.title, 'Nouvelle tache de test')

    # Testez la suppression d'une tâche
    def test_delete_task(self):
        # Ajoutez une tâche pour pouvoir la supprimer
        test_task = Todo(title='Tache à supprimer', complete=False)
        db.session.add(test_task)
        db.session.commit()

        response = self.client.get('/delete/{}'.format(test_task.id))
        self.assertEqual(response.status_code, 302)

        deleted_task = Todo.query.get(test_task.id)
        self.assertIsNone(deleted_task) # Assurez-vous que la tâche a été supprimée de la base de données

    # Testez l'affichage des tâches sur la page d'accueil
    def test_task_list_display(self):
        # Ajoutez des tâches de test à la base de données
        task1 = Todo(title='Test1', complete=False)
        task2 = Todo(title='Test2', complete=False)
        db.session.add_all([task1, task2])
        db.session.commit()

        response = self.client.get('/')
        self.assert200(response)

        # Vérifiez que les tâches sont affichées sur la page
        self.assertIn(b'Test1', response.data)
        self.assertIn(b'Test2', response.data)

if __name__ == '__main__':
    unittest.main()

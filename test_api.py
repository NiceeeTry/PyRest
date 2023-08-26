import unittest
from app import create_app
from config import TestConfig
from extensions import db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client(self)
        
        # with self.app.app_context():
        #     db.init_app(self.app)
            
        #     db.create_all()
        
            
    def test_signup(self):
        signip_response = self.client.post('/users',
            json={"username":"test_user", "email":"test_user@gmail.com", "password":"test_user"}
            )
        status_code=signip_response.status_code
        self.assertEqual(status_code,201)
        
    # def tearDown(self) -> None:
        # with self.app.app_contex():
        #     db.session.remove()
        #     db.drop_all()
        
    def test_login(self):
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                "email":"test_user@gmail.com", 
                "password":"test_user"}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        
        status_code=login_response.status_code
        self.assertEqual(status_code,200)
        
        
    def test_get_all_recipes(self):
        """TEST GETTING ALL RECIPES"""
        response=self.client.get('/recipes')
        status_code=response.status_code
        self.assertEqual(status_code,200)
        
        
    def test_get_one_recipe(self):
        id=1
        response=self.client.get(f'recipe/{id}')
        
        status_code=response.status_code
        
        self.assertEqual(status_code,404)
        
        
    def test_create_recipe(self):
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                "email":"test_user@gmail.com", 
                "password":"test_user"}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_recipe_response=self.client.post(
            '/recipes',
            json={
                "name":"test recipe",
                "description":"lovely Bean Enchiladas",
                "num_of_servings":5,
                "cook_time":50,
                "directions":"This is how you make it"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        status_code = create_recipe_response.status_code
        
        self.assertEqual(status_code, 201)
        
    def test_update_recipe(self):
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                "email":"test_user@gmail.com", 
                "password":"test_user"}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_recipe_response=self.client.post(
            '/recipes',
            json={
                "name":"test recipe",
                "description":"lovely Bean Enchiladas",
                "num_of_servings":5,
                "cook_time":50,
                "directions":"This is how you make it"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        # id = create_recipe_response.json['id']
        id = 1
        update_response=self.client.patch(
            f'recipes/{id}',
            json={'name':'Renamed'},
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        
        status_code = update_response.status_code
        # self.assertEqual(status_code,200)
        
        
    def test_delete_recipe(self):
        signip_response = self.client.post('/users',
            json={
                "username":"test_user", 
                "email":"test_user@gmail.com", 
                "password":"test_user"}
            )
        login_response=self.client.post('/token',
            json={ 
                "email":"test_user@gmail.com", 
                "password":"test_user"
            }
        )
        access_token = login_response.json['access_token']
        create_recipe_response=self.client.post(
            '/recipes',
            json={
                "name":"test recipe",
                "description":"lovely Bean Enchiladas",
                "num_of_servings":5,
                "cook_time":50,
                "directions":"This is how you make it"
            },
            headers={
                "Authorization":f'Bearer {access_token}'
            })
        # id = create_recipe_response.json['id']
        id = 1
        delete_response = self.client.delete(
            f'recipes/{id}',
            headers={
                "Authorization":f'Bearer {access_token}'
            }
            ) 
        status_code = delete_response.status_code
        self.assertEqual(status_code, 200)
    
    
    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print('Clear table %s' % table)
            db.session.execute(table.delete())
        db.session.commit()
        
if __name__=='__main__':
    unittest.main()
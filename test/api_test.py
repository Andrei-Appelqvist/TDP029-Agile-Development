import unittest
import requests
import json

cooki = ""
headers = {'Content-Type':'application/json'}
b = {
"email":"ddd@ddd.com",
"username":"FordPrefect",
"password":"1111"
}

class MyTestClass(unittest.TestCase):
    #assertEqual
    #assertNotEqual
    #assertTrue

    #Kod som körs innan alla tester
    @classmethod
    def setUpClass(cls):
        pass

    #Kod som körs efter alla testerna
    @classmethod
    def tearDownClass(cls):
        pass


    #Kod som körs innan varje test
    def setUp(self):
        pass

    #Kod som körs efter varje test
    def tearDown(self):
        pass

    # test method
    """
    def test_equal_numbers(self):
    self.assertEqual(2, 3)
    self.assertEqual(2, 2)
    """

    def testA_create_200(self):
        response = requests.post("http://127.0.0.1:5000/user/create", json=b)
        self.assertEqual(200, response.status_code)

    def testB_create_400(self):
        #credentials
        response = requests.post("http://127.0.0.1:5000/user/create", json={
            "email":"a",
            "username":"a",
            "password":"a"
        })
        self.assertEqual(400, response.status_code)


    def testC_create_409(self):
        response = requests.post("http://127.0.0.1:5000/user/create", json=b)
        self.assertEqual(409, response.status_code)


    def testD_login(self):
        resp = requests.post("http://127.0.0.1:5000/user/login", json ={
        	"email":"ddd@ddd.com",
        	"password":"1111"
            })
        global cooki
        cooki = resp.cookies

        self.assertEqual(200, resp.status_code)


    def testE_login_400(self):
        #invalid Credentials, format
        response = requests.post("http://127.0.0.1:5000/user/login", json ={"email":"ddd",
        "password":"1111"})
        self.assertEqual(400, response.status_code)

    def testF_login_401(self):
        response = requests.post("http://127.0.0.1:5000/user/login", json ={"email":"ddd@ddd.com",
        "password":"11111"})
        self.assertEqual(401, response.status_code)

    def testG_current_200(self):
        response = requests.get("http://127.0.0.1:5000/user/current", cookies = cooki)
        data = json.loads(response.text)
        self.assertEqual(200, response.status_code)
        self.assertEqual(data['email'], b['email'])
        self.assertEqual(data['username'], b['username'])


    def testI_current_401(self):
        response = requests.get("http://127.0.0.1:5000/user/current")
        self.assertEqual(401, response.status_code)

    def testJ_logout_200(self):
        response = requests.post("http://127.0.0.1:5000/user/logout", cookies=cooki)
        self.assertEqual(200, response.status_code)


    def testK_logout_401(self):
        response = requests.post("http://127.0.0.1:5000/user/logout")
        self.assertEqual(401, response.status_code)

    def testL_remove_user_200(self):
        response = requests.delete("http://127.0.0.1:5000/user/removecurrent", cookies = cooki)
        self.assertEqual(200, response.status_code)

    def testN_remove_401(self):
        response = requests.delete("http://127.0.0.1:5000/user/removecurrent")
        self.assertEqual(401, response.status_code)





# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()

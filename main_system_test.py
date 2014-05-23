import unittest
import random
import requests
import json


class MainSystemTest(unittest.TestCase):

    url = "http://127.0.0.1:5000/position"
    headers = {'Content-Type': 'application/json'}

    def setUp(self):
        requests.delete(self.url, headers=self.headers)

    def create_position(self):
        lat = "{0}{1}.{2}".format(random.choice(["-", ""]), random.randint(00, 99), random.randint(000000, 999999))
        lon = "{0}{1}.{2}".format(random.choice(["-", ""]), random.randint(00, 99), random.randint(000000, 999999))
        data = {"lat": lat, "lon": lon}
        resp = requests.post(self.url, data=json.dumps(data), headers=self.headers)
        return resp

    def test_create_position(self):
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json().get("id"))

    def test_delete_position(self):
        count_before = len(requests.get(self.url).json().get("positions"))
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        resp = requests.delete(self.url, data=json.dumps({"id": _id}), headers=self.headers)
        self.assertTrue(resp.json())
        count_after = len(requests.get(self.url).json().get("positions"))
        self.assertEqual(count_before, count_after)

    def test_delete_all_positions(self):
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        resp = requests.delete(self.url, headers=self.headers)
        self.assertTrue(resp.json())
        self.assertEqual(len(requests.get(self.url).json().get("positions")), 0)

    def test_get_positions(self):
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        self.assertEqual(len(requests.get(self.url).json().get("positions")), 1)

    def test_get_position_with_limit(self):
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        self.assertEqual(len(requests.get(self.url).json().get("positions")), 1)
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        self.assertEqual(len(requests.get(self.url).json().get("positions")), 2)
        resp = self.create_position()
        self.assertEqual(resp.status_code, 200)
        _id = resp.json().get("id")
        self.assertTrue(_id)
        self.assertEqual(len(requests.get(self.url).json().get("positions")), 3)
        resp = requests.get(self.url + "?limit=2").json()
        self.assertEqual(len(resp.get("positions")), 2)
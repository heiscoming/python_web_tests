import unittest
import json

from main import insert_to_db, is_correct_coordinates, delete_from_db, get_from_db, app


class MainTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.delete("/position") # clean all data

    def test_post(self):
        resp = json.loads(self.app.get("/position").data)
        self.assertFalse(resp.get("positions"))
        resp = json.loads(self.app.post("/position",
                                        data=json.dumps({"lat": "32.23431", "lon": "54.34543"}),
                                        content_type='application/json',
                                        ).data
        )
        id = resp.get("id")
        self.assertEqual(len(id), 24)

    def test_get(self):
        lat1 = "32.23431"
        lon1 = "54.34543"
        lat2 = "12.43235"
        lon2 = "54.54341"
        lat3 = "-76.55454"
        lon3 = "-90.86787"
        resp = json.loads(self.app.post("/position",
                                        data=json.dumps({"lat": lat1, "lon": lon1}),
                                        content_type='application/json',
                                        ).data
        )
        id = resp.get("id")
        self.assertEqual(len(id), 24)
        resp = json.loads(self.app.get("/position").data)
        self.assertEqual(lat1, resp.get("positions")[0].get("lat"))
        self.assertEqual(lon1, resp.get("positions")[0].get("long"))
        resp = json.loads(self.app.post("/position",
                                        data=json.dumps({"lat": lat2, "lon": lon2}),
                                        content_type='application/json',
                                        ).data
        )
        id = resp.get("id")
        self.assertEqual(len(id), 24)
        resp = json.loads(self.app.get("/position").data)
        self.assertEqual(len(resp.get("positions")), 2)
        positions = resp.get("positions")
        self.assertIn(lat1, [i.get("lat") for i in positions])
        self.assertIn(lat2, [i.get("lat") for i in positions])
        self.assertIn(lon1, [i.get("long") for i in positions])
        self.assertIn(lon2, [i.get("long") for i in positions])
        # test limit
        resp = json.loads(self.app.post("/position",
                                        data=json.dumps({"lat": lat3, "lon": lon3}),
                                        content_type='application/json',
                                        ).data
        )
        id = resp.get("id")
        self.assertEqual(len(id), 24)
        resp = json.loads(self.app.get("/position?limit=3").data)
        self.assertEqual(len(resp.get("positions")), 3)
        resp = json.loads(self.app.get("/position?limit=2").data)
        self.assertEqual(len(resp.get("positions")), 2)
        resp = json.loads(self.app.get("/position?limit=1").data)
        self.assertEqual(len(resp.get("positions")), 1)
        print resp

    def test_is_correct_coordinates(self):
        self.assertTrue(is_correct_coordinates(lat="56.327358", lon="43.985191"))
        self.assertTrue(is_correct_coordinates(lat="00.000000", lon="00.000000"))
        self.assertTrue(is_correct_coordinates(lat="-32.321321", lon="-323.32321"))
        self.assertFalse(is_correct_coordinates(lat="43", lon="12"))
        self.assertFalse(is_correct_coordinates(lat="eqwewqeq", lon="eweqweqwew"))
        self.assertFalse(is_correct_coordinates(lat="|}{!@#$%^&*()_", lon="./../.,./,/,/.,."))
        self.assertFalse(is_correct_coordinates(lat="", lon=""))

    def test_work_db(self):
        # insert to db
        data_to_insert = {"lat": "32.23432", "lon": "65.456546"}
        id = insert_to_db(data_to_insert)
        self.assertEqual(len(id), 24)
        # get from db
        resp = get_from_db(data_to_insert)
        self.assertEqual(id, resp[0].get("_id"))
        self.assertEqual(data_to_insert.get("lat"), resp[0].get("lat"))
        self.assertEqual(data_to_insert.get("lon"), resp[0].get("lon"))
        # delete from db
        delete_from_db(id)
        resp = get_from_db(data_to_insert)
        self.assertFalse(resp)

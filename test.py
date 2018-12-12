import unittest
import json
import requests
import crawl_data
import process_data
class TestProject(unittest.TestCase):
    def testplayer(self):
        player_list = crawl_data.get_player()
        self.assertIsInstance(player_list, list)
        self.assertEqual(player_list[0], "A.J. Hammons")
        self.assertEqual(player_list[425], "Stephen Curry")
        self.assertEqual(player_list[485], "Zaza Pachulia")
    
    def testtask1(self):
        result_list = process_data.task1()
        self.assertIsInstance(result_list, list)
        self.assertIsInstance(result_list[100], list)
        self.assertEqual(result_list[0], ["A.J. Hammons", 320])
        self.assertEqual(result_list[484], ["Zach Randolph", 94])
    
    def testtask2(self):
        result_list = process_data.task2("Stephen Curry")
        self.assertIsInstance(result_list, list)
        self.assertEqual(result_list[0], ("Curry", 29))
        self.assertEqual(result_list[9], ('hit', 7))
        result_list = process_data.task2("Lebron James")
        self.assertIsInstance(result_list, list)
        self.assertEqual(result_list[0], ("Lebron", 47))
        self.assertEqual(result_list[5], ('missed', 12))
    
    def testtask3(self):
        result_list = process_data.task3("Stephen Curry")
        self.assertIsInstance(result_list, list)
        self.assertTrue(result_list[0] == "Stephen Curry goes 1v1 against Lebron")

if __name__ == "__main__":
    unittest.main(verbosity=2)

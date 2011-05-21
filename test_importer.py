import unittest
import importer

class KnownItems(unittest.TestCase):
    def setUp(self):
        self.importer = importer.Importer()

    def test_Ragnarok(self):
        materials = {"Tritanium": 3261439000, "Pyerite": 782688500, 
                "Mexallon": 266486400, "Isogen": 47405600, "Nocxium": 13257100,
                "Zydrine": 2361800, "Megacyte": 1180900}
        ingredients = self.importer.get_ingredients("Ragnarok")
        self.assertEqual(materials, ingredients.bundle)

if __name__ == "__main__":
    unittest.main()

import unittest
import itemizer
import evedb

_mineral_group = ["Minerals", "Ore & Minerals ", "Materials", 
                  "Manufacture & Research"]

class MarketGroup(unittest.TestCase):
    def setUp(self):
        self.dbman = evedb.default_connect()
        self.itemizer = itemizer.Itemizer()

    def tearDown(self):
        self.dbman.close()

    def test_no_parent(self):
        group = self.itemizer._market_group(self.dbman, 9)
        self.assertEqual(group, ["Ship Equipment"])

    def test_parent(self):
        group = self.itemizer._market_group(self.dbman, 18)
        self.assertEqual(group, _mineral_group)

    def test_cache(self):
        group1 = self.itemizer._market_group(self.dbman, 449)
        group2 = self.itemizer._market_group(self.dbman, 449)
        self.assertEqual(group1, group2)

class KnownItems(unittest.TestCase):
    def setUp(self):
        self.itemizer = itemizer.Itemizer()

    def test_Tritanium(self):
        # Tritanium marketgroupid = 18
        trit = self.itemizer.get_item("Tritanium")
        self.assertEqual(trit.name, "Tritanium")
        self.assertEqual(trit.volume, 0.01)
        self.assertEqual(trit.market_group, _mineral_group)
        self.assertEqual(trit.materials, {})

    def test_Rifter(self):
        # Rifter marketgroupid = 64, typeid = 587
        min_frig_group = ["Minmatar", "Standard Frigates", "Frigates", "Ships"]
        rifter = self.itemizer.get_item("Rifter")
        self.assertEqual(rifter.name, "Rifter")
        self.assertEqual(rifter.volume, 27289)
        self.assertEqual(rifter.market_group, min_frig_group)
        materials = {"Tritanium": 20524, "Pyerite": 5529, "Mexallon": 1841, 
                     "Isogen": 317, "Nocxium": 118, "Zydrine": 13,
                     "Megacyte": 1}
        for mat_name, mat_quantity in materials.items():
            item, quantity = rifter.materials[mat_name]
            self.assertEqual(item.name, mat_name)
            self.assertEqual(quantity, mat_quantity)
            
if __name__ == "__main__":
    unittest.main()

import unittest
import evedb

class KnownValueItems(unittest.TestCase):
    def setUp(self):
        self.dbman = evedb.DB_Manager("evedb", "postgres", "postgrespass")

    def tearDown(self):
        self.dbman.close()

    def test_name_Tritanium(self):
        """item_by_name should get known data for Tritanium"""
        item = self.dbman.item_by_name("Tritanium")
        self._check_Tritanium(item)

    def test_id_34(self):
        """item_by_name should get known data for id 34"""
        item = self.dbman.item_by_id(34)
        self._check_Tritanium(item)

    def _check_Tritanium(self, item):
        trit = {"name": "Tritanium", "id": 34, "volume": 0.01, 
                "market_group": 18}
        self.assertEqual(item, trit)

    def test_name_nonexistant(self):
        """item_by_name should return None when an item name isn't found"""
        item = self.dbman.item_by_name("xdshfsdfdhrqeqf")
        self.assertEqual(item, None)

    def test_material_18(self):
        """materials should get known data for id 18"""
        known_vals = ((18, 34, 256), (18, 35, 512), (18, 36, 256))
        known_materials = [{"item_id": item_id, "material_id": material_id,
                            "quantity": quantity}
                           for (item_id, material_id, quantity) in known_vals]
        materials = self.dbman.materials(18)
        self.assertEqual(materials, known_materials)

    def test_market_group_5(self):
        """market_group should get known data for id 5"""
        known = {"name": "Standard Frigates", "id": 5, "parent": 1361}
        market_group = self.dbman.market_group(5)
        self.assertEqual(market_group, known)

    def test_market_group_with_NULL(self):
        """market_group gives the parent as None when it is NULL in the db"""
        market_group = self.dbman.market_group(2)
        self.assertEqual(market_group["parent"], None)

if __name__ == "__main__":
    unittest.main()

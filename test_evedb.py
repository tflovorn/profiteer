import unittest
import evedb

class KnownValueItems(unittest.TestCase):
    def test_name_Tritanium(self):
        dbman = evedb.DB_Manager("evedb", "postgres", "postgrespass")
        item = dbman.item_by_name("Tritanium")
        self.assertEqual(item, ("Tritanium", 34, 0.01, 18))

    def test_id_34(self):
        dbman = evedb.DB_Manager("evedb", "postgres", "postgrespass")
        item = dbman.item_by_id(34)
        self.assertEqual(item, ("Tritanium", 34, 0.01, 18))

    def test_material_18(self):
        dbman = evedb.DB_Manager("evedb", "postgres", "postgrespass")
        materials = dbman.materials(18)
        self.assertEqual(materials, [(18, 34, 256), (18, 35, 512), 
                (18, 36, 256)])

    def test_market_group_5(self):
        dbman = evedb.DB_Manager("evedb", "postgres", "postgrespass")
        market_group = dbman.market_group(5)
        self.assertEqual(market_group, ("Standard Frigates", 5, 1361))

if __name__ == "__main__":
    unittest.main()

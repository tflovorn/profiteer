import psycopg2

def default_connect():
    return DB_Manager("evedb", "postgres", "postgrespass")

class DB_Manager(object):
    """Provides an interface into the EVE static data dump for extracting item
    construction information.

    """
    def __init__(self, db_name, db_user, db_password):
        self.open(db_name, db_user, db_password)
        self.cache_item_by_id = {}
        self.cache_item_by_name = {}
        self.cache_materials = {}
        self.cache_market_group = {}

    def open(self, db_name, db_user, db_password):
        """Open the database connection."""
        self._conn = psycopg2.connect(database=db_name, user=db_user, 
                password=db_password)
        self._cur = self._conn.cursor()
        self.connected = True

    def close(self):
        """Close the database connection."""
        self._cur.close()
        self._conn.close()
        self.connected = False

    def item_by_id(self, item_id):
        """Get an item by its id.

        Return a dict of properties for item with given id.  Returns None if no
        item exists with that typeid.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if item_id in self.cache_item_by_id:
            return self.cache_item_by_id[item_id]
        self._cur.execute(
            """SELECT typename, typeid, volume, marketgroupid FROM invtypes 
               WHERE typeid=%s""", (item_id,))
        item = _item_to_dict(self._cur.fetchone())
        self.cache_item_by_id[item_id] = item
        if item is not None:
            self.cache_item_by_name[item["name"]] = item
        return item

    def item_by_name(self, item_name):
        """Get an item by its name.

        Return a dict of properties for item with given name.  Returns None if 
        no item exists with that name.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if item_name in self.cache_item_by_name:
            return self.cache_item_by_name[item_name]
        self._cur.execute(
            """SELECT typename, typeid, volume, marketgroupid FROM invtypes 
               WHERE typename=%s""", (item_name,))
        item = _item_to_dict(self._cur.fetchone())
        self.cache_item_by_name[item_name] = item
        if item is not None:
            self.cache_item_by_id[item["id"]] = item
        return item

    def materials(self, item_id):
        """Get the materials required to make an item by its id.

        Return a list of dicts of properties for each material required to make
        item_id.  Returns None if no item exists with that item_id.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if item_id in self.cache_materials:
            return self.cache_materials[item_id]
        self._cur.execute(
            """SELECT typeid, materialtypeid, quantity FROM invtypematerials
               WHERE typeid=%s""", (item_id,))
        try:
            material_list = _material_dicts(self._cur.fetchall())
            self.cache_materials[item_id] = material_list
            return material_list
        except psycopg2.ProgrammingError:
            self.cache_materials[item_id] = None
            return None

    def market_group(self, market_group_id):
        """Get the market group associated with the id.

        Return a dict of properties for the specified market group.  Returns 
        None if no item exists with that market group id.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if market_group_id in self.cache_market_group:
            return self.cache_market_group[market_group_id]
        self._cur.execute(
            """SELECT marketgroupname, marketgroupid, parentgroupid 
               FROM invmarketgroups WHERE marketgroupid=%s""", 
            (market_group_id,))
        group_list = self._cur.fetchone()
        if group_list is None:
            market_group = None
        else:
            market_group = {"name": group_list[0], "id": group_list[1],
                            "parent": group_list[2]}
        self.cache_market_group[market_group_id] = market_group
        return market_group

def _item_to_dict(item_list):
    if item_list is None:
        return None
    item_dict = {"name": item_list[0], "id": item_list[1],
                 "volume": item_list[2], "market_group": item_list[3]}
    return item_dict

def _material_dicts(material_list):
    if material_list is None:
        return None
    material_list_with_dicts = []
    for item in material_list:
        item_dict = {"item_id": item[0], "material_id": item[1],
                     "quantity": item[2]}
        material_list_with_dicts.append(item_dict)
    return material_list_with_dicts

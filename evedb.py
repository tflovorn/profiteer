import psycopg2

class DB_Manager:
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

        Return (typename, typeid, volume, marketgroupid) for item with given
        id.  Returns None if no item exists with that typeid.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if item_id in self.cache_item_by_id:
            return self.cache_item_by_id[item_id]
        self._cur.execute(
            """SELECT typename, typeid, volume, marketgroupid FROM invtypes 
               WHERE typeid=%s""", (item_id,))
        item = self._cur.fetchone()
        if item is not None:
            self.cache_item_by_id[item_id] = item
            self.cache_item_by_name[item[0]] = item
        return item

    def item_by_name(self, item_name):
        """Get an item by its name.

        Return (typename, typeid, volume, marketgroupid) for item with given
        name.  Returns None if no item exists with that name.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if item_name in self.cache_item_by_name:
            return self.cache_item_by_name[item_name]
        self._cur.execute(
            """SELECT typename, typeid, volume, marketgroupid FROM invtypes 
               WHERE typename=%s""", (item_name,))
        item = self._cur.fetchone()
        if item is not None:
            self.cache_item_by_name[item_name] = item
            self.cache_item_by_id[item[1]] = item
        return item

    def materials(self, item_id):
        """Get the materials required to make an item by its id.

        Return a list whose elements are (materialtypeid, quantity) for each
        material required to make item_id.  Returns None if no item exists with
        that item_id.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if item_id in self.cache_materials:
            return self.cache_materials[item_id]
        self._cur.execute(
            """SELECT typeid, materialtypeid, quantity FROM invtypematerials
               WHERE typeid=%s""", (item_id,))
        try:
            material_list = self._cur.fetchall()
            self.cache_materials[item_id] = material_list
            return material_list
        except psycopg2.ProgrammingError:
            return None

    def market_group(self, market_group_id):
        """Get the market group associated with the id.

        Return (marketgroupname, marketgroupid, parentgroupid) for the 
        specified market group.  Returns None if no item exists with that 
        market group id.

        """
        if not self.connected:
            raise IOError("Database connection not active")
        if item_id in self.cache_market_group:
            return self.cache_market_group[market_group_id]
        self._cur.execute(
            """SELECT marketgroupname, marketgroupid, parentgroupid 
               FROM invtypematerials WHERE marketgroupid=%s""", 
            (market_group_id,))
        market_group = self._cur.fetchone()
        if market_group is not None:
            self.cache_market_group[market_group_id] = market_group
        return market_group
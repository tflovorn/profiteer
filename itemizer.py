import evedb

class Itemizer(object):
    def __init__(self):
        self.item_cache = {}
        self.market_group_cache = {}

    def get_item(self, name):
        if name in self.item_cache:
            return self.item_cache[name]
        dbman = evedb.default_connect()
        item_data = dbman.item_by_name(name)
        if item_data is None:
            raise KeyError("Item with name %s not found" % name)
        market_group = self._market_group(dbman, item_data["market_group"])
        materials = self._materials(dbman, item_data["id"])
        dbman.close()
        item = Item(item_data["name"], item_data["volume"], market_group, 
                    materials)
        self.item_cache[item_data["name"]] = item
        return item

    def _get_item_by_id(self, dbman, item_id):
        item_data = dbman.item_by_id(item_id)
        return self.get_item(item_data["name"])

    def _market_group(self, dbman, group_id):
        if group_id in self.market_group_cache:
            return self.market_group_cache[group_id]
        group_data = dbman.market_group(group_id)
        market_group = [group_data["name"]]
        parent = group_data["parent"]
        if parent is not None:
            market_group.extend(self._market_group(dbman, parent))
        self.market_group_cache[group_id] = market_group
        return market_group

    def _materials(self, dbman, item_id):
        '''Recursively calls get_item to build the material tree.'''
        material_data = dbman.materials(item_id)
        materials = {}
        for material in material_data:
            mat_item = self._get_item_by_id(dbman, material["material_id"])
            materials[mat_item.name] = ((mat_item, material["quantity"]))
        return materials

class Item(object):
    def __init__(self, name, volume, market_group, materials):
        self.name = name
        self.volume = volume
        self.market_group = market_group
        self.materials = materials

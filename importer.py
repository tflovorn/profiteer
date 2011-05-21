import itemizer

class Importer(object):
    def __init__(self):
        self.itemizer = itemizer.Itemizer()

    def get_ingredients(self, item_name, quantity=1, bundle=None, 
            stop_names=None, stop_groups=None):
        if stop_names is None:
            stop_names = []
        if stop_groups is None:
            stop_groups = []
        if bundle is None:
            bundle = Ingredients()
        stop_by_groups = lambda item: any([item.in_group(market_group) for 
                market_group in stop_groups])
        item = self.itemizer.get_item(item_name)
        if (item_name in stop_names or stop_by_groups(item) or
                len(item.materials) == 0):
            bundle.add(item_name, quantity)
            return bundle
        for mat_name, (mat_item, mat_quantity) in item.materials.items():
            self.get_ingredients(mat_name, quantity * mat_quantity, bundle,
                    stop_names, stop_groups)
        return bundle

class Ingredients(object):
    def __init__(self):
        self.bundle = {}

    def add(self, name, quantity):
        if name in self.bundle:
            self.bundle[name] += quantity
        else:
            self.bundle[name] = quantity

    def __str__(self):
        return '\n'.join(["%s, %s" % (name, quantity) for name, quantity in 
                self.bundle.items()])

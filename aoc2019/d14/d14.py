'''
gduarte@home-vm
Created on 29-ago-2021
'''


def ceil(x):
    if (x - int(x)) > 0:
        return int(x) + 1
    else:
        return int(x)


class Reactions:
    def __init__(self, fname):
        with open(fname) as f:
            lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l.split(' => ') for l in lines]
        recipes = {}
        for l in lines:
            qty, k = l[1].split()
            v = l[0].strip().split(', ')
            recipes[k] = (int(qty), v)
        self.recipes = recipes
        self.stock = {k: 0 for k in self.recipes}
        self.shop_list = {}

    def get_ingredients(self):
        d_iter = self.shop_list.copy()
        for comp, needed in d_iter.items():
            try:
                # KeyError probably means comp == 'ORE'
                per_recipe, recipe = self.recipes[comp]
                # Remove from the list what is being produced
                self.shop_list[comp] -= needed
                # Take the surplus from the stock
                qty = needed - self.stock[comp]
                n_recipes = ceil(qty/per_recipe)
                # Store the surplus
                self.stock[comp] = n_recipes * per_recipe - qty
            except KeyError:
                continue
            for j in recipe:
                v, k = j.split()
                # Add to the list the new ingredients
                try:
                    self.shop_list[k] += n_recipes * int(v)
                except KeyError:
                    self.shop_list[k] = n_recipes * int(v)

    def reset_stock(self):
        self.stock = {k: 0 for k in self.recipes}
        self.shop_list = {}

    def fuel_cost(self, count=1):
        self.shop_list = ({'FUEL': count})
        while tuple(self.shop_list.keys()) != ('ORE',):
            # Iterate until all that's left in the shopping list is ORE
            self.get_ingredients()
            self.shop_list = {k: v for k, v in self.shop_list.items() if v != 0}
        return self.shop_list['ORE']


def part_two(fname):
    r = Reactions(fname)
    l = 0
    h = int(1e12)
    target = int(1e12)
    while l < h:
        # This method converges real quick
        r.reset_stock()
        fuel = (l + h + 1) // 2
        cost = r.fuel_cost(fuel)
        if (cost <= target):
            l = fuel
        else:
            h = fuel - 1
    return l


if __name__ == "__main__":
    r = Reactions('input.dat')
    print(r.fuel_cost())
    print(part_two('input.dat'))

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
        self.shop_cart = {}

    def get_ingredients(self):
        d_iter = self.shop_cart.copy()
        for comp, needed in d_iter.items():
            try:
                per_recipe, recipe = self.recipes[comp]
                # KeyError probably means comp == 'ORE'
                self.shop_cart[comp] -= needed
                qty = needed - self.stock[comp]
                self.stock[comp] = 0
                n_recipes = ceil(qty/per_recipe)
                self.stock[comp] += n_recipes * per_recipe - qty
            except KeyError:
                continue
            for j in recipe:
                v, k = j.split()
                try:
                    self.shop_cart[k] += n_recipes * int(v)
                except KeyError:
                    self.shop_cart[k] = n_recipes * int(v)

    def reset_stock(self):
        self.stock = {k: 0 for k in self.recipes}
        self.shop_cart = {}

    def fuel_cost(self, count=1):
        self.shop_cart = ({'FUEL': count})
        while tuple(self.shop_cart.keys()) != ('ORE',):
            self.get_ingredients()
            self.shop_cart = {k: v for k, v in self.shop_cart.items() if v != 0}
        return self.shop_cart['ORE']


def part_two(fname):
    r = Reactions(fname)
    l = 0
    h = int(1e12)
    target = int(1e12)
    while l < h:
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

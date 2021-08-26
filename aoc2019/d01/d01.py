import numpy as np

masses     = np.genfromtxt("input.dat")
total_fuel = np.zeros_like(masses, dtype=int)
mod_fuel   = np.zeros_like(masses, dtype=int)

calc_fuel = lambda mass : ( np.int(mass/3) - 2 )

for i,m in enumerate(masses):
    fuel = calc_fuel(m)
    mod_fuel[i] = fuel
    while fuel > 0:
        total_fuel[i] += fuel
        fuel = calc_fuel(fuel)

print("Fuel req = %d" % mod_fuel.sum() )
print("Fuel req + extra = %d" %total_fuel.sum() )

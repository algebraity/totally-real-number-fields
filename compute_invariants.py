from sage.all import *

# Compute the invariants of the number field K.
def compute_field(K):
    # Basic data
    poly = K.defining_polynomial()
    dK = K.discriminant()                           
    hK = K.class_number()                           
    rK = K.regulator()                              
    mb = K.minkowski_bound()

    # Unit group
    U = K.unit_group()
    fu = U.fundamental_units()
    tor = U.torsion_subgroup()
    
    # Prime ramification
    primes = dK.prime_factors()
    prime_ram_data = {}
    for p in primes:
        i = K.ideal(p)
        p_data = []
        for factor in i.prime_factors():
            p_data.append([factor, factor.ramification_index()])
        prime_ram_data[p] = p_data

    int_base = K.integral_basis()

    # Automorphisms and Galois theory
    autos = K.automorphisms()
    galois_grp = K.galois_group()
    galois_clsr = K.galois_closure()

    field_data = {}
    field_data["min_poly"] = poly
    field_data["dk"] = dK
    field_data["hk"] = hK
    field_data["rk"] = rK
    field_data["mb"] = mb
    field_data["unit_group"] = U
    field_data["fund_units"] = fu
    field_data["unit_tor_sbgrp"] = tor
    field_data["ramified_primes"] = prime_ram_data
    field_data["int_basis"] = int_base
    field_data["auto_group"] = autos
    field_data["galois_group"] = galois_grp
    field_data["galois_clsr"] = galois_clsr

# Compute the field invariants of the first n real quadratic fields
def compute_invariants(n):
    orig_n = n
    invariants = {}
    i = 2
    while n > 0:
        if is_squarefree(i):
            x = polygen(ZZ, 'x')
            K = NumberField(x**Integer(2) - i, names=('u',))
            invariants[K] = compute_field(K)
            n-=1
        i+=1

        if n-1 > 0 & (i % 10 == 0):
            print(str(round(((orig_n-n) / (orig_n))*100, 2)) + "%")
    return invariants

from sage.all import *
import json
import time
import os
import multiprocessing as mp
import numpy as np

os.makedirs("data", exist_ok=True)

JOBS = mp.cpu_count()
jobs = JOBS

def main(deg=-1, d_bound=10**6):
    if deg == -1:
        deg = int(input("Enter the degree of the fields to compute: "))
        while not (isinstance(deg, int)) and not (n > 0):
            n = int(input("Input not accepted. Enter 0 for real and 1 for imaginary: "))
        d_bound = int(input("Enter a bound for the discriminant: "))

    invariants = compute_invariants(deg, d_bound)

    file_name = os.path.join("data", "field_data_deg_" + str(deg) + "_d-bound_" + str(d_bound) + ".json")
    to_json(invariants, file_name)

def serialize_field(field_data):
    out = {}

    out["field"] = str(field_data["field"])
    out["min_poly"] = str(field_data["min_poly"])
    out["dk"] = int(field_data["dk"])
    out["hk"] = int(field_data["hk"])

    out["rk"] = float(field_data["rk"])
    out["mb"] = float(field_data["mb"])

    out["class_number"] = int(field_data["class_group"])

    out["fund_units"] = [str(u) for u in field_data["fund_units"]]
    out["unit_tor"] = int(field_data["unit_torsion"])

    out["ramified_primes"] = {
        int(p): [[str(I), int(e)] for (I, e) in data]
        for p, data in field_data["ramified_primes"].items()
    }

    out["auto_group"] = [str(phi) for phi in field_data["auto_group"]]

    out["galois_group"] = str(field_data["galois_group"])
    out["galois_clsr"] = str(field_data["galois_clsr"])

    return out

def to_json(invariants, filename):
    print("Saving data to", filename)
    to_store = [serialize_field(field) for field in invariants]

    with open(filename, 'w') as json_file:
        json.dump(to_store, json_file, indent=2)

def compute_field(K):
    poly = K.defining_polynomial()
    dK = K.discriminant()
    C = K.class_group()
    hK = K.class_number()                           
    rK = K.regulator()                              
    mb = K.minkowski_bound()
    U = K.unit_group()

    fu = [str(u) for u in U.fundamental_units()]
    tor = U.torsion_subgroup()
    
    primes = dK.prime_factors()
    prime_ram_data = {}
    for p in primes:
        i = K.ideal(p)
        p_data = []
        for factor in i.prime_factors():
            p_data.append([repr(factor), int(factor.ramification_index())])
        prime_ram_data[p] = p_data

    int_base = K.integral_basis()

    autos = K.automorphisms()
    galois_grp = K.galois_group()
    galois_clsr = K.galois_closure('v')

    field_data = {}
    field_data["field"] = repr(K)
    field_data["min_poly"] = repr(poly)
    field_data["dk"] = int(dK)
    field_data["hk"] = int(hK)
    field_data["rk"] = float(rK)
    field_data["mb"] = float(mb)
    field_data["class_group"] = int(C.order())
    field_data["fund_units"] = fu
    field_data["unit_torsion"] = int(tor.order())
    field_data["ramified_primes"] = prime_ram_data
    field_data["int_basis"] = int_base
    field_data["auto_group"] = autos
    field_data["galois_group"] = repr(galois_grp)
    field_data["galois_clsr"] = repr(galois_clsr)

    return field_data


def compute_invariants(deg, d_bound):
    computed_fields = enumerate_totallyreal_fields_prim(deg, d_bound)
    fields = [(int(disc), str(poly)) for (disc, poly) in computed_fields]
    print("Finished enumerating " + str(len(fields)) + " fields.")
    field_data = []
    try:
        ctx = mp.get_context("fork")
    except ValueError:
        ctx = mp.get_context()

    with ctx.Pool(processes=jobs) as pool:
        for field in pool.imap_unordered(_worker, fields, chunksize=200):
            field_data.append(field)

    return field_data


def _worker(item):
    disc, poly = item
    R = PolynomialRing(QQ, 'x')
    p = R(poly)
    K = NumberField(p, 'u')
    return compute_field(K)

if __name__ == "__main__":
    main()



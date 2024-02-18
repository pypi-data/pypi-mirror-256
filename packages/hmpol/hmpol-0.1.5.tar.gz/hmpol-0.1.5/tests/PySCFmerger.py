from pyscf import gto
from ase.io import read
from hmpol import Pols
import numpy as np
from ase.visualize import view
from ase.units import Bohr, Ha


mol = gto.Mole()
molecule = read("monomerA.xyz")
mol.atom = "monomerA.xyz" 
mol.basis = "augccpvqz"
mol.build()


field_strength_F = 0.00486/Ha*Bohr


pols = Pols(molecule,mol, irrep=False, field_strength_F=field_strength_F)

print(pols.calc_dd_pol())
print(pols.calc_dq_pol())
print(pols.calc_qq_pol())
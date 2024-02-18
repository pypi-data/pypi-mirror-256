import sys
sys.path.append("../")
from poltensor import Pols
from pyscf import gto
from ase.io import read
from poltensor import Pols
import numpy as np 

mol = gto.Mole()
molecule = read("monomerA.xyz")
mol.atom = "monomerA.xyz" 
mol.basis = "augccpvqz"
mol.build()

AIJKIrrep   = np.load("H2O_mono_AIJK_Trrep.npy")
AIJK        = np.load("H2O_mono_AIJK.npy")
CIJKLIrrep  = np.load("H2O_mono_CIJKL_Trrep.npy")
CIJKL       = np.load("H2O_mono_CIJKL.npy")

def test_poltensor_AijkIrrep():
    print("Testing Aijk Irreducible representation")
    assert Pols(molecule,mol,irrep=True).calcAijk() == AIJKIrrep

def test_poltensor_AijkFullmat():
    print("Testing Aijk Full matrix representation")
    assert Pols(molecule,mol,irrep=False).calcAijk() == AIJK


def test_poltensor_CijklIrrep():
    print("Testing Cijkl Irreducible representation")
    assert Pols(molecule,mol,irrep=True).calcCijkl() == CIJKLIrrep

def test_poltensor_CijklFullmat():
    print("Testing Cijkl Full matrix representation")
    assert Pols(molecule,mol,irrep=False).calcCijkl() == CIJKL

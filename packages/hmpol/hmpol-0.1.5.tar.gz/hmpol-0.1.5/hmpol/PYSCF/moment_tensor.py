"""
Author: Anoop Ajaya Kumar Nair
Date: 2023-10-24
Last update: 2024-02-12
Description: Code calculates:
    - Density cube
    - Quadrupole

Contact Details:
- Email: mailanoopanair@gmail.com
- Company: University of Iceland
- Job Title: Doctoral researcher
"""

import numpy
from pyscf import lib
from pyscf.dft import numint, gen_grid
from pyscf import __config__

RESOLUTION = getattr(__config__, 'cubegen_resolution', None)
BOX_MARGIN = getattr(__config__, 'cubegen_box_margin', 10.0)
ORIGIN = getattr(__config__, 'cubegen_box_origin', None)
EXTENT = getattr(__config__, 'cubegen_box_extent', None)
import numpy as np


class Cube(object):
    def __init__(self, mol, nx=80, ny=80, nz=80, resolution=RESOLUTION,
                 margin=BOX_MARGIN, origin=ORIGIN, extent=EXTENT):
        from pyscf.pbc.gto import Cell
        self.mol = mol
        coord = mol.atom_coords()
        # print(coord)

        if isinstance(mol, Cell):
            self.box = mol.lattice_vectors()
            atom_center = (numpy.max(coord, axis=0) + numpy.min(coord, axis=0))/2
            box_center = (self.box[0] + self.box[1] + self.box[2])/2
            self.boxorig = atom_center - box_center
        else:
            
            if extent is None:
                extent = numpy.max(coord, axis=0) - numpy.min(coord, axis=0) + 2*margin
                extent.fill(np.max(extent))

            self.box = numpy.diag(extent)
            if origin is None:
                origin = np.zeros(3)
                origin.fill(numpy.min(coord) - margin)
            self.boxorig = numpy.asarray(origin)

        if resolution is not None:
            nx, ny, nz = numpy.ceil(numpy.diag(self.box) / resolution).astype(int)

        self.nx = nx
        self.ny = ny
        self.nz = nz

        if isinstance(mol, Cell):
            # Use an asymmetric mesh for tiling unit cells
            self.xs = numpy.linspace(0, 1, nx, endpoint=False)
            self.ys = numpy.linspace(0, 1, ny, endpoint=False)
            self.zs = numpy.linspace(0, 1, nz, endpoint=False)
        else:
            self.xs = numpy.linspace(0, 1, nx, endpoint=True)
            self.ys = numpy.linspace(0, 1, ny, endpoint=True)
            self.zs = numpy.linspace(0, 1, nz, endpoint=True)


    def get_coords(self) :
        """  Result: set of coordinates to compute a field which is to be stored
        in the file.
        """
        frac_coords = lib.cartesian_prod([self.xs, self.ys, self.zs])
        return frac_coords @ self.box + self.boxorig # Convert fractional coordinates to real-space coordinates

    def get_ngrids(self):
        return self.nx * self.ny * self.nz

    def get_volume_element(self):
        return (self.xs[1]-self.xs[0])*(self.ys[1]-self.ys[0])*(self.zs[1]-self.zs[0])






def density(mol, dm, outfile=None, nx=80, ny=80, nz=80,  resolution=RESOLUTION,
            margin=BOX_MARGIN):

    from pyscf.pbc.gto import Cell
    cc = Cube(mol, nx, ny, nz, resolution, margin)

    GTOval = 'GTOval'
    if isinstance(mol, Cell):
        GTOval = 'PBC' + GTOval

    # Compute density_val on the .cube grid
    coords = cc.get_coords()
    ngrids = cc.get_ngrids()
    grid_point_position = coords.reshape(nx, ny, nz,3)

    grid_spacing = np.zeros(3)
    hv1 = grid_point_position[0,0,0]-grid_point_position[1,0,0]
    hv2 = grid_point_position[0,0,0]-grid_point_position[0,1,0]
    hv3 = grid_point_position[0,0,0]-grid_point_position[0,0,1]
    grid_spacing[0] = abs(hv1[0])
    grid_spacing[1] = abs(hv2[1])
    grid_spacing[2] = abs(hv3[2])



    blksize = min(8000, ngrids)
    density_val = numpy.empty(ngrids)
    for ip0, ip1 in lib.prange(0, ngrids, blksize):
        ao = mol.eval_gto(GTOval, coords[ip0:ip1])
        density_val[ip0:ip1] = numint.eval_rho(mol, ao, dm)
    density_val = density_val.reshape(cc.nx,cc.ny,cc.nz)

    # Write out density_val to the .cube file
    if outfile !=None:
        cc.write(density_val, outfile, comment='Electron density_val in real space (e/Bohr^3)')
    return density_val,[nx,ny,nz],grid_spacing,grid_point_position

def quadpole_electric_comp(grid_spacing,center_of_mass,density_val,grid_points,grid_point_position):

    dV = grid_spacing[0] * grid_spacing[1] * grid_spacing[2] #done

    Q_ab = np.zeros(6)
    for i in range(0,grid_points[0]):
        x = i * grid_spacing[0]
        for j in range(0,grid_points[1]):
            y = j* grid_spacing[1]
            for k in range(0,grid_points[2]):
                z = k * grid_spacing[2]
                r = np.zeros(3)
                r[0] = grid_point_position[i,j,k,0] - center_of_mass[0]
                r[1] = grid_point_position[i,j,k,1] - center_of_mass[1] 
                r[2] = grid_point_position[i,j,k,2] - center_of_mass[2] 
                rr = (r[0] * r[0] + r[1] * r[1] + r[2] * r[2])
                rq = rr / 3.0
                cd = density_val[i,j,k] * dV

                cq = cd * 3.0 / 2.0
                Q_ab[0] += cq * (r[0] * r[0] - rq)
                Q_ab[1] += cq * r[0] * r[1]
                Q_ab[2] += cq * r[0] * r[2]
                Q_ab[3] += cq * (r[1] * r[1] - rq)
                Q_ab[4] += cq * r[1] * r[2]
                Q_ab[5] += cq * (r[2] * r[2] - rq)
    quadPole = np.zeros((3,3))
    quadPole[0,0] = Q_ab[0] 
    quadPole[0,1] = quadPole[1,0] =  Q_ab[1] 
    quadPole[0,2] = quadPole[2,0] =  Q_ab[2] 
    quadPole[1,1] = Q_ab[3] 
    quadPole[1,2] = quadPole[2,1] =  Q_ab[4] 
    quadPole[2,2] = Q_ab[5] 
    return quadPole


def calc_center_of_mass(mol):
    atomic_mass  = mol.atom_mass_list()
    atomic_positions   = mol.atom_coords(unit = 'Bohr')
    center_of_mass = np.matmul(atomic_mass.reshape(1,-1),atomic_positions.reshape(-1,3))/atomic_mass.sum()
    return center_of_mass[0]

def quadpole_nuclear_comp(mol):
    charges = mol.atom_charges()
    coords = mol.atom_coords(unit = 'Bohr')
    COM = calc_center_of_mass(mol)
    coordsMod = coords-COM
    # print("qcoord",coordsMod)

    rval = np.sum(np.square(coordsMod),axis=1)
    Quad  = np.zeros((3,3))
    for i in range(len(charges)):
        rvalDiag = np.zeros((3,3))
        rvalDiag[0,0] =  -rval[i]/2.0
        rvalDiag[1,1] =  -rval[i]/2.0
        rvalDiag[2,2] =  -rval[i]/2.0
        Quad += charges[i]*(3.0/2.0*np.outer(coordsMod[i],coordsMod[i])+rvalDiag)

 
    return Quad

def quadrupole(mol,mf):
    quadpole_nuclear_component = quadpole_nuclear_comp(mol)
    center_of_mass = calc_center_of_mass(mol)
    density_val,grid_points,grid_spacing,grid_point_position = density(mol, mf.make_rdm1())
    quadpole_electric_component = quadpole_electric_comp(grid_spacing,center_of_mass,density_val,grid_points,grid_point_position)
    quadrupole_ij = np.round(quadpole_nuclear_component-quadpole_electric_component,4)
    return quadrupole_ij






# This file defines 

import os

import numpy as np
import pandas as pd

# The atom fields defined by PDB for .pdb files
# Check http://pdb101.rcsb.org/ for more information
ATOM_FIELD = [
    'group_PDB',
    'id',
    'label_atom_id',
    'label_comp_id',
    'label_asym_id',
    'auth_comp_id',
    'Cartn_x',
    'Cartn_y',
    'Cartn_z',
    'occupancy',
    'B_iso_or_equiv',
    'type_symbol'
]


def readlines(input_dir):
    """ Read pdb files line by line and get the annotations for atoms.

    Argument:
        input_dir: directory of the pdb file

    Return:
        atoms: a DataFrame contains relevant atom annotations

    Usage:
        >>> readlines(./directory/to/your/pdb/file')
    """
    with open(input_dir, 'r') as pdb:
        line = pdb.readline()
        atoms = []
        while line:
            line = pdb.readline()
            if line[0:4] == 'ATOM':
                columns = [
                    line[0:4].replace(' ', ''),             # group_PDB
                    int(line[5:11].replace(' ', '')),       # id
                    line[13:16].replace(' ', ''),           # label_atom_id
                    line[16:20].replace(' ', ''),           # label_comp_id
                    line[20:22].replace(' ', ''),           # label_asym_id
                    int(line[22:26].replace(' ', '')),      # auth_comp_id
                    float(line[31:38].replace(' ', '')),    # Cartn_x
                    float(line[38:46].replace(' ', '')),    # Cartn_y
                    float(line[46:54].replace(' ', '')),    # Cartn_z
                    float(line[54:60].replace(' ', '')),    # occupancy
                    float(line[60:66].replace(' ', '')),    # B_iso_or_equiv
                    line[77:78].replace(' ', '')            # type_symbol
                ]
                atoms.append({ATOM_FIELD[i]: columns[i]
                              for i in range(len(ATOM_FIELD))})
            else:
                pass

        atoms = pd.DataFrame(atoms)

        return atoms


class PDBDataset():
    """ class for PDB Dataset.

    Usage:
    >>> pdbs = PDBDataset('./directory/to/your/pdb/dataset', ext='.pdb')
    >>> pdbs[32]
    >>> pdbs['4HHB']
    """
    def __init__(self, input_dir, ext='.pdb'):
        self.dir = input_dir
        self.ext = ext
        self.pdbs = [os.path.splitext(i)[0] for i in os.listdir(input_dir)]
        self.num = len(self.pdbs)
        self.ATOM_FIELD = ATOM_FIELD

        print('Read dataset from directory {}.'.format(input_dir))
        print('Read {} pdbs.'.format(self.num))

    def __len__(self):
        return self.num

    def __getitem__(self, key):
        if type(key) == int:
            if key < 0 or key >= self.num:
                raise IndexError(
                    'Index {} out of the range. The dataset only contains {} pdb files.'.format(key, self.num)
                )
            else:
                return readlines(os.path.join(self.dir, self.pdbs[key] + self.ext))
        elif type(key) == str:
            if key not in self.pdbs:
                raise IndexError(
                    '{} not found in the PDB dataset.'.format(key)
                )
            else:
                return readlines(os.path.join(self.dir, key + self.ext))
        else:
            raise KeyError(
                'The key must be integer or string for index.'
            )


if __name__ == '__main__':
    dataset = PDBDataset('pdb')
    print(dataset[0])
    print(dataset['4HHB'])

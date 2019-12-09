class ProcessLig(object):

    def __init__(self, *args):
        import os
        self.args = list(args)
        self.temp_illustration = self.args[0]
        self.charge_model = self.args[1]
        self.line = [_.strip() for _ in open(self.temp_illustration)]
        lig_label = '# small molecule part from complex with split code.'
        self.name = 'empty_ligand.pdb'
        if lig_label in self.line:
            self.name = self.line[self.line.index(lig_label)+1]
        else:
            if len(self.args) == 2:
                os.mknod('empty_ligand.pdb')
                with open(self.temp_illustration, 'a') as tmp_f0:
                    tmp_f0.write('# To avoid failure when itself without ligand, build a empty ligand file.\n\t%s\n' %self.name)
            else:
                self.name = self.args[-1]

    def format_conversion(self):
        '''
            A Tool: convert the small molecules from the origin format to the object format.
            meanwhile, it will add hydrogen and give atomic particle charge under charge model:
            (eem, eem2015ba, eem2015bm, eem2015bn, eem2015ha, eem2015hm, eem2015hn, eqeq,
             fromfile, gasteiger, mmff94, none, qeq, qtpie).
        '''
        import os, sys
        try:
            import pybel
        except Exception as exc:
            sys.stdout.write('\n\033[1;31mThere is a problem:\033[0m\t%s\n' %exc)
            sys.exit('\n\033[1;36mPlease use pip/conda to install it or append its path to PYTHONPATH.\033[0m\n')
        with open(self.temp_illustration, 'a') as tmp_f0:
            tmp_f0.write('# ligand with charge from pybel(charge model: %s).\n\t%s\n' %(self.charge_model, 'lig_pybel.mol2'))

        with open('lig_pybel.mol2', 'w') as lig_object:
            for lig_file in list(self.name.split(',')):
                in_format = lig_file.split('.')[-1]
                in_put = lig_file.strip()
                out_put = pybel.Outputfile('mol2', 'lig_pybel_tmp.mol2')
                mol = list(pybel.readfile(in_format, in_put))[0]
                mol.addh()
                mol.calccharges(model=self.charge_model)
                out_put.write(mol)
                lig_object.writelines([_ for _ in open('lig_pybel_tmp.mol2')])
                os.unlink('lig_pybel_tmp.mol2')

    def ligand_charge(self, mol2charge=0):
        import os
        if mol2charge:
            os.system('cp %s lig_pybel.mol2' %self.name.split(',')[0])
        else:
            self.format_conversion()
        molecule_count = []; paras = []
        each_line = [_m.rstrip() for _m in open('lig_pybel.mol2')]
        for i in range(len(each_line)):
            if each_line[i].startswith('@<TRIPOS>MOLECULE'): molecule_count.append(i)
        molecule_count.append(len(each_line))
        for pp in range(len(molecule_count)-1):
            pline = each_line[molecule_count[pp]:molecule_count[pp+1]]
            atom_info = pline.index('@<TRIPOS>ATOM')
            bond_info = pline.index('@<TRIPOS>BOND')
            if '@<TRIPOS>SUBSTRUCTURE' in pline:
                subs_info = pline.index('@<TRIPOS>SUBSTRUCTURE')
            else:
                subs_info = len(pline)
            x = [0]; y = [0]; z = [0]; natom = [0]; charge = [0]
            resn_resi = [0]; hybrid = [0]; before_charge = [0]; after_charge = [0]
            for i in range(atom_info+1, bond_info):
                natom.append(pline[i][7:14].strip())
                x.append(float(pline[i][16:26].strip()))
                y.append(float(pline[i][26:36].strip()))
                z.append(float(pline[i][36:46].strip()))
                charge.append(float(pline[i][67:77].strip()))
                before_charge.append(pline[i][:67])
                after_charge.append(pline[i][77:])
                resn_resi.append(pline[i][58:67].strip())
                hybrid.append(pline[i][46:53].strip())
            b1 = []; b2 = []
            for i in range(bond_info+1, subs_info):
                b1.append(int(pline[i].split()[1].strip()))
                b2.append(int(pline[i].split()[2].strip()))
            paras.append([pline, atom_info, bond_info, natom, hybrid, before_charge, after_charge, b1, b2, resn_resi, x, y, z, charge])
        return paras

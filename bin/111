# Author : GuanFu Duan
# Email : gfduan178@163.com
# Supervisor : Changge Ji
# All rights reserved 2019
# process recptor with openmm
# Dependencies : opemmm, pdbfixer, openbabel, pybel

class ProcessRec(object):

    def __init__(self, temp_illustration):
        import os
        # obtain the receptor filename and extension
        self.temp_illustration = temp_illustration
        self.line = [_.strip() for _ in open(self.temp_illustration)]
        #charge_label = '# The parameters of residue charge information under force field(MMFF94).'
        self.charge_dat = 'mmff94.dat'
        #self.charge_dat = self.line[self.line.index(charge_label)+1]
        self.name = self.line[self.line.index('# receptor part from complex with split code.')+1]
        self.shotname, self.extension = os.path.splitext(self.name)

    def add_hydrogens_by_openmm(self):
        from simtk.openmm.app import ForceField, Modeller, PDBFile
        from pdbfixer import PDBFixer
        fixer = PDBFixer(self.name)
        field = ForceField('amber99sb.xml', 'tip3p.xml')
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        fixer.addMissingHydrogens(7.0)
        modeller = Modeller(fixer.topology, fixer.positions)
        modeller.addHydrogens(forcefield=field)
        modeller.deleteWater()
        PDBFile.writeModel(modeller.topology, modeller.positions, open(self.shotname+'_h.pdb', 'w'))

    def amino_charge_amber99sb(self):
        charge_dat = [_ for _ in open(self.charge_dat) if _[:1] != ';']
        resn_atom_charge = {}; uniq_res = []
        for dat in charge_dat:
            if dat.split()[0].strip() not in uniq_res:
                uniq_res.append(dat.split()[0].strip())
                resn_atom_charge[dat.split()[0].strip()] = {}
        for dat in charge_dat:
            tmp_dat = dat.split()
            if tmp_dat[0].strip() in uniq_res:
                resn_atom_charge[tmp_dat[0].strip()][tmp_dat[1].strip()] = float(tmp_dat[2].strip())
        return resn_atom_charge

    def receptor_charge(self):
        import re
        # obtain the residue information with charge under amber99sb
        resn_atom_charge = self.amino_charge_amber99sb()
        # add hydrogens for receptor
        self.add_hydrogens_by_openmm()
        # add information to tmp file
        tmp_f0 = open(self.temp_illustration, 'a')
        tmp_f0.write('# add hydrogens and missing residues & atoms by openmm.\n\t%s\n' %(self.shotname+'_h.pdb'))

        pdb_line = [_ for _ in open(self.shotname+'_h.pdb')]
        resn_chain_resi_uniq = []; atom_info = []; pdb_res = []
        for line in pdb_line:
            if line.startswith('ATOM'):
                res_info = re.sub('\W', '', line[17:28].strip())
                if res_info not in resn_chain_resi_uniq:
                    resn_chain_resi_uniq.append(res_info)
                    pdb_res.append(line[17:20].strip())
        for each_res in resn_chain_resi_uniq:
            tmp_atom = []
            for line in pdb_line:
                if line.startswith('ATOM') and re.sub('\W', '', line[17:28].strip()) == each_res:
                    tmp_atom.append(line[11:17].strip())
            atom_info.append(tmp_atom)
        new_resn = resn_chain_resi_uniq[:]; C_terminal = []; N_terminal = []
        # indentify the HID, HIP, HIE, HIS and the terminal residue
        for i in range(len(atom_info)):
            if 'HD1' in atom_info[i] and 'HE2' in atom_info[i] and pdb_res[i] == 'HIS': pdb_res[i] = 'HIP'
            if 'HD1' in atom_info[i] and 'HE2' not in atom_info[i] and pdb_res[i] == 'HIS': pdb_res[i] = 'HID'
            if 'HD1' not in atom_info[i] and 'HE2' in atom_info[i] and pdb_res[i] == 'HIS': pdb_res[i] = 'HIE'
            if 'OXT' in atom_info[i]:
                new_resn[i] = 'C' + pdb_res[i]
                C_terminal.append(resn_chain_resi_uniq[i])
            elif 'H3' in atom_info[i]:
                new_resn[i] = 'N' + pdb_res[i]
                N_terminal.append(resn_chain_resi_uniq[i])
            else:
                new_resn[i] = pdb_res[i]
        # write pdb file with charge from amber99sb
        tmp_f0.write('# write pdb file with charge from amber99sb field.\n\t%s\n' %('rec_opemmm.pdb'))
        with open('rec_opemmm.pdb', 'w') as f2:
            form1 = '%s%5s%3s%s%12.6f\n'
            form2 = '%s%3s%s%12.6f\n'
            for line in pdb_line:
                if line.startswith('ATOM'):
                    atom = line[11:17].strip()
                    label = resn_chain_resi_uniq.index(re.sub('\W', '', line[17:28].strip()))
                    if new_resn[label].startswith('N') and atom == 'H':
                        atom = atom + str(1); am = ' H1  '
                        f2.write(form1 %(line[:12], am, pdb_res[label], line[20:].rstrip(), resn_atom_charge[new_resn[label]][atom]))
                    else:
                        f2.write(form2 %(line[:17], pdb_res[label], line[20:].rstrip(), resn_atom_charge[new_resn[label]][atom]))
                else:
                    f2.write('%s\n' %line.rstrip())
        amber_line = [_.rstrip() for _ in open('rec_opemmm.pdb')]
        atom_name = [0]; resn = [0]; resn_chain_resi = [0]; px = [0]; py = [0]; pz = [0]; pc = [0]; uniq_rcr = []
        for every_line in amber_line:
            if every_line.startswith('ATOM'):
                atom_name.append(every_line[11:17].strip())
                resn.append(every_line[17:20].strip())
                tmp_rcr = re.sub('\W', '', every_line[17:28].strip())
                resn_chain_resi.append(tmp_rcr)
                if tmp_rcr not in uniq_rcr: uniq_rcr.append(tmp_rcr)
                px.append(float(every_line[30:38].strip()))
                py.append(float(every_line[38:46].strip()))
                pz.append(float(every_line[46:54].strip()))
                pc.append(float(every_line.split()[-1].strip()))
        return uniq_rcr, C_terminal, N_terminal, amber_line, atom_name, resn, resn_chain_resi, px, py, pz, pc

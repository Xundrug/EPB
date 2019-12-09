class UpdateCharge(object):
    def __init__(self, *args):
        self.lig_args, self.rec_args, self.lig_polar_args, self.output_ligfile, self.out_form, self.temp_illustration = args

    def polar_ligand(self):
        import numpy as np
        atom_b = self.lig_args[0][0].index('@<TRIPOS>ATOM')
        bond_b = self.lig_args[0][0].index('@<TRIPOS>BOND')
        if bond_b-atom_b == 1: return
        import math, os, re, openbabel
        ff = '%4s%7d %4s %3s %s%4d    %8.3f%8.3f%8.3f%6.2f%12.6f\n'
        rec_x, rec_y, rec_z, rec_c = self.rec_args[-4:]
        atom_hybrid, lig_k, lig_d = self.lig_polar_args
        form = '%7s %7s%9s%7s      %12.6f%12.6f%12.6f%12.6f\n'
        small, tmp_label = [';' + '=' * 86 + '\n'], ''
        small.append(';                                                           CHARGE\n')
        small.append(';  ATOM1   ATOM2  hybrid1  hybrid2         OLD-I      OLD-II      NEW-I       NEW-II\n')
        small.append(';' + '-' * 86 + '\n')
        tmp_f0 = open(self.temp_illustration, 'a')
        with open(self.output_ligfile + '.mol2', 'w') as f2:
            for lig_num in range(len(self.lig_args)):
                new_lig_line = []
                if lig_num == 0:
                    small.append(' %86s\n' %(' molecule ' + str(lig_num+1) + ' ').center(86, '*'))
                else:
                    small.append('\n %86s\n' %(' molecule ' + str(lig_num+1) + ' ').center(86, '*'))
                sline, atom_info, bond_info, natom, hybrid, b_charge, a_charge, b1, b2, res, lig_x, lig_y, lig_z, lig_c = self.lig_args[lig_num]
                uc, replace_charge = lig_c[:], {}
                for i in range(len(b1)):
                    bond1 = hybrid[b1[i]] + hybrid[b2[i]]
                    bond2 = hybrid[b2[i]] + hybrid[b1[i]]
                    n1, n2, label, delta_potential = 0, 0, 0, 0.0
                    for j in range(len(atom_hybrid)):
                        if bond1 == atom_hybrid[j]:
                            n1, n2, label = b1[i], b2[i], j
                        if bond2 == atom_hybrid[j]:
                            n1, n2, label = b2[i], b1[i], j
                        if n1 != 0 and n2 != 0:
                            for k in range(1, len(rec_x)):
                                dis1 = math.sqrt((rec_x[k]-lig_x[n1])**2+(rec_y[k]-lig_y[n1])**2+(rec_z[k]-lig_z[n1])**2)
                                dis2 = math.sqrt((rec_x[k]-lig_x[n2])**2+(rec_y[k]-lig_y[n2])**2+(rec_z[k]-lig_z[n2])**2)
                                delta_potential = delta_potential + rec_c[k]/dis2 - rec_c[k]/dis1
                            break
                    if n1 != 0 and n2 != 0:
                        for ppp in range(len(b1)):
                            if ppp != i:
                                new_bond1 = hybrid[b1[ppp]]+hybrid[b2[ppp]]
                                new_bond2 = hybrid[b2[ppp]]+hybrid[b1[ppp]]
                                if (hybrid[n1]+hybrid[n2]) == 'S.3H':
                                    if 'O.3C.ar' in [new_bond1, new_bond2]:
                                        lig_k[label] = 2.85000
                                if (hybrid[n1]+hybrid[n2]) == 'C.1N.1':
                                    if 'C.1C.ar' in [new_bond1, new_bond2]:
                                        lig_k[label] = 1.28000
                                if (hybrid[n1]+hybrid[n2]) == 'O.3H':
                                    if 'O.3C.ar' in [new_bond1, new_bond2]:
                                        lig_k[label] = 9.15000
                                        lig_d[label] = 0.94000
                                    if 'O.3C.2' in [new_bond1, new_bond2]:
                                        lig_k[label] = 7.74000
                                        lig_d[label] = 0.94000
                                if (hybrid[n1]+hybrid[n2]) == 'C.2H':
                                    if 'C.2O.2' in [new_bond1, new_bond2]: lig_k[label] = 6.35000
                                    if 'C.2S.2' in [new_bond1, new_bond2]: lig_k[label] = 6.35000
                                    if 'C.2N.2' in [new_bond1, new_bond2]: lig_k[label] = 6.35000
                                if (hybrid[n1]+hybrid[n2]) == 'C.2O.2':
                                    if 'C.2N.am' in [new_bond1, new_bond2]:
                                       lig_k[label] = 3.98000 # usual amide
                                       for qqq in range(len(b1)):
                                           if qqq not in [i, ppp]:
                                               bond_new1 = hybrid[b1[qqq]]+hybrid[b2[qqq]]
                                               bond_new2 = hybrid[b2[qqq]]+hybrid[b1[qqq]]
                                               if 'C.2C.ar' in [bond_new1, bond_new2]: lig_k[label] = 3.04000
                        uc[n1] = uc[n1] + 7.2*delta_potential/(lig_k[label]*lig_d[label]**2)
                        uc[n2] = uc[n2] - 7.2*delta_potential/(lig_k[label]*lig_d[label]**2)
                        replace_charge.setdefault(natom[n1], [])
                        replace_charge[natom[n1]].append([n1, n2, natom[n1], natom[n2], hybrid[n1], hybrid[n2], lig_c[n1], lig_c[n2], uc[n1], uc[n2]])
                for ridx in replace_charge.keys():
                    bond_length = len(replace_charge[ridx])
                    if bond_length > 1:
                        atom_charge = np.mean([ac[-2] for ac in replace_charge[ridx]])
                        uc[replace_charge[ridx][0][0]] = atom_charge
                        light_atom = {}
                        for id_1 in range(bond_length):
                            light_atom.setdefault(replace_charge[ridx][id_1][5], [])
                            light_atom[replace_charge[ridx][id_1][5]].append([replace_charge[ridx][id_1][1], replace_charge[ridx][id_1][-1], id_1])
                            replace_charge[ridx][id_1][-2] = atom_charge
                        for lid in light_atom.keys():
                            tmp_lid = light_atom[lid]
                            if len(tmp_lid) > 1:
                                light_charge = np.mean([ac[1] for ac in tmp_lid])
                                for p_lid in tmp_lid:
                                    uc[p_lid[0]] = light_charge
                                    replace_charge[ridx][p_lid[-1]][-1] = light_charge
                    for rdata in replace_charge[ridx]:
                        small.append(form %(rdata[2], rdata[3], rdata[4], rdata[5], rdata[6], rdata[7], rdata[8], rdata[9]))
                if len(self.lig_args) != 1: tmp_label = lig_num + 1
                mol_label = tmp_label
                if len(str(tmp_label).strip()) == 0: mol_label = '1'
                new_lig_line.extend(sline[:atom_info+1])
                for i in range(1, len(lig_c)):
                    new_lig_line.append('%s%10.6f%s' %(b_charge[i], uc[i], a_charge[i]))
                new_lig_line.extend(sline[bond_info:])
                tmp_f0.write('# molecule split %s.\n\t%s\n' %(str(mol_label), self.output_ligfile+str(mol_label)+'.mol2'))
                with open(self.output_ligfile + str(mol_label) + '.mol2', 'w') as obj_mol:
                     obj_mol.writelines(['%s%s' %(_x, os.linesep) for _x in new_lig_line])
                obConversion = openbabel.OBConversion()
                obConversion.SetInAndOutFormats("mol2", "pdb")
                mol = openbabel.OBMol()
                obConversion.ReadFile(mol, self.output_ligfile + str(mol_label) + '.mol2')
                obConversion.WriteFile(mol, 'tmp_ligand.pdb')
                tmp_line = [_.rstrip() for _ in open('tmp_ligand.pdb') if _.startswith('ATOM')]
                with open(self.output_ligfile + str(tmp_label) + '.pdb', 'w') as obj_pdb:
                    l_num = 0
                    for p1 in range(len(tmp_line)):
                        if tmp_line[p1][11:17].strip() == 'H':
                            l_num += 1
                            obj_pdb.write('%s%s%s%12.6f\n' %(tmp_line[p1][:12], ('H'+str(l_num)).center(5), tmp_line[p1][17:80], uc[p1]))
                        else:
                            obj_pdb.write('%s%12.6f\n' %(tmp_line[p1][:80], uc[p1]))
                    obj_pdb.write('%3s %7d%s\n' %('TER', len(tmp_line)+1, ' '*6 +  tmp_line[len(tmp_line)-1][17:28].rstrip()))
                f2.writelines(['%s%s' %(_x, os.linesep) for _x in new_lig_line])
                os.remove('tmp_ligand.pdb')
                if self.out_form == 'mol2': os.remove(self.output_ligfile + str(tmp_label) + '.pdb')
            small.append(';' + '=' * 86 + '\n')
            with open('ligand_charge.dat', 'a') as f1:
                f1.writelines(small)
        if self.out_form == 'pdb': os.remove(self.output_ligfile + '.mol2')
        tmp_f0.write('# The ligand polar bond info(contain: atom,charge change).\n\t%s\n' %'ligand_charge.dat')
        tmp_f0.close()

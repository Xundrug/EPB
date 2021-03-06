#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author : GuanFu Duan
# Email : gfduan178@163.com
# Supervisor : Changge Ji
# All rights reserved 2019
# Replaceing Liagnd atom Charges based on EPB (Effective Polarizable Bond) Model
# Dependencies : opemmm, pdbfixer, openbabel, pybel



from __future__ import division


def calculate(options):
    import sys
    sys.path.append('./bin')
    import os, getpass, shutil
    from compProcess import Complex
    from polarInfoData import Paras_info
    from recWithOpenmm import ProcessRec
    from ligWithPybel import ProcessLig
    from chargeWithEPB import UpdateCharge

    protein, ligand = options.protein_filename, options.ligand_filename
    temp_key, temp_direc, charge_model = options.temp_key, options.temp_name, options.charge_model
    out_form, out_lig = options.out_format, options.out_lig_name
    unchageCharge, draw_key = options.use_mol2_charge, options.draw_lig
    temp_file = '%s.dat' % temp_direc

    if os.path.exists(temp_file): os.unlink(temp_file)
    input_lig = 'empty'
    if ligand: input_lig = ligand
    Complex(protein.strip(), temp_file).split_pdb()
    Paras_info(temp_file).mmff94_charge()
    lig_polar_args = Paras_info(temp_file).ligand_paras()
    rec_args = ProcessRec(temp_file).receptor_charge()
    if input_lig == 'empty':
        lig_args = ProcessLig(temp_file, charge_model, draw_key).ligand_charge(mol2charge=unchageCharge)
    else:
        lig_args = ProcessLig(temp_file, charge_model, draw_key, input_lig).ligand_charge(mol2charge=unchageCharge)
    if os.path.exists(temp_direc): shutil.rmtree(temp_direc)
    r1 = UpdateCharge(lig_args, rec_args, lig_polar_args, out_lig, out_form, temp_file)
    r1.polar_ligand()
    os.mkdir(temp_direc)
    tmp_line = [_.rstrip() for _ in open(temp_file, 'r') if _[:1] != '#']
    for pp in tmp_line:
        for qq in list(pp.split(',')):
            shutil.move(qq.strip(), './'+temp_direc+'/'+qq.strip())
    shutil.move(temp_file, './'+temp_direc+'/'+temp_file)
    if temp_key == 0: shutil.rmtree(temp_direc)

if __name__ == '__main__':
    import sys, argparse
    scripts = 'calculation of polarized ligand charge from a protein-ligand complex structure with the EPB method.'
    parser = argparse.ArgumentParser(description="\033[1;31mA tool:\033[0m \033[1;36m%s\033[0m" %scripts)
    parser.add_argument('-p', action="store", dest="protein_filename", help="Read the pdbid or receptor file(pdb).")
    parser.add_argument('-l', action="store", dest="ligand_filename", help="Read the ligand file(pdb/mol2).")
    parser.add_argument('-c', action="store", dest="charge_model", default='mmff94',
                              choices=['eem', 'eem2015ba', 'eem2015bm', 'eem2015bn', 'eem2015ha', 'eem2015hm',
                                       'eem2015hn', 'eqeq', 'fromfile', 'gasteiger', 'mmff94', 'none', 'qeq', 'qtpie'],
                              help="the charge model using in pybel format convert.")
    parser.add_argument('-u', action="store", dest="use_mol2_charge", type=int, default=0, choices=[0, 1],
                              help="When input is a mol2 file for ligand, use the current charge, 0)No(default), 1)Yes.")
    parser.add_argument('-o', action="store", dest="out_lig_name", type=str, default="LigWithNewCharges",
                              help="Define the output filename(deafult name: LigWithNewCharges).")
    parser.add_argument('-f', action="store", dest="out_format", type=str, default="mol2", choices=['mol2', 'pdb', 'None'],
                              help="Output format: mol2(default), pdb, None(represents output mol2 and pdb file at the same time.)")
    parser.add_argument('-n', action="store", dest="temp_name", type=str, default="tmp_file",
                              help="Define the temporary folder name (default: tmp_file) which store the temptorary file(default: tmp_file.dat).")
    parser.add_argument('-t', action="store", dest="temp_key", type=int, default=0, choices=[0, 1],
                              help="whether reserve the temporary file and store in temporary directory. 0)NoSave(default), 1)Save.")
    parser.add_argument('-k', action="store", dest="draw_lig", type=int, default=0, choices=[0, 1],
                              help="Whether draw the ligand picture, 0)No(default), 1)Yes.")
    options = parser.parse_args()
    if not options.protein_filename:
        parser.error('\033[1;31mneed more than 1 value to input(pdbid or receptor pdb file).\033[0m')
    else:
        calculate(options)

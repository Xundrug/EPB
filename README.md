EPB Charge: Updating Ligand Atom Charges under its Local Environments Based On EPB Model
----------------------------------------------------------------------------------------
    EPB - Effective Polarizable Bond

    Author: GuanFu Duan, gfduan178@163.com

    Supervisor: Changge Ji

    This a set of tools and Python modules for prepare the input files for docking package(eg: Glide、AutoDock、Sybyl) and simulation package(eg: CHARMM、Amber) with the update charge(using EPB method). The default output fileformat is mol2.

    The origin charge of protein's atom by openmm and ligand atom origin charge from pybel

    All rights reversed 2019

Installation
------------
Follow these steps on Linux/OSX:

    1、Download and install Python 2.7 or greater from https://conda.io/miniconda.html
       (Example: your system is ubuntu/Linux with 64-bit, and download file name is Miniconda3-latest-Linux-x86_64.sh)
       after download: chmod +x  Miniconda3-latest-Linux-x86_64.sh
                       ./Miniconda3-latest-Linux-x86_64.sh
       (Attention: During setup, you'd better to choose yes option.)
       
    2、Open terminal in Mac/Linux, install openmm, pdbfixer, openbabel, pybel and run
       conda install -c omnia openmm pdbfixer
       conda install -c openbabel openbabel
       pip install pybel
       
       or install this module from local using "conda install --use-local Module/*.tar.bz2"
       
    3、Download and unzip EPB-master.zip
       After you decompression this package and access it, the usage as follows:
       method I: if the destination is /home/lidong/test
                 cp -r bin /home/lidong/test
                 cp EPBLigCharge.py /home/lidong/test
                 chmod +x EPBLigCharge.py

                 use "python EPBLigCharge.py -h/--help" or "./EPBLigCharge.py -h/--help" for help
    
       method II: cd package
                      chmod +x INSTALL.py .epblib/EPBLigCharge.py
                      ./INSTALL.py
                      source ~/.bashrc

                  use "EPBLigCharge.py -h/--help" for help

Important
---------
    1、You Must install Python and the Python version great than 2.7
    2、The Program need some Python Module: openmm、pdbfixer、openbael and Pybel
    3、Open the terminal in Mac/Linux and run "EPBLigCharge.py -h/--help" will show:
       usage: EPBLigCharge.py [-h] [-p PROTEIN_FILENAME] [-l LIGAND_FILENAME] 
                                   [-t {0,1}]
                                   [-c {eem,eem2015ba,eem2015bm,eem2015bn,eem2015ha,eem2015hm,eem2015hn,eqeq,fromfile,gasteiger..}]
                                   [-o OUT_LIG_NAME] [-f {mol2,pdb,None}] [-n TEMP_NAME]
                                   [-u {0,1}]
       A tool: Based on EPB(Effective Polarizable Bond) method to update molecule charges.

       optional arguments:
          -h, --help            show this help message and exit
          -p PROTEIN_FILENAME   Read the pdbid or receptor file(pdb).
          -l LIGAND_FILENAME    Read the ligand file.
          -t {0,1}              whether reserve the temporary file and store in temporary directory. 0)NoSave(default), 1)Save.
          -c                    {eem,eem2015ba,eem2015bm,eem2015bn,eem2015ha,eem2015hm,eem2015hn,eqeq,fromfile,gasteiger...}
                                the charge model using in pybel format convert.
          -k {0,1}              Whether draw the ligand picture, 0)No(default), 1)Yes.
          -o OUT_LIG_NAME       Define the output filename.
          -f {mol2,pdb,None}    Output format: mol2(default), pdb, None(represents output mol2 and pdb file at the same time.)
          -n TEMP_NAME          Define the directory name which store the temptorary file.
          -u {0,1}              When input is a mol2 file for ligand, use the current charge, 0)No(default), 1)Yes.

Testing
-------
    Please run the test(test pdbid: 1g5s) after you decompression this package and access it:
        EPBLigCharge.py             --------------  it will prompt you how to use this code
        EPBLigCharge.py -p 1g5s     --------------  it will download pdb(PDB ID:1g5s) from RCSB PDB, and saved as 1g5s.dpb
                                                    (Attention: make sure your machine is connect to network if you want download)
    After run it, two new file with exists in this contents:
        1g5s.pdb                    --------------  which you download from RCSB PDB(http://www.rcsb.org/pdb/home/home.do)
        LigWithNewCharges.mol2      --------------  the new ligand mol2 file and the charge is update

Instructions
------------
   1、If you have a PDBID(eg: 1g5s, if no file -- 1g5s.pdb -- in current directory, it will download it from RCSB PDB database)
      
      * If use the default options, it will only update the ligand polar atom charges, and the default output is LigWithNewCharges.mol2 
        
                                    EPBLigCharge.py -p 1g5s
             the ouput file is: LigWithNewCharges.mol2
             
      * If you want to change the output file format, you can add -f options.
           * if you add the option -f pdb, eg:
        
                                    EPBLigCharge.py -p 1g5s -f pdb
        
             the ouput file is: LigWithNewCharges.pdb
             
           * if you add the option -f None (that is to say output file contain pdb and mol2), eg:
        
                                    EPBLigCharge.py -p 1g5s -f None
        
             the ouput file is: LigWithNewCharges.mol2, LigWithNewCharges.pdb
             
      * If you want to change the output filename, you can add -o options

                                    EPBLigCharge.py -p 1g5s -o 1g5s_new
       
             the output file is: 1g5s_new.mol2 
       
      * If you want to reserve the Intermediate file in order to understand the process, you can add -t 1 option, eg:
   
                                    EPBLigChrage.py -p 1g5s -t 1

             the output: LigWithNewCharges.mol2, tmp_file (is a folder which store the temporary file)
             the middle temporary file will saved in tmp_file, the inforamtion of each temporary file write in tmp_file.dat,
             and you can use "-n" to define the temporary directory and the illustrate filename also change at the same time.
   
   2、If you have two file ----- one is protein file(format: pdb), and other is ligand file(format: pdb/mol2)
                                 both of them is the protein file(format: pdb)
   
      * if protein file name is 1g5s_receptor.pdb and ligand file name is 1g5s_ligand.pdb(or 1g5s_ligand.mol2), eg:
      
                                    EPBLigCharge.py -p 1g5s_receptor.pdb -l 1g5s_ligand.pdb
                  
                                    EPBLigCharge.py -p 1g5s_receptor.pdb -l 1g5s_ligand.mol2
      
   *** For example 3, the other option usage, you can get it from example 1.
       You can give the options in any position, but make sure the option key close to the option.

Examples
--------
   1、Download the complex from RCSB PDB
   
                                    EPBLigCharge.py -p 1g5s -t 1
      the output: 1g5s.pdb (download file)
                  LigWithNewCharges.mol2 (the ligand file which update the atom charges)
                  tmp_file (is a folder, and contain some temporary files, the information write in tmp_file.dat)
                  the tmp_file/ligand_charge.dat record the polar atom and the charge changes as:
                  
                  ;======================================================================================
                  ;                                                           CHARGE
                  ;  ATOM1   ATOM2  hybrid1  hybrid2         OLD-I      OLD-II      NEW-I       NEW-II
                  ;--------------------------------------------------------------------------------------
                  ************************************* molecule 1 *************************************
                      N18       H    N.pl3      H         -0.317400    0.186800   -0.358604    0.228004
                      N10       H    N.pl3      H         -0.296000    0.208500   -0.310092    0.222592
                      N17       H      N.3      H         -0.349900    0.125200   -0.403679    0.170825
                      N17       H      N.3      H         -0.349900    0.125200   -0.403679    0.170825
                  ;======================================================================================
                  
                  
   2、use the local separate file contain receptor and ligand file
   
                                    EPBLigCharge.py -p ./example/1g5s_receptor.pdb -l ./example/1g5s_ligand.pdb -t 1
       
       the output: 1g5s.pdb (download file)
                  LigWithNewCharges.mol2 (the ligand file which update the atom charges)
                  tmp_file (is a folder, and contain some temporary files, the information write in tmp_file.dat)

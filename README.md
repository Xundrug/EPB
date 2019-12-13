EPB Charge: Calculation of polarized ligand charge from a protein-ligand complex structure with the EPB method.
================================================================================================================


***EPB - Effective Polarizable Bond***

    Author: GuanFu Duan, gfduan178@163.com

    Supervisor: Changge Ji

    This is a set of tools for the calculation of polarized ligand charge from a protein-ligand complex structure with the EPB method.

    All rights reversed 2019

>***[O'Boyle, N. M.; Banck, M.; James, C. A.; Morley, C.; Vandermeersch, T.; Hutchison, G. R., Open Babel: An open chemical toolbox. Journal of Cheminformatics 2011, 3](https://jcheminf.biomedcentral.com/track/pdf/10.1186/1758-2946-3-33)  
    [Eastman, P.; Swails, J.; Chodera, J. D.; McGibbon, R. T.; Zhao, Y. T.; Beauchamp, K. A.; Wang, L. P.; Simmonett, A. C.; Harrigan, M. P.; Stern, C. D.; Wiewiora, R. P.; Brooks, B. R.; Pande, V. S., OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. Plos Computational Biology 2017, 13](https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1005659&type=printable)***

![](https://raw.githubusercontent.com/Xundrug/EPB/master/bin/openbabel.gif)
![](https://raw.githubusercontent.com/Xundrug/EPB/master/bin/openmm.png)      
>***Open Babel and OpenMM available at：https://openbabel.org/ 、http://openmm.org/***

----------------------------------------------------------------------------------------

Installation
------------
***Follow these steps on Linux/OSX:***

**1、Download and install ```Python``` (from https://conda.io/miniconda.html, Version > 2.7)**  

>```Example```: If your system is ubuntu/Linux with 64-bit, please download the file [Miniconda3-latest-Linux-x86_64.sh](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh))  

>```then run```: **```chmod +x Miniconda3-latest-Linux-x86_64.sh```**

>>>>>**```./Miniconda3-latest-Linux-x86_64.sh```**   
  
**2、Open terminal in Mac/Linux, ```install openmm, pdbfixer, openbabel, pybel``` and run**  

>**```conda install -c omnia openmm pdbfixer```**  

>**```conda install -c openbabel openbabel```**  

>**```pip install pybel```**  
  
**or install this module from local using ```"conda install --use-local Module/*.tar.bz2"```**
  
**3、Download and unzip ```EPB-master.zip```**  

>After decompressing this package, please do the following:
       
>***Install Method I:*** 

>>**```chmod +x EPBLigCharge.py```**  

>>**```use "./EPBLigCharge.py -h/--help" for help```**
       
>***Install Method II:*** 

>>**```cd package```**   

>>>>**```chmod +x INSTALL.py .epblib/EPBLigCharge.py```**    

>>>>**```./INSTALL.py```**  

>>>>**```source ~/.bashrc```**  

>>>>**use "```EPBLigCharge.py -h/--help```" for help**
       
>***Sugguest using method II to install this procedure***

Instructions
---------
>***Open the terminal in Mac/Linux and run "EPBLigCharge.py -h/--help"***

    usage: EPBLigCharge.py [-h] [-p PROTEIN_FILENAME] [-l LIGAND_FILENAME]
                       [-c {eem,eem2015ba,eem2015bm,eem2015bn,eem2015ha,eem2015hm,eem2015hn,eqeq,fromfile,gasteiger,mmff94...}]
                       [-u {0,1}] [-o OUT_LIG_NAME] [-f {mol2,pdb,None}]
                       [-n TEMP_NAME] [-t {0,1}] [-k {0,1}]

    A tool: calculation of polarized ligand charge from a protein-ligand complex structure with the EPB method.

    optional arguments:
        -h, --help            show this help message and exit
        -p PROTEIN_FILENAME   Read the pdbid or receptor file(pdb).
        -l LIGAND_FILENAME    Read the ligand file(pdb/mol2).
        -c {eem,eem2015ba,eem2015bm,eem2015bn,eem2015ha,eem2015hm,eem2015hn,eqeq,fromfile,gasteiger,mmff94,none,qeq,qtpie}
                              the charge model using in pybel format convert (default: mmff94).
        -u {0,1}              When input is a mol2 file for ligand, use the current charge, 0)No(default), 1)Yes.
        -o OUT_LIG_NAME       Define the output filename(deafult name: LigWithNewCharges).
        -f {mol2,pdb,None}    Output format: mol2(default), pdb, None(represents output mol2 and pdb file at the same time.)
        -n TEMP_NAME          Define the temporary folder name (default: tmp_file) which store the temptorary file(default:
                              tmp_file.dat).
        -t {0,1}              whether reserve the temporary file and store in temporary directory. 0)NoSave(default), 1)Save.
        -k {0,1}              Whether draw the ligand picture, 0)No(default), 1)Yes.

Examples
--------

**1、Calculate polarized ligand charge from a complex structure. (https://www.rcsb.org/)**
   
      run: EPBLigCharge.py -p 1g5s -t 1
                                    
      the output: 1g5s.pdb (download or use local file)
                  LigWithNewCharges.mol2 (the ligand file with polarized charge calculated by EPB)
                  tmp_file (is a folder, and contain some temporary files, the information is written in tmp_file.dat)
                  
**2、Calculate polarized ligand charge from a ligand file and a receptor file**
   
       run: EPBLigCharge.py -p ./example/1g5s_receptor.pdb -l ./example/1g5s_ligand.pdb -t 1
            EPBLigCharge.py -p ./example/1g5s_receptor.pdb -l ./example/1g5s_ligand.mol2 -t 1
       
       the output: LigWithNewCharges.mol2 (the ligand file with polarized charge calculated by EPB)
                   tmp_file (is a folder, and contain some temporary files, the information is written in tmp_file.dat)

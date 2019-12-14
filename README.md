EPB Charge: Calculation of polarized ligand charge from a protein-ligand complex structure with the EPB method.
================================================================================================================

***[EPB](https://pubs.acs.org/doi/pdf/10.1021/jp4080866) - Effective Polarizable Bond***

    Author: GuanFu Duan, gfduan178@163.com

    Supervisor: Changge Ji

    This is a set of tools for the calculation of polarized ligand charge from a protein-ligand complex structure with the EPB method.

    All rights reversed 2019

<div align="center">
    <img src="https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2F1758-2946-3-33/MediaObjects/13321_2011_Article_216_Figa_HTML.gif?as=webp" width="500" \><img src="https://avatars1.githubusercontent.com/u/52428936?s=400&v=4" width="250" \>
</div>  

* ***Reference of [openbabel](https://jcheminf.biomedcentral.com/track/pdf/10.1186/1758-2946-3-33) and [openmm](https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1005659&type=printable)***  

* ***It is freely available under an open-source license from: https://openbabel.org/ 、http://openmm.org/***  

----------------------------------------------------------------------------------------

Installation
------------
***Follow these steps on Linux/OSX:***  
* **Download and install [Python](https://conda.io/miniconda.html) (Version > 2.7)**  

    Example: Download the lastest 64-bit Ubuntu/Linux Python 3 file **[Miniconda3-latest-Linux-x86_64.sh](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh)** and run
        
                    chmod +x Miniconda3-latest-Linux-x86_64.sh
    
                    ./Miniconda3-latest-Linux-x86_64.sh

* **Dependency Package(```openbabel、pybel、openmm and pdbfier```) and Program ```EPB-master``` installation**  
    
    Download the **[EPB-master.zip](https://codeload.github.com/Xundrug/EPB/zip/master)** and decompression it  
    
    * **```Install dependency package```** 
        
                    conda install -c omnia openmm pdbfixer
            
                    conda install -c openbabel openbabel
            
                    pip install pybel

    * **```Install Program EPB-master in two methods```**:
    
        * Method I:
        
                    cd EPB-master
            
                        chmod +x EPBLigCharge.py
                
            * using "**./EPBLigCharge.py -h/--help**" for help
        
        * Method II:
        
                    cd EPB-master/package
            
                        chmod +x INSTALL.py ./bin/EPBLigCharge.py  
            
                        ./INSTALL.py  
            
                        source ~/.bashrc    
            
            * using "**EPBLigCharge.py -h/--help**" for help 
       
***Sugguest using second method to install Program ```EPB-master```***

------------------------------------------------------

Instructions
------------

***Open the terminal in Mac/Linux and run "```EPBLigCharge.py -h/--help```"***

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

-----------------------------------------------------------------------------------------------------------------------------

Examples
--------

* **Calculate polarized ligand charge from a complex structure which from https://www.rcsb.org/**
    
    * Example of how to run the code:
    
                    EPBLigCharge.py -p 1g5s -t 1

    * The output: 
    
        * **1g5s.pdb** (suppose 1g5s.pdb not in current directory, it will download from https://www.rcsb.org/)  
        
        * **LigWithNewCharges.mol2** (the ligand file with polarized charge calculated by EPB)  

        * **tmp_file** (is a folder, and contain some temporary files, the information is written in tmp_file.dat)  

* **Calculate polarized ligand charge from a complex structure which from local**
    
    * Example of how to run the code:
    
                    EPBLigCharge.py -p ./example/1g5s.pdb -t 1

    * The output: 
        
        * **LigWithNewCharges.mol2** (the ligand file with polarized charge calculated by EPB)  

        * **tmp_file** (is a folder, and contain some temporary files, the information is written in tmp_file.dat)

* **Calculate polarized ligand charge from a ligand file and a receptor file**

    * Example of how to run the code and the ligand format is "pdb":
            
                    EPBLigCharge.py -p ./example/1g5s_receptor.pdb -l ./example/1g5s_ligand.pdb -t 1
    
    * Example of how to run the code and the ligand format is "mol2":
           
                    EPBLigCharge.py -p ./example/1g5s_receptor.pdb -l ./example/1g5s_ligand.mol2 -t 1
       
    * The output: 
    
        * **LigWithNewCharges.mol2** (the ligand file with polarized charge calculated by EPB)
        
        * **tmp_file** (is a folder, and contain some temporary files, the information is written in tmp_file.dat)

-----------------------------------------------------------------------------------------------------------------------------

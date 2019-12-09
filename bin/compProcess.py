class Complex(object):
    def __init__(self, pdb_id, temp_illustration):
        self.pdb_file = pdb_id.strip()
        self.temp_illustration = temp_illustration

    # download the pdb from web
    def get_pdb(self):
        import sys,requests
        res = requests.get('https://files.rcsb.org/download/' + self.pdb_file)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('\n\033[1;31m   There is a problem:\033[0m\t%s\n' %exc)
            sys.exit('Please cheak your PDBID is valid and the network is connect.')
        else:
            print('\tDownload %s ...\n\tsaved data to file: %s' %(self.pdb_file.split('.')[0], self.pdb_file))
            with open(self.pdb_file, 'wb') as file0:
                for p in res.iter_content(100000):
                    file0.write(p)

    # split pdb with receptor, ligand, ion, confactor, hoh
    def split_pdb(self):
        import re, os
        # whether the input is a valid pdbid
        if len(self.pdb_file) == 4:
            self.pdb_file = '%s.pdb' %self.pdb_file
            self.get_pdb()
        self.title = os.path.basename(self.pdb_file).split('.')[0] + '_'
        self.ls = os.linesep
        # custom confactor list
        default_cofactor = ['00S', '01F', '03R', '06U', '06W', '07L', '0AF',
                            '0F7', '0G6', '0GJ', '0KX', '0L8', '0XU', '0ZJ',
                            '10L', '11Y', '12G', '18W', '1B0', '1BO', '1CL',
                            '1D5', '1D6', '1D8', '1D9', '1DE', '1DK', '1DL',
                            '1FZ', '1HZ', '1JM', '1PE', '1PG', '1S5', '24X',
                            '29P', '2GO', '2H3', '2JZ', '2LT', '2MC', '2MD',
                            '2MO', '2OP', '2PE', '2PG', '2PR', '2R8', '2R9',
                            '2UE', '2UQ', '2X3', '2YR', '2ZF', '301', '3A5',
                            '3A8', '3AD', '3CD', '3CT', '3DR', '3FO', '3FS',
                            '3FU', '3PG', '3PL', '3PO', '3PY', '3VF', '3XV',
                            '402', '40E', '44E', '48V', '4EY', '4HA', '4KL',
                            '4KS', '4LU', '4LV', '4LW', '4M4', '4MJ', '4MO',
                            '4NR', '4PC', '4VR', '4W4', '4W6', '4WV', '4WW',
                            '4WX', '4Z2', '51P', '57O', '5AD', '5KK', '5NH',
                            '5PY', '5QH', '5QJ', '5QK', '5QL', '5SD', '64T',
                            '663', '67W', '67X', '67Y', '68A', '68B', '68C',
                            '68D', '6JO', '6MA', '6MO', '6NA', '6OG', '6PG',
                            '74C', '775', '7BC', '7BG', '7D9', '7HQ', '7HS',
                            '7L1', '89R', '8BF', '8BL', '8BO', '8C0', '8CM',
                            '8CS', '8FF', '8J0', '8J3', '8K6', '8PG', '8PP',
                            '993', '9CV', '9H4', '9H7', '9JA', '9JJ', '9JM',
                            '9L9', '9NU', '9QQ', '9RO', '9SQ', 'A2G', 'A2M',
                            'A3D', 'A3P', 'ABA', 'ACE', 'ACO', 'ACP', 'ACR',
                            'ACT', 'ACY', 'ADE', 'ADN', 'ADP', 'AE3', 'AEW',
                            'AG2', 'AGQ', 'AGS', 'AKG', 'ALO', 'ALY', 'AMP',
                            'ANP', 'ANR', 'AOB', 'AOI', 'AP6', 'AR6', 'ARO',
                            'ASC', 'ASD', 'ASO', 'AST', 'ATP', 'ATR', 'AVG',
                            'AWQ', 'AX1', 'AX2', 'AX3', 'AX4', 'AX5', 'AX6',
                            'AX7', 'AX8', 'AZI', 'B12', 'B1Z', 'B3P', 'BA2',
                            'BCL', 'BCN', 'BCR', 'BCT', 'BEA', 'BEN', 'BES',
                            'BEZ', 'BGC', 'BLP', 'BMA', 'BME', 'BMT', 'BN6',
                            'BNH', 'BNT', 'BOG', 'BPH', 'BRU', 'BTB', 'BTT',
                            'BYN', 'C2F', 'C2H', 'C8E', 'CAC', 'CAF', 'CAS',
                            'CB3', 'CBO', 'CDL', 'CDP', 'CFM', 'CFN', 'CGT',
                            'CGU', 'CIT', 'CLA', 'CLF', 'CLQ', 'CMO', 'CO2',
                            'CO3', 'COA', 'COI', 'COU', 'CPX', 'CRT', 'CSD',
                            'CSO', 'CSX', 'CSZ', 'CTP', 'CU1', 'CXM', 'CYC',
                            'CYN', 'CZL', 'CZM', 'D09', 'D1D', 'D7K', 'DAH',
                            'DAL', 'DAO', 'DCS', 'DDF', 'DGD', 'DGL', 'DHD',
                            'DHF', 'DIO', 'DJN', 'DLZ', 'DMS', 'DPM', 'DPN',
                            'DPQ', 'DRA', 'DTD', 'DTR', 'DTT', 'DTU', 'DTV',
                            'DTY', 'DX1', 'DX2', 'DX3', 'DX4', 'DX6', 'DX7',
                            'DX8', 'DXE', 'EDO', 'EDT', 'EEH', 'EL1', 'EL2',
                            'EM2', 'EMC', 'ENJ', 'EOW', 'EPE', 'EPT', 'EST',
                            'ETF', 'EUG', 'F2Y', 'F3S', 'F4S', 'F5C', 'F5J',
                            'F98', 'FA9', 'FAA', 'FAB', 'FAD', 'FAE', 'FC6',
                            'FDA', 'FDB', 'FDE', 'FE2', 'FE3', 'FE9', 'FEC',
                            'FEG', 'FEO', 'FES', 'FFO', 'FLC', 'FLP', 'FMN',
                            'FMT', 'FMU', 'FNH', 'FNR', 'FO1', 'FOL', 'FOR',
                            'FQW', 'FRE', 'FUC', 'FUM', 'FZZ', 'G2F', 'G3F',
                            'G3H', 'G3P', 'G6P', 'GAR', 'GC7', 'GCP', 'GDP',
                            'GDX', 'GEK', 'GFL', 'GGD', 'GL3', 'GLC', 'GLO',
                            'GLP', 'GMP', 'GOL', 'GOX', 'GSP', 'GTP', 'GUA',
                            'H0V', 'H2B', 'H41', 'H4B', 'H4M', 'HA8', 'HAR',
                            'HB0', 'HBA', 'HBI', 'HBX', 'HCA', 'HCI', 'HDN',
                            'HDZ', 'HE1', 'HE3', 'HEC', 'HEM', 'HEZ', 'HF1',
                            'HG1', 'HHR', 'HIO', 'HMG', 'HOZ', 'HP8', 'HPA',
                            'HPR', 'HQD', 'HSE', 'HSL', 'HSM', 'HSO', 'HSP',
                            'HTJ', 'HTL', 'HTO', 'HU1', 'HU2', 'HU4', 'HU5',
                            'HUD', 'HXS', 'HY1', 'I2A', 'I2C', 'IBU', 'IC9',
                            'ICA', 'ICE', 'ICG', 'ICH', 'ICS', 'ICT', 'IK2',
                            'IMD', 'IMP', 'INS', 'IOD', 'IPA', 'IPH', 'IQW',
                            'IR3', 'ISE', 'ISW', 'ISZ', 'ITR', 'ITU', 'IUP',
                            'IXE', 'IXF', 'IXN', 'IZ9', 'JDD', 'JR2', 'JU2',
                            'JUO', 'KAN', 'KCX', 'KEU', 'KP2', 'KT3', 'KT5',
                            'KTZ', 'L34', 'LAC', 'LCP', 'LDA', 'LDH', 'LGC',
                            'LHG', 'LLP', 'LMR', 'LMT', 'M1P', 'M2N', 'M3L',
                            'M4V', 'M9P', 'MA7', 'MAN', 'MBO', 'MCN', 'MEN',
                            'MES', 'MGD', 'MGE', 'MLE', 'MLI', 'MLY', 'MLZ',
                            'MN3', 'MNH', 'MOA', 'MOM', 'MOO', 'MOS', 'MPD',
                            'MRD', 'MSE', 'MTA', 'MTE', 'MTQ', 'MTX', 'MTY',
                            'MUA', 'MVA', 'MYA', 'MYR', 'N01', 'N2I', 'NAD',
                            'NAG', 'NAI', 'NAJ', 'NAP', 'NCR', 'NDG', 'NDO',
                            'NDP', 'NEA', 'NEP', 'NFU', 'NFV', 'NH2', 'NH4',
                            'NHN', 'NHP', 'NKK', 'NLE', 'NMN', 'NO2', 'NO3',
                            'NOH', 'NTZ', 'NVU', 'NWJ', 'NZQ', 'OAR', 'OBF',
                            'OBL', 'OCA', 'OCS', 'OCY', 'OEC', 'OGA', 'OLC',
                            'OOA', 'OXL', 'OXM', 'OXR', 'OXY', 'OZJ', 'P1T',
                            'P33', 'P3F', 'P6G', 'PAE', 'PAQ', 'PBG', 'PC1',
                            'PCD', 'PCQ', 'PCR', 'PDC', 'PDP', 'PE4', 'PEA',
                            'PEG', 'PEO', 'PFM', 'PG0', 'PG4', 'PGD', 'PGE',
                            'PGO', 'PGR', 'PHG', 'PHO', 'PLA', 'PLM', 'PLP',
                            'PLR', 'PMD', 'PMP', 'PND', 'PNS', 'PO4', 'POA',
                            'POP', 'PPI', 'PQ9', 'PQN', 'PQQ', 'PRH', 'PT1',
                            'PTE', 'PUR', 'PVO', 'PY3', 'PYG', 'PYR', 'Q0K',
                            'QIC', 'QUN', 'RAR', 'RBF', 'REA', 'RED', 'S3F',
                            'S72', 'SAC', 'SAH', 'SAL', 'SAM', 'SCN', 'SEH',
                            'SEP', 'SF4', 'SFG', 'SIN', 'SKA', 'SKM', 'SL5',
                            'SME', 'SO2', 'SO3', 'SO4', 'SPF', 'SPN', 'SPO',
                            'SQD', 'SRM', 'SRT', 'SSN', 'SU3', 'SUC', 'SUE',
                            'SV6', 'SVS', 'T7X', 'TA6', 'TAB', 'TAR', 'TBU',
                            'TDP', 'TEJ', 'TFB', 'THG', 'THJ', 'THV', 'THW',
                            'THY', 'TLA', 'TMF', 'TMG', 'TNE', 'TNF', 'TOL',
                            'TPO', 'TPP', 'TPQ', 'TPW', 'TR8', 'TRL', 'TRQ',
                            'TRS', 'TRW', 'TSR', 'TSV', 'TTB', 'TTN', 'TYQ',
                            'TYS', 'TYT', 'TYY', 'TZD', 'U10', 'UEN', 'UFP',
                            'UHX', 'UIH', 'UMC', 'UMP', 'UNH', 'UNK', 'UNL',
                            'UNX', 'UPG', 'URC', 'URE', 'VA3', 'VD1', 'VD2',
                            'VD4', 'VD5', 'VDX', 'VDZ', 'VO3', 'VO4', 'VS8',
                            'VX6', 'W8G', 'WO4', 'WS6', 'WS7', 'WSD', 'WWF',
                            'XAN', 'XAX', 'XCX', 'XDI', 'XDS', 'XL3', 'XLC',
                            'XLD', 'XMP', 'XP0', 'XYP', 'YE1', 'YE2', 'YGL',
                            'YGP', 'YOK', 'YOL', 'YOM', 'YT3', 'YUG', 'Z34',
                            'ZGP', 'ZU4', 'ZZ8', 'HED', 'EGL', 'GAL', 'GNP',
                            'CMH', 'MMC', 'HGB', 'BE7', 'PMB', '0QE', 'CPT',
                            'DCE', 'EAA', 'IMN', 'OCZ', 'OMY', 'OMZ', 'UN9',
                            '1N1', '2T8', '393', '3MY', 'BMU', 'CLM', 'CP6',
                            'DB8', 'DIF', 'EFZ', 'LUR', 'RDC', 'UCL', 'XMM',
                            'FE1', 'CO1', 'C14', 'C15', 'F9F', 'OAN', 'BLM',
                            'BZG', 'VNL', 'PF5', 'HLT', 'IRE', 'PCI', 'VGH',
                            'UDP', 'PLL', 'OEX', 'OH', 'XE', 'BR', 'CL',
                            'KR', 'SE', 'CO', 'O']
        # custom metal ion list
        default_metal = ['LI', 'BE', 'NA', 'MG', 'AL', 'K', 'CA', 'SC', 'V',
                         'CR', 'MN', 'FE', 'CO', 'NI', 'CU', 'ZN', 'GA', 'GE',
                         'RB', 'SR', 'Y', 'ZR', 'NB', 'MO', 'TC', 'RU', 'RH',
                         'PD', 'AG', 'CD', 'IN', 'SN', 'SB', 'CS', 'BA', 'LU',
                         'HF', 'TA', 'W', 'RE', 'OS', 'IR', 'PT', 'AU', 'HG',
                         'TI', 'PB', 'BI', 'PO', 'AT', 'FR', 'RA', 'LR', 'RF',
                         'DB', 'SG', 'BH', 'HS', 'MT', 'DS', 'RG', 'CN', 'NH',
                         'FI', 'MC', 'LV', 'TS', 'LA', 'CE', 'PR', 'ND', 'PM',
                         'SM', 'EU', 'GD', 'TB', 'DY', 'HO', 'ER', 'TM', 'YB',
                         'AC', 'TH', 'PA', 'U', 'NP', 'PU', 'AM', 'CM', 'BK',
                         'CF', 'ES', 'FM', 'MD', 'NO', 'FE1', 'FE4', 'RU1',
                         'RH1', 'W1']
        # residue name list
        default_resname = ['ALA', 'ARG', 'ASH', 'ASN', 'ASP', 'CYM', 'CYS', 'CYX',
                           'GLH', 'GLN', 'GLU', 'GLY', 'HID', 'HIE', 'HIP', 'HIS',
                           'ILE', 'LEU', 'LYN', 'LYS', 'MET', 'PHE', 'PRO', 'SER',
                           'THR', 'TRP', 'TYR', 'VAL']
        # read the pdb file
        plines = [_.rstrip() for _ in open(self.pdb_file)]
        rec_line = []; hoh_line = []; lig_line, ion_line, confactor_line = {}, {}, {}
        for pline in plines:
            if pline.startswith('ATOM') or pline.startswith('TER'): # receptor part
                if pline[17:20].strip().upper() in default_resname:
                    rec_line.append(pline)
            elif pline.startswith('HETATM'):
                line = pline[17:20].strip().upper()
                if line == 'HOH': # water part
                    hoh_line.append(pline)
                else:
                    uniq_chain = re.sub('\W', '', '_'.join(pline[17:27].split()))
                    if line in default_cofactor: # confactor part
                        if uniq_chain not in confactor_line:
                            confactor_line[uniq_chain] = []
                        confactor_line[uniq_chain].append(pline)
                    elif line in default_metal: # metal ion part
                        if uniq_chain not in ion_line:
                            ion_line[uniq_chain] = []
                        ion_line[uniq_chain].append(pline)
                    else: # ligand part
                        if uniq_chain not in lig_line:
                            lig_line[uniq_chain] = []
                        lig_line[uniq_chain].append(pline)
        # build a describe file which contains tempfile and the illustration
        temp_file = open(self.temp_illustration, 'a')
        # write receptor file and water file
        with open(self.title+'receptor.pdb', 'w') as f1:
            temp_file.write('# receptor part from complex with split code.\n\t%sreceptor.pdb\n' %self.title)
            f1.writelines(['%s%s' %(_x, self.ls) for _x in rec_line])
        if len(hoh_line) != 0:
            temp_file.write('# water part from complex with split code.\n\t%swater.pdb\n' %self.title)
            with open(self.title+'water.pdb', 'w') as f2:
                f2.writelines(['%s%s' %(_x, self.ls) for _x in hoh_line])
        # write ligand, metal ion, confactor file
        confactor_ion_lig_info, type_name = [confactor_line, ion_line, lig_line], 'None'
        for molecule_type in confactor_ion_lig_info:
            if len(molecule_type) != 0:
                type_label = confactor_ion_lig_info.index(molecule_type)
                if type_label == 0: type_name = 'confactor'
                if type_label == 1: type_name = 'metal ion'
                if type_label == 2: type_name = 'small molecule'
                if type_name != 'None': temp_file.write('# %s part from complex with split code.\n' %type_name)
                temp_file.write('\t%s\n' %(', '.join([self.title+key+'.pdb' for key in molecule_type])))
                for key in molecule_type:
                    with open(self.title+key+'.pdb', 'w') as f3:
                        f3.writelines(['%s%s' %(_x, self.ls) for _x in molecule_type[key]])
        temp_file.close()

#/bin/python



def extract_cas_energies(infile):
    '''
    :param infile: The output file of ORCA calculation
    :return: a list (len = # of Multipliciites) where each item is a dictionary
     CAS_ENERGIES[:]={'Mult': ' ', 'units': 'eV', 'N_states': int, 'Energies': [float], 'Relative Energies': [float]}
    '''
    CAS_Energies = []

    f=open(infile,'r')
    for line in f:
        if 'Number of multiplicity blocks' in line :
            Multiplicity_blocks = int(line.split()[5])
    f.close()
    for n in range(Multiplicity_blocks) :
        temp = {}
        temp['units'] = 'eV'
        string="CAS-SCF STATES FOR BLOCK  "+str(n+1)
        #print(n)
        Energies = []

        f=open(infile,'r')
        for line in f:
            if string in line:
                #print(line)
                temp['Mult'] = int(line.split()[6])  # Get multplicity

                for line in f:

                    if "ROOT" in line:
                        Energies.append(float(line.split()[3]))

                    if "Spin-Determinant" in line:
                        temp['Energies'] = Energies
                        temp['Relative Energies'] = [27.2114*(Energies[k] - Energies[0]) for k in range(len(Energies))]
                        temp['N_states'] = len(Energies)
                        break
        f.close()
        CAS_Energies.append(temp)


    return CAS_Energies


def extract_nevpt_energies(infile):
    '''
    :param infile: The output file of ORCA calculation
    :return: a list (len = # of Multipliciites) where each item is a dictionary
     CAS_ENERGIES[:]={'Mult': ' ', 'units': 'eV', 'N_states': int, 'Energies': [float], 'Relative Energies': [float]}
    '''
    Nevpt_Energies = {'State': [], 'Mult': [], 'Energy': []}
    string = 'NEVPT2 TOTAL ENERGIES'
    temp = []
    f=open(infile,'r')
    for line in f:
        if string in line:
            #print(line)
            for line in f :
                #print (line.split())
                if 'NEVPT2 TRANSITION' in line :
                    break
                elif line != '\n' and line.split()[0][:-1].isdigit() :
                    Nevpt_Energies['State'].append(int(line.split()[1]))
                    Nevpt_Energies['Mult'].append(int(line.split()[2]))
                    Nevpt_Energies['Energy'].append(float(line.split()[3]))
    #print(Nevpt_Energies)
    '''
            temp['Mult'] = int(line.split()[6])  # Get multplicity

            for line in f:

                if "ROOT" in line:
                    Energies.append(float(line.split()[3]))

                if "Spin-Determinant" in line:
                    temp['Energies'] = Energies
                    temp['Relative Energies'] = [27.2114*(Energies[k] - Energies[0]) for k in range(len(Energies))]
                    temp['N_states'] = len(Energies)
                    break
    '''

    f.close()
    #print(Nevpt_Energies['Energy'].index(min(Nevpt_Energies['Energy'])),min(Nevpt_Energies['Energy']))
    gs_index= Nevpt_Energies['Energy'].index(min(Nevpt_Energies['Energy']))

    GS={'State': Nevpt_Energies['State'][gs_index], 'Mult' : Nevpt_Energies['Mult'][gs_index], 'Energy' : Nevpt_Energies['Energy'][gs_index]}
    #print(GS)
    Nevpt_Energies['Ground state'] =GS
    return Nevpt_Energies
    #CAS_Energies.append(temp)

def extract_cas_transition_energies(infile):
    string="SA-CASSCF TRANSITION ENERGIES"
    print('\n')
    #f=open('cas9in10_eg_r20.soc.out','r')
    f=open(infile,'r')
    i=0
    for line in f:
        if string in line:
            print(line,end='')
            for line in f:
                print(line,end='')

                if "DENSITY" in line:
                #print(line)
                    break
    f.close()

def get_soc_hamil(infile):
    '''
    
    :param infile: 
    :return: 
    '''
    import numpy as np
    f = open(infile, 'r')
    n = 0
    for line in f:
        if 'CAS-SCF STATES FOR BLOCK' in line:
            n = n + int(line.split()[6]) * int(line.split()[8])

    f.close()
    f=open(infile,'r')
    #n=12
    dat=[]
    for line in f:
        if 'SOC MATRIX (A.U.)' in line:
            i = 0;
            j = 0;
            for line in f:
                if i > 3:
                    # print(line)
                    dat = dat + [float(x) for x in
                                 line.strip().replace('-', ',-').replace('      0 ', '0').replace(' 0', ',0').split(
                                     ',')[1:]]
                    npdat = np.array(dat)
                    # break
                    # i = 0;
                    # for line in f:
                    # print(line)
                    # if i != 0:
                    #    print(dat)
                    # print(npdat.shape)
                if i > n - 1 + 3:
                    dat = []
                    npdat = np.matrix.transpose(npdat.reshape(n, 6))
                    if j == 0:
                        soc_mat_R = npdat
                        # print(npdat.shape)
                        # print(j,soc_mat_R.shape)
                        j += 1
                    else:
                        soc_mat_R = np.concatenate((soc_mat_R, npdat))
                        # print(j,soc_mat_R.shape)
                    # break
                    # print('break')
                    i = 2
                i += 1
                if 'Image' in line:
                    #print(line)
                    i = 0;
                    j = 0;
                    dat = [];
                    for line in f:
                        # print('i=',i,'j=',j)
                        # print(line)
                        if i > 0:
                            if 'Lowest' in line:
                                break
                            # print(line)
                            dat = dat + [float(x) for x in
                                         line.strip().replace('-', ',-').replace('      0 ', '0').replace(' 0',
                                                                                                          ',0').split(
                                             ',')[1:]]
                            npdatI = np.array(dat)
                            # print(len(npdatI))
                        if i == n - 1 + 1:
                            dat = []
                            npdatI = np.matrix.transpose(npdatI.reshape(n, 6))
                            if j == 0:
                                soc_mat_I = npdatI
                                # print(npdatI.shape)
                                # print(j, soc_mat_I.shape)
                                j += 1
                            else:
                                soc_mat_I = np.concatenate((soc_mat_I, npdatI))
                                # print(j, soc_mat_I.shape)
                            # break
                            # print('break')
                            i = -1
                        i += 1
                    break

    soc_mat = soc_mat_R + 1j * soc_mat_I
    eigenValues, eigenVectors = np.linalg.eig(soc_mat)

    idx = eigenValues.argsort()[::1]
    eigenValues = np.real(eigenValues[idx])
    eigenVectors = eigenVectors[:, idx]

    eigenValues_ev = np.around(27.2114 * (eigenValues - min(eigenValues)), decimals=4)
    return eigenValues_ev,eigenVectors,soc_mat


def extract_soc_eval_efun(infile,cal_type='cas'):
    '''

    :param infile: The output file of ORCA calculation
    :return: a list (len = # of Multipliciites) where each item is a dictionary
     SOC_states[:]={'GS_Energy': float, 'n_state': int, 'Energy': float, 'wfc': {}}
     where
     wfc = {'cas_state': [' ',], 's': [' ',], 'ms': [' ',], 'weights': [float,]}
    '''
    import numpy as np
    if cal_type == 'nevpt' :
        string = 'NEVPT2 DIAGONAL'
    else :
        string = 'CASSCF DIAGONAL'

    f=open(infile,'r')
    SOC_states=[]
    #print(string)
    for line in f:
        #print(line)
        if string in line:
            #print(line)
            for line in f:
                if 'Lowest eigenvalue of the SOC matrix:' in line:
                    GS_energy = line.split()[6]
                #print(line)
                if 'STATE' in line:
                    #print(line)
                    temp={'GS_Energy': float(GS_energy)
                    }
                    nstate = line.split()[1][:-1]
                    #print (nstate)
                    temp['n_state'] = int(nstate)
                    temp['Energy'] = float(line.split()[2])/8070
                    cas_state = []
                    s = []
                    ms = []
                    weights = []
                    wfc = {}
                    for line in f :
                        #if line != '\n':
                        if line != '\n' and line.split()[0].startswith('0.'):
                            #print (line.split())
                            cas_state.append(int(line.split()[5]))
                            #print (cas_state)
                            s.append(line.split()[6])
                            ms.append(line.split()[7])
                            weights.append(float(line.split()[0]))
                        if line == '\n' :
                            wfc['weights'] = weights
                            wfc['cas_state'] = cas_state
                            wfc['s'] = s
                            wfc['ms'] = ms
                            break
                                #print('\n')
                            #print(cas_state)
                    temp['wfc'] = wfc
                    SOC_states.append(temp)
        #if 'Center of nuclear charge' in line:
         #   break
    #print (len(SOC_states))
    f.close()
    return SOC_states


def extract_ci_energies(infile):
    CI_Energies=[]
    f = open(infile, 'r')
    mult=[]
    for line in f:
        if 'Number of CI-blocks' in line:
            Multiplicity_blocks = int(line.split()[4])
            #print (Multiplicity_blocks)
            for n in range(Multiplicity_blocks):
                #print(str(n+1))
                string='CI BLOCK ' + str(n+1)
                for line in f:
                    #print(line)
                    if string in line:

                        #print(line)
                        for line in f:
                            if 'Multiplicity' in line:
                                mult.append(int(line.split()[2]))
                        break
            #print(mult)
    f.close()

    for n in range(Multiplicity_blocks):
        temp = {}
        temp['units'] = 'eV'
        string = "CI-BLOCK  " + str(n+1)
        # print(n)
        Energies = []

        f = open(infile, 'r')
        for line in f:
            if string in line:
                #print(line)
                temp['Mult'] = mult[n]  # Get multplicity
                for line in f:
                    if "CI-RESULTS" in line:
                        for line in f:
            #
                            if "STATE" in line:

                                Energies.append(float(line.split()[3]))
                                #print(n,len(Energies))
                            if "MR-PT SELECTION TSel=" in line:
                                temp['Energies'] = Energies
                                temp['Relative Energies'] = [27.2114 * (Energies[k] - Energies[0]) for k in
                                                            range(len(Energies))]
                                temp['N_states'] = len(Energies)
                                break
                        break
        f.close()
        CI_Energies.append(temp)

    return CI_Energies

    """
    string="CI-BLOCK  "+str(n)
    #f=open('cas9in10_eg_r20.soc.out','r')
    f=open(infile,'r')
    i=0
    for line in f:
        if string in line:
            print(line)
            for line in f:
                if "CI-RESULTS" in line:
                    print(line,end='')

                if "STATE" in line:
                    if i==0:
                        gs=float(line.split()[3])
                        print('gs=%s'%gs)
                    i=1
                    print('%3.6f  %4.3f'%(float(line.split()[3]),27.2114*(float(line.split()[3])-gs)))
                if "MR-PT SELECTION TSel=" in line:
                #print(line)
                    break
    f.close()
    """
if __name__ == '__main__':
#     import numpy as np
#infile ="/Users/katukuri/Work/Kitaev_Materials/d7_cobaltates/Na3Co2SbO6/Orca"
# #
# Nevpt_Energies = extract_nevpt_energies(infile)
# #
# for i in range(len(Nevpt_Energies['State'])):
#     print('%3d %3d %5.5f' %(Nevpt_Energies['State'][i], Nevpt_Energies['Mult'][i], Nevpt_Energies['Energy'][i]))
#SOC_states = extract_soc_eval_efun(infile,cal_type='nevpt')
#print(SOC_states)
    infile = '/Users/katukuri/software/Orca_scripts/9csf_s0.5_s1.5_soc.out'
    #eval,evec,H=get_soc_hamil(infile)
    #print(np.around(eval,decimals=4))
    CI_energies=extract_ci_energies(infile)

    for i in range(len(CI_energies)):
        print(CI_energies[i]['Mult'],CI_energies[i]['Relative Energies'])
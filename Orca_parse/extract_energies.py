#/bin/python

def extract_ci_energies(infile,n):
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

def extract_soc_eval_efun(infile):
    '''

    :param infile: The output file of ORCA calculation
    :return: a list (len = # of Multipliciites) where each item is a dictionary
     SOC_states[:]={'GS_Energy': float, 'n_state': int, 'Energy': float, 'wfc': {}}
     where
     wfc = {'cas_state': [' ',], 's': [' ',], 'ms': [' ',], 'weights': [float,]}
    '''

    string = 'Lowest eigenvalue of the SOC matrix:'
    f=open(infile,'r')
    SOC_states=[]

    for line in f:
        if string in line:
            GS_energy = line.split()[6]
            #print(GS_energy)
            for line in f:
                if 'STATE' in line:
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
        if 'Center of nuclear charge' in line:
            break
    #print (len(SOC_states))
    f.close()
    return SOC_states






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
def extract_cas_energies(infile,n):
    string="CAS-SCF STATES FOR BLOCK  "+str(n)
    #f=open('cas9in10_eg_r20.soc.out','r')
    f=open(infile,'r')
    i=0
    for line in f:
        if string in line:
            print(line)
            for line in f:
                if "CI-RESULTS" in line:
                    print(line,end='')

                if "ROOT" in line:
                    if i==0:
                        gs=float(line.split()[3])
                        print('gs=%s'%gs)
                    i=1
                    print('%3.6f  %4.3f'%(float(line.split()[3]),27.2114*(float(line.split()[3])-gs)))
                if "Spin-Determinant" in line:
                #print(line)
                    break

def extract_cas_transition_energies(infile):
    string="SA-CASSCF TRANSITION ENERGIES"
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


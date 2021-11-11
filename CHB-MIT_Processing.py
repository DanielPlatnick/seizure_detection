import os
from pyedflib import highlevel
import numpy as np
import time as t
from scipy.io import savemat



chb_folders = []
for file in os.listdir("/Volumes/D/chb-mit-scalp-eeg-database-1.0.0"):
    if file.startswith("chb"):
        chb_folders.append(file)


with open('/Volumes/D/chb-mit-scalp-eeg-database-1.0.0/RECORDS-WITH-SEIZURES') as f:
    SeizureFiles = f.readlines()
#remove newlines
SeizureFiles = [x.strip() for x in SeizureFiles]
SeizureFiles = SeizureFiles[:-1]

try:
    SaveData = '/Volumes/D/pymatlab1'
    os.mkdir(SaveData)
except:
    pass

NumFolders = len(chb_folders)

#specifying quantization level and type of algorithm for DI and MI
quant_lvls = 10
algs = 'E4'

#folder loop
for i in range(0,len(chb_folders)):
    curr_folder = os.path.dirname('/Volumes/D/chb-mit-scalp-eeg-database-1.0.0/RECORDS-WITH-SEIZURES') + '/' + chb_folders[i]
    curr_chbName = chb_folders[i]




    summary_path = (curr_folder + '/' + curr_chbName + '-summary.txt')

    with open(summary_path) as p:
        summary = p.readlines()
    # remove newlines
    summary = [x.strip() for x in summary]

    fileList = []
    EDFDir = (curr_folder)
    for file in os.listdir(EDFDir):
        if file.endswith('.edf'):
            fileList.append(file)

    NumEDFfile = len(fileList)

    #edf file loop
    for j in range(0, NumEDFfile):
        def CheckSeizureEDF():
            splitpath = os.path.splitext(fileList[j])
            CheckSeizureEDF.name = splitpath[0]
            CheckSeizureEDF.ext = splitpath[1]
            global b
            b = 0
            for element in SeizureFiles:
                if CheckSeizureEDF.name+CheckSeizureEDF.ext in element:
                    b = SeizureFiles.index(element) + 1


        CheckSeizureEDF()

        if b > 0:
            T = []
            set1 = []
            set2 = []
            set3 = []
            set4 = []
            set5 = []
            set6 = []
            ChannelIndex = []
            SpecifiedChannels = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-T3', 'C3-P3', 'P3-O1', 'FP2-F4',
                                 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8', 'P8-O2', 'FZ-CZ', 'CZ-PZ']
            #find channel all names in summary file
            chnameindices = []
            for i1, l1 in enumerate(summary):
                if 'Channels' in l1:
                    chnameindices.append(i1)
            chindices = []
            for i2, l2 in enumerate(summary):
                if 'Channel ' in l2:
                    chindices.append(i2)
            channelName = []
            for ind, val in enumerate(summary):
                if ind in chindices:
                    channelName.append(val)
            k = [1] * len(chnameindices)

            #store channel names
            for z in range(len(channelName)):
                a = []
                for num in range(len(chnameindices)):
                    if chindices[z] > chnameindices[num]:
                        a.append(1)
                    else:
                        a.append(0)

                b = max([i+1 for (i, val) in enumerate(a) if val == 1])
                ch = summary[chindices[z]].split(": ")
                chname = ch[1]

                if b == 1:
                    set1.append(chname)
                if b == 2:
                    set2.append(chname)
                if b == 3:
                    set3.append(chname)
                if b == 4:
                    set4.append(chname)
                if b == 5:
                    set5.append(chname)
                if b == 6:
                    set6.append(chname)



                # T[k[b-1,0]-1, = chname
                # print(T[int(k[b-1]-1),b-1])

                #
                # T[k[b-1],b-1] = chname
                #
                k[b-1] += 1
            T.append(set1)
            T.append(set2)
            T.append(set3)
            T.append(set4)
            T.append(set5)
            T.append(set6)

            # if len(a) == 1:
            #     pass

            #find channel names related to the EDF file
            EDFName = (CheckSeizureEDF.name + CheckSeizureEDF.ext)
            b = []
            for i2, l2 in enumerate(summary):
                if (CheckSeizureEDF.name+CheckSeizureEDF.ext) in l2:
                    b.append(i2)

            c = []
            for num in range(len(chnameindices)):
                if b[0] > chnameindices[num]:
                    c.append(1)
                else:
                    c.append(0)

            j = max([i+1 for (i, val) in enumerate(c) if val == 1])

            EDFChannel = T[j-1]


            # print('debug')

            #remove empty cells
            # EDFChannel = list(filter(None, EDFChannel))

            #find specified channels in the list
            for i5, v in enumerate(EDFChannel):
                if v in SpecifiedChannels:
                    ChannelIndex.append(i5)

            indexsize = len(ChannelIndex)

        if b != 0 and indexsize == 18:
            tictoc = t.time() #tic
            filename = (curr_folder + '/' + (CheckSeizureEDF.name+CheckSeizureEDF.ext))

            #getting signal property
            signals, signal_headers, header = highlevel.read_edf(filename)

            for key, val in signal_headers[1].items():
                if key == "sample_rate":
                    Frequency = int(val)
            Numchannels = len(signal_headers)
            data = signals
            data = data[ChannelIndex,:]

            # try:
            #     SaveData2 = (curr_folder + '/codetestingpymatlab')
            #     os.mkdir(SaveData2)
            # except:
            #     pass

            #find seizure interval and signal duration (Def SignalSiezureIntervalBaseLine)
            DesiredIntv = 10
            whichline = []
            for i3, l3 in enumerate(summary):
                if (CheckSeizureEDF.name + CheckSeizureEDF.ext) in l3:
                    whichline.append(i3)
            txtName = (CheckSeizureEDF.name+CheckSeizureEDF.ext).split('_')
            chbName = txtName[0]
            STimetxt = summary[whichline[0]+1].split(':')
            ETimetxt = summary[whichline[0]+2].split(':')
            q = chbName


            if q[0:5] == 'chb24':
                SigDuration = 3600
                Numseizure = summary[whichline[0]+1]
                x = Numseizure.split(':')
                NumSeizure = int(x[-1])
            else:
                Starttime = int(STimetxt[1])*3600 + int(STimetxt[2])*60 + int(STimetxt[3])
                Endtime = int(ETimetxt[1])*3600 + int(ETimetxt[2])*60 + int(ETimetxt[3])
                SigDuration = Endtime - Starttime
                Numseizure = summary[whichline[0]+3]
                x = Numseizure.split(':')
                NumSeizure = int(x[-1])

            SeizureStart = np.zeros((NumSeizure,1))
            SeizureEnd = np.zeros((NumSeizure,1))
            SeizureDuration = np.zeros((NumSeizure,1))
            SigStart = np.zeros((NumSeizure,1))
            SigEnd = np.zeros((NumSeizure,1))

            for i2 in range(0,NumSeizure):
                if q[0:5] == 'chb24':
                    ss = summary[whichline[0]+2+(i2)*2]
                    ee = summary[whichline[0]+3+(i2)*2]
                else:
                    ss = summary[whichline[0]+4+(i2)*2]
                    ee = summary[whichline[0]+5+(i2)*2]

                c = ss.split()
                SeizureStart[i2] = int(c[-2])

                d = ee.split()
                SeizureEnd[i2] = int(d[-2])

                SeizureDuration[i2] = (SeizureEnd[i2]-SeizureStart[i2])+1
                SigStart[i2] = SeizureStart[i2] - DesiredIntv*SeizureDuration[i2]
                SigEnd[i2] = SeizureEnd[i2] + DesiredIntv*SeizureDuration[i2]

                if SigStart[i2] < 0:
                    SigStart[i2] = 1
                if SigEnd[i2] >= SigDuration:
                    SigEnd[i2] = SigDuration

            #Cleaning the signal and removing noise (Def RemoveNoiseBaseline)

            from scipy import signal
            Fs = Frequency
            n_channels = data.shape[0]
            data = np.array(data)

            dataT = data.T
            f0 = 60.0  # Frequency to be removed from signal (Hz)

            Q = 30.0  # Quality factor

            # Design notch filter

            b, a = signal.iirnotch(f0, Q, Fs)

            # Apply notch filter to the noisy signal using signal.filtfilt

            outputSignal = signal.filtfilt(b, a, dataT)
            outputSignal = outputSignal.T

            #Calculate DI and MI and saving the results
            NumofSeizure = len(SeizureStart)

            #Calculate DI and MI for cleaned data for W1clean
            for p in range(0, NumSeizure):
                RawSig = data[:, int(SigStart[p]*Fs)-1:int(SigEnd[p]*Fs)]
                DenoisedSig = outputSignal[:, int(SigStart[p]*Fs)-1:int(SigEnd[p]*Fs)]
                DenoisedSigSeizure=outputSignal[:, int(SeizureStart[p]*Fs)-1:int(SeizureEnd[p]*Fs)]



                Seizure_start = SeizureStart[p]
                Seizure_end = SeizureEnd[p]
                Sig_Start = SigStart[p]
                Sig_End = SigEnd[p]


                dirname = '/Volumes/D/pymatlab1'
                savemat(os.path.join(dirname, CheckSeizureEDF.name) + '_' + str(p+1) + '.mat', {"Fs":Fs, 'Seizure_start':Seizure_start, 'Seizure_end': Seizure_end, 'Sig_start':Sig_Start, 'Sig_end':Sig_End, 'NoisySignal':data, 'DenoisedSignal':DenoisedSig})





            elapsed = t.time() - tictoc #toc
            print("Processing " + CheckSeizureEDF.name + " Elapsed time is " + str(elapsed)[:-12] + " seconds")



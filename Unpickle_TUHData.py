import pickle
import collections
import matplotlib.pyplot as plt
import numpy as np

seizure_type_data = collections.namedtuple('seizure_type_data', ['patient_id', 'seizure_type', 'seizure_start', 'seizure_end', 'data', 'new_sig_start', 'new_sig_end', 'original_sample_frequency'])
filename_pkl = '/home/dplatnick/TUH_Output_test/v1.5.2/raw_seizures/szr_0_pid_00000258_type_TCSZ.pkl'
filename_lbl = '/home/dplatnick/TUH_Output_test/v1.5.2/raw_seizures/szr_0_pid_00000258_type_TCSZ.lbl'

# unpickle and access .pkl contents
unpickled_contents = pickle.load(open(filename_pkl, 'rb'))

for i in unpickled_contents:
    print(i)

# read .lbl as text (Line-by-line)
with open(filename_lbl) as f:
    test_lbl = f.readlines()
# remove newlines
lbl_contents = [x.strip() for x in test_lbl]

print(lbl_contents)

signal = unpickled_contents[4]
print(signal.shape, type(signal))

print(signal[0,:])

chan_num = 0

for channel in range(len(signal)):
    plt.plot(signal[chan_num,:])
    plt.axis([0, len(signal[chan_num]), -750, 750])
    plt.show()
    plt.title("Channel " + str(1+channel))
    chan_num += 1



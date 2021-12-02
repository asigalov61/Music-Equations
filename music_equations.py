# -*- coding: utf-8 -*-
"""Music_Equations.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/asigalov61/Music-Equations/blob/main/Music_Equations.ipynb

# Music Equations (ver 0.3)

***

## Listen to the muse of mathematics!!!

***

### Project Los Angeles
### Tegridy Code 2021

***

# Setup Environment
"""

# Commented out IPython magic to ensure Python compatibility.
#@title Install dependencies
# %cd /content/
!git clone https://github.com/asigalov61/tegridy-tools
!pip install -U scikit-learn

# Commented out IPython magic to ensure Python compatibility.
#@title Import modules
# %cd /content/tegridy-tools/tegridy-tools
import os
import TMIDIX
from joblib import dump, load
from sklearn.preprocessing import StandardScaler, RobustScaler
import math
import numpy as np
# %cd /content/

"""# Process"""

#@title Load the source MIDI file
full_path_to_MIDI_file = "/content/tegridy-tools/tegridy-tools/seed2.mid" #@param {type:"string"}
perfect_timings = True #@param {type:"boolean"}
data = TMIDIX.Optimus_MIDI_TXT_Processor(full_path_to_MIDI_file, MIDI_patch=range(0, 127), MIDI_channel=-1, perfect_timings=perfect_timings)

#@title Encode to INTs
sts = []
pitches = []
durs = []
pe = data[2][0]
for d in data[2]:

    sts.append(abs(d[1]-pe[1]))
    durs.append(d[2])
    pitches.append(d[4])
    pe = d
print(sts[:5])
print(durs[:5])
print(pitches[:5])
# prepare data for standardization
sts1 = np.asarray(sts)
sts2 = sts1.reshape((len(sts1), 1))
# train the standardization
#scaler = RobustScaler(with_centering=False, with_scaling=True)
scaler = StandardScaler(with_mean=True)
scaler = scaler.fit(sts2)
print('Mean: %f, StandardDeviation: %f' % (scaler.mean_, math.sqrt(scaler.var_)))
# standardization the dataset and print the first 5 rows
sts_norm = scaler.transform(sts2)
sts_ints = []
for d in sts_norm.tolist():
  #print(d * 10000)
  #z = 5
  #y = round(d[0], math.ceil(-math.log10(d[0])) + z)
  #sts_ints.append(y)
  sts_ints.append(abs(math.ceil(d[0])))
for i in range(15):
	  print(sts_ints[i])

dump(scaler, '/content/sts_scaler.bin', compress=True)

print('=====')

# prepare data for standardization
durs1 = np.asarray(durs)
durs2 = durs1.reshape((len(durs1), 1))
#scaler1 = RobustScaler(with_centering=False, with_scaling=True)
scaler1 = StandardScaler(with_mean=True)
scaler1 = scaler1.fit(durs2)
print('Mean: %f, StandardDeviation: %f' % (scaler1.mean_, math.sqrt(scaler1.var_)))
# standardization the dataset and print the first 5 rows
durs_norm = scaler1.transform(durs2)


durs_ints = []
for d in durs_norm:
  #print(d * 10000)
  #z = 5
  #y = round(d, math.ceil(-math.log10(d)) + z)
  #durs_ints.append(y)
  durs_ints.append(abs(math.ceil(d[0])))
for i in range(15):
	  print(durs_ints[i])
dump(scaler1, '/content/sts_scaler1.bin', compress=True)

#@title Decode back to MIDI
floats_vs_ints = True #@param {type:"boolean"}
out_sts = []

if floats_vs_ints:
  z = sts_norm
else:
  z = np.asarray(sts_ints, dtype=float).reshape(-1, 1) # / 20000

# inverse transform and print the first 5 rows
inversed = scaler.inverse_transform(z)
for i in range(len(z)):
  #print(int(inversed[i]))
  out_sts.append(math.ceil(inversed[i]))

print('========')

out_durs = []
if floats_vs_ints:
  z = durs_norm
else:
  z = np.asarray(durs_ints, dtype=float).reshape(-1, 1) #/ 20000

# inverse transform and print the first 5 rows
inversed = scaler1.inverse_transform(z)
for i in range(len(z)):
  #print(int(inversed[i]))
  out_durs.append(math.ceil(inversed[i]))


song = []
time = 0
for i in range(len(pitches)):
  song.append(['note', time, out_durs[i], 0, pitches[i], pitches[i]+15])
  time += out_sts[i]

TMIDIX.Tegridy_SONG_to_MIDI_Converter(song, output_file_name='/content/Music-Equations-Composition',
                                      number_of_ticks_per_quarter=500,
                                      track_name='sklearn StandardScaler',
                                      output_signature='Music Equations')

"""# Listen"""

#@title Install prerequisites
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio
!pip install pretty_midi

#@title Plot and listen to the output
#@markdown NOTE: May be very slow with the long compositions
from midi2audio import FluidSynth
from IPython.display import display, Javascript, HTML, Audio
import pretty_midi
import librosa.display
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

print('Synthesizing the last output MIDI... ')
fname = '/content/Music-Equations-Composition'

fn = os.path.basename(fname + '.mid')
fn1 = fn.split('.')[0]

print('Plotting the composition. Please wait...')

pm = pretty_midi.PrettyMIDI(fname + '.mid')

# Retrieve piano roll of the MIDI file
piano_roll = pm.get_piano_roll()

plt.figure(figsize=(14, 5))
librosa.display.specshow(piano_roll, x_axis='time', y_axis='cqt_note', fmin=1, hop_length=160, sr=16000, cmap=plt.cm.hot)
plt.title(fn1)

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
Audio(str(fname + '.wav'), rate=16000)

"""# Congrats! You did it! :)"""
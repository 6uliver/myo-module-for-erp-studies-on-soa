
# MYO module for ERP studies on SoA  
  
## Requirements
  
- Windows 7 or greater (64-bit)
- Python 2.7.16 (64-bit) (https://www.python.org/downloads/release/python-2716/)
- PsychoPy 1.82.02 (https://github.com/psychopy/psychopy/releases/download/r1.82.02/StandalonePsychoPy-1.82.02-win32.exe)
- Myo gesture control armband by North (formerly Thalmic Labs)
- Myo Connect (https://support.getmyo.com/hc/en-us/articles/360018409792-Myo-Connect-SDK-and-firmware-downloads)

## Install
  
1. Install dependencies to PsychoPy site-packages, for example run in an administrative command prompt the following: `pip install -r requirements.txt -t "C:\Program Files (x86)\PsychoPy2\Lib\site-packages"`
2. Install Myo Connect and follow the setup instructions: https://s3.amazonaws.com/thalmicdownloads/windows/1.0.1/Myo+Connect+Installer.exe

## How to start experiments

1. Start Myo Connect and start Myo Armband
2. Start PsychoPy, open one of the files below and run it

## Experimental paradigms  

roc.py

calibration.py

active.py
It contains the motor-induced (MI) condition. The participant is instructed to perform wrist dorsiflexions in a self-paced manner, aiming at a rhythm of about 2 seconds. The participant is also instructed that the software would not respond to very fast responses (<1500 ms, unbeknownst to the participants) and that each movement will be immediately followed by a briefly presented hand stimulus. The task begins with a practice phase consisting of 15 trials (it is coded in the variable 'gyak_trialszam'). The practice session ends when 80% of the trials are completed successfully (i.e. the participant waits for at least 1.75 s between two movements), otherwise, it is repeated. In this phase, the participant gets feedback about their reaction time.  
In the test phase, the instruction remains the same, but no feedback is given about the reaction time. When a movement is detected, the program triggers the EEG recorder, after which, the stimulus appears on the screen for 300 ms (coded in the variable 'stimulus_interval'). This phase lasts for 120 trials (coded in the variable ‘trialszam’ in the config.py file). Additional reinforcement of control (RoC) trials are inserted five times pseudo-randomly.  

motor.py
It contains the motor-only (MO) condition. The task is identical to the MI condition, but no visual hand stimuli are presentation.  

passive.py
It contains the passive viewing (PV) condition. The participant is instructed to maintain fixation while stimulus appears on the screen. The variable 'ISI' stores 20 interstimulus intervals ranging between 1500 ms and 2450 ms. The task consists of 120 trials (coded in the variable ‘trialszam’ in the config.py file). At the beginning of each trial, a fixation cross is displayed for the duration of one of the predefined ISIs. After the delay, the program triggers the EEG recorder, after which, the stimulus appears on the screen for 300 ms (coded in the variable 'stimulus_interval'). Additional RoC trials are inserted five times pseudo-randomly.  

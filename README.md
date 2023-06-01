# SBND_TPC_Laser
SBND laser control Script
Note that it's actually from microboone written in python 2 by Mathias, I just took the same thing and converted them to python 3 and made some changes as per the new requirements... 
and it's not properly refined... So it contains many unwanted scripts which we either changed the components or not using them anymore...
for example.. heidenhein encoder readers..

What basically I do is go to "RunControl --> devices-->Config -->com_ports.json
set the usb paths to appropriate componnents..
cd back to RunControl..
Open terminal
source Config.sh
python -i Shiva_Demo.py
then from there python intecative shell I just run the mototrs..

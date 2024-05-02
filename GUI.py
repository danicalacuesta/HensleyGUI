# Catalyst design GUI version for use in Stevens CH116 course.
# Last updated: 01/10/2022

import PySimpleGUI as sg
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression

def kubic_harm(En):
	x1 = [0.333333333,1,0.5]
	x2 = [0.037037037,0,0]
	fit_x = np.array([x1,x2]).transpose()
	model = LinearRegression()
	model.fit(fit_x,En)
	return [model.intercept_,model.coef_[0],model.coef_[1]]

def NP_calc(T,E_H,E_O,E_OH,P_H2,P_O2):
	npoints = 50 
	phi = np.radians(np.linspace(0,360,npoints))
	theta = np.radians(np.linspace(0,90,npoints))
	
	P_H2O = 1 # Pa, Pressure (kept as small as possible)
	kB = 1.38064852*10**(-23) # J/K, Boltzmann Constant
	h = 6.62607004*10**(-34) # J*s, Plank's Constant
	mH2 = 1.00784*2/(6.022*10**23)/1000 # kg, H2 Mass
	mO2 = 31.999/(6.022*10**23)/1000 # kg, O2 Mass
	mH2O = 18.01528/(6.022*10**23)/1000 # kg, H2O Mass
	kB2 = 8.617333262145*10**(-5) # eV/K, Boltzmann Constant
	I_H2 = mH2/4*(0.747277565*10**(-10))**2 # kg*m^2, H2 moment of inertia
	I_O2 = mO2/4*(1.239620627*10**(-10))**2 # kg*m^2, O2 moment of inertia
	I_H2O = 5.8399*10**(-141) # kg^3*m^6, H2O moment of inertia
	lamb_H = h/(2*math.pi*mH2*kB*T)**(1/2)
	lamb_O = h/(2*math.pi*mO2*kB*T)**(1/2)
	
	Zrot_H2 = (8*math.pi*I_H2*kB*T/2/h**2) # H2 rotational partition function
	Zrot_O2 = (8*math.pi*I_O2*kB*T/2/h**2) # O2 rotational partition function
	Ztrans_H2 = kB*T/P_H2*1/lamb_H**3 # H2 translational partition function
	Ztrans_O2 = kB*T/P_O2*1/lamb_O**3 # O2 translational partition function
	
	covH = []
	covO = []
	covOH = []
	
	H_Hads = []
	H_Oads = []
	H_OHrxn = []
	H_H2Orxn = []
	
	S_Hads = []
	S_Oads = []
	S_OHrxn = []
	S_H2Orxn = []
	
	G_Hads = []
	G_Oads = []
	G_OHrxn = []
	G_H2Orxn = []
	
	Keq_Hads = []
	Keq_Oads = []
	Keq_OHrxn = []
	Keq_H2Orxn = []
	for ii in range(0,npoints): # loop over all theta values
		for jj in range(0,npoints): # loop over all phi values        
			nx = math.sin(theta[ii])*math.cos(phi[jj])
			ny = math.sin(theta[ii])*math.sin(phi[jj])
			nz = math.cos(theta[ii])
            
			## Energy values
			Eads_H = E_H[0] + E_H[1]*(nx**4+ny**4+nz**4) + E_H[2]*(nx**2*ny**2*nz**2) 
			Eads_O = E_O[0] + E_O[1]*(nx**4+ny**4+nz**4) + E_O[2]*(nx**2*ny**2*nz**2)
			Erxn_OH = E_OH[0] + E_OH[1]*(nx**4+ny**4+nz**4) + E_OH[2]*(nx**2*ny**2*nz**2)
			## equilibrium constants
			Ke_H = 1/(Zrot_H2*(Ztrans_H2*P_H2))*math.exp(-2*Eads_H/kB2/T) # missing vibrations
			Ke_O = 1/(Zrot_O2*(Ztrans_O2*P_O2))*math.exp(-2*Eads_O/kB2/T) # missing vibrations
			Ke_OH = math.exp(-Erxn_OH/kB2/T) # missing vibrations
			## equilibrium coverages
			tS_surf = (1 + (Ke_H*P_H2)**(1/2) + (Ke_O*P_O2)**(1/2) + Ke_OH*(Ke_H*P_H2*Ke_O*P_O2)**(1/2))**(-1)
			tH_surf = (Ke_H*P_H2)**(1/2)*tS_surf
			tO_surf = (Ke_O*P_O2)**(1/2)*tS_surf
			tOH_surf = Ke_OH*(Ke_H*P_H2*Ke_O*P_O2)**(1/2)*tS_surf
			
			covH.append(tH_surf)
			covO.append(tO_surf)
			covOH.append(tOH_surf)
			
			## Enthalpies (without vibrations)
			temp = 2*Eads_H - 5/2*kB2*T - kB2*T
			H_Hads.append(temp)
			temp = 2*Eads_O - 5/2*kB2*T - kB2*T
			H_Oads.append(temp)
			temp = Erxn_OH
			H_OHrxn.append(temp)
			temp = (-2.3916 - 2*Eads_H - Eads_O - Erxn_OH) + 5/2*kB2*T + 3/2*kB2*T
			H_H2Orxn.append(temp)
			
			## Entropies (without vibrations)
			temp = -kB2*(3/2*math.log(2*math.pi*mH2/h**2) + 5/2*math.log(kB*T) - math.log(P_H2) + 5/2) - kB2*(math.log(8*math.pi**2*I_H2*kB*T/2/h**2) + 1)
			S_Hads.append(T*temp)
			temp = -kB2*(3/2*math.log(2*math.pi*mO2/h**2) + 5/2*math.log(kB*T) - math.log(P_O2) + 5/2) - kB2*(math.log(8*math.pi**2*I_O2*kB*T/2/h**2) + 1)
			S_Oads.append(T*temp)
			temp = 0
			S_OHrxn.append(T*temp)
			temp = kB2*(3/2*math.log(2*math.pi*mH2O/h**2) + 5/2*math.log(kB*T) - math.log(P_H2O) + 5/2) + kB2*(math.log(8*math.pi**2/2) + 3/2*math.log(2*math.pi*kB*T/h**2) + 1/2*math.log(I_H2O) + 3/2)
			S_H2Orxn.append(T*temp)
			
			## Gibbs Energies (without vibration)
			temp = H_Hads[-1] - S_Hads[-1]
			G_Hads.append(temp)
			Keq_Hads.append(math.exp(-temp/kB2/T))
			temp = H_Oads[-1] - S_Oads[-1]
			G_Oads.append(temp)
			Keq_Oads.append(math.exp(-temp/kB2/T))
			temp = H_OHrxn[-1] - S_OHrxn[-1]
			G_OHrxn.append(temp)
			Keq_OHrxn.append(math.exp(-temp/kB2/T))
			temp = H_H2Orxn[-1] - S_H2Orxn[-1]
			G_H2Orxn.append(temp)
			Keq_H2Orxn.append(math.exp(-temp/kB2/T))
	
	aveH = sum(covH)/len(covH)
	aveO = sum(covO)/len(covO)
	aveOH = sum(covOH)/len(covOH)
	
	aveH_Hads = sum(H_Hads)/len(H_Hads)
	aveH_Oads = sum(H_Oads)/len(H_Oads)
	aveH_OHrxn = sum(H_OHrxn)/len(H_OHrxn)
	aveH_H2Orxn = sum(H_H2Orxn)/len(H_H2Orxn)
	
	aveS_Hads = sum(S_Hads)/len(S_Hads)
	aveS_Oads = sum(S_Oads)/len(S_Oads)
	aveS_OHrxn = sum(S_OHrxn)/len(S_OHrxn)
	aveS_H2Orxn = sum(S_H2Orxn)/len(S_H2Orxn)
	
	aveG_Hads = sum(G_Hads)/len(G_Hads)
	aveG_Oads = sum(G_Oads)/len(G_Oads)
	aveG_OHrxn = sum(G_OHrxn)/len(G_OHrxn)
	aveG_H2Orxn = sum(G_H2Orxn)/len(G_H2Orxn)
	
	aveKeq_Hads = sum(Keq_Hads)/len(Keq_Hads)
	aveKeq_Oads = sum(Keq_Oads)/len(Keq_Oads)
	aveKeq_OHrxn = sum(Keq_OHrxn)/len(Keq_OHrxn)
	aveKeq_H2Orxn = sum(Keq_H2Orxn)/len(Keq_H2Orxn)
	
	return [aveH,aveO,aveOH,aveH_Hads,aveH_Oads,aveH_OHrxn,aveH_H2Orxn,aveS_Hads,aveS_Oads,aveS_OHrxn,aveS_H2Orxn,
			aveG_Hads,aveG_Oads,aveG_OHrxn,aveG_H2Orxn,aveKeq_Hads,aveKeq_Oads,aveKeq_OHrxn,aveKeq_H2Orxn]

matplotlib.use("TkAgg")
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

sg.theme('SystemDefault1')  # Let's set our own color theme
# STEP 1 define the layout
font1 = ("Arial",12)
font2 = ("Arial",12,"bold")
input_layout = [
			[sg.Text('Select a Primary Metal',font=font1)],
			[sg.Radio('Pt',"Primary",default=False,key="Pt",font=font1),sg.Radio('Ni',"Primary",default=False,key="Ni",font=font1)],
			[sg.Text('Secondary Metal Conc.',size=(20,1),font=font1),sg.Input(key='PConc',size=(7,1),font=font1),sg.Text("mol%",size=(10,1),font=font1)],
			[sg.Text('Temperature',size=(20,1),font=font1),sg.Input(key='Temp',size=(7,1),font=font1),sg.Text("K",size=(10,1),font=font1)],
			[sg.Text('Total Pressure',size=(20,1),font=font1),sg.Input(key='TotPres',size=(7,1),font=font1),sg.Text("bar",size=(10,1),font=font1)],
			[sg.Text('Hydrogen Composition',size=(20,1),font=font1),sg.Input(key='yH2',size=(7,1),font=font1),sg.Text("mol%",size=(10,1),font=font1)],
			[sg.Text('Oxygen Composition',size=(20,1),font=font1),sg.Input(key='yO2',size=(7,1),font=font1),sg.Text("mol%",size=(10,1),font=font1)],
			[sg.Button('Test catalyst!',font=font2),sg.Button('Reset Graphs',font=font2),sg.Button('Exit',font=font2)],
			[sg.Text('')],
			[sg.Text('Elementary Reaction Steps:',size=(25,1),font=font1)],
			[sg.Text('(1) H\u2082(g) + 2* → 2H*',size=(20,1),font=font1)],
			[sg.Text('(2) O\u2082(g) + 2* → 2O*     Rate Limiting Step (RLS)',size=(38,1),font=font1)],
			[sg.Text('(3) H* + O* → OH* + *',size=(20,1),font=font1)],
			[sg.Text('(4) H* + OH* → H\u2082O(g) + 2*',size=(22,1),font=font1)],
			]

output_layout = [
			[sg.Text('Catalyst Performance',font=font1),sg.Output(key='Perf',size=(20,1),font=font1),sg.Text('Catalyst Cost',font=font1),sg.Output(key='Cost',size=(20,1),font=font1),sg.Text('$/g',font=font1)],
			[sg.Text('ΔH(1) [kJ/mol]',size=(23,1),justification='center',font=font1),sg.Text('ΔH(2) [kJ/mol]',size=(23,1),justification='center',font=font1),sg.Text('ΔH(3) [kJ/mol]',size=(23,1),justification='center',font=font1),sg.Text('ΔH(4) [kJ/mol]',size=(23,1),justification='center',font=font1)],
			[sg.Output(key='H_Hads',size=(22,1),font=font1),sg.Output(key='H_Oads',size=(22,1),font=font1),sg.Output(key='H_OHrxn',size=(21,1),font=font1),sg.Output(key='H_H2Orxn',size=(21,1),font=font1)],
			[sg.Text('T*ΔS(1) [kJ/mol]',size=(23,1),justification='center',font=font1),sg.Text('T*ΔS(2) [kJ/mol]',size=(23,1),justification='center',font=font1),sg.Text('T*ΔS(3) [kJ/mol]',size=(23,1),justification='center',font=font1),sg.Text('T*ΔS(4) [kJ/mol]',size=(23,1),justification='center',font=font1)],
			[sg.Output(key='S_Hads',size=(22,1),font=font1),sg.Output(key='S_Oads',size=(22,1),font=font1),sg.Output(key='S_OHrxn',size=(21,1),font=font1),sg.Output(key='S_H2Orxn',size=(21,1),font=font1)],
			[sg.Text('K\u2091(1)',size=(23,1),justification='center',font=font1),sg.Text('K\u2091(2)',size=(23,1),justification='center',font=font1),sg.Text('K\u2091(3)',size=(23,1),justification='center',font=font1),sg.Text('K\u2091(4)',size=(23,1),justification='center',font=font1)],
			[sg.Output(key='K_Hads',size=(22,1),font=font1),sg.Output(key='K_Oads',size=(22,1),font=font1),sg.Output(key='K_OHrxn',size=(21,1),font=font1),sg.Output(key='K_H2Orxn',size=(21,1),font=font1)],
			[sg.Canvas(key="-CANVAS1-")]
			]

layout = [
			[sg.Column(input_layout),sg.VSeperator(),sg.Column(output_layout)]
			]

def ptable_input():
	while True:
		layout2 = [
				[sg.Text('Select a Secondary Metal',size=(26,1),font=font1)],
				[sg.Button('Ti',font=font2,size=(3,1)),sg.Button('V',font=font2,size=(3,1)),sg.Button('Cr',font=font2,size=(3,1)),sg.Button('Mn',font=font2,size=(3,1)),sg.Button('Fe',font=font2,size=(3,1)),sg.Button('Co',font=font2,size=(3,1)),sg.Button('Ni',font=font2,size=(3,1)),sg.Button('Cu',font=font2,size=(3,1))],
				[sg.Button('Zr',font=font2,size=(3,1)),sg.Button('Nb',font=font2,size=(3,1)),sg.Button('Mo',font=font2,size=(3,1)),sg.Button('Tc',font=font2,size=(3,1)),sg.Button('Ru',font=font2,size=(3,1)),sg.Button('Rh',font=font2,size=(3,1)),sg.Button('Pd',font=font2,size=(3,1)),sg.Button('Ag',font=font2,size=(3,1))],
				[sg.Button('Hf',font=font2,size=(3,1)),sg.Button('Ta',font=font2,size=(3,1)),sg.Button('W',font=font2,size=(3,1)),sg.Button('Re',font=font2,size=(3,1)),sg.Button('Os',font=font2,size=(3,1)),sg.Button('Ir',font=font2,size=(3,1)),sg.Button('Pt',font=font2,size=(3,1)),sg.Button('Au',font=font2,size=(3,1))]
				]
		window2 = sg.Window('Transition Metals',layout2,finalize=True)
		event2, values2 = window2.read()
		if event2 == 'Ti':
			EN_p = 1.54
			Nelec_p = 4
			Ed_p = 0.7
			Oxo_p = 1.0
			WF_p = 3.95
			Cost_p = 11.1
			MW_p = 47.867
			break
		elif event2 == 'V':
			EN_p = 1.63
			Nelec_p = 5
			Ed_p = 0.4
			Oxo_p = 0.8
			WF_p = 4.10
			Cost_p = 357
			MW_p = 50.9415
			break
		elif event2 == 'Cr':
			EN_p = 1.66
			Nelec_p = 6
			Ed_p = -0.3
			Oxo_p = 0.6
			WF_p = 4.60
			Cost_p = 9.40
			MW_p = 51.9961
			break
		elif event2 == 'Mn':
			EN_p = 1.55
			Nelec_p = 7
			Ed_p = -0.9
			Oxo_p = 0.4
			WF_p = 3.80
			Cost_p = 1.82
			MW_p = 54.938044
			break
		elif event2 == 'Fe':
			EN_p = 1.83
			Nelec_p = 8
			Ed_p = -0.8
			Oxo_p = 0.4
			WF_p = 4.30
			Cost_p = 0.424
			MW_p = 55.845
			break
		elif event2 == 'Co':
			EN_p = 1.88
			Nelec_p = 9
			Ed_p = -1.5
			Oxo_p = 0.4
			WF_p = 4.40
			Cost_p = 32.8
			MW_p = 58.933195
			break
		elif event2 == 'Ni':
			EN_p = 1.91
			Nelec_p = 10
			Ed_p = -1.6
			Oxo_p = 0.2
			WF_p = 4.50
			Cost_p = 13.9
			MW_p = 58.6934
			break
		elif event2 == 'Cu':
			EN_p = 1.90
			Nelec_p = 11
			Ed_p = -2.5
			Oxo_p = 0.2
			WF_p = 4.40
			Cost_p = 6.00
			MW_p = 63.546
			break
		elif event2 == 'Zr':
			EN_p = 1.33
			Nelec_p = 4
			Ed_p = 0.7
			Oxo_p = 0.8
			WF_p = 3.90
			Cost_p = 35.7
			MW_p = 91.224
			break
		elif event2 == 'Nb':
			EN_p = 1.60
			Nelec_p = 5
			Ed_p = 0.1
			Oxo_p = 0.8
			WF_p = 4.00
			Cost_p = 61.4
			MW_p = 92.90638
			break
		elif event2 == 'Mo':
			EN_p = 2.16
			Nelec_p = 6
			Ed_p = -0.9
			Oxo_p = 0.6
			WF_p = 4.30
			Cost_p = 40.1
			MW_p = 95.94
			break
		elif event2 == 'Tc':
			EN_p = 1.90
			Nelec_p = 7
			Ed_p = -1.6
			Oxo_p = 0.5
			WF_p = 4.4
			Cost_p = 100000
			MW_p = 98
			break
		elif event2 == 'Ru':
			EN_p = 2.20
			Nelec_p = 8
			Ed_p = -1.9
			Oxo_p = 0.4
			WF_p = 4.60
			Cost_p = 10400
			MW_p = 101.07
			break
		elif event2 == 'Rh':
			EN_p = 2.28
			Nelec_p = 9
			Ed_p = -2.1
			Oxo_p = 0.3
			WF_p = 4.75
			Cost_p = 147000
			MW_p = 102.9055
			break
		elif event2 == 'Pd':
			EN_p = 2.20
			Nelec_p = 10
			Ed_p = -1.8
			Oxo_p = 0.0
			WF_p = 4.80
			Cost_p = 49500
			MW_p = 106.42
			break
		elif event2 == 'Ag':
			EN_p = 1.93
			Nelec_p = 11
			Ed_p = -4.0
			Oxo_p = 0.2
			WF_p = 4.30
			Cost_p = 521
			MW_p = 107.8682
			break
		elif event2 == 'Hf':
			EN_p = 1.30
			Nelec_p = 4
			Ed_p = 0.7
			Oxo_p = 1.0
			WF_p = 3.50
			Cost_p = 900
			MW_p = 178.49
			break
		elif event2 == 'Ta':
			EN_p = 1.50
			Nelec_p = 5
			Ed_p = 0.3
			Oxo_p = 0.8
			WF_p = 4.10
			Cost_p = 298
			MW_p = 171.9449
			break
		elif event2 == 'W':
			EN_p = 2.36
			Nelec_p = 6
			Ed_p = -0.8
			Oxo_p = 0.8
			WF_p = 4.50
			Cost_p = 35.3
			MW_p = 183.84
			break
		elif event2 == 'Re':
			EN_p = 1.90
			Nelec_p = 7
			Ed_p = -1.6
			Oxo_p = 0.5
			WF_p = 5.00
			Cost_p = 3010
			MW_p = 186.207
			break
		elif event2 == 'Os':
			EN_p = 2.20
			Nelec_p = 8
			Ed_p = -2.2
			Oxo_p = 0.4
			WF_p = 4.70
			Cost_p = 12000
			MW_p = 190.2
			break
		elif event2 == 'Ir':
			EN_p = 2.20
			Nelec_p = 9
			Ed_p = -2.9
			Oxo_p = 0.4
			WF_p = 5.30
			Cost_p = 55500
			MW_p = 192.22
			break
		elif event2 == 'Pt':
			EN_p = 2.28
			Nelec_p = 10
			Ed_p = -2.4
			Oxo_p = 0.1
			WF_p = 5.30
			Cost_p = 27800
			MW_p = 195.084
			break
		elif event2 == 'Au':
			EN_p = 2.54
			Nelec_p = 11
			Ed_p = -3.4
			Oxo_p = 0.0
			WF_p = 4.30
			Cost_p = 44800
			MW_p = 196.96657
			break
	window2.close()
	return [EN_p,Nelec_p,Ed_p,Oxo_p,WF_p,Cost_p,MW_p]

#STEP 2 - create the window
window = sg.Window('Computational Tool for Catalyst Design and Testing', layout,finalize=True)
fig, ax = plt.subplots(1,4,figsize=(8.8,3))
ax[0].set_xlabel('Test Run #')
ax[1].set_xlabel('Test Run #')
ax[2].set_xlabel('Test Run #')
ax[3].set_xlabel('Test Run #')
ax[0].set_title('Catalyst Performance')
ax[1].set_title('Catalyst Cost')
ax[2].set_title('RLS ΔH')
ax[3].set_title('RLS T*ΔS')
ax[0].set_xticks([0,1])
ax[1].set_xticks([0,1])
ax[2].set_xticks([0,1])
ax[3].set_xticks([0,1])
plt.tight_layout()
fig_agg1 = draw_figure(window["-CANVAS1-"].TKCanvas, fig)

ii = 0
run = []
y_perf = []
y_cost = []
y_H = []
y_S = []
# STEP3 - the event loop
while True:
	event, values = window.read()   # Read the event that happened and the values dictionary
	if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
		break
	if event == 'Reset Graphs':
		ax[0].cla()
		ax[1].cla()
		ax[2].cla()
		ax[3].cla()
		run = []
		y_perf = []
		y_cost = []
		y_H = []
		y_S = []
		ii = 0
		ax[0].set_xlabel('Test Run #')
		ax[0].set_title('Catalyst Performance')
		ax[0].set_xticks([0,1])
		ax[1].set_xlabel('Test Run #')
		ax[1].set_title('Catalyst Cost')
		ax[1].set_xticks([0,1])
		ax[2].set_xlabel('Test Run #')
		ax[2].set_title('RLS ΔH')
		ax[2].set_xticks([0,1])
		ax[3].set_xlabel('Test Run #')
		ax[3].set_title('RLS T*ΔS')
		ax[3].set_xticks([0,1])
		plt.tight_layout()
		fig_agg1.draw()
	if event == 'Test catalyst!':
		ax[0].cla()
		ax[1].cla()	
		ax[2].cla()
		ax[3].cla()		
		ii = ii + 1
		[EN_p,Nelec_p,Ed_p,Oxo_p,WF_p,Cost_p,MW_p] = ptable_input()
		percent = float(values["PConc"])/100
		T = float(values["Temp"])
		P0 = float(values["TotPres"])
		yH2 = float(values["yH2"])/100
		yO2 = float(values["yO2"])/100
		P_H2 = yH2*P0*10**5
		P_O2 = yO2*P0*10**5
		mol_p = 100
		mol_m = (1-percent)/percent*mol_p #
		
		if values["Pt"] == True:
			MW_m = 195.084
			kg_p = mol_p*MW_p/1000 #MW_P is in secondary metal, mol_p is 100
			kg_m = mol_m*MW_m/1000 
			Cost = (kg_p*Cost_p + kg_m*27800)/(kg_p+kg_m)/1000 #COST OF CATALYST
			EN = percent*EN_p + (1-percent)*2.28
			Nelec = percent*Nelec_p + (1-percent)*10
			Ed = percent*Ed_p + (1-percent)*-2.4
			Oxo = percent*Oxo_p + (1-percent)*0.1
			WF = percent*WF_p + (1-percent)*5.30
			E_H_111 = 4.213030693027572 + -0.32727538*EN + 0.05669554*Nelec + -0.09761938*Ed + 0.11309732*Oxo + -0.87419596*WF
			E_O_111 = -11.956527141179059 + 1.50473495*EN + 0.68739438*Nelec + -0.41262222*Ed + -2.47668493*Oxo + -0.01832057*WF
			E_OH_111 = 3.9529494317252314 + -0.87687441*EN + -0.53206556*Nelec + 0.22864321*Ed + 0.72153466*Oxo + 0.72189822*WF
		
			E_H_100 = 0.7755600376217998 + 0.29819632*EN + -0.02581695*Nelec + -0.0241474*Ed + -0.33129999*Oxo + -0.32034615*WF
			E_O_100 = -10.499850324627126 + 1.14696783*EN + 0.76143161*Nelec + -0.14333125*Ed + -2.33331553*Oxo + -0.15271949*WF
			E_OH_100 = 4.309526837821751 + -0.89049206*EN + -0.56069136*Nelec + -0.16625732*Ed + -0.06385006*Oxo + 0.46803022*WF
		
			E_H_110 = 3.4386214388903507 + -0.53028481*EN + 0.16079572*Nelec + 0.00233229*Ed + 0.19778387*Oxo + -0.81348923*WF
			E_O_110 = -12.531253313761404 + 1.02631151*EN + 1.22862898*Nelec + 0.3313771*Ed + -0.31419467*Oxo + -0.45983478*WF
			E_OH_110 = -1.346091374900017 + 0.02414613*EN + -0.76622333*Nelec + -0.18991871*Ed + -0.58588074*Oxo + 1.54998765*WF
		else:
			MW_m = 58.6934
			kg_p = mol_p*MW_p/1000
			kg_m = mol_m*MW_m/1000
			Cost = (kg_p*Cost_p + kg_m*13.9)/(kg_p+kg_m)/1000
			EN = percent*EN_p + (1-percent)*1.91
			Nelec = percent*Nelec_p + (1-percent)*10
			Ed = percent*Ed_p + (1-percent)*-1.6
			Oxo = percent*Oxo_p + (1-percent)*0.2
			WF = percent*WF_p + (1-percent)*4.50
			E_H_111 = -2.226020380380351 + 0.67556302*EN + -0.00206256*Nelec + -0.04349742*Ed + -1.02433858*Oxo + 0.15960867*WF
			E_O_111 = -16.996588072247526 + 1.92509039*EN + 0.48636318*Nelec + 0.13812323*Ed + -2.21438179*Oxo + 1.57681775*WF
			E_OH_111 = 15.827551542622002 + -2.45163976*EN + -0.92428652*Nelec + -0.98479147*Ed + -0.3735415*Oxo + -0.72630852*WF
		
			E_H_100 = -2.142105152211282 + 0.35814843*EN + 0.11678366*Nelec + 0.03951107*Ed + 0.05438802*Oxo + 0.00727691*WF
			E_O_100 = -16.116540944573604 + 0.88704685*EN + 0.7353944*Nelec + -0.11002544*Ed + -2.27095613*Oxo + 1.11957875*WF
			E_OH_100 = 8.813426071986639 + -0.09899061*EN + -0.57825146*Nelec + -0.27992855*Ed + 1.08821171*Oxo + -0.74372344*WF
		
			E_H_110 = -0.04917406021307416 + 0.11288951*EN + 0.13766019*Nelec + -0.00284053*Ed + -0.46324136*Oxo + -0.37363243*WF
			E_O_110 = -9.522228552084762 + 1.20574522*EN + 0.70381791*Nelec + -0.02363718*Ed + -2.34262155*Oxo + -0.25123037*WF
			E_OH_110 = 3.398430449840717 + -0.85342039*EN + -0.67137642*Nelec + -0.18191033*Ed + 0.44028798*Oxo + 0.87223008*WF

		E_H = kubic_harm([E_H_111,E_H_100,E_H_110])
		E_O = kubic_harm([E_O_111,E_O_100,E_O_110])
		E_OH = kubic_harm([E_OH_111,E_OH_100,E_OH_110])
		
		[aH,aO,aOH,H_Hads,H_Oads,H_OHrxn,H_H2Orxn,S_Hads,S_Oads,S_OHrxn,S_H2Orxn,G_Hads,G_Oads,G_OHrxn,G_H2Orxn,Keq_Hads,Keq_Oads,Keq_OHrxn,Keq_H2Orxn] = NP_calc(T,E_H,E_O,E_OH,P_H2,P_O2)
		
		kB = 1.38064852*10**(-23)
		h = 6.62607004*10**(-34)
		catal_perf = math.log10(kB*T/h*aOH*aH) # PERFORMANCE OF CATALYST 
		
		run.append(ii)
		y_perf.append(catal_perf)
		y_cost.append(Cost)
		ax[0].plot(run,y_perf,'o:')
		ax[0].set_xlabel('Test Run #')
		ax[0].set_title('Catalyst Performance')
		ax[0].set_xticks(run)
		ax[1].plot(run,y_cost,'o:')
		ax[1].set_xlabel('Test Run #')
		ax[1].set_title('Catalyst Cost')
		ax[1].set_xticks(run)
		
		ax[2].set_xlabel('Test Run #')
		ax[2].set_title('RLS ΔH')
		ax[2].set_xticks(run)
		ax[3].set_xlabel('Test Run #')
		ax[3].set_title('RLS T*ΔS')
		ax[3].set_xticks(run)
		y_H.append(H_Oads*96.485)
		y_S.append(S_Oads*96.485)
		ax[2].plot(run,y_H,'o:')
		ax[3].plot(run,y_S,'o:')
			
		plt.tight_layout()
		fig_agg1.draw()
		
		window["Perf"].update("{:.2f}".format(catal_perf))
		window["Cost"].update("{:.2f}".format(Cost))
		window["H_Hads"].update("{:.1f}".format(H_Hads*96.485))
		window["H_Oads"].update("{:.1f}".format(H_Oads*96.485))
		window["H_OHrxn"].update("{:.1f}".format(H_OHrxn*96.485))
		window["H_H2Orxn"].update("{:.1f}".format(H_H2Orxn*96.485))
		
		window["S_Hads"].update("{:.1f}".format(S_Hads*96.485))
		window["S_Oads"].update("{:.1f}".format(S_Oads*96.485))
		window["S_OHrxn"].update("{:.1f}".format(S_OHrxn*96.485))
		window["S_H2Orxn"].update("{:.1f}".format(S_H2Orxn*96.485))
		
		window["K_Hads"].update("{:.2e}".format(Keq_Hads))
		window["K_Oads"].update("{:.2e}".format(Keq_Oads))
		window["K_OHrxn"].update("{:.2e}".format(Keq_OHrxn))
		window["K_H2Orxn"].update("{:.2e}".format(Keq_H2Orxn))
  
window.close()

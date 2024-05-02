from flask import Flask, request
#UPDATE: got started, got up to kg_p property of pt
#To do: finish initializing all of the variables of Pt and Ni
# make sure all inputs are under eachother and try to make everything centered
#reach: get started on implementing all of the inputs
app = Flask(__name__)

# Define properties of primary metals as dictionaries
properties = {
    "Pt": {
        "MW_m": 195.084,
        "mol_p": 100
        # Add other properties of Pt here
    },
    "Ni": {
        "MW_m": 58.6934,
        # Add other properties of Ni here
    }
}

#define properties of secondary metals 
properties_2={
    'Ti':{
        "EN_p" : 1.54,
		"Nelec_p" : 4,
		"Ed_p" : 0.7,
		"Oxo_p" : 1.0,
		"WF_p" : 3.95,
		"Cost_p" : 11.1,
		"MW_p" : 47.867
        }
        ,
    'V':{
        "EN_p" : 1.63,
		"Nelec_p" : 5,
		"Ed_p" : 0.4,
		"Oxo_p" : 0.8,
		"WF_p" : 4.10,
		"Cost_p" : 357,
		"MW_p" : 50.9415
        },
    'Cr':{
        "EN_p" : 1.54,
		"Nelec_p" : 4,
		"Ed_p" : 0.7,
		"Oxo_p" : 1.0,
		"WF_p" : 3.95,
		"Cost_p" : 11.1,
		"MW_p" : 47.867
        },
    'Mn':{
        'EN_p': 1.55,
        'Nelec_p': 7,
        'Ed_p': -0.9,
        'Oxo_p': 0.4,
        'WF_p': 3.8,
        'Cost_p': 0.0182,
        'MW_p': 54.938044
    },
    'Fe':{
        'EN_p': 1.83,
        'Nelec_p': 8,
        'Ed_p': -0.8,
        'Oxo_p': 0.4,
        'WF_p': 4.30,
        'Cost_p': 0.0000424,
        'MW_p': 55.845
    },
    'Co':{
        'EN_p': 1.88,
        'Nelec_p': 9,
        'Ed_p': -1.5,
        'Oxo_p': 0.4,
        'WF_p': 4.40,
        'Cost_p': 0.0328,
        'MW_p': 58.933195
    },
    'Ni':{
        'EN_p': 1.91,
        'Nelec_p': 10,
        'Ed_p': -1.6,
        'Oxo_p': 0.2,
        'WF_p': 4.50,
        'Cost_p': 0.0139,
        'MW_p': 58.6934
    },
    'Cu':{
        'EN_p': 1.90,
        'Nelec_p': 11,
        'Ed_p': -2.5,
        'Oxo_p': 0.2,
        'WF_p': 4.40,
        'Cost_p': 0.006,
        'MW_p': 63.546
    },
    'Zr':{
        'EN_p': 1.33,
        'Nelec_p': 4,
        'Ed_p': 0.7,
        'Oxo_p': 0.8,
        'WF_p': 3.90,
        'Cost_p': 0.0357,
        'MW_p': 91.224
    },
    'Nb':{
        'EN_p' : 1.60,
		'Nelec_p' : 5,
      	'Ed_p' : 0.1,
      	'Oxo_p' : 0.8,
      	'WF_p' : 4.00,
      	'Cost_p' : 0.0614,
      	'MW_p' : 92.90638
    },
    "Mo":{
        "EN_p" : 2.16,
      	"Nelec_p" : 6,
      	"Ed_p" : -0.9,
      	"Oxo_p" : 0.6,
      	"WF_p" : 4.30,
      	"Cost_p" : 0.0401,
      	"MW_p" : 95.94
    },
    "Tc":{
        "EN_p" : 1.90,
      	"Nelec_p" : 7,
      	"Ed_p" : -1.6,
      	"Oxo_p" : 0.5,
      	"WF_p" : 4.4,
      	"Cost_p" : 100,
      	"MW_p" : 98
    },
    "Ru":{
        "EN_p" : 2.20,
      	"Nelec_p" : 8,
      	"Ed_p" : -1.9,
      	"Oxo_p" : 0.4,
      	"WF_p" : 4.60,
      	"Cost_p" : 10.40,
      	"MW_p" : 101.07
    },
    "Rh":{
        "EN_p" : 2.28,
      	"Nelec_p" : 9,
      	"Ed_p" : -2.1,
      	"Oxo_p" : 0.3,
      	"WF_p" : 4.75,
      	"Cost_p" : 147,
      	"MW_p" : 102.9055
    },
    "Pd":{
        "EN_p" : 2.20,
      	"Nelec_p" : 10,
      	"Ed_p" : -1.8,
      	"Oxo_p" : 0.0,
      	"WF_p" : 4.80,
      	"Cost_p" : 49.5,
      	"MW_p" : 106.42
    },
    "Ag":{
        "EN_p" : 1.93,
      	"Nelec_p" : 11,
      	"Ed_p" : -4.0,
      	"Oxo_p" : 0.2,
      	"WF_p" : 4.30,
      	"Cost_p" : 0.521,
      	"MW_p" : 107.8682
    },
    "Hf":{
        "EN_p": 1.30,
      	"Nelec_p" : 4,
      	"Ed_p" : 0.7,
      	"Oxo_p" : 1.0,
      	"WF_p" : 3.50,
      	"Cost_p" : 0.9,
      	"MW_p" : 178.49
    },
    "Ta":{
        "EN_p" : 1.50,
      	"Nelec_p" : 5,
      	"Ed_p" : 0.3,
      	"Oxo_p" : 0.8,
      	"WF_p" : 4.10,
      	"Cost_p" : 0.298,
      	"MW_p" : 171.9449
    },
    "W":{
        "EN_p" : 2.36,
      	"Nelec_p" : 6,
      	"Ed_p" : -0.8,
      	"Oxo_p" : 0.8,
      	"WF_p" : 4.50,
      	"Cost_p" : 0.0353,
      	"MW_p" : 183.84
    },
    "Re":{
        "EN_p" : 1.90,
      	"Nelec_p" : 7,
      	"Ed_p" : -1.6,
      	"Oxo_p" : 0.5,
      	"WF_p" : 5.00,
      	"Cost_p" : 3.010,
      	"MW_p" : 186.207
    },
    "Os":{
        "EN_p" : 2.20,
      	'Nelec_p' : 8,
      	'Ed_p' : -2.2,
      	'Oxo_p' : 0.4,
      	'WF_p' : 4.70,
      	'Cost_p' : 12,
      	'MW_p' : 190.2
    },
    "Ir":{
        'EN_p' : 2.20,
      	'Nelec_p' : 9,
      	'Ed_p' : -2.9,
      	'Oxo_p' : 0.4,
      	'WF_p' : 5.30,
      	'Cost_p' : 55.5,
      	'MW_p' : 192.22
    },
    "Pt":{
        'EN_p' : 2.28,
      	'Nelec_p' : 10,
      	'Ed_p' : -2.4,
      	'Oxo_p' : 0.1,
      	'WF_p': 5.30,
      	'Cost_p' :27.8,
      	'MW_p' : 195.084
    },
    "Au":{
        "EN_p": 2.54,
      	"Nelec_p" : 11,
      	"Ed_p" : -3.4,
      	"Oxo_p" : 0.0,
      	"WF_p" : 4.30,
      	"Cost_p" : 44.8,
      	"MW_p" : 196.96657
    }
}

@app.route('/')
def calculator():
    return """
    <style>#k{color:grey;} #k1{color:#1a2421;background-color:#cbcbcb;}</style> 
    <form method="POST" action="/calculate">
    <select name="priM" id="priM">
        <option value="Pt">Pt</option>
        <option value="Ni">Ni</option>
    </select><br><br>
    <label for="SM_Percent">Enter Secondary Metal Concentration:</label>
    <input type="number" id="SM_Percent" name="SM_Percent"><br><br>
    <input type="submit">
    </form>
"""

@app.route("/calculate", methods=["POST"])
def calculate():
    primary_metal = request.form.get('priM')  # Use get() to avoid KeyError
    secondary_metal_concentration = float(request.form.get('SM_Percent'))
#screen if you select Pt
    if primary_metal=="Pt":
        properties_selected = properties.get(primary_metal)
        if properties_selected:
            # Retrieve properties based on selected primary metal
            MW_m = properties_selected["MW_m"]
            mol_p = properties_selected["mol_p"]
            # Calculate kg_p based on the input for Secondary Metal Concentration which involves an input
            kg_p = mol_p * MW_m * secondary_metal_concentration / 1000
            percent= float(secondary_metal_concentration)/100
            mol_m=(1-percent)/percent*mol_p
            kg_m= mol_m*MW_m/1000



            # Perform calculations or return properties as needed
            return f"Properties of {primary_metal}: Mw_m={MW_m}, mol_p={mol_p}, kg_p={kg_p}, kg_m={kg_m}"

    #screen if you select Pt
    elif primary_metal=="Ni":
        return "this is the Ni screen"

if __name__ == '__main__':
    app.run(debug=True, port=7007)


from flask import Flask, request
#UPDATE: got started, got up to kg_p property of pt
#To do: finish initializing all of the variables of Pt and Ni
# make sure all inputs are under eachother and try to make everything centered
#reach: get started on implementing all of the inputs
app = Flask(__name__)

# Define properties of Pt and Ni as dictionaries
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
#valid parameters
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
            return f"Properties of {primary_metal}: MW_m={MW_m}, mol_p= {mol_p}, kg_p= {kg_p}"
    elif primary_metal=="Ni":
        return "this is the Ni screen"

if __name__ == '__main__':
    app.run(debug=True, port=7007)


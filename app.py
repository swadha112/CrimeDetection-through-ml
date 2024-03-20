from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('paCAW.csv')

# Function to get the list of states from the dataset
def get_states():
    return data['STATE/UT'].unique().tolist()

# Function to predict age group and gender based on the highest crime incidents for a given state and crime head
def predict_age_and_gender(state, crime):
    # Filter data for the specified state and crime
    subset = data[(data['STATE/UT'] == state) & (data['Crime head'] == crime)]
    
    # If there's no data for the specified state and crime, return None
    if subset.empty:
        return None, None
    
    # Selecting relevant columns: Age group columns and Gender columns
    age_columns = ['Male Below 18 ', 'Female Below 18', 
                   'Male Between 18-30', 'Female Between 18-30 ', 
                   'Male Between 30-45', 'Female Between 30-45 ', 
                   'Male Between 45-60 ', 'Female Between 45-60 ', 
                   'Male Above 60', 'Female Above 60']
    
    # Get the sum of crime incidents for each age and gender group
    subset_sum = subset[age_columns].sum()
    
    # Find the column with the highest sum
    max_column = subset_sum.idxmax()
    
    # Extract gender and age group from the column name
    gender, age_group = max_column.split(' ')[0], ' '.join(max_column.split(' ')[1:])
    
    return age_group, gender

@app.route('/')
def index():
    states = get_states()
    return render_template('index.html', states=states)

@app.route('/predict', methods=['POST'])
def predict():
    state = request.form['state']
    crime = request.form['crime']
    age_group, gender = predict_age_and_gender(state, crime)
    return render_template('result.html', state=state, crime=crime, age_group=age_group, gender=gender)

if __name__ == '__main__':
    app.run(debug=True)

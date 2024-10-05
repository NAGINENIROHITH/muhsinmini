from flask import Flask, render_template, request

app = Flask(__name__)

# Hydrate Formation Risk Calculation Function
def calculate_hydrate_risk(T, P, P_w):
    # Default critical values
    T_crit = 0  # Critical temperature in °C
    P_crit = 1  # Critical pressure in MPa
    P_w_crit = 0.05  # Critical water vapor pressure in MPa

    # Weighting coefficients
    alpha = 1
    beta = 2
    gamma = 3

    # Hydrate risk equation (raw value)
    R_raw = alpha * (T_crit - T) + beta * (P - P_crit) + gamma * (P_w - P_w_crit)

    # Normalize risk and cap at 100
    R_scaled = max(0, min(100, R_raw))

    return R_scaled

# Function to suggest risk reduction strategies
def suggest_risk_reduction(T, P, P_w):
    # Default critical values
    T_crit = 0  # Critical temperature in °C
    P_crit = 1  # Critical pressure in MPa
    P_w_crit = 0.05  # Critical water vapor pressure in MPa

    suggestions = []

    # Suggest temperature increase if temperature is too low
    if T < T_crit:
        suggestions.append(f"Increase temperature to at least {T_crit}°C.")

    # Suggest pressure reduction if pressure is too high
    if P > P_crit:
        suggestions.append(f"Reduce pressure to at most {P_crit} MPa.")

    # Suggest water vapor pressure reduction if water content is high
    if P_w > P_w_crit:
        suggestions.append(f"Reduce water vapor pressure to at most {P_w_crit} MPa.")

    return suggestions

# Route to display the input form
@app.route('/')
def index():
    return render_template('index.html')

# Route to calculate hydrate formation risk
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get user input from the form
    temperature = float(request.form['temperature'])
    pressure = float(request.form['pressure'])
    water_pressure = float(request.form['water_pressure'])

    # Calculate hydrate formation risk using default critical values
    risk = calculate_hydrate_risk(temperature, pressure, water_pressure)

    # Get suggestions to reduce risk
    suggestions = suggest_risk_reduction(temperature, pressure, water_pressure)

    # Define the equations to be displayed
    risk_equation = "R = α * (T_crit - T) + β * (P - P_crit) + γ * (P_w - P_w_crit)"
    clapeyron_equation = "ln(P) = (ΔH / R) * (1 / T) + C + k * P_w"

    return render_template('index.html', risk=risk, suggestions=suggestions, risk_equation=risk_equation, clapeyron_equation=clapeyron_equation)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
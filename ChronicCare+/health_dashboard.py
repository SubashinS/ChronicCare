import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go

# Initialize Dash App
def create_health_dashboard(flask_app):
    app = dash.Dash(__name__, server=flask_app, routes_pathname_prefix='/health_dashboard/')
    app.title = "Health Monitoring Dashboard"

    # Sample Data
    data = pd.DataFrame(columns=["Week", "Value", "Parameter"])

    # Layout
    app.layout = html.Div([ 
        html.H1("Health Monitoring Dashboard", style={'text-align': 'center'}), 
        
        html.Div([ 
            html.Label("Select Health Parameter:"), 
            dcc.Dropdown( 
                id="select-parameter", 
                options=[ 
                    {"label": "BMI", "value": "BMI"}, 
                    {"label": "Insulin", "value": "Insulin"}, 
                    {"label": "Cholesterol", "value": "Cholesterol"}, 
                    {"label": "Creatinine", "value": "Creatinine"}, 
                    {"label": "Blood Pressure", "value": "Blood Pressure"}, 
                    {"label": "Glucose", "value": "Glucose"} 
                ], 
                placeholder="Select Parameter", 
                style={'width': '300px', 'margin-right': '10px', 'display': 'inline-block'} 
            ), 
            html.Label("Enter Weekly Values:"), 
            html.Div([ 
                dcc.Input(id="week1-input", type="number", placeholder="Week 1", style={'width': '100px', 'margin-right': '10px'}), 
                dcc.Input(id="week2-input", type="number", placeholder="Week 2", style={'width': '100px', 'margin-right': '10px'}), 
                dcc.Input(id="week3-input", type="number", placeholder="Week 3", style={'width': '100px', 'margin-right': '10px'}), 
                dcc.Input(id="week4-input", type="number", placeholder="Week 4", style={'width': '100px'}), 
            ], style={'text-align': 'center', 'margin-top': '10px'}), 
            html.Button("Submit", id="submit-button", n_clicks=0, style={'margin-top': '10px'}) 
        ], style={'text-align': 'center', 'margin-top': '20px'}), 

        dcc.Graph(id="progress-chart", style={'margin-top': '20px'}), 
        
        html.Div(id="analysis-output", style={'text-align': 'center', 'margin-top': '20px', 'font-size': '18px'}) 
    ], style={ 
        'background': 'linear-gradient(135deg, #f3c4fb, #a5d8ff, #ffe6e6)',  # Updated pastel gradient 
        'height': '100vh',  # Full height of the page 
        'display': 'flex', 
        'flexDirection': 'column', 
        'justifyContent': 'center', 
        'alignItems': 'center' 
    })

    # Callback to update the graph and analysis
    @app.callback( 
        [Output("progress-chart", "figure"), 
         Output("analysis-output", "children")], 
        Input("submit-button", "n_clicks"), 
        [State("select-parameter", "value"), 
         State("week1-input", "value"), 
         State("week2-input", "value"), 
         State("week3-input", "value"), 
         State("week4-input", "value")], 
        prevent_initial_call=True 
    ) 
    def update_chart(n_clicks, parameter, week1, week2, week3, week4): 
        # Ensure that inputs are valid 
        if not parameter or any(v is None for v in [week1, week2, week3, week4]): 
            return {}, "Please complete all inputs."

        # Create the DataFrame for weekly data 
        weekly_data = pd.DataFrame({ 
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4"], 
            "Value": [week1, week2, week3, week4], 
            "Parameter": [parameter] * 4 
        })

        # Create the figure 
        fig = go.Figure()

        # Add color bands based on thresholds
        thresholds = {} 
        colors = {}

        if parameter == "BMI":
            thresholds = {"underweight": (0, 18.5), "normal": (18.5, 24.9), "overweight": (25, 29.9), "obese": (30, 50)} 
            colors = {"underweight": "yellow", "normal": "green", "overweight": "orange", "obese": "red"} 
        elif parameter == "Blood Pressure": 
            thresholds = {"low": (0, 90), "normal": (90, 120), "high": (120, 140), "critical": (140, 200)} 
            colors = {"low": "yellow", "normal": "green", "high": "orange", "critical": "red"} 
        elif parameter == "Glucose": 
            thresholds = {"low": (0, 70), "normal": (70, 108), "high": (140, 200), "critical": (200, 400)} 
            colors = {"low": "yellow", "normal": "green", "high": "orange", "critical": "red"} 
        elif parameter == "Insulin": 
            thresholds = {"low": (0, 15), "normal": (15, 50), "high": (50, 100), "critical": (100, 200)} 
            colors = {"low": "yellow", "normal": "green", "high": "orange", "critical": "red"} 
        elif parameter == "Cholesterol": 
            thresholds = {"low": (0, 125), "normal": (125, 200), "high": (200, 240), "critical": (240, 300)} 
            colors = {"low": "yellow", "normal": "green", "high": "orange", "critical": "red"} 
        elif parameter == "Creatinine": 
            thresholds = {"low": (0, 0.6), "normal": (0.6, 1.2), "high": (1.2, 2), "critical": (2, 5)} 
            colors = {"low": "yellow", "normal": "green", "high": "orange", "critical": "red"}

        # Add color bands and labels
        for category, (start, end) in thresholds.items():
            fig.add_shape(
                type="rect",
                x0=0, x1=1, y0=start, y1=end,
                fillcolor=colors[category],
                opacity=0.3,
                line_width=0,
                xref="paper",
                yref="y"
            )

        # Add the user's data as a line plot
        fig.add_trace(go.Scatter(
            x=weekly_data["Week"],
            y=weekly_data["Value"],
            mode="lines+markers",
            line=dict(color="blue", width=2),
            marker=dict(size=8),
            name=parameter
        ))

        # Update layout with white background
        fig.update_layout(
            title=f"Weekly {parameter} Progress",
            xaxis_title="Week",
            yaxis_title=parameter,
            yaxis=dict(range=[0, max(weekly_data["Value"]) + 20]),
            plot_bgcolor="white",  # Set graph background to white
            paper_bgcolor="white",  # Set overall background to white
            font=dict(color="black"),  # Black text for readability
            template="plotly_white",  # Use the Plotly white template
            showlegend=True,
            legend=dict(
                itemsizing="constant",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        # Adding consultation advice
        advice = ""
        if parameter == "Blood Pressure":
            if weekly_data["Value"].iloc[-1] < 90 or weekly_data["Value"].iloc[-1] > 140:
                advice = "Consult a doctor for high/low blood pressure."
        elif parameter == "Glucose":
            if weekly_data["Value"].iloc[-1] < 70 or weekly_data["Value"].iloc[-1] > 200:
                advice = "Consult a doctor for high/low glucose levels."

        # Analyze the data
        analysis = ""
        if weekly_data["Value"].iloc[-1] > weekly_data["Value"].iloc[0]:
            analysis = f"{parameter} has increased from Week 1 to Week 4."
        elif weekly_data["Value"].iloc[-1] < weekly_data["Value"].iloc[0]:
            analysis = f"{parameter} has decreased from Week 1 to Week 4."
        else:
            analysis = f"{parameter} has remained stable from Week 1 to Week 4."

        return fig, analysis + (" " + advice if advice else "")

    return app

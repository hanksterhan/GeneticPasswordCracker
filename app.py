import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from PasswordCracker import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Password Cracking Using a Genetic Algorithm'),

    html.Div(children='Adjust the values to see how they affect the genetic algorithm.'),

    html.Label('Target Password'),
    dcc.Input(id='password', value='password', type='text'),

    html.Label('Population Size'),
    dcc.Input(id='size_of_population', value=100, type='number'),

    html.Label('Lucky Few'),
    dcc.Input(id='lucky_few', value=20, type='number'),

    html.Label('Best Sample'),
    dcc.Input(id='best_sample', value= 20, type='number'),

    html.Label('Number of Children'),
    dcc.Input(id='num_children', value= 20, type='number'),

    html.Label('Number of Generations'),
    dcc.Input(id='num_generation', value= 50, type='number'),

    html.Label('Chance of Mutation'),
    dcc.Input(id='chance_of_mutation', value= 5, type='number'),

    html.Div(id='my-div'),
    
])

@app.callback(
    Output(component_id='my-div', component_property='children'), 
    [Input(component_id='password', component_property='value'),
     Input(component_id='size_of_population', component_property='value'),
     Input(component_id='lucky_few', component_property='value'),
     Input(component_id='best_sample', component_property='value'),
     Input(component_id='num_children', component_property='value'),
     Input(component_id='num_generation', component_property='value'),
     Input(component_id='chance_of_mutation', component_property='value')]
)
def update_output_div(password, size_of_population, lucky_few, best_sample, num_children, num_generation, chance_of_mutation):
    GA = PasswordCracker()
    GA.multipleGeneration(num_generation, password, size_of_population, best_sample, lucky_few, num_children, chance_of_mutation)
    print(GA.returnResult(GA.historic, password, num_generation))
    return (GA.returnResult(GA.historic, password, num_generation))

# @app.callback(
#     Output(component_id='my-slider', component_property='children'),
#     [Input(component_id='mark-slider', component_property='value'),
#      Input(component_id='password', component_property='value')]
# )
# def update_div(slider, password):
#     return 'You entered {} and {}'.format(slider, password)

if __name__ == '__main__':
    app.run_server(debug=True)
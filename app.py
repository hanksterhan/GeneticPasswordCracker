import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import json
from collections import namedtuple
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

    html.Button(id="submit-button", children="Run"),

    html.Div(id='my-div'),
    html.Div(id='my-graph'),

    dcc.Graph(id='genetics-graph'),

    # Hidden div inside the app that stores the intermediate json of the object
    html.Div(id='intermediate-value', style={'display':'none'})
    
])

# callback to run algorithm and store the object in the hidden Div
# activated when the "Run" button is clicked
@app.callback(
    Output('intermediate-value', 'children'), 
    [Input('submit-button', 'n_clicks')],
    [State('password', 'value'),
     State('size_of_population', 'value'),
     State('lucky_few', 'value'),
     State('best_sample', 'value'),
     State('num_children', 'value'),
     State('num_generation', 'value'),
     State('chance_of_mutation', 'value'),
    ]
)
def store_obj(nclicks, password, size_of_population, lucky_few, best_sample, num_children, num_generation, chance_of_mutation):
    GA = PasswordCracker()
    GA.multipleGeneration(num_generation, password, size_of_population, best_sample, lucky_few, num_children, chance_of_mutation)
    # return (GA.returnResult(GA.historic, password, num_generation), graph_check)
    return (json.dumps(GA, default=lambda o: o.__dict__))

# callback to take the object and display the best result and fitness score
# activated when the "Run" button is clicked
@app.callback(
    Output('my-div', 'children'),
    [Input('submit-button', 'n_clicks'),
     Input('intermediate-value', 'children')],
    [State('password', 'value'),
     State('num_generation', 'value')]
)
def output_to_div(nclicks, obj_json, password, num_generation):
    # instantiate an instance of this object to use the returnResult method
    GA = PasswordCracker()
    
    # read in the object metadata
    obj_metadata = json.loads(obj_json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    
    # transfer the object metadata
    GA.historic = obj_metadata.historic
    
    # sanity check:
    print(GA.returnResult(GA.historic, password, num_generation))
    return (GA.returnResult(GA.historic, password, num_generation))

# callback to update the graph
@app.callback(
    Output('genetics-graph', 'figure'),
    [Input('submit-button', 'n_clicks'),
     Input('intermediate-value', 'children')],
    [State('password', 'value')]
)
def update_graph(n_clicks, obj_json, password):
    # instantiate an instance of this object to use the 
    GA = PasswordCracker()
    
    # read in the object metadata
    obj_metadata = json.loads(obj_json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    
    # transfer the object metadata
    GA.historic = obj_metadata.historic

    # iterate through historic and keep track of the member with the highest fitness score
    evolutionFitness = []
    averageEvolutionFitness = []
    for population in GA.historic:
        # to keep track of the most fit individuals
        evolutionFitness.append(GA.getBestIndividualFromPopulation(population, password)[1])
        
        # to calculate average fitness for a generation:
        populationPerf = GA.computePerfPopulation(population, password)
        averageFitness = 0
        for individual in populationPerf:
            averageFitness += individual[1]
        averageEvolutionFitness.append(averageFitness/len(population))

    return {
        'data': [go.Scatter(
            x = range(len(population)+1),
            y = averageEvolutionFitness,
            mode='lines+markers',
            name='Average Evolution Fitness'
            ),
                go.Scatter(
            x = range(len(population)+1),
            y = evolutionFitness,
            mode='lines+markers',
            name='Best Individual Fitness'
            )],
        'layout': go.Layout(
            xaxis={
                'title': 'Generation',
                'type': 'linear'
            },
            yaxis={
                'title': 'Fitness Score',
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
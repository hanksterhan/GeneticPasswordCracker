#!/usr/bin/env python2

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import json
from collections import namedtuple
from PasswordCracker import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

intro1 = 'A Genetic Algorithm is an algorithm inspired by the process of natural selection. They are \
                commonly used in optimization and search problems. The idea of a genetic algorithm is to \
                start with a random population, choose the best members in the population by a certain heurestic,\
                "breeding" those members to generate the next generation of members, and iterating until some \
                convergence or for some number of generations. In this project, I implemented a genetic algorithm \
                as a password cracker to try to generate a target string.'
intro2 = 'Adjust the values on the left and click "RUN" to see how they affect the genetic algorithm\'s \
                best guess at the password. A \'fitness\' score is a measure of how close a member matches the \
                target password. In each generation, the members with the highest fitness scores and some random lucky \
                members are chosen to be parents and "breed" to generate the members in the next generation. \
                The graph generated on the right displays the best \
                individual fitness score per generation and the average fitness score per generation. \
                Hover over data points to see the best/average fitness score of a particular generation.'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('Password Cracking Using a Genetic Algorithm'),
    html.P(intro1),
    html.P(intro2),
    html.Div([
        html.Div([
            html.Label('Target Password - password for the genetic algorithm to learn'),
            dcc.Input(id='password', value='password', type='text'),

            html.Label('Population Size - number of members per generation'),
            dcc.Input(id='size_of_population', value=100, type='number'),

            html.Label('Best Sample - the number of most fit members in a generation selected to breed'),
            dcc.Input(id='best_sample', value= 20, type='number'),

            html.Label('Lucky Few - the number of random members in a generation selected to breed'),
            dcc.Input(id='lucky_few', value=20, type='number'),

            html.Label('Number of Children - number of children each parent can breed'),
            dcc.Input(id='num_children', value= 20, type='number'),

            html.Label('Number of Generations - number of generations in the genetic algorithm'),
            dcc.Input(id='num_generation', value= 50, type='number'),

            html.Label('Chance of Mutation - percent chance that there is a mutation when breeding'),
            dcc.Input(id='chance_of_mutation', value= 5, type='number'),

            html.Button(id="submit-button", children="Run"),

            html.Div(id='my-div'),
        ], style={
            'backgroundColor': 'rgb(255,255,255)',
            'padding': '10px 10px',
            'width':'49%',
            'float':'left'
        }),
        html.Div([    
            dcc.Graph(id='genetics-graph'),

            # Hidden div inside the app that stores the intermediate json of the object
            html.Div(id='intermediate-value', style={'display':'none'})
        ], style={
            'margin-left': '55%',
        })
    ],style={
        'width':'90%',
        'margin-left': '5%',
        'margin-top': '5%',
        'display':'inline-block',
    })
], style={
    'backgroundColor': 'rgb(220,220,220)',
    'margin-top': '5%',
    'padding': '10px 10px',
})

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
            title='Best and Average Fitness Score by Generation',
            xaxis={
                'title': 'Generation',
                'type': 'linear'
            },
            yaxis={
                'title': 'Fitness Score',
                'type': 'linear'
            },
            hovermode='closest',
            legend=dict(x=1, y=-0.2, orientation="h")
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)

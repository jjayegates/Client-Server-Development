from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table as dt
from dash.dependencies import Input, Output, State 
import base64

import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from Animal_Shelter import AnimalShelter





###########################
# Data Manipulation / Model
###########################
# FIX ME change for your username and password and CRUD Python module name
username = "accuser"
password = "changeme"
shelter = AnimalShelter()


# class read method must support return of cursor object 
df = pd.DataFrame.from_records(shelter.read({}))



#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
buttonList = [html.Button('Water Rescue', id='water', n_clicks=0),
        html.Button('Mountain/Wilderness Rescue', id='mount-wild', n_clicks=0),
        html.Button('Disaster/Individual Tracking', id='dis-ind', n_clicks=0),
        html.Button('Reset', id='reset', n_clicks=0)]
binfo = { button.id : button.n_clicks for button in buttonList}
app.layout = html.Div([
#    html.Div(id='hidden-div', style={'display':'none'}),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),
    html.Center(html.B(html.H1('Janece Gates'))),
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    html.Div(
        
#FIXME Add in code for the interactive filtering options. For example, Radio buttons, drop down, checkboxes, etc.
        buttonList

    ),
    html.Hr(),
    dt.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here 
        editable=False,
        row_selectable="single",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################

triggerInfo = []
    
@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('water', 'n_clicks'),
               Input('mount-wild', 'n_clicks'),
               Input('dis-ind', 'n_clicks'),
               Input('reset', 'n_clicks')])
def update_dashboard(w, m, d, r):
### FIX ME Add code to filter interactive data table with MongoDB queries
    cInfo = {"water":w, "mount-wild":m, "dis-ind":d, "reset":r}
    triggerID = ""
    try:
        for bid, bclicks in binfo.items():
            triggerID += {True:"", False:bid}[bclicks == cInfo[bid]]
            binfo[bid] = cInfo[bid]
    except Exception as e: 
        triggerInfo.append("Exception:  ")
        triggerInfo.append(str(e))
    
    filter_option  = {'water':{"animal_type":"Dog",
                               "breed":{"$in":["Chesapeake Bay Retriever","Labrador Retriever Mix", "Newfoundland"]}, 
                               "sex_upon_outcome":"Intact Female",
                               "age_upon_outcome_in_weeks":{"$gte":26},
                               "age_upon_outcome_in_weeks":{"$lte":156}}, 
                      'mount-wild':{"animal_type":"Dog","breed":{"$in":["German Shepherd","Alaskan Malamute","Old English Sheepdog","Siberian Husky","Rottweiler"]}, "sex_upon_outcome":"Intact Male","age_upon_outcome_in_weeks":{"$gte":26},"age_upon_outcome_in_weeks":{"$lte":156}}, 
                      'dis-ind':{"animal_type":"Dog","breed":{"$in":["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]}, "sex_upon_outcome":"Intact Male","age_upon_outcome_in_weeks":{"$gte":20},"age_upon_outcome_in_weeks":{"$lte":300}}, 
                      'reset':{}}[triggerID]
    df = pd.DataFrame.from_records(shelter.read(filter_option))
        
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')
        
    return (data,columns)




@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "data")])
def update_graphs(viewData):
    triggerInfo.append("in pie chart")
    try:
        dff = pd.DataFrame.from_dict(viewData)
        dff = dff.groupby("breed").count()
        fig = px.pie(dff, values="name", names=dff.index, title='Breeds of Dogs')
    except Exception as e:
        triggerInfo.append(str(e))
        triggerInfo.append(dff)
    triggerInfo.append("Right Before Return")
    
    return [dcc.Graph(figure = fig)]
    ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #
    #return [
    #    dcc.Graph(            
    #        figure = ###
    #    )    
    #]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data"),
     Input('datatable-id', 'selected_rows')])
def update_map(viewData, selected):
#FIXME: Add in the code for your geolocation chart
#If you completed the Module Six Assignment, you can copy in the code you created here.
    dff = pd.DataFrame.from_dict(viewData)
    try:
        row = selected[0]
    except:
        row = 0
    longitude, latitude = dff.iloc[row, 13 ], dff.iloc[row, 14]
    
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[longitude, latitude], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            dl.Marker(position=[longitude, latitude], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]


app
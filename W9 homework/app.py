import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


df = pd.read_csv('C:/Users/Taguhi/Desktop/Data S.B. materials/Data vis/W7 homework/games.csv')
df['game_rating']=(df.black_rating+df.white_rating)/2


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)



# -------------------------------------------------------------------------------------------------------------- 

#											PART 1: DESIGN PARAMETERS

# --------------------------------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters


colors = {
		'full-background': 	'#DCDCDC',
		'block-borders': 'grey' 
		}

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 2px 4px'
}

sizes = {
		'subblock-heights': '330px'
}


graph_1= dcc.Graph(
        figure= {
        'data' :
        	[go.Scatter(
        		x=df["turns"], 
        		y=df["game_rating"],
        		mode = "markers")
        	],
        	'layout' : go.Layout(
        		title = 'Relationship between number of turns and rating',
        		xaxis = {'title':"turns"},
        		yaxis = {'title':"rating"})
        	},
        	style = {
        	'margin': margins['block-margins'],
        	'width': '99%',
        	'height': '300px',
					}
    )

graph_2= dcc.Graph(
        figure= px.box(df, 
        	x="winner", 
        	y="turns", 
        	color="victory_status",
        	color_discrete_map={
        'outoftime': 'steelblue',
        'resign': 'green',
        'mate' : 'firebrick',
        'draw': 'purple'},
        	title="Does the length of game affect the result?"),
        	style = {
        	'margin': margins['block-margins'],
        	'width': '99%',
        	'height': '300px',
					}
    )

graph_3= dcc.Graph(
        figure= px.bar(
        	x = df.winner.unique(),
        	y = df.winner.value_counts(normalize = True)*100,
        	title="Do players with white pieces win more?",
        	labels=dict(x ="winner", y="Percentage"),
        	color_discrete_sequence =['green']*3),
        	style = {
        	'margin': margins['block-margins'],
        	'width': '99%',
        	'height': '300px',
					}
    )


plot = plt.hist(df.turns, color = 'darkblue')
plt.title('Distribution of move counts')
matplot = io.BytesIO()
plt.savefig(matplot, format = "png")
data = base64.b64encode(matplot.getbuffer()).decode("utf8")

graph_4 = html.Img(src = "data:image/png;base64,{}".format(data),
	style = {
        	'margin': margins['block-margins'],
        	'width': '99%',
        	'height': '300px',
					})


# -------------------------------------------------------------------------------------------------------------- 

#											PART 2: ACTUAL LAYOUT

# --------------------------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need too have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app



# -------------------------------------------------------------------------------------- DIV for TITLE
div_title = html.Div(children =html.H1('Title'),
					style ={ 'color' : 'blue',
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center',
							'color' :'blue',
							'font-weight': 'bold'
							})
					

# -------------------------------------------------------------------------------------- DIV for first raw (1.1 and 1.2)
div_1_1 = html.Div(children = ['block 1-1',graph_1],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights'],
							'font-weight': 'bold',
					},
					
				)

div_1_2 = html.Div(children = ['block 1-2',graph_2],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							'height': sizes['subblock-heights'],
							'font-weight': 'bold'},
		)

# Collecting DIV 1.1 and 1.2 into the DIV of first raw.
# Pay attention to the 'display' and 'flex-flaw' attributes.
# With this configuration you are able to let the DIV-s 1.1 and 1.2 be side-by-side to each other.
# If you skip them, the DIV-s 1.1 and 1.2 will be ordered as separate rows.
# Pay also attention to the 'width' attributes, which specifiy what percentage of full row will each DIV cover.
div_raw1 = html.Div(children =	[div_1_1,
								div_1_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


# -------------------------------------------------------------------------------------- DIV for second raw (2.1 and 2.2)
div_2_1 = html.Div(children = ['block 2-1',graph_3] ,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights'],
							'font-weight': 'bold'
					},
					)

div_2_2 = html.Div(children = ['block 2-2',graph_4],
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '50%',
							'height': sizes['subblock-heights'],
							'font-weight': 'bold'
					}
				)


div_raw2 = html.Div(children =	[div_2_1,
								div_2_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})

# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV







app.layout = html.Div([div_title,
						div_raw1,
						div_raw2
						],
						style = {
							'backgroundColor': colors['full-background']
						}
					)




# -------------------------------------------------------------------------------------------------------------- 

#											PART 3: RUNNING THE APP

# --------------------------------------------------------------------------------------------------------------
# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
app.run_server(debug=True, port = 8082)



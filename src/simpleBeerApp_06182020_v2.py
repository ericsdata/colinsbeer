# -*- coding: utf-8 -*-
"""
Created on Thu May 28 15:37:22 2020

@author: colin
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go #use plotly graph object rather than dcc.graph
import pandas as pd
import dash_table 
import dash_bootstrap_components as dbc
import dash_html_components as html
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import nltk
from nltk.corpus import stopwords 
from metric_formatting import indicator, expIndicator


#Using reviews2 which can be queried from the beer_ExploratoryAnalysis File
df = pd.read_csv('BeerReviewsSample.csv')
df['AB'] = df['AB'].replace('-', np.nan)
df['AB'] = pd.to_numeric(df['AB'], errors='coerce')
df_short = df[['name', 'overall', 'style']]

#Get list of style options for drop-down
style_dropdown = df['style'].unique()
style_dropdown = np.append("All", style_dropdown)
style_dropdown = np.sort(style_dropdown)


#Text dashboard data load
rec_df = pd.read_csv('beer_recs_df.csv')
sentiment_df = pd.read_csv('sentiment_df_06192020.csv', dtype= {'highest': np.str , 's_highest': np.str, 
                                   'lowest': np.str, 's_lowest':np.str} )

textdash_df = rec_df.merge(sentiment_df, left_on = 'ind_beerID', right_on = 'beerID', how = 'left')

beerDetails = df.groupby('beerID').agg({'review_text': 'count',
        'overall':'mean',
        'taste':'mean',
        'palate':'mean',
        'aroma':'mean',
        'appearance':'mean', 
        'AB' : 'mean'
        })


textdash_df2 = textdash_df.merge(beerDetails, how = 'left', left_on = 'ind_beerID', right_on = 'beerID')
chosenBeercols = pd.DataFrame(columns = ['ind_name', 'ind_ab', 'ind_style', 'ind_rating', 'ind_appearance', 'ind_aroma', 'ind_palate', 'ind_taste'])

topRecCols = pd.DataFrame(columns = ['top1_name', 'top1_ab', 'top1_style', 'top1_rating_y', 'top1_appearance', 
                          'top1_aroma', 'top1_palate', 'top1_taste'])

beername_dropdown = textdash_df2['ind_name'].unique()
beername_dropdown = np.sort(beername_dropdown)


#Create empty df for top 5 and bottom 5 column names
column_names_df = pd.DataFrame(columns = ['name', 'avg rating', 'count'])

external_stylesheets = [dbc.themes.BOOTSTRAP]


#Allow for bootstrap to work using grid layout
#external_stylesheets = [dbc.themes.DARKLY]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

#Create the app and add the layout which will include a dcc.Dropdown to define the manager dropdown field.
##drop down needs to have an ID to reference later
##the dc.graph portion  contains the id funnel-graph which is a placeholder for more detail to come later

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Go to Exploratory', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Text Analysis', href='/page-2'),
])

page_1_layout = html.Div(style={'backgroundColor': colors['background']}, children= [
    html.H2("Beer Review Visual", style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    html.Div(
        [
            dcc.Dropdown(
                id="beer_style",
                options=[{
                    'label': i,
                    'value': i
                } for i in style_dropdown],
                value='All',
                multi = True, 
                style={'backgroundColor': colors['background']}),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
        html.Div(id='page-1-content'),
        html.Br(),
        dcc.Link('Go to Text Analysis', href='/page-2'),
        html.Br(),
        dcc.Link('Go back to home', href='/'),
            dbc.Row(
                [
                    dbc.Col(expIndicator('7FDBFF', "Percent of Total", 'kpi_total'), width = 2, align = 'center'),
                    dbc.Col(expIndicator('7FDBFF', "Average Rating", 'kpi_avgrating'), width = 2, align = 'center'),
                    dbc.Col(expIndicator('7FDBFF', "Unique Beers", 'kpi_uniquebeers'), width = 2, align = 'center'),
                    dbc.Col(expIndicator('7FDBFF', "Unique Breweries", 'kpi_uniquebrewers'), width = 2, align = 'center'),
                    dbc.Col(expIndicator('7FDBFF', "Unique Reviewers", 'kpi_uniquereviewers'), width = 2, align = 'center'),
                    dbc.Col(expIndicator('7FDBFF', "Average Alochol %", 'kpi_avgABV'), width = 2, align = 'center'),
                ],  className="h-99",
            ), 
            dbc.Row(
                [
                    dbc.Col(children = [
                        dbc.Row(html.H4("Top Five Rated Beers", style={
                        'textAlign': 'center',
                        'color': colors['text']
                        })),
                        dbc.Row(dash_table.DataTable(id='table_top',
                                columns=[{"name": i, "id": i} for i in column_names_df.columns],
                                style_header={'backgroundColor': colors['background']},
                                style_cell={
                                'backgroundColor':  colors['background'],
                                'color': colors['text']
                            }))],
                            width = 4, align = "center"),
                    dbc.Col(dcc.Graph(id = 'boxplot_graph'), width = 8, align = 'top')
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(children = [
                        dbc.Row(html.H4("Lowest Five Rated Beers", style={
                        'textAlign': 'center',
                        'color': colors['text']
                        })),
                        dbc.Row(dash_table.DataTable(id='table_bottom',
                                columns=[{"name": i, "id": i} for i in column_names_df.columns],
                                style_header={'backgroundColor': colors['background']},
                                style_cell={
                                'backgroundColor':  colors['background'],
                                'color': colors['text']
                            }))],
                            width = 4, align = "center"),
                    dbc.Col(dcc.Graph(id = 'scatter-graph'), width = 8, align = 'top')
                ]
            )        
    ]) 

@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('beer_style', 'value')])

def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


# build up the interactive components by adding a callback decorator to a function 
#that manipulates the data and returns a dictionary. This resulting dictionary looks like 
#the figure dictionary defined in the simpler example above so the basic concept continues to build upon itself.

#Keeping callback separates allows for parallel processing

#app callback for the scatter graph
@app.callback(
    dash.dependencies.Output('scatter-graph', 'figure'),
    [dash.dependencies.Input('beer_style', 'value')])

#Manipulate data based on the style selected
def update_graph(beer_style):
    
    if beer_style == 'All':
       df2 = df.groupby(['name']).agg({'overall':'mean', 'review_text': 'count', 'style' : lambda x: x.mode()})   
    else:
       df2 = df[df['style'].isin(beer_style)]
       df2 = df2.groupby(['name']).agg({'overall':'mean', 'review_text': 'count', 'style' : lambda x: x.mode()})      
    
    figure = {
        'data': [
            go.Scatter(                   
                y = df2['overall'],
                x = df2['review_text'],
                mode = 'markers')
        ],     
        
        'layout':{
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']}
        }
    }
    return figure
@app.callback(
    dash.dependencies.Output('boxplot_graph', 'figure'),
    [dash.dependencies.Input('beer_style', 'value')])

def update_box(beer_style):
    if beer_style == 'All':
       df2 = df.groupby(['name']).agg({'overall':'mean', 'review_text': 'count', 'style' : lambda x: x.mode()})   
    else:
       df2 = df[df['style'].isin(beer_style)]
       df2 = df2.groupby(['name']).agg({'overall':'mean', 'review_text': 'count', 'style' : lambda x: x.mode()})        
    
    box = {
        'data': [
            go.Box(                      
                y = df2['overall'],
                x = df2['style'])
        ],
        'layout':{
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']}
        }
    }
    
    #box['layout'].update(height = 300, width = 1000)
    
    return box

@app.callback(
    dash.dependencies.Output('kpi_total', 'children'),
    [dash.dependencies.Input('beer_style', 'value')])

def update_metrics(beer_style):
    kpi_total = 100 if beer_style == 'All' else round(float(len(set(df[df['style'].isin(beer_style)]['name'])) / len(set(df['name'])))*100,2)
    kpi_total = str(kpi_total) + '%'
    print(kpi_total)
    return kpi_total

@app.callback(
    dash.dependencies.Output('kpi_avgrating', 'children'),
    [dash.dependencies.Input('beer_style', 'value')])

def update_metrics2(beer_style):
    kpi_avgrating = round(float(df['overall'].mean())*100, 0) if beer_style == 'All' else round(float(df[df['style'].isin(beer_style)]['overall'].mean())*100, 0)
    return str(kpi_avgrating)

@app.callback(
    dash.dependencies.Output('kpi_uniquebeers', 'children'),
    [dash.dependencies.Input('beer_style', 'value')])

def update_metrics3(beer_style):
    kpi_uniquebeers =  len(df['name'].unique()) if beer_style == 'All' else len(df[df['style'].isin(beer_style)]['name'].unique()) 
    return str(kpi_uniquebeers)

@app.callback(
    dash.dependencies.Output('kpi_uniquebrewers', 'children'),
    [dash.dependencies.Input('beer_style', 'value')])

def update_metrics4(beer_style):
    kpi_uniquebrewers = len(df['brewerId'].unique()) if beer_style == 'All' else  len(df[df['style'].isin(beer_style)]['brewerId'].unique())
    return str(kpi_uniquebrewers)

@app.callback(
    dash.dependencies.Output('kpi_avgABV', 'children'),
    [dash.dependencies.Input('beer_style', 'value')])


def update_metrics5(beer_style):
    kpi_avgABV = float(df['AB'].mean()) if beer_style == 'All' else float(df[df['style'].isin(beer_style)]['AB'].mean())
    kpi_avgABV = round(float(kpi_avgABV),2)
    return str(kpi_avgABV)


@app.callback(
    dash.dependencies.Output('kpi_uniquereviewers', 'children'),
    [dash.dependencies.Input('beer_style', 'value')])

def update_metrics6(beer_style):
    kpi_uniquereviewers= len(df['profileName'].unique()) if beer_style == 'All' else  len(df[df['style'].isin(beer_style)]['profileName'].unique())  
    kpi_uniquereviewers = int(kpi_uniquereviewers)
    print(kpi_uniquereviewers)
    return str(kpi_uniquereviewers)


@app.callback(
    dash.dependencies.Output('table_top', 'data'),
    [dash.dependencies.Input('beer_style', 'value')])


def updated_top(beer_style):
    if beer_style == 'All' :
        df2 = df
        style_agg = df2.groupby('name').agg({ 'overall':'mean', 'review_text': 'count'})
        style_agg_pddf = pd.DataFrame(style_agg)
        bot5_df = style_agg_pddf[style_agg_pddf['review_text']>5].sort_values(by = 'overall', ascending = False)[:5]
        bot5_df2 = bot5_df.reset_index()
        bot5_df2.columns = ['name', 'avg rating', 'count'] #must be equal to column names in layout
        bot5_df3 = bot5_df2.copy()
        bot5_df3 = bot5_df3.round({'avg rating': 2})
    else:         
        df2 = df[df['style'].isin(beer_style)]
        style_agg = df2.groupby('name').agg({ 'overall':'mean', 'review_text': 'count'})
        style_agg_pddf = pd.DataFrame(style_agg)
        bot5_df = style_agg_pddf[style_agg_pddf['review_text']>5].sort_values(by = 'overall', ascending = False)[:5]
        bot5_df2 = bot5_df.reset_index()
        bot5_df2.columns = ['name', 'avg rating', 'count'] #must be equal to column names in layout
        bot5_df3 = bot5_df2.copy()
        bot5_df3 = bot5_df3.round({'avg rating': 2})
    
    return bot5_df3.to_dict("rows")

@app.callback(
    dash.dependencies.Output('table_bottom', 'data'),
    [dash.dependencies.Input('beer_style', 'value')])


def updated_bottom(beer_style):
    if beer_style == 'All' :
        df2 = df
        style_agg = df2.groupby('name').agg({ 'overall':'mean', 'review_text': 'count'})
        style_agg_pddf = pd.DataFrame(style_agg)
        bot5_df = style_agg_pddf[style_agg_pddf['review_text']>5].sort_values(by = 'overall', ascending = True)[:5]
        bot5_df2 = bot5_df.reset_index()
        bot5_df2.columns = ['name', 'avg rating', 'count'] #must be equal to column names in layout
        bot5_df3 = bot5_df2.copy()
        bot5_df3 = bot5_df3.round({'avg rating': 2})
    else:         
        df2 = df[df['style'].isin(beer_style)]
        style_agg = df2.groupby('name').agg({ 'overall':'mean', 'review_text': 'count'})
        style_agg_pddf = pd.DataFrame(style_agg)
        bot5_df = style_agg_pddf[style_agg_pddf['review_text']>5].sort_values(by = 'overall', ascending = True)[:5]
        bot5_df2 = bot5_df.reset_index()
        bot5_df2.columns = ['name', 'avg rating', 'count'] #must be equal to column names in layout
        bot5_df3 = bot5_df2.copy()
        bot5_df3 = bot5_df3.round({'avg rating': 2})
    
    return bot5_df3.to_dict("rows")

###PAGE 2

page_2_layout =  html.Div(style={'backgroundColor': colors['background']}, children= [
      html.H2("Beer Recommender", style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    dcc.Dropdown(
                id="beer_selector",
                options=[{
                    'label': i,
                    'value': i
                } for i in beername_dropdown],
                value='Abita Light',
                multi = False, 
                style={'backgroundColor': colors['background']}),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go Exploratory Analysis', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),

    html.Br(),
    dbc.Row([
            dbc.Col(
                [
             html.H2("Seleted Beer Metrics", style={
            'textAlign': 'left',
            'color': colors['text']
            }),
                    dbc.Row(dash_table.DataTable(id='table_selectedBeer',
                                columns=[{"name": i, "id": i} for i in chosenBeercols.columns],
                                style_header={'backgroundColor': colors['background']},
                                style_cell={
                                'backgroundColor':  colors['background'],
                                'color': colors['text']
                            })), 
                    html.Br(),
                    dbc.Row(indicator('7FDBFF', "Highest Review", "selected_highest_review")
                            ),
                    html.Br(),
                    dbc.Row(indicator('7FDBFF', "Second Highest Review", 'selected_shighest_review')),
                    html.Br(),
                    dbc.Row(indicator('7FDBFF', "Worst Rated Review", 'selected_lowest_review')),
                    html.Br(),
                    dbc.Row(indicator('7FDBFF', "Second Worst Rated Review", 'selected_slowest_review'))
            ], width = 3) ,
            dbc.Col(
                [html.H2("Top Recommendation", style={
            'textAlign': 'left',
            'color': colors['text']
            }),
                         dbc.Row(dash_table.DataTable(id='table_toprecbeer',
                                 columns=[{"name": i, "id": i} for i in topRecCols.columns],
                                 style_header={'backgroundColor': colors['background']},
                                 style_cell={
                                 'backgroundColor':  colors['background'],
                                 'color': colors['text']
                             })), 
                     html.Br(),
                     dbc.Row(indicator('7FDBFF', "Highest Review", "toprec_highest_review")
                             ),
                     html.Br(),
                     dbc.Row(indicator('7FDBFF', "Second Highest Review", 'toprec_shighest_review')),
                     html.Br(),
                     dbc.Row(indicator('7FDBFF', "Worst Rated Review", 'toprec_lowest_review')),
                     html.Br(),
                     dbc.Row(indicator('7FDBFF', "Second Worst Rated Review", 'toprec_slowest_review'))
        ], width = 3)
        ])
    ])
    
@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def page_2_dropdown(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('table_selectedBeer', 'data'),
    [dash.dependencies.Input('beer_selector', 'value')])

def printSelectedBeerDeets(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    beerData2 = beerData[['ind_name', 'ind_ab', 'ind_style', 'ind_rating', 'ind_appearance', 'ind_aroma', 'ind_palate', 'ind_taste']]
    return beerData2.to_dict("rows")



@app.callback(dash.dependencies.Output('selected_highest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def selectedTopReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    text = str(beerData.iloc[0,61])
    return text


@app.callback(dash.dependencies.Output('selected_shighest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def selectedShighestReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    text = str(beerData.iloc[0,62])
    print(text)
    return text



@app.callback(dash.dependencies.Output('selected_lowest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def selectedLowestReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    text = str(beerData.iloc[0,63])
    return text
                        

@app.callback(dash.dependencies.Output('selected_slowest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def selectedSlowestReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    text = str(beerData.iloc[0,64])
    return text




##TOP RECOMMENDED BEER INFORMATION
@app.callback(
    dash.dependencies.Output('table_toprecbeer', 'data'),
    [dash.dependencies.Input('beer_selector', 'value')])

def printtoprecBeerDeets(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    toprecData = beerData[['top1_name', 'top1_ab', 'top1_style', 'top1_rating_y', 'top1_appearance', 
                          'top1_aroma', 'top1_palate', 'top1_taste']]
    return toprecData.to_dict("rows")



@app.callback(dash.dependencies.Output('toprec_highest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def toprecTopReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    toprec_beer = str(beerData.iloc[0,11])
    topRecData = textdash_df2[textdash_df2['ind_name'] == toprec_beer]
    text = str(topRecData.iloc[0,61])
    return text


@app.callback(dash.dependencies.Output('toprec_shighest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def toprecShighestReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    toprec_beer = str(beerData.iloc[0,11])
    topRecData = textdash_df2[textdash_df2['ind_name'] == toprec_beer]
    text = str(topRecData.iloc[0,62])
    return text



@app.callback(dash.dependencies.Output('toprec_lowest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def toprecLowestReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    toprec_beer = str(beerData.iloc[0,11])
    topRecData = textdash_df2[textdash_df2['ind_name'] == toprec_beer]
    text = str(topRecData.iloc[0,63])
    return text
                        

@app.callback(dash.dependencies.Output('toprec_slowest_review', 'children'),
              [dash.dependencies.Input('beer_selector', 'value')])
def toprecSlowestReview(beer_selector):
    beerData = textdash_df2[textdash_df2['ind_name'] == beer_selector]
    toprec_beer = str(beerData.iloc[0,11])
    topRecData = textdash_df2[textdash_df2['ind_name'] == toprec_beer]
    text = str(topRecData.iloc[0,64])
    return text








# =============================================================================
# def word_cloud: 
#     #World cloud based on review text
#     review_words = ' '.join(df["review_text"])
#     stop_words = set(stopwords.words('english')) 
#     
#     review_list = review_words.split()
#     review_words = [w for w in review_list if not w in stop_words] 
#     
#     wordcloud = WordCloud().generate(review_words)
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.show()
# =============================================================================








@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
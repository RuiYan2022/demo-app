import dash

 
from dash import html, dcc, callback, Input, Output, dash_table
 

import plotly.express as px
 
#import dash_table
import pandas as pd 
import numpy as np

dash.register_page(__name__)

# import dash_html_components as html
# from plotly import graph_objs as go
# from datetime import datetime as dt
# import json
# import plotly.offline as py
# import plotly.graph_objects as go
# import dash_bootstrap_components as dbc
# from dash.dash_table import DataTable
# from dash.dash_table.Format import Format, Scheme, Sign

   
def make_dash_table(df_table):
    # Return a dash definition of an HTML table for a Pandas dataframe
    mydashtable = []
    for index, row in df_table.iterrows():
        html_row = []
        for i in range(len(row)):
            print(row[i], type(row[i]))
            if isinstance(row[i], float):
                # item = dict(id=row[i], name=row[i], type='numeric', format=dict(specifier=',.2f'))
                item = '${:,.0f}'.format(row[i])
                print("in formatting ", item)
                html_row.append(html.Td(item))
            else:
                print(type(row[i]))
                html_row.append(html.Td(row[i]))
        mydashtable.append(html.Tr(html_row))
    return mydashtable
 
        
def make_percent_table(df_copy):
    df1 = df_copy.copy()

    df1['AnnualGrowth'] = (df1['TotalSavings']-df1['TotalSavings'].shift(1))*100/df1['TotalSavings'].shift(1)
    df1_perc = df1[['Year', 'AnnualGrowth']]
    # Return a dash definitio of an HTML table for a Pandas dataframe
    myperctable = []
    for index, row in df1_perc.iterrows():
        html_row = []
        for i in range(len(row)):
            print(row[i], type(row[i]))
            if isinstance(row[i], float):
                # item = dict(id=row[i], name=row[i], type='numeric', format=dict(specifier=',.2f'))
                item = '${:,.0f}'.format(row[i])
                print("in formatting ", item)
                html_row.append(html.Td(item))
            else:
                print(type(row[i]))
                html_row.append(html.Td(row[i]))
        myperctable.append(html.Tr(html_row))
    return myperctable


'''  HERE IS THE DATA SEGMENT  '''

totalDF = pd.read_csv("Client1.csv", engine='python') 

totalAnnualSaving = totalDF.groupby(['Year']).Saving_by_CostPerDaySupply.sum().reset_index() 
totalAnnualSaving.rename(columns={'Saving_by_CostPerDaySupply':'TotalSavings'}, inplace=True)
 
#totalAnnualSaving['TotalSavings'].round(decimals = 2)
#print(totalAnnualSaving)
totalDF['DispenseMonth'] = totalDF['DispenseDate_SKey'].astype(str).str[0:7] 
totalMonthlySaving = totalDF.groupby(['DispenseMonth']).Saving_by_CostPerDaySupply.sum().reset_index() 
totalMonthlySaving.rename(columns={'Saving_by_CostPerDaySupply':'TotalSavings',
                                  'DispenseMonth':'Month'}, inplace=True)
 
# initialize data of lists.
map_info = {"lat": [45.5,  43.4,  49.13, 51.1,  44.64,   49.89, 50.45, 46.5, 53.1, 46.6], 
         "lon": [-73.57, -79.24, -123.06, -114.1,  -63.57, -97.13, -104.6, -63.5, -57.7, -66.5], 
         "Province_Code":['QC','ON','BC','AB','NS','MB','SK','PE', 'NL','NB'],
         "text":['Quebec','Ontario','British Columbia', 'Alberta','Nova Scotia','Manitoba','Saskatchewan','Prince Edward Island','Newfoundland and Labrador','New Brunswick']
        }
  
# Create DataFrame
df_map = pd.DataFrame(map_info)

# by Route_Show savings on Common_BrandNamE
listProv = totalDF.Province_Code.unique()
listProv = np.append(listProv,'-')


#prepare data for table 
tableData = totalDF


# Create a Dash table with sorting functionality
table = dash_table.DataTable(
    id='sortable-table',
    columns=[{'name': col, 'id': col} for col in tableData.columns],
    data=tableData.to_dict('records'),
    sort_action='native',
    sort_mode='multi',
    style_table={'overflowX': 'scroll'}
)




# saving by province
Prov_saving = totalDF.groupby(['Province_Code']).Saving_by_CostPerDaySupply.sum().reset_index()
Prov_saving_map = pd.merge(left = Prov_saving, right = df_map, on=['Province_Code'], how='left')
Prov_saving_map.rename(columns={'Saving_by_CostPerDaySupply':'TotalSaving'}, inplace=True)
Prov_saving_map['adjustedSaving']= (Prov_saving_map['TotalSaving'])/5000
  

map_data = [dict(
        type = 'scattergeo',
        ##### WHAT TO REPLACE? ########
        #locationmode = 'Canada',
        ###############################s
        lon = Prov_saving_map['lon'],
        lat = Prov_saving_map['lat'],
        saving = Prov_saving_map['TotalSaving'],
        text = Prov_saving_map['text'],
        mode = 'markers',
        marker = dict(
            colorscale= 'Jet',  
            size = np.where(Prov_saving_map['adjustedSaving']<10, 10, Prov_saving_map['adjustedSaving']/5),
            color = Prov_saving_map['adjustedSaving'],
            colorbar = dict(
                title = 'Saving',
                titleside = 'top',
                tickmode = 'array',
            )
    ))]

map_dictionary = dict(
            ##### WHAT TO REPLACE? ########
            #scope='north-america',
            ###############################
            showland = True,
            
            # Add coordinates limits on a map
            lataxis = dict(range=[40,70]),
            lonaxis = dict(range=[-130,-55], gridcolor='blue'),
            bgcolor="grey",
            showocean = True,
            landcolor="green",
            lakecolor="blue",
           # landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 3,
            subunitwidth = 3
        )
 
 
#saving by DrugRoute
stats = totalDF.loc[totalDF['Year']==2022].groupby(['ROUTE_OF_ADMIN_DESC']).Saving_by_CostPerDaySupply.sum().reset_index() 
stats.sort_values(by=['Saving_by_CostPerDaySupply'], ascending=False, inplace=True) 
stats.rename(columns={"ROUTE_OF_ADMIN_DESC":"DrugRoute", "Saving_by_CostPerDaySupply":"Total Savings"}, inplace=True)


#BOB LEVEL Year - Route_Drug and DrugName
stats_by_commonBrandName = totalDF.groupby(['Year','ROUTE_OF_ADMIN_DESC','COMMON_BRAND_NAME']).Saving_by_CostPerDaySupply.sum().reset_index()
stats_by_commonBrandName.rename(columns={'ROUTE_OF_ADMIN_DESC':'DrugRoute', 'COMMON_BRAND_NAME':'DrugName', 'Saving_by_CostPerDaySupply':'Total Savings'}, inplace=True)
    
sample_stats = stats_by_commonBrandName.loc[(stats_by_commonBrandName['Year']=='2022') & (stats_by_commonBrandName['DrugRoute']=='INHALATION')]
sample_stats.sort_values(by=['Total Savings'], ascending=False, inplace=True) 


### plot images

client1_annual_saving_barplot = px.bar(totalAnnualSaving, x="Year", y="TotalSavings",   barmode="group")
client1_monthly_saving_lineplot = px.line(totalMonthlySaving, x="Month", y="TotalSavings" )
 

client1_drugroute_saving_barplot = px.bar(stats, x="Total Savings", y="DrugRoute",  barmode="group")
client1_drugroute_drugname_saving_barplot = px.bar(sample_stats, x="Total Savings", y="DrugName",  barmode="group")
 
tableDF = totalDF.copy()


#app.server.run()
#app = dash.Dash('RBC CMP Saving Reports',external_stylesheets=['https://example.com/style1.css', 'https://example.com/style2.css'])
  

#visualize the province_Saving
client1_canada_map_fig = dict(data=map_data, layout=map_dictionary)
 
 
# Describe the layout, or the UI, of the app


def layout():
    
    return html.Div([
        html.Div([ # page 1

           # html.A([ 'Print PDF' ], className="button no-print",  style=dict(position="absolute", top=-40, right=0)),

            html.Div([ # subpage 1

                # Row 1 (Header)

                html.Div([
                    html.Div([      
                        html.H1('Saving Report for Client  ', style={'textAlign': 'center' ,'color':'purple' }),
                      #  html.H4('An annual analysis on the savings',  style={'textAlign': 'center' ,'color':'darkmagenta' }), #color='#7F90AC')),
                    ], className = "nine columns padded" ),

                    html.Div([            
                        html.H1([html.Span('2022 - 2023 June', style=dict(opacity=0.8))]), #, html.Span('17')]),
                  #      html.H4('Annual Update')
                    ], className = "three columns gs-header gs-accent-header padded", style=dict(float='right')),

                ], className = "row gs-header gs-text-header" ),

                html.Br([]),   

                 # Row 2

                html.Div([     

                    html.Div([
                     #   html.H4('RBC Profile', className = "gs-header gs-text-header padded",style={'paddingLeft': '20px'}),

                        html.Strong('Saving Report',style={'paddingLeft': '20px'}),
                        html.P('This report simulated the potential savings by calculating the different drug costs after using XXX Complete Program ', className = 'blue-text',style={'paddingLeft': '20px'}),

                        html.Strong('Overall Savings',style={'paddingLeft': '20px'}),
                        html.P('GROUP demonstrated a strong savings of using XXX Complete Program. ', className = 'blue-text',style={'paddingLeft': '20px'}),

                        html.Strong('The main savings:',style={'paddingLeft': '20px'}),
                        html.P('Add high level summary for the savings', className = 'blue-text' ,style={'paddingLeft': '20px'}),

                    ], className = "four columns" ),

                    html.Div([
                        html.H5(["Overall Monthly Savings from 2022 - 2023 June"],
                                className = "gs-header gs-table-header padded",style={'paddingLeft': '20px'}),
                        #add the image here
                        dcc.Graph(id ='monthly-saving',
                                  figure=client1_monthly_saving_lineplot)
                      #  html.Iframe(src="https://plot.ly/~jackp/17553.embed?modebar=false&link=false&autosize=true", \
                      #          style=dict(border=0), width="100%", height="250")
                    ], className = "eight columns" ),

                ], className = "row "),


                # Row 2.5

                html.Div([     

                    html.Div([
                        html.H5('Total Annual Saving ',  className = "gs-header gs-text-header padded",style={'paddingLeft': '20px'}),
                        html.Table( make_dash_table( totalAnnualSaving ), className = 'tiny-header' )
                    ], className = "four columns" ),

                    html.Div([
                        html.P("This is saving by the dispense Year-Month. This demonstrates that the savings using XXX Complete Program \
                           increase significantly especially in 2022."),
                        html.Strong("Savings between 2022-01-01 to 2023-06:"),
                        html.Br([]),
                        html.P("Monthly Saving Per Cardholder"),
                        
                        html.P("2022 July: $757"),
                        html.P("2023 March: $1,347"),
                        html.P("2023 May: $806"),

                    ], className = "eight columns" ),

                ], className = "row "),  #end row 2.5


            ], className = "subpage" ),

        ]),



        html.Div([ #page 2, map
            html.H4('Saving By Province', style={'textAlign': 'center' ,'color':'darkmagenta' }),
            dcc.Graph(id='canada-map', figure=client1_canada_map_fig)
        ]),



        html.Div([ # page 3

          #  html.A([ 'Print PDF' ],
          #     className="button no-print",
          #     style=dict(position="absolute", top=-40, right=0)),

            ###ADDING THE MENU DROP DOWN CODE - DrugRoute
            html.Div(
                id="menu-area",
                style={'backgroundColor': 'lightgray'},
                children=[

                    html.H5("Saving by Drug Route",style={'paddingLeft': '20px'}),
                    html.Div(
                        children=[
                            html.Div(
                                className="menu-title",
                                children="Year"
                            ),
                            dcc.Dropdown(
                                id="year_fiter",
                                className="dropdown",
                                options=[{"label":year, "value":year} for year in totalDF.Year.unique()],
                                clearable=False,
                                value="2022"

                            ),
                            html.Br(),
                            html.Div(
                                className="menu-title",
                                children="Province"
                            ),

                             dcc.Dropdown(
                                id="prov_fiter",
                                className="dropdown",
                                options=[{"label":province, "value":province} for province in listProv],
                                clearable=False,
                                value="-"

                        ),
                        ]
                    ),
                     dcc.Graph(id="client1_drugroute_saving",figure = client1_drugroute_saving_barplot),

                     html.Div(
                            className="menu-title",
                            children="DrugName"
                     ),
                     dcc.Dropdown(
                                id="drugroute_fiter",
                                className="dropdown",
                                options=[{"label":drugroute, "value":drugroute} for drugroute in stats_by_commonBrandName.DrugRoute.unique()],
                                clearable=False,
                                value="INHALATION"

                    ),

                     dcc.Graph(id="client1_drugroute_drugname_saving",figure = client1_drugroute_drugname_saving_barplot),
                ]
            ), 

        ]),


       html.Div(
                children=[
                    dcc.Dropdown(
                        id='header-dropdown',
                        options=[{'label': col, 'value': col} for col in tableDF.columns],
                        value=[],
                        multi=True
                    ),
                
                    dcc.Input(
                        id='filter-RouteAdmin',
                        type='text',
                        placeholder='Enter ROUTE_OF_ADMIN_DESC filter...'
                    ),               
                    dcc.Input(
                        id='filter-BrandName',
                        type='text',
                        placeholder='Enter COMMON_BRAND_NAME filter...'
                    ),
                    dcc.Input(
                        id='filter-Year',
                        type='number',
                        placeholder='Enter Year filter...'
                    ),       
                    dcc.Input(
                        id='filter-DIN',
                        type='number',
                        placeholder='Enter DIN filter...'
                    ),
                    dcc.Dropdown(
                        id='sort-dropdown',
                        options=[{'label': col, 'value': col} for col in totalDF.columns],
                        value=[],
                        multi=True,
                        placeholder='Sort by...'
                    )
                ],
                style={'marginBottom': '20px'}
            ),
            html.Table(id='client1_filtered-table')


      # dbc.Container([
      #  dbc.Label('Click a cell in the table:'),
      #  dash_table.DataTable(totalDF.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
      #  dbc.Alert(id='tbl_out'),
      #  ])

    ])


 

# Define the callback function
 
@callback(
    Output(component_id='client1_filtered-table', component_property='children'),
    [Input(component_id='header-dropdown', component_property='value'),
    Input(component_id='filter-RouteAdmin', component_property='value'),
    Input(component_id='filter-BrandName', component_property='value'),
    Input(component_id='filter-Year', component_property='value'),
    Input(component_id='filter-DIN', component_property='value'),
    Input(component_id='sort-dropdown', component_property='value')]
)
 
def update_table(selected_headers, filter_RouteAdmin,filter_BrandName, filter_Year,filter_DIN, sort_column):
    print("calling update_table")
    print("filtered df the top columns")
    filtered_df = tableDF  # Filter the DataFrame based on selected headers
    if selected_headers:
        filtered_df = tableDF[selected_headers]
    print(filtered_df.head())
 
    if filter_RouteAdmin:
        filtered_df = filtered_df[filtered_df['ROUTE_OF_ADMIN_DESC'].str.contains(filter_RouteAdmin, case=False)]
        

    if filter_BrandName:
        filtered_df = filtered_df[filtered_df['COMMON_BRAND_NAME'].str.contains(filter_BrandName, case=False)]
        

    if filter_Year:
        filtered_df = filtered_df[filtered_df['Year']==int(filter_Year)]

    if filter_DIN:
         filtered_df = filtered_df[filtered_df['DIN']==int(filter_DIN)]
        
        
    if sort_column:
        filtered_df = filtered_df.sort_values(by=sort_column)

    #    Round the numeric columns to two decimal places 
    if 'Saving_by_CostPerDaySupply' in selected_headers:
        filtered_df['Saving_by_CostPerDaySupply'] = filtered_df['Saving_by_CostPerDaySupply'].round(2)

         
    # Create the HTML table with the filtered data
    mytable = [
        html.Thead(
            html.Tr([html.Th(col) for col in filtered_df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns
            ]) for i in range(len(filtered_df))
        ])
    ]
    return mytable
#def update_graphs(active_cell):
#    return str(active_cell) if active_cell else "Click the table"

## update the map
# Callback function to update the map 


@callback(
    Output(component_id='client1_drugroute_saving', component_property='figure'),
     [Input(component_id='year_fiter', component_property='value'), 
     Input (component_id='prov_fiter', component_property='value')]  
           
)
#function to support callback
def update_drugroute_plot(targetYear, targetProv):
    df_tmp=totalDF.loc[totalDF['Year']==targetYear]
    
    if targetProv != '-':
        data_to_plot = df_tmp.loc[df_tmp['Province_Code']==targetProv]
    else:
        data_to_plot = df_tmp
        
    
    tmp_stats = data_to_plot.groupby(['ROUTE_OF_ADMIN_DESC']).Saving_by_CostPerDaySupply.sum().reset_index() 
    tmp_stats.sort_values(by=['Saving_by_CostPerDaySupply'], ascending=False, inplace=True)
    tmp_stats.rename(columns={"ROUTE_OF_ADMIN_DESC":"DrugRoute", "Saving_by_CostPerDaySupply":"Total Savings"}, inplace=True)
    
    fig = px.bar(tmp_stats, x="Total Savings", y="DrugRoute",   barmode="group")
    
    fig.update_layout()
    return fig
 

## add drugname barplot    
@callback(
    Output(component_id='client1_drugroute_drugname_saving', component_property='figure'),
    [Input(component_id='year_fiter', component_property='value'),
     Input (component_id='drugroute_fiter', component_property='value'),
     Input (component_id='prov_fiter', component_property='value')]  
           
)
#function to support callback
def update_drugnameplot(targetYear, targetDrugroute, targetProv): 
    
    stats_by_commonBrandName = totalDF.groupby(['Year','Province_Code','ROUTE_OF_ADMIN_DESC','COMMON_BRAND_NAME']).Saving_by_CostPerDaySupply.sum().reset_index()
    stats_by_commonBrandName.rename(columns={'ROUTE_OF_ADMIN_DESC':'DrugRoute', 'COMMON_BRAND_NAME':'DrugName', 'Saving_by_CostPerDaySupply':'Total Savings'}, inplace=True)
    
    sample_stats = stats_by_commonBrandName.loc[(stats_by_commonBrandName['Year']==targetYear) & (stats_by_commonBrandName['DrugRoute']==targetDrugroute)]
    sample_stats.sort_values(by=['Total Savings'], ascending=False, inplace=True) 

    print(targetYear)
    print(targetDrugroute) 
     
    if targetProv != '-':
        data_to_plot = sample_stats.loc[sample_stats['Province_Code']==targetProv] 
    else:        
        data_to_plot = sample_stats.groupby(['Year','DrugRoute','DrugName'])["Total Savings"].sum().reset_index()
    print(data_to_plot.head())
         
    data_to_plot.sort_values(by=['Total Savings'], ascending=False, inplace=True)  
    fig = px.bar(data_to_plot, x="Total Savings", y="DrugName",   barmode="group")
  
    fig.update_layout()
    return fig

  
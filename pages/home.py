import dash
from dash import html, dcc 
dash.register_page(__name__)


layout = html.Div([ # page 1

    #    html.A([ 'Print PDF' ], className="button no-print",  style=dict(position="absolute", top=-40, right=0)),     
                        
        html.Div([ # subpage 1

            # Row 1 (Header)

            html.Div([
                html.Div([      
                    
                    html.H3('Introducing Saving Calculation for Telus Complete Program ', style={'textAlign': 'center' ,'color':'darkmagenta' }),
                    html.Br([]),
                    html.H4('Methodology',  style={'textAlign': 'left' ,'color':'darkmagenta'}),  
                    html.Br([]),
                    html.Strong('First, Collect the target claims', style={'textAlign': 'left'}), 
                    html.Ul([
                        html.Li("Rejected Claims for the target group is identified as the rejected claim with rejected code as 2070 from the program effective date up  to 1 year or to the specific date"),
                        html.Li("Accepted Claims for the same group during the same period of time")                        
                    ]),
                    
                    
                    html.Strong('Second, Identify \'valid\' acccepted claims, satisfied with the following conditions ', style={'textAlign': 'left'   }), #color='#7F90AC')),
                    html.Ul([
                        html.Li("Same claimant <u>(Cardholder + Relationship code)</u> with the rejected claim"),
                        html.Li("Same medication (DIN) under the same drug category (DINClass8) as the rejected claim"),
                        html.Li("Dispense date from accepted claim is >= the dispense date from the rejected claim"),
                        
                    ]),
                    html.P("Once the valid accepted claim is identified, FLEX_DIN_COST from the rejected claim needs to be calculated"),
                    
                    html.Br([]),
                    html.Strong("Third, Match FLEX_DIN_COST for the rejected claim by matching the FLEX DIN table"),
                      html.Ul([
                        html.Li("Matching by DIN, Province, Dispense Date"),
                        html.Li("If there are multiple records found, choose the one with 'PACKAGE_SIZE'=1"), 
                        
                    ]),
                    html.P("Note: for paper submission, the PACKAGE_SIZE!=1. To exclude the paper submission by excluding claims with Provideer_ID ending with '111111'"),
                     
                    html.Br([]),
                    html.Strong("Fourth, Calculate the FLEX_DIN_COST for the rejected claim by applying the MARKUPs"),
                     html.Br([]),
                    html.Ul([
                        html.Li("If MARKUP_METHOD = 'A' (Additive)"),
                        html.P(r"FLEX_DIN_COST_Rejected = FLEX_DIN_COST+ MARKUP_1 * FLEX_DIN_COST + MARKUP_2*FLEX_DIN_COST"),
                                          
                        html.Li("If MARKUP_METHOD = 'C'(Compounded)"),
                        html.P(r"FLEX_DIN_COST_Rejected = FLEX_DIN_COST+ MARKUP_1 * FLEX_DIN_COST + MARKUP_2 * /(FLEX_DIN_COST+ MARKUP_1*FLEX_DIN_COST/)"),
                    ]),
                    
                    html.Br([]),
                    html.Strong("Fifth, Calculate savings on an accepted claim"),
                    html.Br([]),
                    html.P("Saving_Accepted = DaySupply_Accepted * (CostPerDay_Rejected - CostPerDay_Accepted)"),
                    html.P("CostPerDay_Accepted = FLEX_DIN_COST * QTY_Accepted/DaysSupply_Accepted"),
                    html.P("CostPerDay_Rejected = FLEX_DIN_COST_Rejected * QTY_Accepted/DaysSupply_Rejected"),
                    
                    html.Br([]),
                    html.Strong("Lastly, Sum up all the savings from all accepted claims")
                    
                    
                    
                ], className = "nine columns padded" ),
                 
            ], className = "row gs-header gs-text-header" ),

            html.Br([]),   
                
        ])
])
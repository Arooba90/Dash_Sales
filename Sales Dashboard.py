from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

df = pd.read_csv('sales_data_sample.csv', encoding='latin1')

colors = {
    'text': '#3e3f40',
    'accent1': '#68a697',
    'accent2': '#a0cac0',
    'background': '#D3D3D3'
}

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    dbc.Row([
        html.Div('Sales Dashboard', className="text-center fs-3", style={
            'color': colors['text'],
            'backgroundColor': colors['accent1'],
            'padding': '10px',
            'borderRadius': '5px',
            'marginBottom': '20px',
            'fontWeight': 'bold'
        })
    ]),

    dbc.Row([
        dbc.Col([
            html.Div('MONTHLY SALES FOR', className="text-center fs-4", style={
                'color': colors['text'],
                'backgroundColor': colors['accent1'],
                'padding': '10px',
                'borderRadius': '5px',
                'marginBottom': '10px'
            }),
            dcc.Graph(id='monthly-sales-graph', style={
                'border': f'2px solid {colors["accent1"]}',
                'borderRadius': '10px',
                'padding': '10px',
                'backgroundColor': colors['background']
            }),
            html.Div(
                dcc.RadioItems(
                    id='year-radio',
                    options=[{'label': str(year), 'value': year} for year in df['YEAR_ID'].unique()],
                    value=df['YEAR_ID'].unique()[0],
                    inline=True,
                    labelStyle={'margin-right': '10px', 'color': colors['text']},
                    style={'marginBottom': '20px'}
                ),
                style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center'
                }
            )
        ], width=6, style={
            'alignItems': 'center'
        }),

        dbc.Col([
            html.Div('YEARLY SALES', className="text-center fs-4", style={
                'color': colors['text'],
                'backgroundColor': colors['accent1'],
                'padding': '10px',
                'borderRadius': '5px',
                'marginBottom': '10px'
            }),
            dcc.Graph(id='yearly-sales-graph', style={
                'border': f'2px solid {colors["accent1"]}',
                'borderRadius': '10px',
                'padding': '10px',
                'backgroundColor': colors['background']
            })
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div('TOP 10 COUNTRIES BY SALES', className="text-center fs-4", style={
                'color': colors['text'],
                'backgroundColor': colors['accent1'],
                'padding': '10px',
                'borderRadius': '5px',
                'marginBottom': '10px'
            }),
            dcc.Graph(id='top-countries-graph', style={
                'border': f'2px solid {colors["accent1"]}',
                'borderRadius': '10px',
                'padding': '10px',
                'backgroundColor': colors['background']
            })
        ], width=12),
    ]),
], fluid=True, style={'backgroundColor': colors['background'], 'padding': '20px'})

@callback(
    Output(component_id='monthly-sales-graph', component_property='figure'),
    Input(component_id='year-radio', component_property='value')
)
def update_monthly_graph(selected_year):
    filtered_df = df[df['YEAR_ID'] == selected_year]
    monthly_sales = filtered_df.groupby('MONTH_ID')['SALES'].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_sales['MONTH_ID'],
        y=monthly_sales['SALES'],
        mode='lines+markers',
        name=str(selected_year),
        hovertemplate='Month: %{x}<br>Sales: %{y}<extra></extra>',
        line=dict(color=colors['accent1']),
        marker=dict(color=colors['accent2'])
    ))
    fig.update_layout(
        xaxis_title='MONTHS',
        yaxis_title='SALES',
        xaxis=dict(tickmode='linear', tick0=1, dtick=1),
        hovermode='closest',
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        margin=dict(t=10)
    )
    return fig

@callback(
    Output(component_id='yearly-sales-graph', component_property='figure'),
    Input(component_id='year-radio', component_property='value')
)
def update_yearly_graph(_):
    yearly_data = df.groupby('YEAR_ID')['SALES'].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_data.index,
        y=yearly_data.values,
        mode='lines+markers',
        name='Yearly Sales',
        hovertemplate='Year: %{x}<br>Sales: %{y}<extra></extra>',
        line=dict(color=colors['accent1']),
        marker=dict(color=colors['accent2'])
    ))
    fig.update_layout(
        xaxis_title='YEARS',
        yaxis_title='SALES',
        xaxis=dict(tickmode='linear'),
        hovermode='closest',
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        margin=dict(t=10)
    )
    return fig

@callback(
    Output(component_id='top-countries-graph', component_property='figure'),
    Input(component_id='year-radio', component_property='value')
)
def update_top_countries_graph(_):
    sales_by_country = df.groupby('COUNTRY')['SALES'].sum().reset_index()
    top_10_countries = sales_by_country.nlargest(10, 'SALES')
    fig = px.choropleth(
        top_10_countries,
        locations='COUNTRY',
        locationmode='country names',
        color='SALES',
        labels={'SALES': 'Sales'},
        color_continuous_scale=[colors['accent2'], colors['accent1']],
        projection='natural earth'
    )
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        margin=dict(t=10)
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
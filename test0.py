import dash
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo


df = pd.read_csv('school_dataset.csv')


# print(df[:5])

trace0= go.Scatter(

    x=df.ID,
    y=df.First,
    mode='lines+markers',
    name='Math plot'
)

trace1 = go.Scatter(

    x=df.ID,
    y=df.Second,
    mode='lines+markers',
    name='English plot'
)
trace2 = go.Scatter(
    x=df.ID,
    y=df.Third,
    mode='lines+markers',
    name='Physics plot'

)

trace3 = go.Scatter(
    x=df.ID,
    y=df.Fourth,
    mode='lines+markers',
    name='Chemistry plot'

)

trace4 = go.Scatter(
    x=df.ID,
    y=df.Fifth,
    mode='lines+markers',
    name='Biology plot'

)

trace5 = go.Scatter(
    x=df.ID,
    y=df.ave,
    mode='lines+markers',
    name='Average plot'

)
data= [trace0,trace1,trace2,trace3,trace4,trace5]


layout = go.Layout(title = 'School Result',
                   xaxis_title='Student ID',
                   yaxis_title='Student Performance')

figure = go.Figure(data=data,layout=layout)
pyo.plot(figure)

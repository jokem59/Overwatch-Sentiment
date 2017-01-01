import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import time

def setupPlotly(points):
    '''
    Sets up plotly graph to write to
    :param points: <int> of max number of points to keep plotted on graph
    :return: Plotly Stream object
    '''

    # Setup plotly
    stream_ids = tls.get_credentials_file()['stream_ids']

    # Get stream id from stream id list
    stream_id = stream_ids[0]

    # Make instance of stream id object
    stream_1 = go.Stream(
        token=stream_id,  # link stream id to 'token' key
        maxpoints=points  # keep a max of 80 pts on screen
    )

    # Initialize trace of streaming plot by embedding the unique stream_id
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines',
        stream=stream_1  # (!) embed stream id, 1 per trace
    )

    data = go.Data([trace1])

    # Add title to layout object
    layout = go.Layout(
        title='Twitter Overwatch Sentiment',
        xaxis=dict(
            title='Date & Time',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Aggregate Sentiment',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    # Make a figure object
    fig = go.Figure(data=data, layout=layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.iplot(fig, filename='python-streaming')

    # We will provide the stream link object the same token that's associated with the trace we wish to stream to
    stream_object = py.Stream(stream_id)

    # We then open a connection
    stream_object.open()

    time.sleep(5)

    return stream_object

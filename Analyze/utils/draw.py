import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from user import User
from typing import List
import pandas as pd
import plotly.express as px




def drawDiffTargetHist(c1: List[User], c2: List[User]):
    df1 = getHistDf(c1)
    df2 = getHistDf(c2)

    trace1 = px.bar(df1, x="ID", y="Score", color="Type", barmode="group")
    trace2 = px.bar(df2, x="ID", y="Score", color="Type", barmode="group")

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Add List", "Not Add List"))


    for i in range(len(trace1["data"])):
        fig.append_trace(trace1['data'][i], row=1, col=1)

    for i in range(len(trace2["data"])):
        fig.append_trace(trace2['data'][i], row=2, col=1)

    fig.update_layout(title_text="Diff Intent")
    fig.show()


def getHistDf(c: List[User]):
    likeScores = [(sum(x.WDLikeScores)+sum(x.TLikeScores))/(len(x.WDLikeScores)*2) for x in c]
    likeScores = [[i, 'Like', likeScores[i]] for i in range(len(likeScores))]

    dislikeScores = [(sum(x.WDDislikeScores)+sum(x.TDislikeScores))/(len(x.WDDislikeScores)*2) for x in c]
    dislikeScores = [[i, 'Dislike', dislikeScores[i]] for i in range(len(dislikeScores))]

    endScores = [(sum(x.WDEndScores)+sum(x.TEndScores))/(len(x.WDEndScores)*2) for x in c]
    endScores = [[i, 'End', endScores[i]] for i in range(len(endScores))]

    songListScores = [(x.WDScore + x.TScore)/2 for x in c]
    songListScores = [[i, 'SongListScores', songListScores[i]] for i in range(len(songListScores))]

    data = []
    data.extend(likeScores)
    data.extend(dislikeScores)
    data.extend(endScores)
    data.extend(songListScores)

    df = pd.DataFrame(data, columns=["ID", "Type", "Score"])
    return df

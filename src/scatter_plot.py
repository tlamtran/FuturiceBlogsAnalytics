import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from ast import literal_eval

def scatter_plot():
    df = pd.read_csv('data/processed/futurice/streamlit_scatterplot.csv')

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        feature = st.selectbox("Select a feature:", ["title", "teaser text"])
    with col2:
        stat = st.selectbox("Select a metric:", ["total users", "bounce rate", "average session duration"])


    if feature and stat:
        metric = df[stat].values

        q20 = np.percentile(metric, 20)
        q40 = np.percentile(metric, 40)
        q60 = np.percentile(metric, 60)
        q80 = np.percentile(metric, 80)

        colors = []
        for value in metric:
            if value <= q20:
                colors.append("#FF0000")  # 0-20%
            elif value <= q40:
                colors.append("#FFA200")  # 20-40%
            elif value <= q60:
                colors.append("#FFF200")  # 40-60%
            elif value <= q80:
                colors.append("#B3FF00")  # 60-80%
            else:
                colors.append("#008000")  # 80-100%

        df['color'] = colors

        brush = alt.selection_interval()

        points = alt.Chart(df).mark_circle(
            size=70
        ).encode(
            x=feature +" x",
            y=feature +" y",
            color=alt.condition(brush, alt.Color('color:N', scale=None), alt.value('grey')),
            tooltip=[feature]
        ).properties(
            width=700,
            height=600
        ).add_selection(brush)

        ranked_text = alt.Chart(df).mark_text(align='left', size=15).encode(
            y=alt.Y('row_number:O',axis=None)
        ).transform_filter(
            brush
        ).transform_window(
            row_number='row_number()'
        ).transform_filter(
            'datum.row_number < 15'
        )

        # Data Tables
        link = ranked_text.encode(text='link:N').properties(title=alt.TitleParams(text='Link', align='left'))
        text = ranked_text.encode(text=feature + ':N').properties(title=alt.TitleParams(text=feature, align='left'))

        table = alt.hconcat(link, text)

        chart = alt.vconcat(
            points,
            table
        )

        st.altair_chart(chart, theme="streamlit")

import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import altair as alt


st.title('Pokemon Data')

@st.cache
def get_pokemon_data():
    path = 'pokemon_out_csv'
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for f in csv_files:
        df = pd.read_csv(f)
        return df

def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'


df_no_idx = get_pokemon_data()


def select_data(df, idx_name):
    if idx_name in ("name","type"):
        # collaps the two type columns into one
        if idx_name == "type":            
            df = pd.melt(df, id_vars=["name","id","order","bmi", "height","weight","base_experience", "front_default_sprite_url"], 
                value_vars=['type_primary','type_secondary'], var_name='primary_secondary_type', value_name='type').dropna() 
        df = df.set_index(idx_name)
        if idx_name == 'type':
            pokemon = st.multiselect(
            f"Select Pokemon by {idx_name.title()}", sorted(list(set(df.index))), ["grass", "fire"]
            )  
        if idx_name == 'name':  
            pokemon = st.multiselect(
                f"Select Pokemon by {idx_name.title()}", sorted(list(df.index)), ["Bulbasaur", "Pikachu"]
            )
        if not pokemon:
            st.error("Please select at least one pokemon.")
        else:
            data = df.loc[pokemon].sort_index()
            st.markdown(
                data.to_html(escape=False, formatters=dict(front_default_sprite_url=path_to_image_html)),
                unsafe_allow_html=True,
            )

            data = data.reset_index()
            chart_data = data
            c = alt.Chart(chart_data, title="Pokemon experience and BMI").mark_circle().encode(
                x=idx_name, y='base_experience', size='bmi', color='bmi', tooltip=["name", "base_experience","bmi"])

            st.altair_chart(c, use_container_width=True)

            c = alt.Chart(chart_data, title="Pokemon experience and Height").mark_circle().encode(
            x=idx_name, y='base_experience', size='height', color='height', tooltip=["name", "base_experience","height"])

            st.altair_chart(c, use_container_width=True)

            c = alt.Chart(chart_data, title="Pokemon experience and Weight").mark_circle().encode(
            x=idx_name, y='base_experience', size='weight', color='weight', tooltip=["name", "base_experience","weight"])

            st.altair_chart(c, use_container_width=True)


selection = st.radio(
    "How do you want to select your Pokemon? By:",
    ('Name', 'Type'))

if selection  == 'Name':
    select_data(df_no_idx, "name")
elif selection == 'Type':
    select_data(df_no_idx, "type")
else:
    st.write("You didn't select an option.")


import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go

"""## Lineplot of Random PPG Signal using Plotly"""

feather_dir_path_full = "./MIMIC-III_sub_full_feather_dataset/"

# For Random Signal
# Function to load dataframe based on the index
@st.cache_resource
def load_dataframe_full(file_index, input_dir_feather):
    feather_file_name = f'MIMIC-III_sub_full_{file_index}.feather'
    feather_file_path = os.path.join(input_dir_feather, feather_file_name)
    df_feather = pd.read_feather(feather_file_path)

    # Reset the index to ensure Row_Index starts from 0
    df_feather.reset_index(drop=True, inplace=True)

    # Add a new column "Row_Id"
    df_feather['Row_Index'] = df_feather.reset_index().index
    return df_feather


# Function to plot random PPG signal
def plot_random_ppg_signal(df):
    random_row = df.sample(1).iloc[0]

    row_index = random_row['Row_Index']
    subject_index = random_row['Subject_Index']
    sbp_value = random_row['SBP']
    dbp_value = random_row['DBP']
    ppg_signal = random_row['PPG']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(ppg_signal))), y=ppg_signal, mode='lines', name='PPG Signal', line=dict(color='orange')))
    label_text = f"Row_Index: {row_index}, <br> Subject_Index: {subject_index}, <br> SBP: {sbp_value}, DBP: {dbp_value}"
    fig.add_annotation(x=1.0, y=1.2, xref='paper', yref='paper', text=label_text, showarrow=False, font=dict(size=15))
    fig.update_layout(title="Random PPG Signal with Row_Index, Subject_Index, SBP, and DBP",
                      xaxis_title="PPG Array Index",
                      yaxis_title="PPG Value",
                      template="plotly_dark")
    st.plotly_chart(fig)


# Function to plot sequential PPG signal
def plot_sequential_ppg_signal(df, current_row):
    if 0 <= current_row < len(df):
        row_index = df.iloc[current_row]['Row_Index']
        subject_index = df.iloc[current_row]['Subject_Index']
        sbp_value = df.iloc[current_row]['SBP']
        dbp_value = df.iloc[current_row]['DBP']
        ppg_signal = df.iloc[current_row]['PPG']

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(ppg_signal))), y=ppg_signal, mode='lines', name='PPG Signal', line=dict(color='yellow')))
        label_text = f"Row_Index: {row_index}, <br> Subject_Index: {subject_index}, <br> SBP: {sbp_value}, DBP: {dbp_value}"
        fig.add_annotation(x=1.0, y=1.2, xref='paper', yref='paper', text=label_text, showarrow=False, font=dict(size=15))
        fig.update_layout(title="Sequential PPG Signal with Row_Index, Subject_Index, SBP, and DBP",
                          xaxis_title="PPG Array Index",
                          yaxis_title="PPG Value",
                          template="plotly_dark")
        st.plotly_chart(fig)
    else:
        st.write("End of dataframe reached.")


# Streamlit app
def main():
    st.title("MIMIC-III PPG Signal Visualization")

    # Dropdown/select box for choosing dataframe index
    index = st.selectbox("Select the Dataframe: ", options=[""] + list(range(1, 3)))

    # # User input for selecting the starting row index
    # start_row = st.number_input("Select Row Index:", 0, 9053999, 0)

    # Check if a value has been selected
    if index != "":

        # Load dataframe only if the index has changed
        df_fea = load_dataframe_full(index, feather_dir_path_full)

        # "Loading the Dataframe from .feather"

        # Progress bar while loading dataframe
        progress_bar = st.progress(0)

        # Load dataframe (this will only be executed once for each unique index)
        df_fea = load_dataframe_full(index, feather_dir_path_full)

        # Update progress bar to completion
        progress_bar.progress(100)

        "...Dataframe Loaded"

        # User input for selecting the starting row index
        start_row = st.number_input("Select Row Index:", 0, 452699, 0)
        st.write("Sequential PPG Signal Visualization")
        # Show the graph immediately when the user enters the row index
        plot_sequential_ppg_signal(df_fea, start_row)


        st.write("Random PPG Signal Visualization")
        # Button to create the graph
        if st.button("Click to see Random PPG Signal"):

            # Plot the graph
            plot_random_ppg_signal(df_fea)

        
        
# Run the Streamlit app
if __name__ == "__main__":
    main()

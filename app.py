import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

# read the global shark attacks dataset
df = pd.read_csv("attacks.csv", encoding="ISO-8859-1")


# convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# set up the pages and tabs
PAGES = {
    "Overview": "This page displays an overview of the global shark attacks dataset.",
    "Explore by Country": "This page displays a map of the global shark attacks by country.",
    "Reasons for Attacks": "This page displays a chart showing the reasons for shark attacks."
}

# set up the app
st.set_page_config(page_title="Global Shark Attacks", page_icon=":shark:", layout="wide")
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# set up the pages
page = PAGES[selection]

# set up the tabs
if selection == "Overview":
    tab1, tab2, tab3 = st.tabs(['Summary', 'Map', 'Analysis'])
    with tab1:
        image = Image.open('Images/shark_attack.jpg')
        image = image.resize((200,100), Image.ANTIALIAS)
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(image, caption="Source: Unsplash")
            st.subheader("Fatal vs Non-Fatal Attacks")
            fatal_counts = df['Fatal (Y/N)'].value_counts()
            fatal_counts = fatal_counts[fatal_counts.index.isin(['Y', 'N'])]
            fig2 = px.pie(values=fatal_counts.values, names=fatal_counts.index,
                        title='Fatal vs Non-Fatal Shark Attacks',
                        hole=.5, color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig2)
        with col2:
            st.markdown("<h1 style='text-align: center;'>Global Shark Attacks: An Analysis</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>This application will take you through an analysis of global shark attacks through a series of visual representations and information.</h2>", unsafe_allow_html=True)
            st.subheader("About the Dataset")
            st.markdown('The dataset used in this analysis was obtained from the Global Shark Attack File (GSAF), which documents and tracks shark attacks worldwide.')
            st.markdown('The dataset includes information on the date, location, activity, type of attack, species of shark, and other related details for each recorded shark attack.')
            st.markdown('The data spans from 1800 to 2021.')

    
       
    with tab2:
        col1, col2 = st.columns([1,2])
        image2 = Image.open('Images/shark_attack.jpg')
        image2 = image2.resize((200,100),Image.ANTIALIAS)
        with col1:
            st.image(image2)
            st.markdown(" ")
            st.markdown('Shark attacks have long been a topic of fascination and fear for people all over the world. However, despite the media attention given to shark attacks, they are actually relatively rare events.')
        with col2:
            st.markdown('The dataset reveals interesting trends in shark attacks, such as the top species responsible for attacks, the most common activities that lead to attacks, and the countries with the highest number of recorded shark attacks.')
            st.markdown('In addition, the dataset allows us to explore the impact of various factors on shark attacks, such as climate change, changes in human behavior, and advances in technology.')
            
        st.markdown(" ")
        st.write('Use the filters on the left to explore the shark attack dataset.')
       
    with tab3:
        st.title("Global Shark Attacks")
        st.write("This app displays data on global shark attacks, including information on the date, country, activity, and injury type. Use the dropdown menus to filter the data and the table to view the results.")
        
        # create a sidebar with dropdown menus to filter data
        st.sidebar.title("Filter Data")
        countries = df['Country'].unique()
        selected_country = st.sidebar.selectbox("Country", ["All"] + list(countries))
        activities = df['Activity'].unique()
        selected_activity = st.sidebar.selectbox("Activity", ["All"] + list(activities))
        injury_types = df['Injury'].unique()
        selected_injury_type = st.sidebar.selectbox("Injury Type", ["All"] + list(injury_types))
        
        # filter the data based on the user's selection
        filtered_df = df
        if selected_country != "All":
            filtered_df = filtered_df[filtered_df['Country'] == selected_country]
        if selected_activity != "All":
            filtered_df = filtered_df[filtered_df['Activity'] == selected_activity]
        if selected_injury_type != "All":
            filtered_df = filtered_df[filtered_df['Injury'] == selected_injury_type]
        
        # display the filtered data in a table
        st.write("## Shark Attack Data")
        st.write("Use the table below to view the filtered data.")
        st.dataframe(filtered_df)

        
        


elif selection == "Explore by Country":
    st.title("Explore by Country")
    st.write("This page allows you to explore global shark attacks by country. Use the tabs below to view the data as a list or on a map.")
    
    # set up the tabs
    
    tab1, tab2 = st.tabs(['Country List', 'Country Map'])
    with tab1:
        

        df['Fatality'] = df['Fatal (Y/N)'].apply(lambda x: 'Fatal' if x == 'Y' else 'Non-fatal')

        # group the data by year and fatality, and count the number of attacks
        fatality_counts = df.groupby(['Year', 'Fatality']).size().reset_index(name='Count')

        # create the chart using altair
        chart = alt.Chart(fatality_counts).mark_circle(size=50).encode(
            x='Year:O',
            y='Count:Q',
            color=alt.condition(alt.datum.Fatality == 'Fatal', alt.value('#F03B20'), alt.value('#6c8ebf')),
            tooltip=['Year', 'Fatality', 'Count']
        ).properties(
            width=800,
            height=400,
            title="Fatal vs Non-Fatal Shark Attacks over Time"
        )


       


       



        
      
                

        
    with tab2:
        st.write("## Map of Countries")
        st.write("This map displays the locations of global shark attacks by country. Use the dropdown menu to filter the data.")
        
        # create a sidebar with a dropdown menu to filter data
        countries = df['Country'].unique()
        selected_country = st.sidebar.selectbox("Country", ["All"] + list(countries))
        filtered_df = df
        if selected_country != "All":
            filtered_df = filtered_df[filtered_df['Country'] == selected_country]

  



        # calculate the proportion of fatal shark attacks for each country
        fatal_prop = filtered_df[filtered_df['Fatal (Y/N)'] == 'Y'].groupby('Country')['Fatal (Y/N)'].count() / filtered_df.groupby('Country')['Fatal (Y/N)'].count()

        # set the baseline proportion
        baseline_prop = 0.264

        # create a bar chart
        fig, ax = plt.subplots(figsize=(10,5))
        ax.bar(fatal_prop.index, fatal_prop, color=['green' if prop > baseline_prop else 'red' for prop in fatal_prop])
        ax.axhline(y=baseline_prop, color='black', linestyle='--')
        ax.set_xlabel('Country')
        ax.set_ylabel('Proportion of Fatal Attacks')
        ax.set_title('Proportion of Fatal Shark Attacks by Country')
        plt.xticks(rotation=90)
        plt.show()

        
       
else:

    tab1, tab2 = st.tabs(['Injury Type', 'Species and Time'])

    with tab1:
        st.title("Reason for Attacks")
        st.write("This tab displays a bar chart of the different types of injuries caused by shark attacks.")

        # create a sidebar with dropdown menus to filter data
        countries = df['Country'].unique()
        selected_country = st.sidebar.selectbox('Country', ["All"] + list(countries))
        selected_type = st.sidebar.multiselect('Type', df['Type'].unique())

        
        filtered_df = df
        if selected_type:
         filtered_df = filtered_df[filtered_df['Type'].isin(selected_type)]
        if selected_country != "All":
         filtered_df = filtered_df[filtered_df['Country'] ==selected_country]
          
        
        # group the data by injury type and count the number of attacks
        injury_counts = filtered_df.groupby('Injury').count().reset_index()[['Injury', 'Case Number']]
        injury_counts.columns = ['Injury', 'Count']

        injury_counts = injury_counts.sort_values(by='Count', ascending=False).head(10)
        
        # create a bar chart of the injury types and their counts
        chart = alt.Chart(injury_counts).mark_bar().encode(
            x=alt.X('Count'),
            y=alt.Y('Injury', sort='-x'),
            color=alt.Color('Injury', scale=alt.Scale(scheme= 'category10'))
        ).properties(
            title='Types of Injuries Caused by Shark Attacks',
            width=100
        )
        st.altair_chart(chart, use_container_width=True)
        

    with tab2:
        st.title("Global Shark Attacks")
        st.write("This chart displays the number of shark attacks by species and time. Use the dropdown menus to filter the data.")

        countries = df['Country'].unique()
        year_range = st.sidebar.slider("Select a range of years", 1900, 2018, (1995,2018))
        

        # filter the data based on the user's selection
        filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        

        # group the data by country and year and count the number of attacks
        attacks_by_country = filtered_df.groupby(['Country', 'Year']).size().reset_index(name="Count")

        # Filter the data to include only the top five countries with the most shark attacks in the selected range of years
        top_countries = attacks_by_country.groupby('Country')['Count'].sum().reset_index().sort_values('Count', ascending=False).head(5)
        top_countries_list = list(top_countries['Country'])
        filtered_df = attacks_by_country[attacks_by_country['Country'].isin(top_countries_list)]

        # create the chart using altair
        line_chart = alt.Chart(filtered_df).mark_line(point=alt.OverlayMarkDef()).encode(
            x=alt.X('Year:O', axis=alt.Axis(title='Year')),
            y=alt.Y('Count:Q', axis=alt.Axis(title='Number of Shark Attacks')),
            color='Country:N'
        ).properties(
            width=800,
            height=400,
            title="Number of Shark Attacks by Country and Year"
        )

        st.altair_chart(line_chart)



        

        
    
    




import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
import plotly.express as px
import chardet

with open("Global_attacks.csv", 'rb') as f:
    result = chardet.detect(f.read())
    
df = pd.read_csv("Global_attacks.csv", encoding=result['encoding'], low_memory=False)

PAGES = {
    "Overview": "This page displays an overview of the global shark attacks.",
    "Fatal vs Non Fatal Attacks": "This page showcases visualizations that uncover the fatality rates of shark attacks by type, country, and over time.",
    "Attacks over Time": "This page displays a chart showing the number of sharks attacks globally."
}

st.set_page_config(page_title="Global Shark Attacks", layout="wide")
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

if selection == "Overview":
        st.markdown("<h1 style='text-align: center;'>Global Shark Attacks</h1>", unsafe_allow_html=True)
        st.markdown("The graph shows the top 15 countries with the most shark attacks.") 

        st.markdown("Click on the checkbox to filter by Gender!")
        df["sex"] = df["sex"].map({"M": "Male", "F": "Female"})
        gender_filter = st.checkbox("Filter by Gender", value=False)
        if gender_filter:
            gender = st.radio("Select Gender", ("All", "Male", "Female"))
            if gender != "All":
                df = df[df["sex"] == gender]

        attacks_by_country = df.groupby("Country").size().reset_index(name="Count")
        attacks_by_country = attacks_by_country.sort_values("Count", ascending=False).head(15)
        
        bar_chart = alt.Chart(attacks_by_country, title="Top 15 Countries with the Most Shark Attacks").mark_bar(color='#8C6BB1').encode(
            x=alt.X("Count", title="Number of Shark Attacks"),
            y=alt.Y("Country:N", sort="-x", title="Country"),
            tooltip=["Country", "Count"]
        ).properties(
           width=800, height=450
        )
        st.altair_chart(bar_chart)

        boat_involved = ["Boat", "Boating", "Boatomg"]
        invalid2 = ["?", "Unverified", "Under investigation", "Unconfirmed", "Questionable", "Invalid"]
        df["Type"] = df["Type"].replace(boat_involved, "Boating")
        df["Type"] = df["Type"].replace(invalid2, "Invalid")
        attack_counts = df.groupby("Type").size().reset_index(name="Count")


        bar1 = alt.Chart(attack_counts).mark_bar(color='#8C6BB1').encode(
            x=alt.X("Type", title="Attack Type"),
            y=alt.Y("Count", title="Number of Attacks"),
            tooltip=["Type", "Count"]
        ).properties(
            width=500,
            height=400
        )
        st.altair_chart(bar1)

        
        st.markdown("This tab displays a bar chart of the different types of injuries caused by shark attacks.")

        countries = df['Country'].unique()
        selected_country = st.sidebar.selectbox('Country', ["All"] + list(countries))
        selected_type = st.sidebar.multiselect('Type', df['Type'].unique())

        
        filtered_df = df
        if selected_type:
         filtered_df = filtered_df[filtered_df['Type'].isin(selected_type)]
        if selected_country != "All":
         filtered_df = filtered_df[filtered_df['Country'] ==selected_country]
          
        injury_counts = filtered_df.groupby('Injury').count().reset_index()[['Injury', 'Case Number']]
        injury_counts.columns = ['Injury', 'Count']
        injury_counts = injury_counts.sort_values(by='Count', ascending=False).head(10)
        chart = alt.Chart(injury_counts).mark_bar().encode(
            x=alt.X('Count'),
            y=alt.Y('Injury', sort='-x'),
            color=alt.Color('Injury', scale=alt.Scale(scheme= 'category20b'))
        ).properties(
            title='Types of Injuries Caused by Shark Attacks',
            width=100
        )
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Fatal vs Non-Fatal Attacks")
        country = df['Country'].unique()
        selected_country = st.sidebar.selectbox("Country", ["All"] + list(country), key="country_selectbox")
        filtered_df = df
        if selected_country != "All":
         filtered_df = filtered_df[filtered_df['Country'] == selected_country]

        fatal_counts = df['Fatal (Y/N)'].value_counts().rename_axis('Fatal').reset_index(name='Count')
        fatal_counts = fatal_counts[fatal_counts['Fatal'].isin(['Y', 'N'])]
        fatal_counts['Fatal'] = fatal_counts['Fatal'].map({'Y': 'Fatal', 'N': 'Non-Fatal'})

        fig2 = px.pie(values=fatal_counts['Count'], names=fatal_counts['Fatal'],
                    title='Fatal vs Non-Fatal Shark Attacks',
                    hole=.5, color_discrete_sequence=px.colors.qualitative.Dark2)
        st.plotly_chart(fig2)
        st.markdown("Pick a country on the left side of the page to see the number of Fatal and Non Fatal attacks per each country.")

elif selection == "Fatal vs Non Fatal Attacks":
    st.title("Analysis of Fatal and Non Fatal Attacks")
    st.markdown("This page showcases visualizations that uncover the fatality rates of shark attacks by type, country, and over time.")

    countries = df['Country'].unique()
    selected_countries = st.sidebar.multiselect("Select Countries", ["All"] + list(countries), default=["All"])
    filtered_df1 = df
    if selected_countries != ["All"]:
     selected_countries = list(selected_countries) 
     filtered_df1 = filtered_df1[filtered_df1['Country'].isin(selected_countries)]
    
    tab1, tab2, tab3 = st.tabs(['Type of Activity', 'Country', 'Time'])
    with tab1:

        boat_involved = ["Boat", "Boating", "Boatomg"]
        invalid2 = ["?", "Unverified", "Under investigation", "Unconfirmed", "Questionable", "Invalid"]
        filtered_df1["Type"] = filtered_df1["Type"].replace(boat_involved, "Boating")
        filtered_df1["Type"] = filtered_df1["Type"].replace(invalid2, "Invalid")
        filtered_df1['Fatality'] = filtered_df1['Fatal (Y/N)'].apply(lambda x: 'Fatal' if x == 'Y' else 'Non-fatal')
         
        fatality_counts = filtered_df1.groupby(["Type", "Fatality"]).size().reset_index(name="Count")
        fig = px.bar(fatality_counts, x="Type", y="Count", color="Fatality", barmode="group",
                    title="Fatal vs Non-Fatal shark attacks by type", color_discrete_map={"Non-Fatal": "#800000", "Fatal": "#A9A9A9"})
        fig.update_layout(xaxis_title="Type of Activity", yaxis_title="Number of Attacks", legend_title="Fatality", width=900, height=450)
        st.plotly_chart(fig)

    with tab2:
        country_counts = df.groupby(["Country", "Fatality"]).size().reset_index(name="Count")
        country_counts = country_counts.sort_values("Count", ascending=False).head(15)

        fig2 = px.bar(country_counts, x="Country", y="Count", color="Fatality", barmode="group",
                    title="Fatal vs Non-Fatal shark attacks by country", color_discrete_map={"Non-Fatal": "#800000", "Fatal": "#A9A9A9"})
        fig2.update_layout(xaxis_title="Country", yaxis_title="Number of Attacks", legend_title="Fatality", width=900, height=450)
        st.plotly_chart(fig2)

    with tab3:
        st.markdown('The Scatter plot below shows that the number of fatal shark attacks has remained almost constant over time, and it is possible that many of those non-fatal attacks would have been fatal if they had happened decades earlier.')
        df['Fatality'] = df['Fatal (Y/N)'].apply(lambda x: 'Fatal' if x == 'Y' else 'Non-fatal')
        fatality_counts = df.groupby(['Year', 'Fatality']).size().reset_index(name='Count')
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
        st.altair_chart(chart)
        
else:
       
        st.title("Global Shark Attacks Over Time")
        st.markdown("This chart displays the number of shark attacks in different countries over time. Use the dropdown selectbox to filter the data.")

        countries = df['Country'].unique()
        year_range = st.sidebar.slider("Select a range of years", 1900, 2023, (2000,2022))
        filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        attacks_by_country = filtered_df.groupby(['Country', 'Year']).size().reset_index(name="Count")
        top_countries = attacks_by_country.groupby('Country')['Count'].sum().reset_index().sort_values('Count', ascending=False).head(5)
        top_countries_list = list(top_countries['Country'])
        filtered_df = attacks_by_country[attacks_by_country['Country'].isin(top_countries_list)]
        
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
        st.markdown('The graph above shows that the top 5 countries with number of shark attacks over the years, USA and Australia are the top countries with most attacks')

        countries = df['Country'].unique()
        selected_country = st.sidebar.selectbox("Country", ["All"] + list(countries))
        filtered_df = df
        if selected_country != "All":
         filtered_df = filtered_df[filtered_df['Country'] == selected_country]


        filtered_df['Year'] = pd.to_datetime(filtered_df['Year'], format='%Y')
        attacks_by_year = filtered_df.groupby(filtered_df['Year'].dt.year).size().reset_index(name='count')
        line_chart = alt.Chart(attacks_by_year).mark_line().encode(
           x=alt.X('Year:O', sort=alt.EncodingSortField('Year', order='ascending'), title='Year'),
           y=alt.Y('count:Q', title='Number of Shark Attacks'),
            tooltip=['Year', 'count']
        ).properties(
            title='Shark Attacks Over Time',
            width=800,
            height=400
        ).properties(title='Shark Attacks Over Time')
        st.altair_chart(line_chart, use_container_width=True)
        st.markdown('The line chart above shows the Total number of attacks over time which increased until 2015 and started decreasing from 2015 and has been reducing over the years.')
        st.markdown('select a country from the selectbox on the left to view the number of attacks for each country.')



        

        
    
    




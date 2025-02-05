import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Title for the dashboard
st.title("Indonesia COVID-19 Mobility Trends")

# Load shapefile
try:
    st.write("Loading shapefile...")
    # Ensure the shapefile path matches your GitHub repository structure
    indonesia_map = gpd.read_file("data/ne_10m_admin_0_countries.shp")
    st.write("Shapefile loaded successfully!")

    # Filter only for Indonesia
    if 'ADMIN' in indonesia_map.columns:
        indonesia_map = indonesia_map[indonesia_map['ADMIN'] == 'Indonesia']
        st.write("Filtered GeoDataFrame for Indonesia:")
    else:
        st.write("Column 'ADMIN' not found in shapefile.")
        indonesia_map = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry')  # Empty GeoDataFrame
except Exception as e:
    st.write(f"Error loading shapefile: {e}")
    indonesia_map = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry')  # Fail-safe GeoDataFrame

# Load mobility datasets
try:
    st.write("Loading mobility data for 2020, 2021, and 2022...")
    df2020 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2020_ID_Region_Mobility_Report.csv")
    df2021 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2021_ID_Region_Mobility_Report.csv")
    df2022 = pd.read_csv("https://raw.githubusercontent.com/Ram4UnMi/bisnis_visualisasi_data/main/dataset/2022_ID_Region_Mobility_Report.csv")
    st.write("Mobility data loaded successfully!")

    # Combine all years into one DataFrame
    mobility_data = pd.concat([df2020, df2021, df2022], ignore_index=True)
    st.write("Combined mobility dataset:")
    st.write(mobility_data.head())  # Display for debugging

    # Filter for workplace mobility
    workplace_mobility = mobility_data[['sub_region_1', 'workplaces_percent_change_from_baseline']].groupby('sub_region_1').mean().reset_index()
    st.write("Filtered workplace mobility data:")
    st.write(workplace_mobility.head())
except Exception as e:
    st.write(f"Error loading mobility data: {e}")
    workplace_mobility = pd.DataFrame()  # Empty DataFrame for fail-safe

# Merge data (if both GeoDataFrame and workplace mobility data are valid)
if not indonesia_map.empty and not workplace_mobility.empty:
    try:
        st.write("Merging data...")
        # Adjust column names as needed (use actual column names from your datasets)
        workplace_mobility['sub_region_1'] = workplace_mobility['sub_region_1'].str.strip()
        indonesia_map = indonesia_map.merge(
            workplace_mobility,
            left_on='ADMIN',  # Change to the correct column in the shapefile (e.g., 'name', 'ADMIN', etc.)
            right_on='sub_region_1',  # Change based on the column in your CSV
            how='left'
        )
        st.write("Data merged successfully!")
        st.write(indonesia_map.head())
    except Exception as e:
        st.write(f"Error during merge: {e}")
else:
    st.write("Cannot merge data. Please check your GeoDataFrame and mobility dataset.")

# Plot geospatial map
if not indonesia_map.empty:
    try:
        st.write("Plotting geospatial map...")
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        indonesia_map.plot(
            column='workplaces_percent_change_from_baseline',  # Change to the appropriate column in your merged data
            cmap='coolwarm',
            legend=True,
            legend_kwds={'label': "Workplace Mobility Change (%)"},
            ax=ax
        )
        plt.title('Workplace Mobility Trends Across Provinces')
        st.pyplot(fig)
    except Exception as e:
        st.write(f"Error during plotting: {e}")
else:
    st.write("GeoDataFrame is empty. Skipping map plotting.")

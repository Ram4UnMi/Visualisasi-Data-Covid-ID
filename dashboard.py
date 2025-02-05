import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load shapefile
try:
    indonesia_map = gpd.read_file("data/ne_10m_admin_0_countries.shp")
    print("Shapefile loaded successfully.")
    indonesia_map = indonesia_map[indonesia_map['ADMIN'] == 'Indonesia']
except Exception as e:
    print(f"Error loading shapefile: {e}")
    indonesia_map = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry')  # Fail-safe GeoDataFrame

# Check GeoDataFrame
if not indonesia_map.empty:
    st.write("Loaded GeoDataFrame:")
    st.write(indonesia_map.head())
else:
    st.write("GeoDataFrame is empty. Check your shapefile and filter criteria.")

# Merge and plot (example)
try:
    workplace_mobility = pd.read_csv("data/workplace_mobility.csv")
    indonesia_map = indonesia_map.merge(workplace_mobility, left_on='ADMIN', right_on='sub_region_1', how='left')

    # Plot geospatial map
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    indonesia_map.plot(
        column='workplaces_percent_change_from_baseline',
        cmap='coolwarm',
        legend=True,
        legend_kwds={'label': "Workplace Mobility Change (%)"},
        ax=ax
    )
    plt.title('Workplace Mobility Trends Across Provinces')
    st.pyplot(fig)

except Exception as e:
    st.write(f"Error during merge or plot: {e}")

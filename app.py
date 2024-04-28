import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import panel as pn
import streamlit as st

df_weather=pd.read_csv('weather.csv')
df=df_weather.copy()

#conveting to datetime format and dropping rows without dates
df=df.dropna(subset=['Päivämäärä'])
df['Päivämäärä']=pd.to_datetime(df['Päivämäärä'],format="%d/%m/%Y")
df['month']=df['Päivämäärä'].dt.month
df['year']=df['Päivämäärä'].dt.year
df['day']=df['Päivämäärä'].dt.day
df['month']=df['month'].astype(int)


my_dict={'-':np.nan,'nan':np.nan}
df['Lämpötila']=df['Lämpötila'].replace(my_dict)
df['Lämpötila']=df['Lämpötila'].astype(int,errors='ignore')


#getting today's date and corresponding month
today=date.today()
today_day=today.day
today_month=today.month

df_temp=df[(df['month']==today_month) & (df['day']==today_day)]

def get_plot(df_temp):
    fig, ax = plt.subplots(figsize=(10,10))

    temperature_df=df_temp.dropna(subset='Lämpötila')
    year=temperature_df['year']
    lampotila=temperature_df['Lämpötila'].astype(float)


    #aamulampotila
    aamu_df=df_temp.dropna(subset='Aamu lämpötila')
    year_aamu=aamu_df['year']
    aamulampotila=aamu_df['Aamu lämpötila'].astype(float)
    
    #iltalampotila
    ilta_df=df_temp.dropna(subset='Iltalämpötila')
    year_ilta=ilta_df['year']
    iltalampotila=ilta_df['Iltalämpötila'].astype(float)

    #plt.barh(year-0.2, lampotila,label='Lämpötila')
    ax=plt.bar_label(plt.barh(year_aamu+0.15, aamulampotila,0.4, label='Aamulämpötila'))
    ax=plt.bar_label(plt.barh(year, lampotila,0.4,label='Lämpötila'))
    ax=plt.bar_label(plt.barh(year_ilta-0.15, iltalampotila,0.4,label='iltalämpötila'))
    plt.legend()
    plt.grid(color='black', linewidth=1, axis='y', alpha=0.2)
    ##plt.show
    plt.close(fig) # CLOSE THE FIGURE!
    st.pyplot(fig)
    return fig

pn.extension()
bound_plot = pn.pane.Matplotlib(get_plot(df_temp))
#bound_plot=pn.pane.Matplotlib(bound_plot)
pn.template.MaterialTemplate(
    site="Panel",
    title="Getting Started App",
    main=[bound_plot],
).servable();




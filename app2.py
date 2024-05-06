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
df_month=df[df['month']==today_month]

def get_month(month):
    dict_m={1:'Tammikuu',2:'Helmikuu',3:'Maaliskuu',4:'Huhtikuu',5:'Toukokuu',6:'Kesäkuu',7:'Heinäkuu',8:'Elokuu',9:'Syyskuu'
           ,10:'Lokakuu',11:'Marraskuu',12:'Joulukuu'}
    return dict_m[month]

def temperature(row):
    if row['Lämpötila']is np.nan:
        aamu=float(row['Aamu lämpötila'])
        ilta=float(row['Iltalämpötila'])
        value=(aamu + ilta)/2
    else:
        value= float(row['Lämpötila'])
    return value



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

def get_plot_month(df_month):
    #testing
    fig = plt.figure()
    fig.set_figheight(30)
    fig.set_figwidth(15)

    ax1 = plt.subplot2grid(shape=(5, 3), loc=(1, 0), colspan=4)
    ax2 = plt.subplot2grid(shape=(5, 3), loc=(2, 0), colspan=4)
    ax3 = plt.subplot2grid(shape=(5, 3), loc=(3, 0), colspan=4)
    ax4 = plt.subplot2grid(shape=(5, 3), loc=(4, 0), colspan=4)
    #ax5 = plt.subplot2grid(shape=(2, 3), loc=(1, 0), colspan=3)
    #########
    
    #df_month_line=df_month[df_month['year']<2014]
    df_month_line=df_month

    df_month_line.loc[:,'avg_temp']=df_month_line.apply(temperature,axis=1)
    df_month_line_nona=df_month_line.dropna(subset='avg_temp')
    #fig, ax = plt.subplots(nrows=4, ncols=1,figsize=(10,10))
    #month_temp_df=df_month_line.dropna(subset='Lämpötila')
    #day=month_temp_df['day']
    #daily_temp=month_temp_df['Lämpötila'].astype(float)
    year_list=df_month_line_nona['year'].unique()
    day_list=df_month['day'].unique()
    temperature_min=int(df_month_line_nona['avg_temp'].min())
    temperature_max=int(df_month_line_nona['avg_temp'].max())
    y_values=range(temperature_min,temperature_max)

    for i in year_list:
        if i <2000:
            x1=df_month_line_nona['day'][df_month_line_nona['year']==i]
            y1=df_month_line_nona['avg_temp'][df_month_line_nona['year']==i]
            
            X_Y_Spline = make_interp_spline(x1, y1)
            X_ = np.linspace(x1.min(), x1.max(), 500)
            Y_ = X_Y_Spline(X_)
            ax1.plot(X_, Y_, label=i)
            #ax1.plot(x1,y1,label=i)
            ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
            ax1.set_xticks(day_list)
            #plt.xticks(day_list)
            ax1.set_yticks(y_values)
            ax1.axhline(color='black')
            ax1.set_title("{} keskilämpötilat 90-luvulla".format(get_month(today_month)),fontsize=16)

            
        if 2000<=i < 2010:
            x2=df_month_line['day'][df_month_line['year']==i]
            y2=df_month_line['avg_temp'][df_month_line['year']==i]
            
            X_Y_Spline = make_interp_spline(x2, y2)
            X_ = np.linspace(x2.min(), x2.max(), 500)
            Y_ = X_Y_Spline(X_)
            ax2.plot(X_, Y_, label=i)
            #ax2.plot(x2,y2,label=i)
            ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
            ax2.set_xticks(day_list)
            #plt.xticks(day_list)
            ax2.set_yticks(y_values)
            ax2.axhline(color='black')
            ax2.set_title("{} keskilämpötilat 2000-luvulla".format(get_month(today_month)),fontsize=16)
        
        if 2010<=i < 2020:
            x3=df_month_line['day'][df_month_line['year']==i]
            y3=df_month_line['avg_temp'][df_month_line['year']==i]
            
            X_Y_Spline = make_interp_spline(x3, y3)
            X_ = np.linspace(x3.min(), x3.max(), 500)
            Y_ = X_Y_Spline(X_)
            ax3.plot(X_, Y_, label=i)
            #ax2.plot(x2,y2,label=i)
            ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
            ax3.set_xticks(day_list)
            #plt.xticks(day_list)
            ax3.set_yticks(y_values)
            ax3.axhline(color='black')
            ax3.set_title("{} keskilämpötilat 2010-luvulla".format(get_month(today_month)),fontsize=16)    
        
        if 2020<=i:
            x4=df_month_line['day'][df_month_line['year']==i]
            y4=df_month_line['avg_temp'][df_month_line['year']==i]
            
            X_Y_Spline = make_interp_spline(x4, y4)
            X_ = np.linspace(x4.min(), x4.max(), 500)
            Y_ = X_Y_Spline(X_)
            ax4.plot(X_, Y_, label=i)
            #ax2.plot(x2,y2,label=i)
            ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
            ax4.set_xticks(day_list)
            #plt.xticks(day_list)
            ax4.set_yticks(y_values)
            ax4.axhline(color='black')
            ax4.set_title("{} keskilämpötilat 2020-luvulla".format(get_month(today_month)),fontsize=16) 
    
    fig.tight_layout()
    plt.close(fig)
    #plt.show()
    st.pyplot(fig)
    return fig

pn.extension()
def page1():
    #bound_plot = pn.pane.Matplotlib(get_plot(df_temp))
    month_plot = pn.pane.Matplotlib(get_plot_month(df_month))
    #bound_plot=pn.pane.Matplotlib(bound_plot)
    kuvio=pn.template.MaterialTemplate(
        site="Panel",
        title="Getting Started App222",
        main=[month_plot],
    ).servable()
    return kuvio

def page2():
    bound_plot = pn.pane.Matplotlib(get_plot(df_temp))
    #month_plot = pn.pane.Matplotlib(get_plot_month(df_month))
    #bound_plot=pn.pane.Matplotlib(bound_plot)
    kuvio2=pn.template.MaterialTemplate(
        site="Panel",
        title="Getting Started App 2",
        main=[bound_plot],
    ).servable()
    return kuvio2

ROUTES = {
    "1": page1, "2": page2
}
pn.serve(ROUTES)

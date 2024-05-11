import pandas as pd
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import panel as pn
import streamlit as st
from scipy.interpolate import make_interp_spline



pn.extension()
def page1():
    #bound_plot = pn.pane.Matplotlib(get_plot(df_temp))
    #month_plot = pn.pane.Matplotlib(get_plot_month(df_month))
    #bound_plot=pn.pane.Matplotlib(bound_plot)
    month_plot='piirra kuvio 1'
    kuvio=pn.template.MaterialTemplate(
        site="Panel",
        title="Getting Started App222",
        main=[month_plot],
    )#.servable();
    return kuvio

def page2():
    #bound_plot = pn.pane.Matplotlib(get_plot(df_temp))
    bound_plot = 'piirra kuvio 2'
    #month_plot = pn.pane.Matplotlib(get_plot_month(df_month))
    #bound_plot=pn.pane.Matplotlib(bound_plot)
    kuvio2=pn.template.MaterialTemplate(
        site="Panel",
        title="Getting Started App 2",
        main=[bound_plot],
    )#.servable();
    return kuvio2

ROUTES = {
    "1": 'page1', "2": 'page2'
}
pn.serve(page1);
#pn.panel(ROUTES).servable();

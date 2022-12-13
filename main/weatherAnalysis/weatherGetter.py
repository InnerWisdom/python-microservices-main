import numpy as np
import matplotlib.pyplot as plt
import main

# an example graph type
def fig_barh(city):
    fig, ax = main(city)
    fig.savefig()
    plt.close(fig)
    return fig
from tqdm import tqdm

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def main():

    make_heatmaps()


def make_barplots():
    
    for kind in ["pragmatic", "hyperpragmatic"]:

        print("Operating on {} mastermind ...".format(kind))

        stats = pd.read_csv("{}_strategy_stats.csv".format(kind), index_col=0)



def make_heatmaps():

    for kind in ["pragmatic", "hyperpragmatic"]:

        print("Operating on {} mastermind ...".format(kind))

        stats = pd.read_csv("{}_strategy_stats.csv".format(kind), index_col=0)

        for value, vmin, vmax in zip(["mean_rounds", "mean_utt_Listener-Win", "mean_utt_many"], [3.0, 0.8, 0.0], [6.0, 1.0, 1.0]):

            matrix = condense_strategies(stats, value)
            
            ax = sns.heatmap(matrix, cmap="inferno", vmin=vmin, vmax=vmax)

            ax.set_title("{} of {} Mastermind\n".format(titlelize(value), titlelize(kind))) 
            ax.set_xlabel("Listener Strategy")
            ax.set_ylabel("Speaker Strategy")

            plt.tight_layout()

            plt.savefig("plots/{}_{}.png".format(value, kind))
            plt.clf()


def titlelize(text):

    text = " ".join(text.split("_"))
    text = " ".join([capfirst(word) for word in text.split() if word != "utt"])

    return text


def capfirst(word):

    chars = list(word)
    chars[0] = chars[0].upper()

    return "".join(chars)


def condense_strategies(df, vcol):

    strategies = ["greedyUncoop", "stochasticUncoop", "stochasticCoop", "greedyCoop"]

    matrix = pd.DataFrame(index=strategies, columns=strategies[::-1])

    for ix, (s_strat, l_strat) in enumerate(zip(df["speakerStrategy"].values, df["listenerStrategy"].values)):
        matrix.at[s_strat, l_strat] = df.iloc[ix][vcol]

    return matrix.astype(np.float32)
    

    


if __name__ == "__main__":
    main()

from tqdm import tqdm

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def main():

    print("Making heatmaps ...")
    make_heatmaps()

    print("Making barplots ...")
    make_barplots()


def make_barplots():

    colors = {
        "greedyUncoop": "blue",
        "stochasticUncoop": "yellow",
        "stochasticCoop": "green",
        "greedyCoop": "red"
    }
    
    for kind in ["pragmatic", "hyperpragmatic"]:

        print("Operating on {} mastermind ...".format(kind))

        stats = pd.read_csv("{}_strategy_stats.csv".format(kind), index_col=0)
        patches = [mpatches.Patch(color=c, label=s) for s, c in colors.items()]

        fig, axes = plt.subplots(4, 4, squeeze=True, figsize=(8, 8))

        l_base_pos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        s_add_pos = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for s_ix, s_strat in enumerate(stats["speakerStrategy"].unique()):
            for l_ix, l_strat in enumerate(stats["listenerStrategy"].unique()):

                base_x, base_y = l_base_pos[l_ix]
                add_x, add_y = s_add_pos[s_ix]
                ax = axes[base_x + add_x, base_y + add_y]
                
                ax.bar([0.5, 1.5, 2.5], stats.iloc[s_ix * 4 + l_ix][["mean_utt_some", "mean_utt_many", "mean_utt_none"]], color=colors[s_strat])
                ax.set_xticks([0.5, 1.5, 2.5])
                ax.set_xlim(0.0, 3.0)
                ax.set_ylim(0, 2)
                ax.set_xticklabels(["some", "many", "none"])
                ax.set_title(l_strat)
                
        plt.suptitle("{} Mastermind\nMean Utterance Frequencies by Listener Strategy\n".format(titlelize(kind)))
        plt.tight_layout(pad=3.0)
        plt.subplots_adjust(top=0.85, bottom=0.25)
        fig.legend(handles=patches, loc="lower center", title="Speaker Strategy")

        plt.savefig("plots/utterances_barplots_{}.png".format(kind.lower()))



def make_heatmaps():

    for kind in ["pragmatic", "hyperpragmatic"]:

        print("Operating on {} mastermind ...".format(kind))

        stats = pd.read_csv("{}_strategy_stats.csv".format(kind), index_col=0)

        for value, vmin, vmax in zip(["mean_rounds", "mean_utt_many"], [3.0, 0.0], [6.0, 1.0]):

            matrix = condense_strategies(stats, value)
            
            ax = sns.heatmap(matrix, cmap="inferno", vmin=vmin, vmax=vmax)

            ax.set_title("{} of {} Mastermind\n".format(titlelize(value), titlelize(kind))) 
            ax.set_xlabel("Listener Strategy")
            ax.set_ylabel("Speaker Strategy")

            plt.tight_layout()

            plt.savefig("plots/{}_{}.png".format(value.lower(), kind.lower()))
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

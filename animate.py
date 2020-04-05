from aggregate import parse_log, generate_states

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import imageio
import os

DIR_FP = "animation_data/stochastic_stochastic_beliefs"
NUM_PINS = 4
NUM_COLORS = 2


def main():

    with open(DIR_FP + "/log.txt", "r") as fh:
        log = fh.read()

    beliefs = read_beliefs(DIR_FP, NUM_PINS, NUM_COLORS)
    history = parse_log(log).set_index("round", drop=True)

    print(history)
    print(beliefs)

    make_animated_gif(history, beliefs, filename=DIR_FP.split("/")[-1])



def make_animated_gif(history, beliefs, filename):

    state_labels = np.array(beliefs.columns.values)
    state_labels[list(set(range(len(beliefs.columns))) - {0, 5, 10, 15})] = ""

    true_state_ix = np.where(beliefs.columns == history["prediction"].values[-1])[0][0]

    imgs = []

    for rnd in history.index:

        fig, ax = plt.subplots()
        
        x = np.arange(len(beliefs.columns))
        current_prediction_ix = np.where(beliefs.columns == history.loc[rnd]["prediction"])[0][0]

        colors = ["b"] * len(beliefs.columns)
        colors[true_state_ix ] = "r"
        colors[current_prediction_ix] = "g"

        ax.bar(x, height=beliefs.loc[rnd].values, tick_label=state_labels, color=colors)

        ax.set_ylim(0.0, 1.0)
        ax.set_xlabel("State")
        ax.set_ylabel("Probability")
        ax.set_title("Round {}: Utterance '{}' ".format(rnd, history.loc[rnd]["utterance"]))

        belief_patch = mpatches.Patch(color="b", label="Listener Belief")
        prediction_patch = mpatches.Patch(color="g", label="Listener Prediction")
        true_state_patch = mpatches.Patch(color="r", label="True State")

        ax.legend(handles=[belief_patch, prediction_patch, true_state_patch], loc="upper left")

        fig.savefig("plots/anim_{}_{}.png".format(filename, rnd))
        img = imageio.imread("plots/anim_{}_{}.png".format(filename, rnd))
        imgs.append(img)

        plt.clf()

    imageio.mimsave(filename + ".gif", imgs, fps=1)



def read_beliefs(dir_fp, num_pins, num_colors):

    rows = []
    rnd = 1
    fn = "belief_{}.csv".format(rnd)

    while fn in os.listdir(dir_fp):
        rows.append(pd.read_csv(dir_fp + "/" + fn).iloc[0])
        rnd += 1
        fn = "belief_{}.csv".format(rnd)

    df = pd.DataFrame(rows)
    df["round"] = range(1, len(rows) + 1)

    return df.fillna(value=0).set_index("round", drop=True)

if __name__ == "__main__":
    main()

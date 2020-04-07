""" Script to aggregate statistics about strategies in WebPPL Mastermind simulations. """

from itertools import product
from tqdm import tqdm

import pandas as pd
import subprocess
import argparse
import os


def main():

    parser = argparse.ArgumentParser(description="Aggregates statistics about strategies in WebPPl Mastermind simulations.")

    parser.add_argument("script_fp", type=str, help="Path to a WebPPL Mastermind simulation script.")
    parser.add_argument("--num_pins", type=int, default=4, help="Number of pins in a Mastermind game state (>= 4).")
    parser.add_argument("--num_colors", type=int, default=2, help="Number of colors in a Mastermind game state (>= 2).")

    args = parser.parse_args()

    prefix = args.script_fp.split("/")[-1].split("_")[0]

    print("Aggregating strategy statistics for {} Mastermind simulation with numPins {} and numColors {} ...".format(prefix, args.num_pins, args.num_colors))
    res = run_all_strategies(args.script_fp, args.num_pins, args.num_colors, prefix)

    filename = "{}_strategy_stats.csv".format(prefix)
    print("Exporting results to {} ...".format(filename))
    res.to_csv(filename)


def run_all_strategies(script_fp, num_pins, num_colors, prefix):
    """ Runs all strategy combinations on all states. """

    os.makedirs("statistics", exist_ok=True)

    rows = []

    for speaker_strategy in ["stochasticCoop", "stochasticUncoop", "greedyCoop", "greedyUncoop"]:
        for listener_strategy in ["stochasticCoop", "stochasticUncoop", "greedyCoop", "greedyUncoop"]:

            params = {
                "numPins": num_pins,
                "numColors": num_colors,
                "speakerStrategy": speaker_strategy, 
                "listenerStrategy": listener_strategy
            }

            filepath = "statistics/{}_{}_{}_{}_{}.csv".format(prefix, num_pins, num_colors, speaker_strategy, listener_strategy).lower()

            if os.path.exists(filepath):
                stats = pd.read_csv(filepath, index_col=0)
            else:
                stats = run_all_states(script_fp, params)
                stats.to_csv(filepath)
            
            info = {"mean_rounds": stats["n_rounds"].mean(), **{"mean_" + col: stats[col].mean() for col in stats.columns if col.startswith("utt")}}
            rows.append({**info, **params})

    return pd.DataFrame(rows).fillna(value=0)
                

def run_all_states(script_fp, params):
    """ Runs a parameter setting on all states. """

    all_states = generate_states(params["numPins"], params["numColors"])
    
    rows = []

    print("Running {} possible states with parameters {} ...".format(len(all_states), params))

    for state in tqdm(all_states):

        state_params = {**params, "trueState": state}
        history = call(script_fp, state_params)

        info = condense_history(history)
        rows.append({**info, **params})

    return pd.DataFrame(rows).fillna(value=0)



def call(script_fp, params):
    """ Calls a WebPPL Mastermind script. """

    args = ["--"] + " ".join(["--{} {}".format(key, value) for key, value in params.items()]).split()

    process = subprocess.run(["webppl", script_fp] + args, stdout=subprocess.PIPE)
    output = process.stdout.decode("utf-8")

    history = parse_log(output)

    return history


def parse_log(log):
    """ Parses a Mastermind log into a history of rounds. """

    lines = log.split("\n")
    rounds = []
    
    for ix in range(len(lines) // 3):

        r_ix = ix * 3

        round_info = {
            "round": ix + 1,
            "n_beliefs": int(lines[r_ix].split()[4]),
            "prediction": lines[r_ix + 1].split()[2],
            "utterance": lines[r_ix + 2].split()[2]
        }

        rounds.append(round_info)

    return pd.DataFrame(rounds)


def condense_history(history):
    """ Extracts relevant statistics from a Mastermind game history. """
    return {"n_rounds": len(history.index), **{"utt_" + key: value for key, value in history.utterance.value_counts().astype(int).iteritems()}}


def generate_states(num_pins, num_colors):
    """ Generates all possible Mastermind states for a pin and color combination. """
    return ["s" + "".join(str(c) for c in comb) for comb in product(*([range(num_colors)] * num_pins))]


if __name__ == "__main__":
    main()


# mastermind
Meta-Analysis of a Pragmatic Mastermind Simulation in WebPPL.

Project for the course "Computational Pragmatics" in WS 2019/20 at Osnabrück University by mpoemsl and rakrueger.

The underlying models are loosely based on:  
[Michael C. Frank and Noah D. Goodman. Predicting pragmatic reasoning in language games. *Science*, 336(6084):998, 2012.](http://langcog.stanford.edu/papers/FG-science2012full.pdf)


## Overview

There are two Mastermind simulation scripts in this project, `pragmatic_mastermind.wppl` and `hyperpragmatic_mastermind.wppl`. You can learn more about the distinction between the two in the project slides `mastermind_presentation.pdf`. 

There are also two meta-analysis scripts in this project, `aggregate.py` and `visualize.py`. `aggregate.py` runs multiple simulations for all possible true states with different parameters, stores the protocols of the runs in `protocols/` and a summary in a file with the suffix `_strategy_stats.csv`. `visualize.py` generates plots from the aggregated statistics and stores them in `plots/`.


## Installation

The Mastermind simulation runs in WebPPL, a probabilistic programming language embedded in Javascript. Installation instructions to run WebPPL locally can be found [here](https://webppl.readthedocs.io/en/master/installation.html). The meta-analysis scripts require Python 3 and the packages listed in `requirements.txt`, which are best installed with `pip install -r requirements.txt`.


## Usage

To run a Mastermind simulation script, run `webppl NAME_OF_SCRIPT -- --numPins NUM_PINS --numColors NUM_COLORS --trueState TRUE_STATE --speakerStrategy SPEAKER_STRATEGY --listenerStrategy LISTENER_STRATEGY`, where capitalized strings are hyperparameters chosen by you that have to be formatted as follows:

* `NAME_OF_SCRIPT`: One of `pragmatic_mastermind.wppl`, `hyperpragmatic_mastermind.wppl`
* `NUM_PINS`: Theoretically any integer greater than 3, practically only 4 and 5 are realistic due to compuational costs
* `NUM_COLORS`: Theoretically any integer greater than 1, practically only 2 and 3 are realsitic due to computational costs
* `TRUE_STATE`: A valid true state congruent with the `NUM_PINS` and `NUM_COLORS` parameters preceded by the character `s`, e.g. `s0010` for `NUM_PINS=4` and `NUM_COLORS=2`
* `SPEAKER_STRATEGY`: Selection strategy to be used by the speaker, one of `greedyUncoop`, `stochasticUncoop`, `stochasticCoop`, `greedyCoop`
* `LISTENER_STRATEGY`: Selection strategy to be used by the listener, one of `greedyUncoop`, `stochasticUncoop`, `stochasticCoop`, `greedyCoop`

To run `aggregate.py`, run `python aggregate.py SCRIPT_FILEPATH`, where `SCRIPT_FILEPATH` is the path to the Mastermind simulation script you want to use. To learn more about possible parameters for `aggregate.py`, run `python aggregate.py -h`.

To run `visualize.py`, run `python visualize.py`. 


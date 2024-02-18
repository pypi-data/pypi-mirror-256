"""
Hyperparameter tuner for tinyllama using Bayesian implementation of a noiseless Gaussian Process using STAN.
"""

import os
import sys
from copy import deepcopy
from itertools import islice, product
from typing import TextIO

import numpy as np
import pandas as pd
import stan
import torch
from scipy.stats import qmc
from tqdm import tqdm

from ..diagnosis import Diagnose
from ..models import Llama
from ..training import TrainConfig, Trainer


def generate_matrix(arrays, num_combinations):
    # generate all possible combinations of elements from the arrays
    combinations = product(*arrays)

    # create a set to store unique combinations
    unique_combinations = set()

    # iterate over the combinations and add unique ones to the set
    for combo in combinations:
        if len(set(combo)) == len(combo):  # Check for uniqueness
            unique_combinations.add(combo)

    # convert the set of unique combinations back to a list of lists
    matrix = [list(combo) for combo in unique_combinations]

    # returns the specific number of combinations
    matrix = list(islice(matrix, num_combinations))

    return matrix, len(matrix)


def generate_integer_samples(lower_bound, upper_bound, max_num_eval_samples):
    M = len(upper_bound)

    int_params = []
    for i in range(M):
        int_param = np.arange(lower_bound[i], upper_bound[i] + 1)
        int_params += [int_param]

    int_samples, num_eval_samples = generate_matrix(int_params, max_num_eval_samples)

    return np.array(int_samples), num_eval_samples


# redirects output streams
def redirect_streams(stdout: TextIO, stderr: TextIO):
    streams = (sys.stdout, sys.stderr)
    sys.stdout = stdout
    sys.stderr = stderr
    return streams


# reads the STAN model
script_directory = os.path.dirname(os.path.realpath(__file__))
with open(script_directory + "/gptuner.stan", "r") as file:
    gptuner_stan = file.read()


def process_results(
    results: stan.fit.Fit,
    X_train: np.ndarray,
    Y_train: np.ndarray,
    X_test: np.ndarray,
    N_val: int,
    hyperparam_to_tune: list[str],
):
    """
    Process results and plots a 3D plot with the mean, 25% and 75% percentiles.

    :param results: Stan output result
    :type model: Fit object
    :param X_train: Training samples for noiseless GP
    :type X_train: List
    :param Y_train: Loss samples for noiseless GP
    :type X_train: List
    :param X_test: Test samples for noiseless GP
    :type X_test: List
    """

    # retrieving results
    df_results = results.to_frame().describe().T
    Y_test_mean = df_results["Y_test.1" : "Y_test." + str(N_val)]["mean"].values
    Y_test_25qtl = df_results["Y_test.1" : "Y_test." + str(N_val)]["25%"].values
    Y_test_75qtl = df_results["Y_test.1" : "Y_test." + str(N_val)]["75%"].values

    # stacking matrices for X_train & X_test
    train_matrix = np.column_stack((X_train, Y_train))
    eval_matrix = np.column_stack((X_test, Y_test_25qtl, Y_test_mean, Y_test_75qtl))

    # creating datafranes for X_train & X_test
    train_df = pd.DataFrame(train_matrix, columns=hyperparam_to_tune + ["Y_train"])
    eval_df = pd.DataFrame(
        eval_matrix, columns=hyperparam_to_tune + ["Y_25qtl", "Y_mean", "Y_75qtl"]
    )

    return train_df, eval_df


class GPTuneConfig:
    num_training_samples: int
    l_bounds: list[int]
    u_bounds: list[int]
    hyperparams_to_tune: list[str]
    max_num_evaluations: int

    def __init__(self, **kwargs):
        try:
            self.num_training_samples = kwargs.pop("num_training_samples")
            self.l_bounds = kwargs.pop("l_bounds")
            self.u_bounds = kwargs.pop("u_bounds")
            self.hyperparams_to_tune = kwargs.pop("hyperparams_to_tune")
            self.max_num_evaluations = kwargs.pop("max_num_evaluations")
        except KeyError as e:
            print(f"Missing keyword argument {e}=...in GPTuneConfig")

    def __getitem__(self, name: str):
        return self.__getattribute__(name)

    def __setitem__(self, name: str, value: int):
        self.__setattr__(name, value)


class GPTune(Diagnose):
    def __init__(self, GPTUNE_CONFIG: GPTuneConfig):
        self.GPTUNE_CONFIG = GPTUNE_CONFIG

    def run(
        self,
        model: Llama,
        tokens: torch.Tensor,
        TRAIN_CONFIG: TrainConfig,
        num_stan_samples: int = 50,
    ):
        N_train, M = (
            self.GPTUNE_CONFIG["num_training_samples"],
            len(self.GPTUNE_CONFIG["hyperparams_to_tune"]),
        )

        # get latin hypercube distributed samples for hyperparameters
        sampler = qmc.LatinHypercube(d=M)
        sample = sampler.random(n=N_train)

        # samples should be intergers
        X_train = qmc.scale(
            sample, self.GPTUNE_CONFIG["l_bounds"], self.GPTUNE_CONFIG["u_bounds"]
        ).astype(int)

        # training & retrieve validation error for each sampled hyperparameter
        Y_train = np.array([])
        for hyperparam in tqdm(X_train, total=N_train, colour="blue"):
            model_clone = deepcopy(model)

            for index, hyperparam_to_tune in enumerate(
                self.GPTUNE_CONFIG["hyperparams_to_tune"]
            ):
                if hyperparam_to_tune in [
                    "context_window",
                    "emb_dim",
                    "n_heads",
                    "n_blocks",
                ]:
                    setattr(model_clone, hyperparam_to_tune, hyperparam[index])

                elif hyperparam_to_tune in ["epochs", "batch_size", "log_size"]:
                    TRAIN_CONFIG[hyperparam_to_tune] = hyperparam[index]

                else:
                    raise ValueError(
                        f"The parameter {hyperparam_to_tune} is inexistant"
                    )

            Y_train = np.append(
                Y_train,
                float(
                    Trainer(TRAIN_CONFIG).run(model_clone, tokens, hide_progress=True)[
                        -1
                    ]["train"]
                ),
            )

        # generating test samples for hyperparameters
        N_val = self.GPTUNE_CONFIG["max_num_evaluations"]

        X_test, N_val = generate_integer_samples(
            self.GPTUNE_CONFIG["l_bounds"], self.GPTUNE_CONFIG["u_bounds"], N_val
        )

        data = {
            "N_train": N_train,
            "N_val": N_val,
            "M": M,
            "X_train": X_train,
            "X_test": X_test,
            "Y_train": Y_train,
        }

        posterior = stan.build(gptuner_stan, data=data)

        # redirects output streams to devnull
        dev_null = open(os.devnull, "w")
        stdout, stderr = redirect_streams(dev_null, dev_null)

        fit_results = posterior.sample(num_chains=4, num_samples=num_stan_samples)

        # redirects them back
        _, _ = redirect_streams(stdout, stderr)
        dev_null.close()

        results = process_results(
            fit_results,
            X_train,
            Y_train,
            X_test,
            N_val,
            self.GPTUNE_CONFIG["hyperparams_to_tune"],
        )

        return results

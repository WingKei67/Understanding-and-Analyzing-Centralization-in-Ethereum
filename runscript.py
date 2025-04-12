# Description: This file is used to run the simulation for the auction model. It uses the main.py file to run the simulation and saves the results to a csv file.

import random
import pandas as pd
from collections import Counter
import os
from main import Auction

def generate_strategies(manual_values=None):
    if manual_values:
        return manual_values

    strategy_labels = ['N', 'A', 'L', 'S', 'B']

    # Randomly assign each of the 8 players to a strategy
    assigned = [random.choice(strategy_labels) for _ in range(8)]

    # Count how many players got each strategy
    strategies = {k: 0 for k in strategy_labels}
    strategies.update(Counter(assigned))

    return strategies

def run_simulation(strategies, delay, num_simulations):
    sim_results = pd.DataFrame(columns=['winning_agent', 'winning_bid_value', 'winner_aggregated_signal', 'signal_max','Profit', 'Probability', 'True Profit', 'efficiency', 'auction_time', 'N', 'A', 'L', 'S', 'B', 'Delay'])  # Add 'Aggregated Signal Max' to columns
    for _ in range(num_simulations):
        N, A, L, S, B = strategies.values()
        model = Auction(N, A, L, S, B, rate_public_mean=0.0905, rate_public_sd=0.0371, rate_private_mean=0.0487, rate_private_sd=0.0241,
                        T_mean=12, T_sd=0, delay=delay, custom=True)
        for i in range(int(model.T * 100)):
            model.step()
        time_step = int(model.T * 100) - 1
        sim_results.loc[len(sim_results)] = [model.winning_agents[-1:][0], model.max_bids[-1:][0],model.winner_aggregated_signal, model.aggregated_signal_max,
                                             model.winner_profit, model.winner_probability, model.winner_trueprofit, model.auction_efficiency,time_step, N, A, L, S, B, delay]

    return sim_results

manual_values = None
num_simulations = 20
num_runs = 500
all_results = pd.DataFrame(columns=['Fixed Strategy', 'Chances of Winning', 'Mean Winning Bid Value', 'Delay'])

for run in range(num_runs):
    all_sim_results = []
    for fixed_strategy in [None]:
        print('Run ' + str(run))
        # for delay in range (1,11):
        #     print('Delay ' + str(delay))
        strategies = generate_strategies(manual_values)
        sim_results = run_simulation(strategies, 10, num_simulations)
        all_sim_results.append(sim_results)

    concatenated_sim_results = pd.concat(all_sim_results, ignore_index=True)
    filename = f'test3.csv'
    if os.path.exists(filename):
        concatenated_sim_results.to_csv(filename, mode='a', header=False, index=False)
    else:   
        # If the file doesn't exist, write the header
        concatenated_sim_results.to_csv(filename, header=True, index=False)
    print(f'Simulation results saved to {filename}')
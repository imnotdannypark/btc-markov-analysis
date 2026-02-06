# Markov Chain based Bitcoin Transaction Network Analysis
This project models a 7-node Bitcoin transaction network using Markov Chains to analyze fund flow dynamics and quantify the influence of centralized exchanges.

## Project Overview
* Project Type: MATH 2270 Linear Algebra

## Project Goal
To numerically quantify the systemic influence of centralized exchanges on fund flow dynamics by modeling a 7-node Bitcoin transaction network using Markov Chains.

## Technologies
* Language: Python
* Libraries: NumPy

## Methodology
* Mathematical Modeling: Built a stochastic transition matrix for a 7-node network representing wallets and exchanges.
* Steady-State Analysis: Computed the stationary distribution to identify dominant nodes in the network.
* Monte Carlo Simulation: Validated analytical solutions through a 10,000-trial simulation using Python.

## Key Finding
* Identified that a specific centralized exchange node commands 24.1% of the long-term influence within the modeled network.
* Confirmed an exact alignment between theoretical Markov Chain predictions and simulated Monte Carlo data, proving the robustness of the stochastic model.

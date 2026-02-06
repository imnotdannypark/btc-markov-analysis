# Markov Chain based Bitcoin Transaction Network Analysis
This project is an advanced evolution of a linear algebra coursework assignment, upgraded to model a realistic, large-scale Bitcoin transaction network. Moving beyond a static 7-node model, this project simulates over 100,000 transactions across 1,000+ nodes to analyze fund flow dynamics and systemic influence using Markov Chains and the PageRank algorithm.

## Project Overview
* Project Type: MATH 2270 Linear Algebra -> Enhanced Personal Project
* Expanded the network from 7 manual nodes to 1,005 nodes (1,000 Wallets + 5 Major Exchanges) with 100,000 generated transactions.
* Applied Pareto Distribution to wallet generation to mimic real-world wealth inequality and transaction patterns.

## Technologies
* Language: Python
* Libraries: NumPy, Pandas, Matplotlib

## Methodology
* Synthetic Data Generation: Constructed a transaction log using NumPy with weighted probabilities, and modeled "Whale" users using Pareto distribution weights.
* Transition Matrix Construction: Built and normalized a stochastic matrix to ensure valid probability transitions.
* PageRank Implementation: Implemented the Power Iteration method with Damping Factor to handle dangling nodes and calculate Stationary Distribution.
* Sensitivity Analysis: Visualized changes in node influence based on varying alpha values.

## Key Finding
* Exchange nodes consistently occupied the top 5 ranks, accounting for over 70% of total stationary probability mass.
* Demonstrated that the network converges to a steady state, allowing for the quantitative ranking of node importance.

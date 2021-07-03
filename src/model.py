import numpy as np
import pandas as pd
from scipy.stats import binom
import plotly.graph_objects as go
import plotly.express as px

class game():
    def __init__(self):
        """Initialize the game with two arms, each with their unique probabilities 'p' of success"""
        if np.random.choice([0,1]) == 0:
            self.p = np.array([0.5, 0.7])
        else:
            self.p = np.array([0.7, 0.5])
        self.points = {0:0, 1:0}
        self.rounds = {0:0, 1:0}
        self.priors = {0:np.ones(1000), 1:np.ones(1000)}
        self.p_grid = np.linspace(0, 1, 1000)
        self.figs = {0:go.Figure(),
                     1:go.Figure()}

    def make_bet(self, selected_arm: int, n=1):
        """Make 'n' bets on the selected arm and add points if our rng is less than the probability p"""
        selection = self.p[selected_arm]
        for i in range(n):
            if np.random.uniform() <= selection:
                self.points[selected_arm] += 1
            self.rounds[selected_arm] += 1
        self._make_figs(selected_arm)

    def score(self):
        """Share the number of points and rounds both arms"""
        return(f"points: {self.points}, rounds: {self.rounds}")

    def show_answers(self):
        """Reveal the actual underlying probabilities (p)"""
        print(self.p)

    def _make_figs(self, selected_arm):
        """
        helper function to update the plotly figures for the selected arm given. The resulting figs
        should show the old curves as 'greyed out' and the latest curve in blue.
        """
        n = self.rounds[selected_arm]
        k = self.points[selected_arm]

        # Start with uniform prior
        prob_data = binom.pmf(k=k, n=n, p=self.p_grid) # Likelihood 
        # The binom.pmf function returns the probability of k successes over n trials when the probability of success is p
        # We want to plot the likelihood of each of these models across all values of p from 0 to 1
        posterior = prob_data * self.priors[selected_arm]
        posterior = posterior/sum(posterior)
        self.priors[selected_arm] = posterior

        self.figs[selected_arm].update_traces(overwrite=True, marker_color="LightGrey", marker_opacity=0.2)
        self.figs[selected_arm].add_scatter(x=self.p_grid, y=posterior, mode='lines', marker_color='Blue')
        self.figs[selected_arm].update_layout(title=f"{k} successes out of {n} trials")
        self.figs[selected_arm].update_layout(showlegend=False)

    def show_fig(self, selected_arm):
        """one-liner to return the figure object of the selected arm for feeding the dashboard"""
        return self.figs[selected_arm]
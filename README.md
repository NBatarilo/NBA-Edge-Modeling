# NBA Edge Modeling

Python implemented Logistic Regression Model used to predict probability of the home team winning an NBA game. This is then compared against posted sports book odds to calculate an estimated edge, which can subsequently be used to make efficient bets.

Currently uses basic and advanced box score statistics, which are then averaged and normalized to predict future performance. Superfluous variables are eliminated through multicollinearity analysis (VIF), with the final model being chosen through a cross validated grid search. 


## Future Work
* Incorporate playoff games (currently only regular season, which have higher variance)
* Set up pipeline to predict odds of upcoming games
* Set up pipeline to import sports book odds and calculate edge
* Implement ELO score as an attribute


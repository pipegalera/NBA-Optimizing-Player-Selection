# Creating Dream Teams under the Salary Cap:  NBA PlayerSelection Optimization

How can teams use computer modeling to increase their winning rate? This project-paper proposes optimizing NBA player selection based on stats and salary of the players. I use a linear regression model to estimate the weight of offensive and defensive stats on winning an NBA game. Then, I use these weights to set up an optimization problem to select the best NBA line-up to achieve two main goals: i) Maximum wins under the 2018 salary cap ii) Minimum team salary that match the win threshold of the last league champion.

The project applies:

* Scrapping static and dynamic webpages with Selenium and BeautifulSoup.
* Preprocessing data with Pandas and Numpy.
* Descriptive analysis visualization with Seaborn.
* Modeling with Scikit-learn.
* Optimization with PuLP.

# Data-Exploration-Tool

Welcome to the Data Exploration Tool repo! This project was started in Summer 2022.

## Plotly / Dash

We decided to create this tool using the Plotly library, because it has all the functionality we think we will need, and it is highly customizable. Plotly is a python library that has interactive graphing, as well as interactive menu components. Plotly also has [excellent documentation](https://dash.plotly.com/installation).

Plotly is closely associated with Dash, which is a way of deploying Plotly interfaces to a website. They try to push for Dash Enterprise, their paid version which automatically hosts your Dash interface on their server. However, we believe it can be deployed just as easily using Flask and hosted on the Air Partners web server.

To get more detailed information on Plotly and Dash, read through the [tutorial](https://dash.plotly.com/installation) in the documentation linked above. It has lots of examples and copy-pasteable code to make graphs and interactive menus work. For a more detailed listing of the interactive components, look at [the Dash Core Components](https://dash.plotly.com/dash-core-components).

## Using this Repo

To try out the scripts in this repository, you will need to `pip install plotly`. Clone this repo and open up the file `dash_layout1.py`, then run it. By default, the dash interface will be running on your computer's local IP address [`127.0.0.1:8050`](`http://127.0.0.1:8050/`). Type this IP into your browser to view the interface.

Plotly comes with a 'hot-reload' feature, meaning whenever you save the file you are working in, it will automatically update the dash interface in your browser.



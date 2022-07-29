# Data-Exploration-Tool

Welcome to the Data Exploration Tool repo! This project was started in Summer 2022.

## Plotly / Dash

We decided to create this tool using the Plotly library, because it has all the functionality we think we will need, and it is highly customizable. Plotly is a python library that has interactive graphing, as well as interactive menu components. Plotly also has [excellent documentation](https://dash.plotly.com/installation).

Plotly is closely associated with Dash, which is a way of deploying Plotly interfaces to a website. They try to push for Dash Enterprise, their paid version which automatically hosts your Dash interface on their server. However, we believe it can be deployed just as easily using Flask and hosted on the Air Partners web server.

To get more detailed information on Plotly and Dash, read through the [tutorial](https://dash.plotly.com/installation) in the documentation linked above. It has lots of examples and copy-pasteable code to make graphs and interactive menus work. For a more detailed listing of the interactive components, look at the [Dash Core Components](https://dash.plotly.com/dash-core-components).

## Using Plotly

To try out the scripts in this repository, you will need to `pip install plotly`. Clone this repo and open up the file `dash_layout1.py`, then run it. By default, the dash interface will be running on your computer's local IP address [`127.0.0.1:8050`](http://127.0.0.1:8050/). Type this IP into your browser to view the interface.

Plotly comes with a 'hot-reload' feature, meaning whenever you save the file you are working in, it will automatically update the dash interface in your browser.

## Structure of this Repo

### dash_layout1.py

The main script that will run the data exploration tool is titled `dash_layout1.py`. This initializes the main page, loads the data, and creates all the graph objects. Let's take a quick look at the `__init__()` function of `Page`, the main class defined in `dash_layout1.py`:

```
def __init__(self, app, n_charts = 10) -> None:
    self.app = app

    ...

    self.outer_layout = html.Div(
        children = [self.inner_layout, self.create_sidebar()],
        id = 'outer_main',
        style = self.outer_layout_style,
    )

    ...

    self.data_importer = DataImporter()

    self.create_layout()
```

#### Breakdown of `__init__()`

```
def __init__(self, app, n_charts = 10) -> None:
    self.app = app
```

Much like if you've ever used Flask, `app` is the object that Plotly uses to display your code into a web browser. The `app` object is used to create callbacks, which cause the page to update when certain buttons are clicked.

```
    self.outer_layout = html.Div(
        children = [self.inner_layout, self.create_sidebar()],
        id = 'outer_main',
        style = self.outer_layout_style,
    )
```

This is the structure used to generate HTML elements using `dash.html` python objects. Here, a `Div` object is created. The `children` argument is the contents of the `Div`, the `style` is a dictionary of html styling properties, and the `id` is a unique string that identifies the element so it can be used in callbacks (similar to how javascript uses `getElementById()` to refer to HTML elements).

In this case, the Div holds `self.inner_layout`, which is a container for the main contents of the page, and a sidebar element which is displayed side by side with the contents.

```
self.data_importer = DataImporter()
```

This line creates a `DataImporter` object, which is defined in the file `data_importer.py`. When initialized, it loads East Boston data from a set of CSV files and performs a bit of processing. Once this object is created, it will be passed to all the graph-making functions so that the data-loading step does not need to be redone each time a graph is created.

```
    self.create_layout()
```

This function populates the contents of the page in `self.inner_layout` by modifying its `children` attribute. Basically, it creates all the graphs that will ever be displayed and then sets all of them to invisible except for the ones that appear on the starting screen. Then there are buttons (defined in `def create_dropdown()`) that will toggle the visibility of certain graphs.
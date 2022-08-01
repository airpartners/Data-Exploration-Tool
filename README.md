# Data-Exploration-Tool

Welcome to the Data Exploration Tool repo! This project was started in Summer 2022. This project and this repo will be handed off to another group of students on the Fall 2022 semester ADE team. Hence, this README is designed to give future students an insight into the structure of the code so they can continue working on it without having met with the original developers.

## Plotly / Dash

We decided to create this tool using the Plotly library, because it has all the functionality we think we will need, and it is highly customizable. Plotly is a python library that has interactive graphing, as well as interactive menu components. Plotly also has [excellent documentation](https://dash.plotly.com/installation).

Plotly is closely associated with Dash, which is a way of deploying Plotly interfaces to a website. They try to push for Dash Enterprise, their paid version which automatically hosts your Dash interface on their server. However, we believe it can be deployed just as easily using Flask and hosted on the Air Partners web server.

To get more detailed information on Plotly and Dash, read through the [tutorial](https://dash.plotly.com/installation) in the documentation linked above. It has lots of examples and copy-pasteable code to make graphs and interactive menus work. For a more detailed listing of the interactive components, look at the [Dash Core Components](https://dash.plotly.com/dash-core-components).

## Getting up and running

Start by cloning this repo. Then you will need to download some data files separately. Open up the file `my_data_directory.py` and follow the instructions in the docstring. It will guide you through making the proper file structure and downloading the raw data. You will also need to modify one line in that file and run a git command to avoid committing your changes back into this repo.

Next, you should be able to open up the file `dash_layout1.py`, then run it. It will take a little while (~1-2 minutes) to process the data (it will be faster the next time you run it). By default, the dash interface will be running on your computer's local IP address [`127.0.0.1:8050`](http://127.0.0.1:8050/). Type this IP into your browser to view the interface.

# Structure of this Repo

## dash_layout1.py

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

### Breakdown of `__init__()`

```
def __init__(self, app, n_charts = 10) -> None:
    self.app = app
```

Much like if you've ever used Flask, `app` is the object that Plotly uses to display your code into a web browser. The `app` object is used to create callbacks, which cause the page to update when certain buttons are clicked.

---

```
    self.outer_layout = html.Div(
        children = [self.inner_layout, self.create_sidebar()],
        id = 'outer_main',
        style = self.outer_layout_style,
    )
```

This is the structure used to generate HTML elements using `dash.html` python objects. Here, a `Div` object is created. The `children` argument is the contents of the `Div`, the `style` is a dictionary of html styling properties, and the `id` is a unique string that identifies the element so it can be used in callbacks (similar to how javascript uses `getElementById()` to refer to HTML elements).

In this case, the Div holds `self.inner_layout`, which is a container for the main contents of the page, and a sidebar element which is displayed side by side with the contents.

---

```
self.data_importer = DataImporter()
```

This line creates a `DataImporter` object, which is defined in the file `data_importer.py`. When initialized, it loads East Boston data from a set of CSV files and performs a bit of processing. Once this object is created, it will be passed to all the graph-making functions so that the data-loading step does not need to be redone each time a graph is created.

---

```
    self.create_layout()
```

This function populates the contents of the page in `self.inner_layout` by modifying its `children` attribute. Basically, it creates all the graphs that will ever be displayed and then sets all of them to invisible except for the ones that appear on the starting screen. Then there are buttons (defined in `def create_dropdown()`) that will toggle the visibility of certain graphs.

## graph_frame.py

This file defines the `GraphFrame` class, which is the parent class to all of the graphs that make up the tool. It is called a `GraphFrame` because it contains not only the graph in question, but also any filters, dropdown menus, and text that surround the graph and let you interact with the data.

For example, each `GraphFrame` subclass must define a function `def get_explanation()` function, which returns a chunk of `dash.html` code to display above the graph; `def get_html()`, which returns `dash.html` code containing the layout of the supporting elements (text, dropdowns, etc.); and `def add_graph_callback()`, which defines the callbacks for those elements and imbues them with the power to update the graph in question.

`GraphFrame` is a parent class for `TimeSeries` (defined in `time_series.py`), `Scatter` (`Scatterplot_final.py`), BarChartGraph (`bar_chart_graph.py`), `CalendarPlot` (`calendar_plot.py`), and `Polar` (two different versions are defined in `Polar.py` and `polar_plot_v2.py`; check which one is being used based on which of those two files is imported at the top of `dash_layout1.py`).

### Other notes on graph_frame.py

The first 200 lines or so of `graph_frame.py` define styling and chunks of `dash.html` that will be used repeatedly by `GraphFrame` subclasses.

The `__init__()` function is quite small, and just calls the  `self.get_explanation()`, `self.get_html()`, and `self.add_graph_callback()` functions on its subclasses, wrapping the resulting `dash.html` code in a Div with a special `id` so that `dash_layout1.py` knows how to turn its visibility on and off.

Arguably the most important function in this entire class is the `self.get_id()` function, which is, verbatim:

```
def get_id(self, id_str):
    return id_str + "-" + str(self.id_num)
```

This function is used to define the `id`s of pretty much every element defined inside of `GraphFrame` or one of its subclasses. The reason is that every element in the app *must* have a unique `id`, and there are close to 50 `GraphFrame` objects (most of them invisible) in the layout at once. This is solved by giving each `GraphFrame` object a unique `id_num`, which is appended to the end of every element `id` using the function `self.get_id()`.

## data_importer.py

This is the file that loads all the East Boston data and makes it available as a Pandas dataframe for making graphs. A single `DataImporter` object is created at the start of `dash_layout1.py`, and it is passed to each `GraphFrame` as one of the `__init__()` arguments. This avoids having to repeat the expensive data loading process for each graph.

When it is initialized, `DataImporter` looks for files specified in the file `csv_file_paths.py`. (If you look in that file, you will see that it imports from `my_data_directory.py`, which is the file you modified to specify the root path for the data directories).

The way `DataImporter` works is it looks first for files in the `processed/` directories. If those files do not exist, it will instead read from the raw csv files, perform some processing on them, and then save them as [parquet](https://www.upsolver.com/blog/apache-parquet-why-use) files in the proper location. The reason we use parquet files is that they take less storage space and are faster to read than CSV files; they also preserve column structure which is important for storing dataframes with nested columns, which is useful for storing multiple types of summary data (mean, median, min, max) for multiple different sensors.

The processing steps are mainly:
* Converting the data from a csv or parquet file into a Pandas dataframe
* Combining multiple dataframes into one (for example, the flight data comes in a separate file for each month; these are all concatenated together)
* Merging dataframes containing different sets of data (combining sensor data and flight data) on the same date ranges
* Calculating summary data (min, 1st quartile, median, 3rd quartile, max, and mean) for each sensor and variable over the entire date range and storing these statistics in their own file

After `DataImporter` loads and processes the data, the data can be accessed using the `get_data_by_sensor()` method, where you pass it a sensor number from 0 to 5. It also has methods `get_all_sensor_names()` and `get_stats()`.

## presets.py

This is one of the most important features of the data exploration tool, because it addresses a direct user need. This feature allows us (the developers) to pre-program several different sets of starting configurations, including which graph types to show and what the settings of all the dropdowns and filters should be. The pre-programmed ("preset") graphs are chosen to show specific insights about the data obtained through data science.

This is similar to showing someone a PDF of a few graphs created from the dataset that illustrate a point, except that 1) it is still a fully interactive tool, so people can change the settings and play with it themselves; and 2) it shows people how to use the tool to create new graphs by manipulating the dropdowns and filters.

### Defining new presets

The presets are defined inside a giant nested dictionary called `preset_scenarios`. The keys of the dictionary are the names for the different scenarios, to be displayed on the radio buttons where the presets can be selected. The nested structure looks like this (it's a dictionary of lists of tuples of dictionaries).

```
preset_scenarios = {
    "Preset 1": [
        (
            chart_1_type,
            {
                setting_names: setting_values
            }
        ),
        (
            chart_2_type,
            {
                setting_names: setting_values
            }
        ),
        ...
    ],
    "Preset 2": [ ... ],
    ...
}
```

To add another preset, just add another entry into `preset_scenarios`.


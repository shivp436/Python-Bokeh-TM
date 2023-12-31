from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap
from bokeh.palettes import Blues8
from bokeh.embed import components # to create a div and script to embed the bar into another file
import pandas as pd

# Read the CSV file
df = pd.read_csv("cars.csv")

# Sort DataFrame by 'Horsepower'
df = df.sort_values(by='Horsepower', ascending=True)  # this creates a descending sort for the hbar wrt horsepower
# df = df.sort_values(by='Horsepower', ascending=False) # this does in ascending order

# Create ColumnDataSource from data frame
source = ColumnDataSource(df)

# Car list variable for the plot
cars_list = source.data["Car"].tolist()

# Output to HTML file
output_file("index.html")

# Reverse the color palette
reversed_palette = list(reversed(Blues8)) # otherwise it starts from light to dark, we want dark to light

# Add plot
p = figure(
    y_range=cars_list,
    width=800,
    height=600,
    title="Cars vs HP",
    x_axis_label="Horsepower",
    tools="pan, box_select, zoom_in, zoom_out, save, reset",
)

# Add glyph
p.hbar(
    y="Car",
    right="Horsepower",
    left=0,
    height=0.5,
    fill_color = factor_cmap(
        'Car',
        palette=reversed_palette,
        factors=cars_list
    ),
    fill_alpha=0.9,
    source=source,
    # legend = 'Car' # gives key error, outdated key
)

# add legend
# p.legend.orientation='vertical'
# p.legend.location = 'top_right'
# p.legend.label_text_font_size = '10px'

# Add tooltip on hover
hover = HoverTool()
hover.tooltips = """
    <div>
        <h3>@Car</h3>
        <div><strong>Price: </strong>@Price</div>
        <div><strong>HP: </strong>@Horsepower</div>
        <div><img src="@Image" alt="" width="200" /></div>
    </div>
"""

p.add_tools(hover)

# Render output
save(p)

# print out div and script
script, div = components(p)
print(div)
print(script)
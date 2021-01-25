from math import pi
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.layouts import row, column
from bokeh.transform import factor_cmap, cumsum
from bokeh.palettes import Blues256, linear_palette, Viridis256
from bokeh.models import GlyphRenderer, Circle, Spacer
from bokeh.embed import components
from bokeh.io import show

import pandas as pd

# constants
IPC = 'G'
YEAR_APC_WIDTH = 900
YEAR_HEIGHT = 300
APC_HEIGHT = 350
COUNTRY_WIDTH = 500
ORG_WIDTH = 400
COUNTRY_ORG_HEIGHT = 350
WORD_HEIGHT = 350
WORD_WIDTH = 500
WORD_CLOUD_WIDTH = 400
YEAR = 'data/year_ipc_count.csv'
APPLICANTS = 'data/applicants.csv'
WORD = 'data/word_top.csv'
WORD_IMG = 'data/word_img.csv'
COUNTRY = 'data/country_top10.csv'
ORG = 'data/org.csv'

# data
df_year = pd.read_csv(YEAR)
df_apc = pd.read_csv(APPLICANTS)
df_org = pd.read_csv(ORG)
for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'default']:
    df_org[i] = df_org[i + '_count'] / df_org[i + '_count'].sum() * 2 * pi
df_org['color'] = linear_palette(Viridis256, 12)
df_word = pd.read_csv(WORD)
df_country = pd.read_csv(COUNTRY)
df_word_img = pd.read_csv(WORD_IMG)

# space
space0 = Spacer(width=YEAR_APC_WIDTH, height=20)
space1 = Spacer(width=YEAR_APC_WIDTH, height=10)
space2 = Spacer(width=YEAR_APC_WIDTH, height=10)
space3 = Spacer(width=YEAR_APC_WIDTH, height=20)
space4 = Spacer(width=10, height=COUNTRY_ORG_HEIGHT)
space5 = Spacer(width=10, height=COUNTRY_ORG_HEIGHT)

# time series
p_year = figure(plot_width=YEAR_APC_WIDTH, plot_height=YEAR_HEIGHT, tools='pan,wheel_zoom,save,reset',
                toolbar_location='above')
p_year.title.text = 'year & IPC count'
source_year = ColumnDataSource(df_year)
p_year.line(source=source_year, x='year', y=IPC, line_width=1.8, color='#05445E', alpha=0.4)
hover = HoverTool(mode='vline')
hover.tooltips = [('Year', '@year'), ('Count', f'@{IPC}')]
p_year.add_tools(hover)

# top 10 countries
source_country = ColumnDataSource(df_country)
dot_country = figure(title="top 10 country ranking", tools='pan,wheel_zoom,save,reset', toolbar_location='above',
                     y_range=source_country.data[f'country_{IPC}'], plot_height=COUNTRY_ORG_HEIGHT,
                     plot_width=COUNTRY_WIDTH)
dot_country.ygrid.grid_line_color = None

d = dot_country.segment(0, f'country_{IPC}', IPC, f'country_{IPC}', line_width=2, line_color="#7f7f7f", line_alpha=0.6,
                        source=source_country)
c = dot_country.circle(x=IPC, y=f'country_{IPC}', size=12, fill_color="#0ba28d", fill_alpha=1, line_color="#0ba28d",
                       line_width=2, source=source_country)

grs = c.select(dict(type=GlyphRenderer))
for glyph in grs:
    if isinstance(glyph.glyph, Circle):
        circle_renderer = glyph

hover_country = HoverTool(renderers=[circle_renderer], mode='hline')
hover_country.tooltips = f'@country_{IPC}: @{IPC}'
dot_country.add_tools(hover_country)

# organizations distribution
source_org = ColumnDataSource(df_org)
p_org = figure(plot_height=COUNTRY_ORG_HEIGHT, plot_width=ORG_WIDTH, title='organizations distribution',
               toolbar_location='above', tools=['pan', 'wheel_zoom', 'save', 'reset', 'hover'],
               tooltips=f'@org: @{IPC}_count',
               x_range=(-0.52, 0.7))
p_org.wedge(x=0, y=1, radius=0.4, start_angle=cumsum(IPC, include_zero=True), end_angle=cumsum(IPC),
            line_color="white", fill_color='color', fill_alpha=0.5, legend_field='org_abr', source=source_org)
p_org.axis.axis_label = None
p_org.axis.visible = False
p_org.grid.grid_line_color = None
p_org.legend.label_text_font_size = '6pt'
p_org.legend.border_line_color = None

# applicants
source_apc = ColumnDataSource(df_apc)
x = source_apc.data[f'applicant_{IPC}_abr']
y = source_apc.data[IPC]
p_apc = figure(x_range=x.tolist(), x_axis_label='', plot_width=YEAR_APC_WIDTH, plot_height=APC_HEIGHT,
               tools='pan,wheel_zoom,save,reset',
               toolbar_location='above',
               title='top 15 applicants & patents count')
p_apc.xgrid.grid_line_color = None
p_apc.vbar(source=source_apc, x=f'applicant_{IPC}_abr', top=IPC, width=0.4,
           fill_color=factor_cmap(
               f'applicant_{IPC}_abr',
               palette=linear_palette(Blues256, 20),
               factors=x
           ),
           fill_alpha=0.6,
           color=None
           )

hover_apc = HoverTool(mode='vline')
hover_apc.tooltips = f'@applicant_{IPC}: @{IPC}'
p_apc.add_tools(hover_apc)

# word cloud
source_word_img = ColumnDataSource(df_word_img)
p_word = figure(title='word cloud', plot_height=WORD_HEIGHT, plot_width=WORD_CLOUD_WIDTH, tools='save',
                toolbar_location='above')
p_word.image_url(source_word_img.data[IPC], x=0, y=1, w=2, h=1, global_alpha=0.6)

p_word.axis.visible = False
p_word.xgrid.grid_line_color = None
p_word.ygrid.grid_line_color = None

# top 10 words
factors = df_word[f'word_{IPC}'].tolist()
x = df_word[IPC].tolist()
source_word = ColumnDataSource(df_word)

dot = figure(title="top 10 word ranking", tools='pan,wheel_zoom,save,reset', toolbar_location='above',
             y_range=factors, plot_height=WORD_HEIGHT, plot_width=WORD_WIDTH)
dot.ygrid.grid_line_color = None
dot.segment(0, f'word_{IPC}', IPC, f'word_{IPC}', line_width=2, line_color="#7f7f7f", line_alpha=0.6,
            source=source_word)
dot.circle(x=IPC, y=f'word_{IPC}', size=12, fill_color="#0ca29b", fill_alpha=1, line_color="#0ca29b", line_width=2,
           source=source_word)

hover_word = HoverTool(mode='hline')
hover_word.tooltips = f'"@word_{IPC}": @{IPC}'
dot.add_tools(hover_word)

# layout
layout = column(space0, p_year, space1, row(dot_country, space4, p_org), space2, p_apc, space3, row(dot, space5, p_word))
show(layout)

script, div = components(layout)
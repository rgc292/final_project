'''Module with plotting functions and the Plotter class

This module handles all the plotting for the web app.
'''

import cStringIO
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt
import numpy as np

# Use seaborn if installed
# Seaborn may be hard to install in some systems, so we make it optional
try:
    import seaborn as sns
    # Use seaborn styles to make prettier plots
    sns.set_style('white')
except ImportError:
    pass



def fig_to_svg(figure=None):
    '''Convert the matplotlib figure to SVG data, to be included in a web page'''
    # If figure is not set, get current figure
    if figure is None:
        figure = plt.gcf()

    # Use a StringIO stream/buffer to store the figure, rather than writing
    # to a file on disk
    io_buffer = cStringIO.StringIO()
    figure.savefig(io_buffer, format='svg')
    svg_data = io_buffer.getvalue()
    io_buffer.close()

    return svg_data


def init_fig():
    '''Initialize a figure object'''
    fig = plt.figure()
    fig.set_size_inches(4, 4)
    fig.set_tight_layout(True)
    return fig



class Plotter(object):
    '''Class to handle plotting data'''

    def __init__(self, data, label=''):
        '''Constructor. Initialize the data, and set a label to be added to titles'''
        self.data = data
        self.label = label


    def price_per_unit_histogram(self):
        '''Plot a histogram of price-per-unit in 2015'''
        fig = init_fig()

        self.data.loc[self.data.year == 2015, 'sale_price_per_res_unit'].hist(xrot=90)

        plt.xlabel("Sale Price")
        plt.ylabel("Sales")
        plt.title("Distribution of Sale Price per Residential Unit\n%s" % self.label, y=1.05)

        return fig_to_svg(fig)


    def sales_volume_bar_chart(self, groupby='building_type',
                               groupbylabel="Building Type"):
        '''Plot a bar chart of sales volume by a groupby variable.

        groupby variable is used to create different bars as subsamples.
        groupbylabel is a descriptive string to include for the title and axis label.'''
        fig = init_fig()

        # Get the sum of residential units over the groupby groups
        units = self.data.loc[self.data.year == 2015].groupby(groupby).residential_units.sum()

        plt.barh(np.arange(len(units)), units)

        plt.ylabel(groupbylabel)
        plt.xlabel("Residential Units in Properties Sold", x=0)
        plt.title("Residential Units Sold by %s\n%s" % (groupbylabel, self.label), x=0)

        # Use the units index to label the y axis ticks; add .5 to center them
        plt.yticks(np.arange(len(units)) + 0.5, units.index, va='top')

        return fig_to_svg(fig)


    def sales_volume_year_bar_chart(self):
        '''Plot the sales volume by year'''
        fig = init_fig()

        # Get sum of residential units by year
        yearly_count = self.data.groupby('year').residential_units.sum()

        plt.bar(np.arange(len(yearly_count)), yearly_count)

        plt.xlabel("Year")
        plt.ylabel("Residential Units in Properties Sold")
        plt.title("Residential units Sold by Year\n%s" % self.label)

        # Add .5 to the tick locations to center them
        plt.xticks(np.arange(len(yearly_count))+0.5, yearly_count.index, ha='center')

        return fig_to_svg(fig)


    def sale_price_per_sq_foot_boxplot(self, groupby, title):
        '''Boxplot of sale price per square foot, grouped by a groupby variable

        title is the plot title'''
        fig = init_fig()

        # This figure needs to be extra wide
        fig.set_size_inches(10, 4)

        # Remove missings and restrict to the columns we need
        data = self.data[[groupby, 'sale_price_per_sqft']].dropna()

        # The boxplot function takes a list of Series, so we make one Series for each
        # group, and append them all into a list
        groups = list()
        values = data[groupby].value_counts().index # All the levels of the groupby variable

        for value in values:
            groups.append(data.loc[data[groupby] == value, 'sale_price_per_sqft'])

        # Now make the plot. The empty string means we don't want the outliers, since
        # they will mess up the axis scale
        plt.boxplot(groups, 0, '')

        plt.ylabel("Sale Price per Sq. Ft.")
        plt.title(title)
        plt.xticks(np.arange(len(values))+1, values)

        return fig_to_svg(fig)


    def all_plots(self):
        '''Return a list of all the plots for a single geography'''
        return [self.price_per_unit_histogram(),
                self.sales_volume_bar_chart(groupby='building_type',
                                            groupbylabel='Building Type'),
                self.sales_volume_year_bar_chart(),
                self.sale_price_per_sq_foot_boxplot('building_type',
                                                    "Sale Price per Sq. Ft. by Building Type\n%s" \
                                                        % self.label)
               ]


    def borough_plots(self):
        '''Return a list of plots comparing all boroughs'''
        return [self.price_per_unit_histogram(),
                self.sales_volume_bar_chart(groupby='borough_name',
                                            groupbylabel='Borough'),
                self.sales_volume_year_bar_chart(),
                self.sale_price_per_sq_foot_boxplot('borough_name',
                                                    "Sale Price per Sq. Ft. by Borough\n%s" \
                                                        % self.label)
               ]

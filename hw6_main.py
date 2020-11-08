# hessmad
# Madison Hess
# 5/22/19
# CSE 163 AB
# Homework 6

'''
The following program utilizes census and food access data to track areas
affected by limited food access.  Low access to food is considered having at
least 500 people or 33% of the population not having access to food within
0.5 miles for urban areas and 10 miles for rural areas.  As seen in the maps
to follow, Washington state collected data of food access in 97% of the census
tracts but this data does reveal a large issue with food access throughout most
of the state.
'''

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Part 0 - Load in data using merge


def load_in_data(shapes, data):
    '''
    This method reads in a shape file and a csv and joins the two on the column
    indicating their census tract.
    '''
    shape = gpd.read_file(shapes)
    csv = pd.read_csv(data)
    joined = shape.merge(csv, left_on='CTIDFP00',
                         right_on='CensusTract', how='left')
    return joined


# Part 1

def percentage_food_data(info):
    '''
    This method takes the joined dataset and returns the percentage of food
    access data that was collected for census tracts in Washington state.
    '''
    info = info.dropna(subset=['State'])
    wash = info[info['State'] == 'WA']
    total = len(wash)
    have_info = len(wash[(wash['lapophalf'] != 0) | (wash['lapop10'] != 0)])
    return (have_info/total) * 100


def plot_map(info):
    '''
    Plots a map of the census tracts in Washington state and saves it to a
    .png file.
    '''
    info.plot()
    plt.savefig('washington_map.png')


def plot_population_map(info):
    '''
    Takes in the joined dataset and saves a .png file of a map showing the
    2010 census population sizes across the different census tracts.
    '''
    info.plot(column='POP2010', legend=True)
    plt.savefig('washington_population_map.png')


def plot_population_county_map(info):
    '''
    Takes in the joined dataset and saves a .png file of a map showing the
    2010 census population sizes across the different counties.
    '''
    info = info[['County', 'geometry', 'POP2010']]
    info.dissolve(by='County', aggfunc='sum')
    info.plot(column='POP2010', legend=True)
    plt.savefig('washington_county_population_map.png')


def plot_food_access_by_county(info):
    '''
    The following method takes in the joined dataset and parses it down to
    the County, geometry, population, and various indicators of food access.
    Following this, it computes what proportion of the population in each
    county has low access to food for the different measurements available.
    Finally, the method plots this data in four chloropleth maps side by side
    and saves this figure into a .png file.
    '''
    info = info[['County', 'geometry', 'POP2010', 'lapophalf', 'lapop10',
                 'lalowihalf', 'lalowi10']]
    info = info.dissolve(by='County', aggfunc='sum')
    info['lapophalf_ratio'] = info['lapophalf'] / info['POP2010']
    info['lapop10_ratio'] = info['lapop10'] / info['POP2010']
    info['lalowihalf_ratio'] = info['lalowihalf'] / info['POP2010']
    info['lalowi10_ratio'] = info['lalowi10'] / info['POP2010']
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, figsize=(20, 10), ncols=2)
    info.plot(ax=ax1, column='lapophalf_ratio', legend=True, vmin=0, vmax=1)
    ax1.set_title('Low Access: Half')
    info.plot(ax=ax3, column='lapop10_ratio', legend=True, vmin=0, vmax=1)
    ax3.set_title('Low Access: 10')
    info.plot(ax=ax2, column='lalowihalf_ratio', legend=True, vmin=0, vmax=1)
    ax2.set_title('Low Access + Low Income: Half')
    info.plot(ax=ax4, column='lalowi10_ratio', legend=True, vmin=0, vmax=1)
    ax4.set_title('Low Access + Low Income: 10')
    fig.savefig('washington_county_food_access.png')


def plot_low_access_tracts(info):
    '''
    This method takes in the joined dataset and uses it to plot a multi-layered
    map of Washington state. The first layer in light grey, shows all of the
    census tracts in Washington.  The second layer shows the census tracts we
    have food access data for in a dark grey.  And finally, in bright blue, we
    can see both urban and rural areas which are considered to have low access
    to food with respect to their corresponding definitions of low access.
    '''
    fig, ax = plt.subplots(1, figsize=(10, 5))
    info.plot(ax=ax, color='#EEEEEE')
    have_info = info[(info['lapophalf'] != 0) | (info['lapop10'] != 0)]
    have_info.plot(ax=ax, color='#AAAAAA')
    urban = info[info['Urban'] == 1.0]
    urban_la = urban[(urban['lapophalf'] >= 500) |
                     ((urban['lapophalf'] / urban['POP2010']) >= 0.33333333)]
    rural = info[info['Rural'] == 1.0]
    rural_la = rural[(rural['lapophalf'] >= 500) |
                     ((rural['lapophalf'] / rural['POP2010']) >= 0.33333333)]
    urban_la.plot(ax=ax)
    rural_la.plot(ax=ax)
    plt.savefig('washington_low_access.png')


def main():
    data = load_in_data('tl_2010_53_tract00/tl_2010_53_tract00.shp',
                        'food_access.csv')
    percentage_food_data(data)
    plot_map(data)
    plot_population_map(data)
    plot_population_county_map(data)
    plot_food_access_by_county(data)
    plot_low_access_tracts(data)


if __name__ == '__main__':
    main()

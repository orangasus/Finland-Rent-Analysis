import csv
import json

import pandas as pd
import requests
from matplotlib import pyplot
from matplotlib.gridspec import GridSpec


class Apartment:
    def __init__(self, city, district, rooms, rent, address, construct_year, housing_type, on_sale, size):
        self.city = city
        self.district = district
        self.rooms = rooms
        self.rent = rent
        self.address = address
        self.construct_year = construct_year
        self.housing_type = housing_type
        self.on_sale = on_sale
        self.size = size

    def in_list_view(self):
        return [self.city, self.district, self.rooms, self.rent, self.address,
                self.construct_year, self.housing_type, self.on_sale, self.size]


def get_apartment_object(apart):
    city = apart['city']
    address = apart['address']
    district = apart['district']
    rooms = apart['rooms']
    rent = apart['rent']
    construct_year = apart['construction_year']
    housing_type = apart['housing_type']
    on_sale = apart['is_on_sale']
    size = apart['size']
    return Apartment(city, district, rooms, rent, address, construct_year, housing_type, on_sale, size)


def create_csv_report(apartments):
    with open('my_data.csv', 'w', encoding="utf-8") as new_file:
        csv_writer = csv.writer(new_file)
        column_names = 'city, district, rooms, rent, address, construct_year, housing_type, on_sale, size'.split(', ')
        csv_writer.writerow(column_names)
        for el in apartments:
            csv_writer.writerow(el.in_list_view())


def update_apartments_info():
    url = 'https://api.kodisto.fi/v1/apartments/search?'
    params = {'location': '', 'categories': '', 'count': '5000'}
    res = requests.get(url, params=params)
    data = json.loads(res.text)['data']
    apartments = [get_apartment_object(x) for x in data]
    create_csv_report(apartments)


def save_district_bar_chart(df_city, city):
    total_apartments = df_city['apartments'].sum()
    gs = GridSpec(10, 10)
    fig = pyplot.figure(figsize=(16, 9))
    ax = fig.add_subplot(gs[:9, :])
    bars = ax.bar(df_city['district'], df_city['apartments'], color='#86D7FB')

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h}', xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 2),
                    textcoords='offset points', ha='center', va='bottom')

    ax.set_xticks([x for x in range(0, len(df_city['apartments']))])
    ax.set_xticklabels(df_city['district'], rotation=75)

    ax.set_title(f'Apartments by District, {city}', fontsize=20)
    for lab in ax.get_xticklabels():
        lab.set_fontsize(11)
    ax.set_ylabel('Number of Apartments', fontsize=14)

    fig.text(0.0125, 0.025, f"Apartments in total: {total_apartments}\nData from Kodisto.fi", fontsize=12,
             bbox=dict(facecolor='none', alpha=1, edgecolor='black'))

    fig.savefig(f'plots/bar_{city}.png', format='png', dpi=150)
    pyplot.close()


def get_bar_apartment_per_district(df_city, city):
    apartments = df_city['district'].value_counts(sort=False)
    districts = apartments.axes[0]
    d = {'district': districts, 'apartments': [x for x in apartments]}
    new_df = pd.DataFrame(d)

    cr = sum(new_df['apartments']) * 0.01
    delta = cr if cr >= 1 else 1
    num_of_other = sum(new_df.loc[new_df['apartments'] <= delta, 'apartments'])
    new_df = new_df.loc[new_df['apartments'] > delta]
    df_1 = pd.DataFrame({'district': ['Other'], 'apartments': [num_of_other]})
    new_df = pd.concat([new_df, df_1], axis=0, ignore_index=True)

    total = sum(new_df['apartments'])
    percent_df = pd.DataFrame({'percent': round(new_df['apartments'] / total * 100, 1)})
    new_df = pd.concat([new_df, percent_df], axis=1)

    save_district_bar_chart(new_df, city)


def create_charts_country(new_df, rooms_info):
    my_labels = [f'{x}\n{int(y)}\u20AC' for x, y in zip(new_df['city'], new_df['avg_rent'])]

    gs = GridSpec(5, 5)
    fig = pyplot.figure(figsize=(16, 9))
    ax1 = fig.add_subplot(gs[0:6, 0:3])
    ax2 = fig.add_subplot(gs[1:6, 3:6])

    ax1.pie(new_df['total'], labels=my_labels, autopct='%.1f%%')
    ax1.set_title('Apartments per City, Finland', fontsize=20)

    fig.text(0.025, 0.05, f"Apartments in total: {new_df['total'].sum()}\nData from Kodisto.fi", fontsize=12,
             bbox=dict(facecolor='green', alpha=0.4))

    bars = ax2.bar(list(rooms_info.axes[0]), list(rooms_info), width=0.6)
    ax2.set_title('Number of apartments depending on rooms\n', fontsize=16)
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 1), textcoords='offset points', ha='center', va='bottom')
    ax2.set_ylabel('Number of Apartments')
    ax2.set_xlabel('Rooms')
    pyplot.savefig('plots/pie_FINLAND.png', format='png', dpi=150)
    pyplot.close()


def get_charts_country(data):
    new_df = get_data_per_city(data)

    delta = new_df['total'].sum() * 0.02
    num_of_other = sum(new_df.loc[new_df['total'] <= delta]['total'])
    avg_of_other = new_df.loc[new_df['total'] <= delta]['avg_rent'].mean().round(0)

    new_df = new_df.loc[new_df['total'] > delta]
    df_1 = pd.DataFrame({'city': ['OTHER'], 'total': [num_of_other], 'avg_rent': [avg_of_other]})
    new_df = pd.concat([new_df, df_1], axis=0, ignore_index=True)

    rooms_info = data['rooms'].value_counts()
    create_charts_country(new_df, rooms_info)


def get_data_per_city(df, sorted=False):
    new_df = df.groupby('city').agg({'rooms': 'count', 'rent': 'mean'})
    new_df.reset_index(inplace=True)
    new_df.rename(columns={'rooms': 'total', 'rent': 'avg_rent'}, inplace=True)
    new_df['avg_rent'] = new_df['avg_rent'].apply(lambda x: round(x))

    if sorted:
        new_df = new_df.sort_values(by='total', ascending=False)

    return new_df


def main():
    try:
        update_apartments_info()
    except:
        pass

    data = pd.read_csv('my_data.csv')
    top_cities = get_data_per_city(data, sorted=True)[0:5]['city']

    for city in top_cities:
        get_bar_apartment_per_district(data.loc[data['city'] == city], city)
    get_charts_country(data)


if __name__ == '__main__':
    main()

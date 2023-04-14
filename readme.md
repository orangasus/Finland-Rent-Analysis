# Analysis of Apartments for rent in Finland


## What it does
Using a reliable data to get info about apartments for rent in Finland the script does some Pandas magic on it. As the result, it creates six plots. <br><br>
Fist of them illustrating distribution of apartments per city in Finland and how many apartments of each type are there. By type I mean the number of rooms. Here's an example:
<br><br>
<img src="./plots/pie_FINLAND.png" alt="your-image-description" style="border: 1px solid  black;">
<br><br><br>
Each of the other five plot represent data for one of the five cities in Finland that have the largest number of available apartments. Each plot displays the number of apartments per city district. 
<br><br>
<img src="./plots/bar_HELSINKI.png" alt="your-image-description" style="border: 1px solid  black;">
<img src="./plots/bar_ESPOO.png" alt="your-image-description" style="border: 1px solid  black;">
<img src="./plots/bar_TAMPERE.png" alt="your-image-description" style="border: 1px solid  black;">
<img src="./plots/bar_TURKU.png" alt="your-image-description" style="border: 1px solid  black;">
<img src="./plots/bar_VANTAA.png" alt="your-image-description" style="border: 1px solid  black;">
<br><br><br>

## How it works
- The script makes a request to [Kodisto.fi](https://kodisto.fi/)
- Transforms data for each apartment in a class instance and saves info in a csv file
- Creates a general-purpose Dataframe from the csv
- Creates specific Dataframe using filtering and aggregating for each plot
- Creates plots using Matplotlib and saves them as pngs
<br><br><br>

## Technology Stack
- **Requests** library for collecting data
- **CSV** and **JSON** modules for processing it
- **Pandas** for data analysing
- **Matplotlib** for creating plots
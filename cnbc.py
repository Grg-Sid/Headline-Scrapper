import requests
import csv
from dateutil import parser

template_url = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query=green hydrogen&endindex={end}&batchsize=100&callback=&showfaceted=false&timezoneoffset=-330&facetedfields=formats&facetedkey=formats|&facetedvalue=!Press Release|&needtoptickers=1&additionalindexes=4cd6f71fbf22424d,937d600b0d0d4e23,3bfbe40caee7443e,626fdfcd96444f28"

try:
    csv_rows = []
    for i in range(0, 1000, 100):
        api_url = template_url.format(end=i, batchsize=100)
        response = requests.get(api_url)

        if response.status_code == 200:
            api_data = response.json()
            results = api_data["results"]
            for result in results:
                sum_text = result["summary"]
                date = result["cn:lastPubDate"]
                date = parser.parse(date)
                csv_rows.append((sum_text, date, "CNBC"))
        else:
            print(f"Error: {response.status_code} - {response.text}")

    csv_file_path = "data.csv"

    with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_rows)

    print(f"Data has been appended to '{csv_file_path}'.")

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")

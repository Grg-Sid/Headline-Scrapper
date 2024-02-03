import csv
import re
import feedparser
from dateutil import parser

rss_feed_url = "https://news.google.com/rss/search?q=green%20hydrogen&hl=en-IN&gl=IN&ceid=IN:en&num=200"

try:
    feed = feedparser.parse(rss_feed_url)
    csv_rows = []

    for entry in feed.entries:
        title = re.split(r"-", entry.title)[0]
        date_string = entry.published
        if date_string:
            date_object = parser.parse(date_string)
        else:
            date_object = None
        source = entry.source.title if hasattr(entry.source, "title") else ""
        csv_rows.append((title, date_object, source))

    csv_file_path = "data.csv"

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(["headlines", "date", "source"])

        csv_writer.writerows(csv_rows)

    print(f"CSV data has been saved to '{csv_file_path}'.")

except Exception as e:
    print("Exception:", e)

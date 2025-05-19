import time
import pandas as pd
import schedule
from datetime import datetime
from pytrends.request import TrendReq

# Initialize Google Trends API
pytrends = TrendReq(hl='en-US', tz=360)

# More specific keywords
base_keywords = [
    "Best tool for graphic design",
    "Best tool for video editing",
    "Best tool for AI writing",
    "Best free online tool for SEO",
    "Best open-source tool for developers",
    "Top 10 AI-powered tools",
    "Which tool is best for content writing",
    "Best no-code tool for app development",
    "Must-have tools for digital marketing",
    "Automated tool for social media scheduling",
    "GPT-powered tool for writing",
]

# Function to fetch top searches (Hourly)
def get_hourly_top_searches():
    all_results = []

    for base_query in base_keywords:
        try:
            pytrends.build_payload([base_query], cat=0, timeframe="now 1-H", geo="", gprop="")
            related_queries = pytrends.related_queries()

            # Check if data exists before processing
            if related_queries and base_query in related_queries and "top" in related_queries[base_query]:
                top_queries = related_queries[base_query]["top"]
                
                # Ensure the dataframe is not empty
                if top_queries is not None and not top_queries.empty:
                    top_queries = top_queries.sort_values("value", ascending=False).head(10)
                    for _, row in top_queries.iterrows():
                        all_results.append([
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Last 1 Hour",
                            base_query,
                            row["query"],
                            row["value"]
                        ])
                else:
                    print(f"No trending searches found for '{base_query}' in the last hour.")

            else:
                print(f"No data available for '{base_query}'. Trying a different keyword...")

        except Exception as e:
            print(f"Error fetching data for '{base_query}': {e}")

    if all_results:
        save_hourly_top_searches(all_results)
        print(f"Saved {len(all_results)} results to 'google_top_searches_hourly.csv'.")
    else:
        print("No results found for any keywords. Consider using more specific queries.")

# Function to save results to CSV
def save_hourly_top_searches(results, filename="google_top_searches_hourly.csv"):
    df = pd.DataFrame(results, columns=["Timestamp", "Time Interval", "Base Keyword", "Top Search", "Search Interest"])
    df.to_csv(filename, mode="a", index=False, header=not pd.io.common.file_exists(filename))

# Schedule the script to run every hour
schedule.every().hour.at(":00").do(get_hourly_top_searches)

if __name__ == "__main__":
    print("🔍 Tracking hourly Google Trends. Press Ctrl+C to stop.")
    get_hourly_top_searches()  # Run immediately
    while True:
        schedule.run_pending()
        time.sleep(60)

from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load data
filename = "google_top_searches_hourly.csv"

def get_trending_data():
    df = pd.read_csv(filename)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    # Get the latest hour data
    latest_hour = df["Timestamp"].max()
    df_latest = df[df["Timestamp"] == latest_hour]

    # Aggregate data
    df_top = df_latest.groupby("Top Search")["Search Interest"].sum().reset_index()
    df_top = df_top.sort_values(by="Search Interest", ascending=False).head(10)

    # Generate bar chart
    fig = px.bar(df_top, x="Search Interest", y="Top Search", orientation="h", title="Top 10 Trending Searches (Last Hour)")
    graph_html = fig.to_html(full_html=False)

    return graph_html

@app.route("/")
def index():
    graph_html = get_trending_data()
    return render_template("index.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)

# import os
# import sys
# import pandas as pd

# # add src directory to path so we can import the pievis package
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
# import pievis as pieviz
import pieviz

if __name__ == "__main__":
    pieviz.create_all_charts_from_csv("data/pie_chart_trend.csv", prefix="GTrends in ")

    pieviz.create_all_charts_from_csv("data/ged_analysis.csv", prefix="GED: ")
    
    pieviz.create_all_charts_from_csv("data/ink_efficiency.csv", prefix="Ink Efficiency: ")

    pieviz.create_3d_pie_google({"When to use Pie Charts": 100}, title="")
    pieviz.save_google_chart_as_png("temp_chart.html", "pie/pie_fig1.png")

    pieviz.create_3d_pie_google({"Markus": 50, "Kevin": 50}, title="")
    pieviz.save_google_chart_as_png("temp_chart.html", "pie/author_contribution.png")

    pieviz.create_3d_pie_google({"blue": 69, "red": 42, "orange": 19, "green":9}, title="")
    pieviz.save_google_chart_as_png("temp_chart.html", "pie/paper_analysis.png")

    pieviz.create_3d_pie_google({"carbs": 39.7, "fat": 12.8, "protein": 2.2}, title="Nutritional Benefits")
    pieviz.save_google_chart_as_png("temp_chart.html", "pie/nutri_stats.png")

    pieviz.create_3d_pie_google({"apple pie": 750, "other food": 100250})
    pieviz.save_google_chart_as_png("temp_chart.html", "pie/food101.png")

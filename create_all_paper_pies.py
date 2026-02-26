import pievis
import pandas as pd

if __name__ == "__main__":
    pievis.create_all_charts_from_csv("data/pie_chart_trend.csv", prefix="GTrends in ")

    pievis.create_all_charts_from_csv("data/ged_analysis.csv", prefix="GED: ")
    
    pievis.create_all_charts_from_csv("data/ink_efficiency.csv", prefix="Ink Efficiency: ")

    pievis.create_3d_pie_google({"When to use Pie Charts": 100}, title="")
    pievis.save_google_chart_as_png("temp_chart.html", "pie/pie_fig1.png")

    pievis.create_3d_pie_google({"Markus": 50, "Kevin": 50}, title="")
    pievis.save_google_chart_as_png("temp_chart.html", "pie/author_contribution.png")

    pievis.create_3d_pie_google({"blue": 69, "red": 42, "orange": 19, "green":9}, title="")
    pievis.save_google_chart_as_png("temp_chart.html", "pie/paper_analysis.png")

    pievis.create_3d_pie_google({"carbs": 39.7, "fat": 12.8, "protein": 2.2}, title="Nutritional Benefits")
    pievis.save_google_chart_as_png("temp_chart.html", "pie/nutri_stats.png")

    pievis.create_3d_pie_google({"apple pie": 750, "other food": 100250})
    pievis.save_google_chart_as_png("temp_chart.html", "pie/food101.png")

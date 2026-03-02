import os
import sys

# add src directory to path so we can import the pievis package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import pieviz

if __name__ == "__main__":
    # 1 Pie for dummmies
    pieviz.create_all_charts_from_dict("pie_fig1", {"When to use Pie Charts": 100})
    pieviz.create_all_charts_from_dict("nutri_stats", {"carbs": 39.7, "fat": 12.8, "protein": 2.2})

    # 2 Unrelated work
    # Numbers taken from https://en.wikipedia.org/wiki/Blood_type_distribution_by_country
    pieviz.create_all_charts_from_dict("blood", {"O+": 38.4, "A+": 27.3, "B+": 8.1, "AB+": 2.0, "O-": 13.1, "A-": 8.1, "B-": 2, "AB-": 0.01})
    pieviz.create_all_charts_from_dict("ABO",{"O": 51.5, "A": 37.41, "B": 12.11})
    pieviz.create_all_charts_from_dict("Rh", {"+": 75.8, "-": 23.21})

    # 3 Theoretical dough
    ## 3.1 Ink efficiency
    pieviz.create_all_charts_from_csv("data/ink_efficiency.csv", prefix="Ink Efficiency: ")
    ## 3.2 GTrends
    pieviz.create_all_charts_from_csv("data/pie_chart_trend.csv", prefix="GTrends in ")
    ## 3.3 User study
    user_pie_pieces = {f"P{k}": 1 for k in range(1, 17)} # Create a dictionary with keys 1-16 and values set to 1
    pieviz.create_all_charts_from_dict("piepieces", user_pie_pieces)
    pieviz.create_all_charts_from_dict("identified", {"Pie Chart": 16})
    pieviz.create_all_charts_from_dict("simulation", {"Pie": 33, "Venn": 36, "UpSet": 31})
    pieviz.create_all_charts_from_dict("userstudy", {"Pie": 32.36125, "Venn": 12.07791, "UpSet": 5.68470})

    # 4 Pieviz experiments
    ## 4.1 Benchmarking
    pieviz.create_all_charts_from_dict("food101", {"apple pie": 750, "other food": 100250})
    ## 4.2 Case study: GEB
    pieviz.create_all_charts_from_csv("data/geb_analysis.csv", prefix="GEB: ")
    ## 4.3 Recursive paper analysis
    pieviz.create_all_charts_from_dict("paper_analysis", {"blue": 69, "red": 42, "orange": 19, "green":9})

    # 5+ After superiority of pie charts
    pieviz.create_all_charts_from_dict("author_contribution", {"Markus": 50, "Kevin": 50})

    # Appendix
    pieviz.create_all_charts_from_dict("pielike", {"Like": 15, "♥": 1})
    pieviz.create_all_charts_from_dict("piecompliment", {"Compliment": 3, "Stoic": 13})

    # Delete the temporary HTML file
    os.remove("temp_chart.html")

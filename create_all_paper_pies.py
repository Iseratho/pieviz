import pieviz

if __name__ == "__main__":
    # 1 Pie for dummmies
    pieviz.bake_and_store_pie({"When to use Pie Charts": 100}, "pie/pie_fig1.png")
    pieviz.bake_and_store_pie({"carbs": 39.7, "fat": 12.8, "protein": 2.2}, "pie/nutri_stats.png")

    # 2 Unrelated work
    # Numbers taken from https://en.wikipedia.org/wiki/Blood_type_distribution_by_country
    pieviz.bake_and_store_pie({"O+": 38.4, "A+": 27.3, "B+": 8.1, "AB+": 2.0, "O-": 13.1, "A-": 8.1, "B-": 2, "AB-": 0.01}, "pie/blood.png")
    pieviz.bake_and_store_pie({"O": 51.5, "A": 37.41, "B": 12.11}, "pie/ABO.png")
    pieviz.bake_and_store_pie({"+": 75.8, "-": 23.21}, "pie/Rh.png")

    # 3 Theoretical dough
    ## 3.1 Ink efficiency
    pieviz.bake_all_pies_from_csv("data/ink_efficiency.csv", prefix="Ink Efficiency: ")
    ## 3.2 GTrends
    pieviz.bake_all_pies_from_csv("data/pie_chart_trend.csv", prefix="GTrends in ")
    ## 3.3 User study
    user_pie_pieces = {f"P{k}": 1 for k in range(1, 17)} # Create a dictionary with keys 1-16 and values set to 1
    pieviz.bake_and_store_pie(user_pie_pieces, "pie/piepieces.png")
    pieviz.bake_and_store_pie({"Pie Chart": 16}, "pie/identified.png")
    pieviz.bake_and_store_pie({"Pie": 33, "Venn": 36, "UpSet": 31}, "pie/simulation.png")
    pieviz.bake_and_store_pie({"Pie": 32.36125, "Venn": 12.07791, "UpSet": 5.68470}, "pie/userstudy.png")

    # 4 Pieviz experiments
    ## 4.1 Benchmarking
    pieviz.bake_and_store_pie({"apple pie": 750, "other food": 100250}, "pie/food101.png")
    ## 4.2 Case study: GEB
    pieviz.bake_all_pies_from_csv("data/geb_analysis.csv", prefix="GEB: ")
    ## 4.3 Recursive paper analysis
    pieviz.bake_and_store_pie({"blue": 69, "red": 42, "orange": 19, "green":9}, "pie/paper_analysis.png")

    # 5+ After superiority of pie charts
    pieviz.bake_and_store_pie({"Markus": 50, "Kevin": 50}, "pie/author_contribution.png")

    # Appendix
    pieviz.bake_and_store_pie({"Like": 15, "♥": 1}, "pie/pielike.png")
    pieviz.bake_and_store_pie({"Compliment": 3, "Stoic": 13}, "pie/piecompliment.png")

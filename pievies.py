from playwright.sync_api import sync_playwright
import time
import os
import pandas as pd

def create_3d_pie_google(data_dict, title=""):
    # Convert dictionary to Google's data format: [['Label', 'Value'], ...]
    rows = [["Label", "Value"]]
    for k, v in data_dict.items():
        rows.append([k, v])

    html_content = f"""
    <html>
      <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load("current", {{packages:["corechart"]}});
          google.charts.setOnLoadCallback(drawChart);
          function drawChart() {{
            var data = google.visualization.arrayToDataTable({rows});

            var options = {{
              title: '{title}',
              is3D: true,
              pieSliceText: 'label',     // Forces TEXT labels inside
              legend: 'none',            // Cleaner look without side legend
              backgroundColor: 'transparent',
              chartArea: {{left:20, top:20, width:'90%', height:'90%'}},
              // Use standard colors
              colors: ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099']
            }};

            var chart = new google.visualization.PieChart(document.getElementById('pie_3d_render'));
            google.visualization.events.addListener(chart, 'ready', function() {{
              window.chartReady = true;
            }});
            chart.draw(data, options);
          }}
        </script>
      </head>
      <body>
        <div id="pie_3d_render" style="width: 100%; height: 100%;"></div>
      </body>
    </html>
    """

    # Save to a temporary file to ensure it loads in the IFrame
    with open("temp_chart.html", "w") as f:
        f.write(html_content)

def save_google_chart_as_png(html_file, output_png):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1200, 'height': 800})
        
        file_path = "file://" + os.path.abspath(html_file)
        page.goto(file_path)
        
        # Wait for chart to render
        page.wait_for_function('() => window.chartReady === true', timeout=10000)
        time.sleep(0.5)
        
        page.locator('#pie_3d_render').screenshot(path=output_png)
        print(f"Chart saved as {output_png}")

if __name__ == "__main__":
    df = pd.read_csv("pie_chart_trend.csv", index_col=0)
    # title = df.index[0]
    # data = df.iloc[0].to_dict()  # Specific row by index
    # print(title, data)

    # 
    for index, row in df.iterrows():
        title = f"GTrends in {index}"
        data = row.to_dict()
        print(title, data)
        create_3d_pie_google(data, title=title)
        save_google_chart_as_png("temp_chart.html", f"pie/pie_{index}.png")
    # Data
    # data = {
    #     "Pie Chart": 55,
    #     "Venn Diagram": 37,
    #     "Upset Plot": 1
    # }

    # # Render
    # create_3d_pie_google(data, title="2025 Pie Chart Usage")

    # # Usage (assuming you ran the previous script to create 'temp_chart.html')
    # save_google_chart_as_png("temp_chart.html", "my_3d_pie.png")
    # # Clean up temporary file
    # os.remove("temp_chart.html")
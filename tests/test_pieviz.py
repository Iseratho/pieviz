# Add src/ to path so pievis can be imported
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pieviz
import os

class TestStringMethods(unittest.TestCase):
    def test_create_3d_pie_google(self):
        data = {"A": 30, "B": 50, "C": 20}
        pieviz.create_3d_pie_google(data, title="Test Pie Chart")
        
        # Check if the temporary HTML file was created
        assert os.path.exists("temp_chart.html"), "temp_chart.html was not created"
        
        # Clean up
        os.remove("temp_chart.html")

if __name__ == '__main__':
    unittest.main()
# battedball3
testing python math libs with 2016 mlb batted ball data (python3 version)

uses python's numpy, scipy, pandas, plotly, and mpld3 libraries

# what it does
creates interactive plots to visualize players' batted ball performance. source data from FanGraphs and Baseball Savant (MLB.com). can create scatter plots and histograms


# plots
- "barrels/PA" versus average hitting speed scatterplot, [link](https://patwong.github.io/bb/brl_pa_vs_avg_hit_speed.html)
- average hit speed histogram, with average wRC+ hover text for every bin, [link](https://patwong.github.io/bb/avg_hit_speed_hist.html)
- (maximum hit speed and average hit speed differential) versus batting average scatter plot (inspiration from jeff sullivan), [link](https://patwong.github.io/bb/max_bb_ahs_ba.html)
- more graphs can be found on my project page [here!!](https://patwong.github.io/bb_project_page.html)
- a few of thoughts can be found in the above project page link
- more graph types and functionality to come


# file description
bb3class.py encapsulates all the functionality of battedball.py (parser) and bbp3 (plotly plotter) into a class. a sample script using bb3class is located in class_testscript.py

other files:
- dictplay.py: used to test the dictionaries created by the parsers, retrieving them from their pickle files if they exist
- cleanfiles.py: removes all auxiliary files

deprecated files (located in "old"):
- battedball.py contains parsers and a script in main() that sends data to the plotter
- bbp2 uses the mpld3 library
- bbp3 uses plotly
- bbplotter uses matplotlib

# license

The MIT License (MIT)

Copyright (c) 2017 Patrick Wong \<<patrick.wong@uwaterloo.ca>\>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
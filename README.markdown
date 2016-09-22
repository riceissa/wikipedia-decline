# Plots for Wikipedia "decline" post

For the post draft, go to
<http://issarice.com/revisiting-the-great-decline-in-wikipedia-pageviews>.

## File explanations

Here is an explanation of the most important files in this repository:

  * `data/` contains Wikipedia Views pageview exports.
  * `google_trends_mj/` contains Google Trends CSV exports where each
    musicians is plotted alongside Michael Jackson.
    This is the version of exports that was actually used.
  * `google_trends/` contains Google Trends CSV exports where each file
    is part of a "chain" containing two musicians running down the list
    of musicians.
    If the musicians are A, B, C, D, then this directory has the files
    'A and B', 'B and C', and 'C and D'.
    This is was not used in the final analysis.
  * `old_data/` contains some miscellaneous data files that were used
    when experimenting.
  * `plot.py` is the plotting file for pageviews.
    The list of plots can be found [here][plots_dir].
  * `csv_list.py` is a listing of files in `data`, used for easier
    access in `plot.py`.
  * `ratio_convert.py` is the plotting file for comparing the Google
    Trends and Wikipedia Views data.

## Exporting CSVs

### Wikipedia Views

Here are the steps used to export the CSVs used from Wikipedia Views.

1.  Go to <http://wikipediaviews.org/multipletagsandmonths.php>.
    This is the "Multiple tags and months" option from the top menu.
2.  Select a tag.
    For this example we choose "Colors".
3.  Select the "Check this to simultaneously select all months excluding the
    current month" checkbox.
4.  Click "Submit".
    You will get a table that has three columns: Month, Views of pages with tag
    Colors, and Percentage.
5.  Click on the word "Colors" in the middle column.
    This will take you to
    <http://wikipediaviews.org/displayviewsformultiplemonths.php?tag=Colors&language=en&device=desktop&allmonths=allmonths>.
    This page depends on the tag used.
    You will now see a table with more columns, one for each color, as well as
    the "Total" column.
6.  Scroll down, to find the link that says "Show technical settings (for
    advanced users only)".
    Click to reveal the options; I think this requires JavaScript.
7.  Go to where it says "Enter the format in which you want statistics to be
    displayed".
    Choose "CSV: Month and number of views separated by pipe delimiter (|);
    each line for a different month".
8.  Scroll up and click "Submit" again.
    You will get a page that looks like this:

        Month|Views of page Black|Views of page Blue|Views of page Brown|Views of page Green|Views of page Grey|Views of page Orange|Views of page Purple|Views of page Red|Views of page Violet|Views of page White|Views of page Yellow|Total|Percentage
        201608|17579|27770|8001|18100|17999|7010|17847|21613|1909|11616|12246|161690|0.3
        201607|17662|68046|8008|18477|22252|8375|16952|22034|1691|11194|15013|209704|0.4
        201606|21070|28176|8121|20080|23575|7348|19018|21993|1854|11994|16637|179866|0.3
        (More rows here...)

    (Technical note: Wikipedia
    [does not allow a pipe character in page titles][pageres]:
    "A pagename cannot contain any of the following
    characters: # \< \> [ ] | { } \_ (which all have special meanings in wiki
    syntax)".
    This makes them particularly attractive to use as delimiters.)

9.  Copy the page and paste into a local file and save.
10. Press the back button in your browser.
11. Under "Enter the device type for which you are interested in pageviews",
    select "Mobile web", and hit "Submit" again.
    Repeat step 9.
    Do the same for "Mobile app".

### Exporting Google Trends data

Google Trends allows export of trends as CSV.
[Example][gt_eg]; click on the three dots on the upper right of the plot and
select "CSV".
This is pretty useful, but there are some limitations:

  * All data points are integers.
    This means that if the range of values is large, the smaller values might
    just appear as "0".
  * You can only graph ~5 trends at a time.
  * Each time you plot a trend, the data points gets normalized so that 100 is
    assigned to the highest value among all the trend lines.
    This means that when looking at two plots, the numbers don't mean the same
    things unless the peak in each plot is the same.

To get around these limitations, we did the following:

  * We exported two trends at a time.
  * Each export included Michael Jackson, so that we could use that as a
    common "scale".
    In particular, within each export, we divide by the maximum Michael
    Jackson value, so that in every export the maximum Michael Jackson
    value is assigned 1.
  * We only exported the data starting in the end of September 2011
    (last 5 years). In
    particular, this means that the trend for Michael Jackson is fairly
    stable, and we avoid the huge spike in traffic on account of [his
    death][mj_death].

Note that because of the ambiguity of the word "Pitbull", for
[Pitbull][pitbull]
only we used the "rapper" version of the search term instead of the
generic search term.

[pageres]: https://en.wikipedia.org/wiki/Wikipedia:Page_name#Technical_restrictions_and_limitations
[gt_eg]: https://www.google.com/trends/explore?q=Michael%20Jackson,Justin%20Bieber
[mj_death]: https://en.wikipedia.org/wiki/Death_of_Michael_Jackson#Media_and_Internet_coverage
[plots_dir]: http://23.226.229.10/~issa/pageview_plots/
[pitbull]: https://en.wikipedia.org/wiki/Pitbull_(rapper)

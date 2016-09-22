
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
    This makes them particularly useful to use as delimiters.)

9.  Copy the page and paste into a local file and save.
10. Press the back button in your browser.
11. Under "Enter the device type for which you are interested in pageviews",
    select "Mobile web", and hit "Submit" again.
    Repeat step 9.
    Do the same for "Mobile app".

### Exporting Google Trends data

Google Trends allows export of trends as CSV.
[Example][gt_eg].
This is pretty useful, but there are some limitations:

  * All data points are integers.
  * You can only graph ~5 trends at a time.
  * Each time you plot a trend, the data points gets normalized so that 100 is
    assigned to the highest value.
    This means that when looking at two plots, the numbers don't mean the same
    things unless the peak in each plot is the same.

[pageres]: https://en.wikipedia.org/wiki/Wikipedia:Page_name#Technical_restrictions_and_limitations
[gt_eg]: https://www.google.com/trends/explore?q=Michael%20Jackson,Justin%20Bieber

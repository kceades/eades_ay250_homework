# Homework 8
# Caleb Eades

<h2>Running the Program</h2>

Simply download, pull or fork this repository, cd into the directory where it is contained locally on your device and then run the command

python bibmanager.py

in your terminal. The important pieces are the templates folder (and all templates inside) and the bibmanager.py file. Note that I didn't upload the test data from the original homework file, so if you want to use test data, probably a good source would be that python-seminar folder.

<h2>Notes</h2>

<ul>
<li>I didn't do any fancy CSS to make it look pretty, but there is rendering of failure and success pages which should be useful.</li>
<li>There is no guard against SQL injection or anything like that, but given that people would run this locally on there own machines, I don't think that's too much of an issue.</li>
<li>I tried to give helpful advice on how to search in the search page, but basically you just enter the part of a query that would come after the WHERE clause in the statement.</li>
<li>The fields that exist in the table are Key, Authors, Journal, Pages, Year, Title, and Collection where Collection is specified by the user at the time of uploading a bib file.</li>
<li>Authors is a string of comma-delimited names.</li>
<li>It may have just been some issue with the test data, but right now Journal doesn't render that nicely. It appears as an abbreviation I suspect.</li>
<li>Only .bib files are allowed in uploading, otherwise it will route to the failure page.</li>
</ul>

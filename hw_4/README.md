#Homework 4, Caleb Eades

First off, I went with an jupyter notebook to do all my code in. Hopefully you didn't just want a script, but I assumed notebook since that's what all the other assignments used.

Processor: Intel Core i5-4210U CPU @ 1.70GHz x 4

I have extensive notes and documentation and explanation of my functions and how to use them, what to watch out for, and various tidbits about why they were made the way I made them in the notebook itself.

Graph behavior: For small numbers of darts thrown in the Monte Carlo simulation, both multiprocessing and IPcluster introduce overhead in the context managers that slows down the runtime compared to serial. However, as the dart throws increase, this overhead becomes insignificant compared to the runtime of the core code itself, so then multiprocessing and IPcluster overtake simple execution. This also explains why the rate of darts thrown increases up to a plateau: for small dart amounts, most of the execution time is in overhead of function calls, setting up variables and other non-core code parts. As the number of darts increases, most of the function evaluation time switches to the dart interactions and hence the rate of dart throwing plateaus to its maximum value. In the long run for large dart tosses, both Multiprocessing and IPcluster should reach about 1/4 the run time of simple execution (at least with 4 "cores") since it is effectively splitting the work up across cores.

The last interesting thing to explain in the graph is that IPcluster does worse than multiprocessing almost across the board. I think this is because IPcluster has to go through additional hurdles and incur extra overhead in managing processes since they are (at least virtually) on the web rather than core to the machine.

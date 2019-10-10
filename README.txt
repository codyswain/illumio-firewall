Installation:
--------------------------------------------------------------------------
pip install requirements.txt
python3 firewall.py


Testing:
--------------------------------------------------------------------------
Due to time constraints, I didn't spend time testing the performance of my program. 
However, I implemented a few pass / no pass test cases, and made sure to check edge
cases such as ports and ip addresses at the edge of the (inclusive) ranges.

Code Choice:
--------------------------------------------------------------------------
After scanning the spec, my first thought was to implement a naive solution,
where a list is created at class construction, and iterated through each time. 
This would lead to extremely innefficient querying when accept_packet() is called. 

My next thought was to try and figure out how to implement some hash map storage of
rules upon intializing the class, but I was stumped by how to incorporate queryable 
ranges into the mix. One solution I had was to create a list of tuples and checking the lower
and upper bounds. 

Finally, I looked around on Google and stumbled upon the interval trees, a data structure
built to combine overlapping ranges and query them — perfect for this application. Since both
port and ip address inputs may be ranges, I had to decide how to organize the search space. I chose
to make ip address a key in a hash, because

Optimization:
--------------------------------------------------------------------------
While I was happy with my hacked together solution, I noticed that the constructor stores
all the rules in RAM, which could potentially be problematic given a large enough rule set. A solution
would be to use a SQL database and and execute a query each time you want to check whether a packet may pass.

When looking online I saw some papers which discussed a Structured Firewall Query Language (SFQL) 
https://www.cs.utexas.edu/~gouda/FirewallQueries.pdf, which I'd look into more before implementing a 
production ready firewall. 

Area / Team of Interest: 
--------------------------------------------------------------------------
I'm really interested in working on the Data Team, and I believe my past experience best aligns with this.

I look forward to hearing back! 



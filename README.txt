Installation:

# The spec says that the function accept_packet should take an int for the port
# but the input spec specifies that the port may be either an int [1, 65535] or
# range separated by a dash. I changed the port arg in accept_packet to str
# to accomodate for this.

# First I considered the naive solution, where I create a list of every rule, and
# check each incoming rule against the whole list which has O(N) complexity if
# n is the number of rules

# Instead of attempting to implement the naive solution, I brainstormed how you
# could optimize the querying process. If ranges weren't present, it'd be
# trivial to hash rules and achieve O(1) time complexity (with O(N) space complexity)

# I had two other ideas that seemed like they could have potential, each with their
# own weaknesses. The first would be to create a seperate database, which would allow
# SQL's optimized query, but also take O(N) space. The alternative would be to create a
# rolling pandas dataframe across a window of csv rows... probably an even worse solution

# Finally I decided upon building a sort of decision tree, which I implement using nested
# hash maps. I found a pretty great Python module for dealing with intervals, and
# create an interval tree for ports, which reduces the dimensionality of the search place
# significantly.

# This solution stores everything in RAM

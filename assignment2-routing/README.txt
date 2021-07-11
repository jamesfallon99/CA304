Parts 1, 2, 3 are completely working, part 4 works for multiple routers even when "print_routing_table()" is called. Part 4 slightly breaks when "remove_router" is called.
Only thing it doesn't cater for is e.g b->a = 0 when a router isn't connected so I added this edge in myself when testing. Other than that part 4 seems to work fine.
My dijkstra algorithm that I implemented has a bug in it that I wasn't sure how to fix as I got help with this algorithm online(source in comments of code).
On the off chance that this bug occurs when correcting this assignment, I have provided the sample test code in my main function. Please run this code to see the program working(if it doesn't work with test code that you may use)
I didn't add anything extra in this assignment.
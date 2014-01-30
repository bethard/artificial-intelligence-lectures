edge(a, b).
edge(b, c).
edge(b, d).
edge(d, f).
connected(X, Z):- edge(X, Z).
connected(X, Z):- edge(X, Y), connected(Y, Z).



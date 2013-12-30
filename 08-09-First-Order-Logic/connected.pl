edge(a, b).
edge(b, c).
edge(b, d).
edge(c, e).
edge(d, f).
connected(X, Z):- edge(X, Z).
connected(X, Z):- connected(Y, Z), edge(X, Y).



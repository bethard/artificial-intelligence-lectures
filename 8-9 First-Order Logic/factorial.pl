factorial(1, 1).
factorial(N, _):- N =< 0, fail.
factorial(N, F):- N > 1, N1 is N - 1, factorial(N1, F1), F is F1 * N.

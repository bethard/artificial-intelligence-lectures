color(X) :- X = blue; X = green; X = red.
color_australia(A) :-
	A = [WA, NT, Q, NSW, V, SA, T],
	color(WA), color(NT), color(Q), 
	color(NSW), color(V), color(SA), color(T),
	WA \= NT, NT \= Q, Q \= NSW, NSW \= V,
	WA \= SA, NT \= SA, Q \= SA, NSW \= SA, V \= SA,
	writef('WA=%7l NT=%7l Q=%7l NSW=%7l V=%7l SA=%7l T=%7l\n', A),
	fail.


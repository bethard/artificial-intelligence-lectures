color(X) :- X = blue; X = green; X = red.
color_australia(_{western_australia:WA,
		  northern_territory:NT,
		  queensland:Q,
		  new_south_wales:NSW,
		  victoria:V,
		  south_australia:SA,
		  tasmania:TA}) :-
	color(WA), color(NT), color(Q),
	color(NSW), color(V), color(SA), color(TA),
	WA \= NT, NT \= Q, Q \= NSW, NSW \= V,
	WA \= SA, NT \= SA, Q \= SA, NSW \= SA, V \= SA.

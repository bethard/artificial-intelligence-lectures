% Harry Potter 7 Potions Problem

% First clue - wine always has poison to its left
poisonIsLeftOfWine([P1,P2|P]):-
	(P2 \== wine; P1 == poison), poisonIsLeftOfWine([P2|P]).
poisonIsLeftOfWine([P1]):- P1 \== wine.

% Second clue - the ends are different and neither is forward
endsAreDifferent([P1, _, _, _, _, _, P7]):- P1 \== P7.
endsAreNotForward([P1, _, _, _, _, _, P7]):- P1 \== forward, P7 \== forward.

% Third clue - neither the smallest nor the largest is poison
smallestIsNotPoison(P):- smallest(P, P1), P1 \== poison.
largestIsNotPoison(P):-	largest(P, P1),	P1 \== poison.

% Fourth clue - second left and second right are the same
secondsAreTheSame([_, P2, _, _, _, P6, _]):- P2 == P6.

% The full potions problem
potions(P):-
	permutation(P, [forward, backward,
			wine, wine,
			poison, poison, poison]),
	poisonIsLeftOfWine(P),
	endsAreDifferent(P), endsAreNotForward(P),
	smallestIsNotPoison(P), largestIsNotPoison(P),
	secondsAreTheSame(P).

solve(P):- bagof(_, potions(P), _).



%smallest([_, _, P3, _, _, _, _], P3).
%largest([_, P2, _, _, _, _, _], P2).
smallest(_, _):- true.
largest(_, _):- true.


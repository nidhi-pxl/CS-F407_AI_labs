% ============================================
% Logical Reasoning Lab
% Task 6 - Prolog as a Plan Verifier
% ============================================


% Warehouse connectivity

connected(a,b).
connected(b,a).
connected(b,c).
connected(c,b).


% A move is possible when two locations
% are directly connected.

can_move(X,Y) :-
    connected(X,Y).



% ============================================
% Task 7 - Verify proposed movements
% ============================================

valid_move(X,Y) :-
    connected(X,Y).




% --------------------------------------------
% Task 8 - Logical reasoning
% --------------------------------------------

wet_road.

slippery :-
    wet_road.

reduce_speed :-
    slippery.
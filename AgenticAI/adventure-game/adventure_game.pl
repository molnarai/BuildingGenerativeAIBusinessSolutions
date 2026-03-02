:- dynamic i_am_at/1.
:- dynamic at/2.

% Rooms
room(kitchen).
room(hall).
room(garden).

% Connections
connected(kitchen, hall).
connected(hall, kitchen).
connected(hall, garden).
connected(garden, hall).

% Initial state
i_am_at(kitchen).

% Items
at(apple, kitchen).
at(key, hall).

% Room descriptions
describe(kitchen, "You are in a small kitchen. There is a wooden table here.").
describe(hall,    "You are in a hall with a coat rack and a dusty mirror.").
describe(garden,  "You are in a quiet garden with flowers and a stone bench.").

% State transition API
step(go(Direction), Result, state{location: NewPlace, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    connected(Here, NewPlace),
    retract(i_am_at(Here)),
    asserta(i_am_at(NewPlace)),
    inventory_list(Inv),
    visible_items(NewPlace, Visible),
    describe(NewPlace, Desc),
    atomic_list_concat(["You go ", Direction, ". ", Desc], Result), !.

step(take(Item), Result, state{location: Here, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    at(Item, Here),
    retract(at(Item, Here)),
    asserta(at(Item, inventory)),
    inventory_list(Inv),
    visible_items(Here, Visible),
    atomic_list_concat(["You pick up the ", Item, "."], Result), !.

step(look, Result, state{location: Here, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    describe(Here, Desc),
    inventory_list(Inv),
    visible_items(Here, Visible),
    atomic_list_concat(["You look around. ", Desc], Result), !.

step(_Command, "Nothing happens.", state{location: Here, inventory: Inv, visible: Visible}) :-
    i_am_at(Here),
    inventory_list(Inv),
    visible_items(Here, Visible).

inventory_list(Items) :-
    findall(Item, at(Item, inventory), Items).

visible_items(Place, Items) :-
    findall(Item, at(Item, Place), Items).

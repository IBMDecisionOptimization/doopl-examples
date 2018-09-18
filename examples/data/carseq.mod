using CP;

tuple T{
int value;
};
{T} nbCars = ...;
{T} nbOptions = ...;
{T} nbSlots = ...;

int  _nbCars    = first(nbCars).value; // # of cars
int   _nbOptions = first(nbOptions).value;// # of options
int   _nbSlots   = first(nbSlots).value;// # of slots

range   Cars    = 1.._nbCars;
range   Options = 1.._nbOptions;
range   Slots   = 1.._nbSlots;

tuple T1{
int car;
int demand;
};
tuple T2{
int opt;
int car;
int option;
};
{T1} demand = ...;
{T2} option = ...;

int _demand[Cars] = [c : d | <c,d> in demand];
int _option[Options,Cars] = [opt : [car : o] | <opt, car, o> in option];

tuple Tcapacity {
key int option;
int l;
int u;
};
{Tcapacity} capacity = ...;
//Tcapacity _capacity[Options] = [o : <l,u> | <o,l,u> in capacity];
int optionDemand[i in Options] = sum(j in Cars) _demand[j] * _option[i,j];

dvar int slot[Slots] in Cars;
dvar int setup[Options,Slots] in 0..1;

subject to {
// # of cars = demand
forall(c in Cars )
sum(s in Slots ) (slot[s] == c) == _demand[c];

forall(o in Options, s in 1..(_nbSlots - item(capacity,<o>).u + 1) )
sum(j in s..(s + item(capacity,<o>).u - 1)) setup[o,j] <= item(capacity, <o>).l;

forall(o in Options, s in Slots )
setup[o,s] == _option[o][slot[s]];

forall(o in Options, i in 1..optionDemand[o])
sum(s in 1 .. (_nbSlots - i * item(capacity,<o>).u)) setup[o,s] >=
    optionDemand[o] - i * item(capacity,<o>).l;
        };

        tuple slotSolutionT{
        int Slots;
        int value;
        };
      {slotSolutionT} slotSolution = {<i0,slot[i0]> | i0 in Slots};
        tuple setupSolutionT{
        int Options;
        int Slots;
        int value;
        };
        {setupSolutionT} setupSolution = {<i0,i1,setup[i0][i1]> | i0 in Options,i1 in Slots};

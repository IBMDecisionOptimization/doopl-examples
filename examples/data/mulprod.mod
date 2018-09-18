// --------------------------------------------------------------------------
// Licensed Materials - Property of IBM
//
// 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55
// Copyright IBM Corporation 1998, 2013. All Rights Reserved.
//
// Note to U.S. Government Users Restricted Rights:
// Use, duplication or disclosure restricted by GSA ADP Schedule
// Contract with IBM Corp.
// --------------------------------------------------------------------------

{string} Products = ...;
{string} Resources = ...;
int NbPeriods = ...;
range Periods = 1..NbPeriods;

float Consumption[Resources][Products] = ...;

tuple T{
key string id;
float value;
}
{T} Capacity = ...;

float _Capacity[Resources]  = [ id : value | <id, value> in Capacity];
float Demand[Products][Periods] = ...;
float InsideCost[Products] = ...;
float OutsideCost[Products]  = ...;
float Inventory[Products]  = ...;
float InvCost[Products]  = ...;
range Periods0 = 0..NbPeriods;

dvar float+ Inside[Products][Periods];
dvar float+ Outside[Products][Periods];
dvar float+ Inv[Products][Periods0];


minimize
  sum( p in Products, t in Periods ) 
      (InsideCost[p]*Inside[p][t] + 
       OutsideCost[p]*Outside[p][t] +
       InvCost[p]*Inv[p][t]);

subject to {
  forall( r in Resources, t in Periods )
    ctCapacity:
      sum( p in Products ) 
        Consumption[r][p] * Inside[p][t] <= _Capacity[r];
  forall( p in Products , t in Periods )
    ctDemand:
      Inv[p][t-1] + Inside[p][t] + Outside[p][t] == Demand[p][t] + Inv[p][t];
  forall( p in Products )
    ctInventory:
      Inv[p][0] == Inventory[p]; 
};
tuple plan {
   float inside;
   float outside;
   float inv;
}
plan Plan[p in Products][t in Periods] = <Inside[p,t],Outside[p,t],Inv[p,t]>;


tuple InsideSolutionT{ 
	string Products; 
	int Periods; 
	float value; 
};
{InsideSolutionT} InsideSolution = {<i0,i1,Inside[i0][i1]> | i0 in Products,i1 in Periods};
tuple OutsideSolutionT{ 
	string Products; 
	int Periods; 
	float value; 
};
{OutsideSolutionT} OutsideSolution = {<i0,i1,Outside[i0][i1]> | i0 in Products,i1 in Periods};
tuple InvSolutionT{ 
	string Products; 
	int Periods0; 
	float value; 
};
{InvSolutionT} InvSolution = {<i0,i1,Inv[i0][i1]> | i0 in Products,i1 in Periods0};

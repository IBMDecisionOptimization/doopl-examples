tuple T1{
key int index;
int value;
};

        tuple T2{
key int index1;
key int index2;
int value;
};	

{T2} A = ...;

{T1} B = ...;
{T2} C = ...;

//int number_of_s = max(<i,value> in B) i;
//range _range = 0..number_of_s;

int ci = max(<i,j,value> in C) i;
int cj = max(<i,j,value> in C) j;
//range _range = 0..ci;

{T1} multipliers = ...;
execute{
//writeln(multipliers);
//writeln(ci);
//writeln(cj);
};
//int multipliers[_range] = [i : j | <i,j> in multiplersS];


dvar int x_vars[0..ci][0..cj] in 0..1;       
dvar float p_vars[0..ci] in 0..infinity;

dexpr float total_penalty = sum(i in 0..ci) p_vars[i] * item(multipliers, <i>).value; // mdl.scal_prod(p_vars, multipliers)

dexpr float total_profit = sum(i in 0..ci, j in 0..cj) item(C, <i,j>).value * x_vars[i][j];

maximize(total_profit + total_penalty);

subject to{
    forall(i in 0..ci)
		sum(j in 0..cj) x_vars[i][j] == 1 - p_vars[i];

    forall(j in 0..cj)
		sum(i in 0..ci) x_vars[i][j] * item(A, <i,j>).value <= item(B, <j>).value;
}
	
tuple T3{
key int index;
float value;
};
{T3} penalties = { <i, p_vars[i]> | i in 0..ci};
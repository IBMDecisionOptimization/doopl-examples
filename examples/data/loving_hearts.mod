// Author: vberaudi


tuple T{
	int x;
	int y;
};

int r = 12;

// the dictionary of decision variables, one variable
// for each circle with i in (1 .. r) as the row and
// j in (1 .. i) as the position within the row
{T} idx = {<i, j> | i in 1..r, j in 1..i};

tuple T3{
T u;
T v;
T w;
};
{T3} ss = {<<i + m, j>, <i + k, j + m>, <i + k - m, j + k - m>> | i in 1..r-1, j in 1..i, k in 1..r-i, m in 0..k-1};


dvar boolean a[idx];// = mdl.binary_var_dict(idx)

// the constraints - enumerate all equilateral triangles
// and prevent any such triangles being formed by keeping
// the number of included circles at its vertexes below 3
maximize(sum(i in idx) a[i]);

subject to{
forall(<u,v,w> in ss) a[u] + a[v] + a[w] <= 2;
}

dexpr int obj = sum(i in idx) a[i];
dexpr int kpi1 = sum(i in idx : i.x == 1) a[i];
dexpr int kpi2 = sum(i in idx : i.y == 2) a[i];

tuple solution{
int x;
int y;
int value;
};
{solution} mySolution = {<i,j,a[<i,j>]> | <i,j> in idx};

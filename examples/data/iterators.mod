{string} names = {"toto", "titi", "tata", "tutu"};
{int} ints = {i | i in 0..4};
{float} floats = {i+0.12 | i in 0..4};

tuple T{
string a;
int b;
float c;
}
        {T} solution = {<i,j,k> | i in names, j in ints, k in floats};

subject to{
}

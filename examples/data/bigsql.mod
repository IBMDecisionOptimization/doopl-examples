tuple TT1{
int a;
int b;
int c;
};

tuple TT2{
string a;
string b;
string c;
};


tuple T{
key int a;
key int b;
key int c;

TT1 x;

TT1 y;

TT2 z;

string s;
string t;
};

{T} entities = ...;
execute{
writeln("size of data is ", entities.size);
};

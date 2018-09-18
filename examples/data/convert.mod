dvar int x in 0..10;

minimize x;
subject to {
  ct :
    x >= 1/2;
}
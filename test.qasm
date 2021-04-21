OPENQASM 3;
include "stdgates.inc";

def func1 (bit[n]:a1, int[1]:a2) qubit:q1, qubit:q2 -> int[1] {
    int[1] x1;
    int[1] x2;
    if (a2 > n) {
        x1 = 1;
        x2 = 2;
    } else {
        x1 = 2;
        x2 = 1;
    }
    return x1 - x2;
}
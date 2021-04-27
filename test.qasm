OPENQASM 3;
include "stdgates.inc";

def func1 (int[5]:a1, int[5]:a2) -> int[5] {
    int[5] t = 0;
    if (a1 > a2) {
        t = a1++;
    } else {
        t = a1 + a2;
    }
    t /= 2;
    return t;
}
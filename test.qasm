OPENQASM 3;
include "stdgates.inc";

int[2] n = 3;

def f1 (int[5]:a1, int[5]:a2) -> int[5] {
    int[5] t = 0;
    if (a1 > a2) {
        t = a1++;
    } else {
        t = a1 + a2;
    }
    t /= 2;
    return t;
}

def f2 (int[5]:x) qreg[5]:q -> int[8] {
    int[5] r;
    r = measure q;
    int[5] s = r + x;
    return s;
}
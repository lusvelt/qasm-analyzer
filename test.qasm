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

def f2 (int[5]:x) qreg[5]:q, qreg[5]:u -> int[8] {
    int[5] r;
    if (x * x > 2) {
        r = measure q;
    } else {
        CX q[0:3], u[1:4];
        r[0:2] = measure q[2:4];
    }
    int[5] s = r + x;
    return s;
}
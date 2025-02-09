pragma circom 2.0.0;

template IsSquare() {
    signal input x;
    signal output y;
    signal square;

    square <== x * x;
    y <== square;
}

component main = IsSquare();

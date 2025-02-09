#!/bin/bash

# Install dependencies (one-time setup)
if ! command -v circom &> /dev/null; then
    echo "Installing circom..."
    npm install -g circom@latest
fi

if ! command -v snarkjs &> /dev/null; then
    echo "Installing snarkjs..."
    npm install -g snarkjs@latest
fi

# Download trusted setup (phase1)
if [ ! -f powersOfTau.ptau ]; then
    echo "Downloading powersOfTau..."
    wget https://hermez.s3-eu-west-1.amazonaws.com/powersOfTau28_hez_final_12.ptau -O powersOfTau.ptau
fi

# Compile all .circom files in circuits directory
for circuit in circuits/*.circom; do
    base=$(basename "$circuit" .circom)
    echo "Compiling $base..."
    
    mkdir -p build/$base
    # 1. Compile circuit
    circom "$circuit" --wasm --r1cs --sym -o build/$base
    
    # 2. Perform trusted setup
    snarkjs groth16 setup "build/$base/$base.r1cs" powersOfTau.ptau "build/$base/$base.zkey"
    
    # 3. Export verification key
    snarkjs zkey export verificationkey "build/$base/$base.zkey" "build/$base/verification_key_$base.json"
done

echo "All circuits compiled to build/"
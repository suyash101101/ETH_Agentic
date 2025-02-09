pragma circom 2.1.9;

include "circomlib/circuits/comparators.circom";
include "circomlib/circuits/bitify.circom";
include "@openpassport/zk-email-circuits/utils/array.circom";
include "@zk-kit/binary-merkle-root.circom/src/binary-merkle-root.circom";
include "circomlib/circuits/poseidon.circom";

/// @title SMTVerify
/// @notice Verifies inclusion or non-inclusion of a key in a Sparse Merkle Tree
/// @param nLength Maximum depth of the tree
/// @input virtualKey The key to verify (user's input key)
/// @input key The key stored in the tree at the path
/// @input root The root of the Sparse Merkle Tree
/// @input siblings Array of sibling nodes
/// @input mode Verification mode (0 for non-inclusion, 1 for inclusion)
/// @output out 1 if verification succeeds, 0 otherwise
template SMTVerify(nLength) {
    signal input virtualKey;
    signal input key;
    signal input root;
    signal input siblings[nLength];
    signal input mode;
    signal depth <-- getSiblingsLength(siblings); // no need to constraint this as bad input will give the wrong root

    // Calculate path
    signal path[nLength];
    signal path_in_bits_reversed[nLength] <== Num2Bits(256)(virtualKey);
    var path_in_bits[nLength];

    for (var i = 0; i < nLength; i++) {
        path_in_bits[i] = path_in_bits_reversed[nLength-1-i];
    }
    
    // Shift the path to the left by depth to make it compatible for BinaryMerkleRoot function
    component pathShifter = VarShiftLeft(nLength, nLength);
    pathShifter.in <== path_in_bits;
    pathShifter.shift <== (nLength - depth);
    path <== pathShifter.out;

    // Closest_key to leaf
    signal leaf <== Poseidon(3)([key, 1, 1]); // compute the leaf from the key
    signal isClosestZero <== IsEqual()([key,0]); // check if the inital key is 0, in that case the leaf will be 0 too, not Hash(0,1,1);
    signal leafOrZero <== leaf * (1 - isClosestZero);

    // Verification
    signal computedRoot <== BinaryMerkleRoot(nLength)(leafOrZero, depth, path, siblings);
    signal computedRootIsValid <== IsEqual()([computedRoot,root]);

    // check is leaf equals virtual leaf
    signal virtualLeaf <== Poseidon(3)([virtualKey, 1,1]);
    signal areLeafAndVirtualLeafEquals <== IsEqual()([virtualLeaf, leaf]);

    signal isInclusionOrNonInclusionValid <== IsEqual()([mode,areLeafAndVirtualLeafEquals]);

    signal output out <== computedRootIsValid * isInclusionOrNonInclusionValid;
}

/// @title SiblingsLength
/// @notice Computes the effective length of a Merkle proof siblings array by finding the last non-zero element
/// @dev Handles arrays that may have zeros in between valid elements
/// @input siblings[256] Array of sibling nodes in a Merkle proof
/// @output length The effective length of the siblings array (position of last non-zero element)
function getSiblingsLength(siblings) {
    var length;

    for (var i = 0; i < 256; i++) {
        if (siblings[i] != 0) {
            length = i;
        }
    }
    return length + 1;
}
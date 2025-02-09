<p align="center">
    <h1 align="center">
        Binary Merkle Root
    </h1>
    <p align="center">A circuit to calculate the root of a binary Merkle tree using a provided proof-of-membership.</p>
</p>

<p align="center">
    <a href="https://github.com/privacy-scaling-explorations/zk-kit.circom">
        <img src="https://img.shields.io/badge/project-zk--kit-blue.svg?style=flat-square">
    </a>
    <a href="https://github.com/privacy-scaling-explorations/zk-kit.circom/tree/main/packages/binary-merkle-root/LICENSE">
        <img alt="NPM license" src="https://img.shields.io/npm/l/%40zk-kit%2Fbinary-merkle-root.circom?style=flat-square">
    </a>
    <a href="https://www.npmjs.com/package/@zk-kit/binary-merkle-root.circom">
        <img alt="NPM version" src="https://img.shields.io/npm/v/@zk-kit/binary-merkle-root.circom?style=flat-square" />
    </a>
    <a href="https://npmjs.org/package/@zk-kit/binary-merkle-root.circom">
        <img alt="Downloads" src="https://img.shields.io/npm/dm/@zk-kit/binary-merkle-root.circom.svg?style=flat-square" />
    </a>
</p>

<div align="center">
    <h4>
        <span>&nbsp;&nbsp;|&nbsp;&nbsp;</span>
        <a href="https://github.com/privacy-scaling-explorations/zk-kit.circom/issues/new/choose">
            🔎 Issues
        </a>
        <span>&nbsp;&nbsp;|&nbsp;&nbsp;</span>
        <a href="https://discord.com/invite/sF5CT5rzrR">
            🗣️ Chat &amp; Support
        </a>
    </h4>
</div>

> [!INFO]  
> This library has been audited as part of Semaphore V4: https://semaphore.pse.dev/Semaphore_4.0.0_Audit.pdf. The source
> has been moved from zk-kit to zk-kit.circom but remained the same.

## 🛠 Install

Install the `@zk-kit/binary-merkle-root.circom` package with npm:

```bash
npm i @zk-kit/binary-merkle-root.circom --save
```

or yarn:

```bash
yarn add @zk-kit/binary-merkle-root.circom
```

## 📜 Usage

Try out the circuit with [zkREPL](https://zkrepl.dev/?gist=fffaac93085b9a1ade2fb711706a9e98) on your browser or use
Circom locally:

```circom
include "binary-merkle-root.circom";

component main = BinaryMerkleRoot(5);
```

```bash
circom -l ./node_modules/@zk-kit/binary-merkle-root.circom/src -l ./node_modules/circomlib/circuits your-circuit.circom
```

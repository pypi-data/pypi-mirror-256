# The titanQ SDK for Python

![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue) ![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)

titanQ is the infinityQ Software Development Kit (SDK) for Python. The SDK facilitates and opens the way for faster implementation
of the titanQ solver without having to deal directly with the API.

This titanq package is maintained and published by [InfinityQ](https://www.infinityq.tech/)


## API Key

In order to use the titanQ service, a user needs an API key.
The API key can be obtained by contacting [InfinityQ support](support@infinityq.tech)


## Installation

The following steps assume that you have:

- A **valid** and **active** API Key
- A supported Python version installed


## Setting up an environment

``` bash
python -m venv .venv
.venv/bin/activate
```


## Install titanQ

``` bash
pip install titanq
```


## Using titanQ

The titanQ solver is designed to support very large problems and therefore very large files. To simplify the user experience, titanQ will instead use cloud storage set up and managed by the end users.

Currently, the SDK only supports two types of storage

| Storage options                | Vector variables limit           |
|--------------------------------|----------------------------------|
| S3 Buckets                     | ✅ Up to 100k vector variables   |
| Managed storage                | ⚠️ Up to 10k vector variables     |

Both options are documented with examples at the titanQ's [Quickstart documentation](https://docs.titanq.infinityq.io/quickstart/category/python-sdk)

## Problem construction

> **_NOTE:_**  The weights matrix must be symmetrical.

The QUBO problem is defined as finding the minimal energy configuration (the state $\mathbf{x}$ which results in the minimal $E(\mathbf{x})$).
Each state $\mathbf{x}$ is a vector of $n$ binary elements $x_i$ which can take the values of 0 or 1 (binary values).
This model formulation is given in the equation below

$
\begin{align}
argmin_{\mathbf{x}} \,\,\,\, E(\mathbf{x}) = \sum_{i=1}^n\sum_{i \leq j}^n Q_{i,j} x_i x_j \,\,\,\,\,\,\,\, \mathbf{x}=(x_i)\in \{0,1\}^{n} \notag
\end{align}
$

The bias terms of a QUBO model are stored along the diagonal of the $\mathbf{Q}$ matrix. However, to simplify converting between Ising and QUBO models,
we assume that the diagonals of the $\mathbf{Q}$  matrix are 0, and take in an additional bias vector instead. To avoid confusion, the modified $\mathbf{Q}$  matrix with 0s
along its diagonal is referred to as the *weights* matrix, denoted by

$
\begin{align}
\mathbf{W}=(W_{i,j})\in \mathbb{R}^{n \times n}, ~ where ~ \mathbf{Q} = \mathbf{W} + \mathbf{b}^{\intercal}\boldsymbol{I}, ~ and ~ \mathbf{b} = (b_i) \in \mathbb{R}^{n} \notag
\end{align}
$

denotes the *biases*, which are used in the final model formulation described below

$
\begin{align}
argmin_{\mathbf{x}} \, \, \, \, E(\mathbf{x}) & = \sum_{i=1}^n \sum_{i < j}^n W_{i,j}x_i x_j + \sum_i^n b_i x_i \notag \\
& = \frac{1}{2}\sum_{i=1}^n\sum_{j=1}^n W_{i,j}x_{i}x_{j} + \sum_{i=1}^{n} b_{i}x_{i} \notag \\
& = \frac{1}{2}(\mathbf{x}^{\intercal}\mathbf{W}\mathbf{x}) + \mathbf{b}^{\intercal}\mathbf{x} \notag
\end{align}
$

## Getting support or help


Further help can be obtained by contacting [InfinityQ support](support@infinityq.tech)
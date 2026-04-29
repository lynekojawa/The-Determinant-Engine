# 📐 Determinant Calculator

## 🧩Why I Built This
I built this because I wanted to have when I want this as undergraduate students. I studied and researched in ElGamal Encryption system in my undergraduate thesis and this required to use some computations, but by the time I was in undergraduate student I had to modify Mathematica script to drive the results that is why I build this determinant calculator that works in R and finite field. 

## 🧮 What It Does
It calculates determinants for you. Good to check your answers after practice. and hope to check your matrix is a good key for ElGamal-cannot guarantee! 

## 🏗️ Architecture & Phases
| Phase | Milestone | Logic Focus |
| :--- | :--- | :--- |
| **Phase 1** | The Square Base | Define the Matrix class. Implement basic properties ($n \times n$ check) and hardcoded logic for $1 \times 1$ and $2 \times 2$ cases. |
| **Phase 2** | The Laplace Engine | Implement the Cofactor Expansion algorithm. Focus on recursive sub-matrix slicing and sign alternating logic $(-1)^{i+j}$. |
| **Phase 3** | The $n \times m$ Pivot | Transition to Gaussian Elimination. Move from $O(n!)$ to $O(n^3)$ complexity using row reduction to Upper Triangular form. |
| **Phase 4** | The Visual Tensor | Wrap the engine in a Streamlit UI. Add LaTeX rendering and a step-by-step "Show Work" toggle. |

## 💻  Technical Stack
Python, Streamlit

## 🧠 What I Learned
In this project I learned that self built engine could be useful, and importing an engine file is strong tool. <br>
Phase 1 is always the hardest, it feels like staring at a blank canvas. <br>
Extending O(n!) to O(n^3) is also efficient to as n gets larger. <br>
Computer handle numbers weird, so I faced the number looks like 287648.0000000008 something like this which was annoying. <br>
It was first time I used classes and many new variables and functions <br> 

## 🚀 Current Status & Next Steps
*   **Status:** Currently completed, I reached my goal.
*   **Next Step:** Using this engine to create the cryptography program that demonstrates how ElGamal encryption works.
import streamlit as st
import numpy as np
import pandas as pd
from determinant_engine import Matrix

def matrix_to_latex(matrix):
    latex = r"\begin{bmatrix}"
    for row in matrix:
        latex += "&".join(map(str,row))+r"\\"
    latex += r"\end{bmatrix}"
    return latex
st.set_page_config(page_title="Determinant Calculator", layout = "centered")
st.title("Determinant Calculator")
st.write("It will calculate your determinant :D")
st.sidebar.header("⚙️ Setting")
mode= st.sidebar.radio("Calculation Mode", ["Standard (Float)", "Finite Field (F_q)"])
mod_val = None
if mode == "Finite Field (F_q)":
    mod_val =st.sidebar.number_input("Enter Prime (q)", value = 2)

dim_n = st.number_input("Enter dimensions (n x n)", min_value=1, max_value=10, value = 3)

initial_df = pd.DataFrame(np.zeros((dim_n, dim_n), dtype = int))
st.write("input your values")
edited_df = st.data_editor(initial_df, num_rows="fixed")

if st.button("Calculate"):
    matrix_data = edited_df.values.tolist()

    try:
        matrix = Matrix(matrix_data)
        st.write("input varriables")
        st.latex(f"A = {matrix_to_latex(matrix_data)}")

        det = matrix.calculate_determinant(mod=mod_val)

        st.success(f"RESULT: {int(round(det)) if mode == 'standard (Float)' else det}")

    except Exception as e:
        st.error("ERROR!")


class Matrix:
    def __init__(self, matrix_data):
        row_length = [len(row) for row in matrix_data]
        if len(set(row_length)) > 1:
            raise ValueError("All rows must have the same number of columns")

        self.matrix = matrix_data
        self.swap_count = 0

    def __repr__(self):
        if not self.matrix:
            return "[ ]"
        return "\n".join([f"[{', '.join(map(str, row))}]" for row in self.matrix])

    def get_row(self, index):
        return self.matrix[index]

    def get_col(self, index):
        return [row[index] for row in self.matrix]

    @property
    def shape(self):
        rows = len(self.matrix)
        cols = len(self.matrix[0]) if rows > 0 else 0
        return rows, cols

    @property
    def is_square(self):
        n, m = self.shape
        return n == m


    def get_minor(self, row_idx, col_idx):
        n, m = self.shape
        sub_data = [
            [self.matrix[r][c] for c in range(m) if c != col_idx]
            for r in range(n) if r != row_idx
        ]
        return Matrix(sub_data)

    def calculate_determinant(self, mod=None):
        if not self.is_square:
            raise ValueError("Determinant can only be calculated for a Square matrix!")
        original_matrix = [row[:] for row in self.matrix]
        n, m = self.shape

        if n == 1: return self.matrix[0][0] % mod if mod else self.matrix[0][0]
        if n == 2: return (self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]) % mod \
            if mod else (self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0])
        if n <= 3:
            result = 0
            for j in range(n):
                sign = 1 if j %2 ==0 else -1
                minor = self.get_minor(0,j)
#This is how recursive works
                sub_det = minor.calculate_determinant(mod)
                result += sign * self.matrix[0][j] * sub_det
            return result % mod if mod else result
        else:
            self.to_upper_triangular(mod)
            det = 1
            for i in range(n):
                det = (det * self.matrix[i][i]) % mod if mod else det * self.matrix[i][i]
            if self.swap_count % 2 != 0:
                det = -det
            det = det % mod if mod else det
            self.matrix = original_matrix
            return det

    def swap_rows(self, i,j):
        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
        self.swap_count += 1
        pass

    def add_scaled_row(self, target_idx, source_idx, scalar, mod = None):
        target = self.matrix[target_idx]
        source = self.matrix[source_idx]

        if mod is not None:
            updated_row = [(t + scalar *s) % mod for t, s in zip(target, source)]
        else:
            updated_row = [(t + scalar *s) for t, s in zip(target, source)]

        self.matrix[target_idx] = updated_row

    def to_upper_triangular(self, mod = None):
        n, m = self.shape
        self.swap_count = 0
        self.matrix = [row[:] for row in self.matrix]
        if mod is not None:
            self.matrix = [[int(val) % mod for val in row] for row in self.matrix]

        for j in range(n):
            pivot_row = j
            for i in range(j+1, n):
                if abs(self.matrix[i][j]) > abs(self.matrix[pivot_row][j]):
                    pivot_row = i

            if pivot_row != j:
                self.swap_rows(j, pivot_row)

            pivot_element = self.matrix[j][j]
            if pivot_element == 0:
                return

            inv_pivot = None
            if mod is not None:
                inv_pivot = pow(pivot_element, mod -2, mod)

            for k in range(j+1, n):
                element_to_zero = self.matrix[k][j]

                if mod is not None:
                    scalar = (-element_to_zero * inv_pivot) % mod
                else:
                    if abs(element_to_zero) < 1e-12:
                        continue
                    scalar = (-element_to_zero/pivot_element)

                self.add_scaled_row(k,j,scalar,mod)

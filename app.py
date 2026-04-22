#Today 4/22 I am going to review code with Dante, and there are four issues
#1. I had matrix class defined twice while I import it from my previous file: deleted, fixed
#2. Mod comparison: investigate: fixed?
#3. Error message: fixed
#4. Typo: fixed
#extra review with code: prompted you are an AI, and my logic orchestrator and find what can I make it better
#5. key=f"matrix_editor_{dim_n}" to set this will prevent from ghost data
#6. Latex float clean up,
#7. Int casting for finite field, changed the input values from integer to float, so that decimal can be calculated \bbZ to \bbR
#EX. This is something both of my agents wasn't catching, my result was coming out as input variables not a result :D
#EX2 Handling edge case of saving internally 10 into 10.00000002 due to some calculation.

import streamlit as st
import numpy as np
import pandas as pd
from determinant_engine import Matrix

def matrix_to_latex(matrix):
    latex = r"\begin{bmatrix}"
    for row in matrix:
        formatted_row =[]
        for v in row:
            if abs(v-round(v))<1e-12:
                formatted_row.append(str(int(round(v))))
            else:
                formatted_row.append(f"{v:.4f}")
        latex += "&".join(formatted_row) + r"\\"
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
    st.warning("In finite field, do not put any decimal")
dim_n = st.number_input("Enter dimensions (n x n)", min_value=1, max_value=10, value = 3)

initial_df = pd.DataFrame(np.zeros((dim_n, dim_n), dtype = float))
st.write("Input your values")
edited_df = st.data_editor(initial_df, num_rows="fixed", key = f"matrix_editor_{dim_n}")

if st.button("Calculate"):
    raw_data = edited_df.values.tolist()

    if mod_val is not None:
        matrix_data = [[int(x) for x in row] for row in raw_data]
    else:
        matrix_data = [[float(x) for x in row]for row in raw_data]
    try:
        matrix = Matrix(matrix_data)
        st.write("***Result***")
        st.latex(f"A = {matrix_to_latex(matrix_data)}")

        det = matrix.calculate_determinant(mod=mod_val)

        st.success(f"RESULT: {int(round(det)) if mode == 'Standard (Float)' else det}")

    except Exception as e:
        st.error(f"ERROR!: {e}")



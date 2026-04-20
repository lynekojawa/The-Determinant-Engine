# 4/20 We are jumping into phase 3 which is guassian elimination for the efficiency of the calculator.

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
        return "\n".join([f"[{','.join(map(str, row))}]" for row in self.matrix])

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

#phase 2 function
    def get_minor(self, row_idx, col_idx):
        n, m = self.shape
        sub_data = [
            [self.matrix[r][c] for c in range(m) if c != col_idx]
            for r in range(n) if r != row_idx
        ]

        return Matrix(sub_data)
#adding Gaussian eliminations in this function to efficiency.
#in O(n!) and O(n^3) when n=3 3!=6 and 3^3=27 HOWEVER when n =4 4!=24 and 4^3=64
#This is why we are dividing at n=3

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
#phase 3
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
#this happens because computer thinks .0000000000001 is not 0?
                if mod is not None:
                    scalar = (-element_to_zero * inv_pivot) % mod
                else:
                    if abs(element_to_zero) < 1e-12:
                        continue
                    scalar = (-element_to_zero/pivot_element)

                self.add_scaled_row(k,j,scalar,mod)






# --- Test Strike Zone ---
if __name__ == "__main__":
    print("=== Test v2.0 ===")
    try:
        n = int(input("Enter dimension of Square Matrix(n x n): "))


        print(f"Enter each row's elements separated by spaces (e.g, '1 2 3'):")

        user_matrix_data = []
        for i in range(n):
            row_input = input(f"Row {i + 1}: ")
            row_data = list(map(float, row_input.split()))
            user_matrix_data.append(row_data)

        user_matrix = Matrix(user_matrix_data)


        print("\n--- Ingested Matrix ---")
        print(user_matrix)
        print(f"Shape: {user_matrix.shape}")

        if user_matrix.is_square:
            std_det = user_matrix.calculate_determinant()
            print(f"Standard Determinant: {std_det}")
            int_matrix_data = [[int(x) for x in row] for row in user_matrix.matrix]
            int_matrix = Matrix(int_matrix_data)

            f2_det = int_matrix.calculate_determinant(mod = 2)
            print(f"Determinant in F2 (Modular Arithmetic): {f2_det}")
        else:
            print("Notice: This is not a Square Matrix. Determinant is undefined.")

    except ValueError as e:
        print(f"Critical Input Error: {e}")

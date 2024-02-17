/**
 * @file IVCSC_SparseMatrix.hpp
 * @author Skyler Ruiter and Seth Wolfgang
 * @brief IVCSC Sparse Matrix Class Declarations
 * @version 0.1
 * @date 2023-07-03
 */

#pragma once

namespace IVSparse {

    /**
     * @tparam T The data type of the values in the matrix
     * @tparam indexT The data type of the indices in the matrix
     * @tparam compressionLevel The compression level used
     * @tparam columnMajor Whether the matrix is stored in column major format
     *
     * A class to represent a sparse matrix compressed in the Compressed Sparse
     * Fiber format (IVSparse). \n \n IVSparse Sparse Matrix is a read-only matrix
     * class optimized for sparse-dense computation in cases where values are highly
     * redundant. For such cases, sparse fiber storage can reduce memory footprint
     * by up to 50% compared to standard sparse compression. IVSparse also increases
     * the ability to further compress index arrays within each run. This default
     * templated version is for compression3 specifically. For compression level 1
     * and 2 there are template specializations.
     */
    template <typename T, bool columnMajor = true>
    class IVCSC {
        private:
        //* The Matrix Data *//

        void** data = nullptr;         // The data of the matrix
        void** endPointers = nullptr;  // The pointers to the end of each column

        uint32_t innerDim = 0;  // The inner dimension of the matrix
        uint32_t outerDim = 0;  // The outer dimension of the matrix

        uint32_t numRows = 0;  // The number of rows in the matrix
        uint32_t numCols = 0;  // The number of columns in the matrix

        uint32_t nnz = 0;  // The number of non-zero values in the matrix

        size_t compSize = 0;  // The size of the compressed matrix in bytes

        //* The Value and Index Types *//

        uint32_t val_t;  // Information about the value type (size, signededness, etc.)
        uint32_t index_t;  // Information about the index type (size) (DEPRECATED)

        uint32_t* metadata = nullptr;  // The metadata of the matrix

        //* Private Methods *//

        // Calculates the number of bytes needed to store a value
        inline uint8_t byteWidth(size_t size);

        //* Private Methods *//

        // Compression Algorithm for going from CSC to VCSC or IVCSC
        template <typename T2, typename indexT>
        void compressCSC(T2* vals, indexT* innerIndices, indexT* outerPointers);


        // Takes info about the value type and encodes it into a single uint32_t
        void encodeValueType();

        // Checks the value type matches the class template T
        void checkValueType();

        // Does checks on the class to ensure it is valid
        void userChecks();

        // Method to calcuate and set the byte size of the matrix in memory
        void calculateCompSize();

        // Scalar Multiplication
        inline IVSparse::IVCSC<T, columnMajor>scalarMultiply(T scalar);

        // In Place Scalar Multiplication
        inline void inPlaceScalarMultiply(T scalar);

        // Matrix Vector Multiplication
        inline Eigen::Matrix<T, -1, 1> vectorMultiply(Eigen::Matrix<T, -1, 1>& vec);

        // Matrix Matrix Multiplication
        inline Eigen::Matrix<T, -1, -1> matrixMultiply(Eigen::Matrix<T, -1, -1> mat);

        // helper for ostream operator
        void printHelper(std::ostream& stream);
        void printHelper(std::stringstream& stream);

        public:

        // Gets the number of rows in the matrix
        uint32_t rows() const { return numRows; }

        // Gets the number of columns in the matrix
        uint32_t cols() const { return numCols; }

        // Gets the inner dimension of the matrix
        uint32_t innerSize() const { return innerDim; }

        // Gets the outer dimension of the matrix
        uint32_t outerSize() const { return outerDim; }

        // Gets the number of non-zero elements in the matrix
        uint32_t nonZeros() const { return nnz; }

        // Gets the number of bytes needed to store the matrix
        size_t byteSize() const { return compSize; }


        //* Nested Subclasses *//

        // Iterator Class for IVCSC Sparse Matrix
        class InnerIterator;

        //* Constructors *//
        /** @name Constructors
         */
         ///@{

         /**
          * Construct an empty IVSparse matrix \n \n
          * The matrix will have 0 rows and 0 columns and
          * will not be initialized with any values. All data
          * will be set to nullptr.
          *
          * @warning This constructor is not recommended for use as updating a IVSparse
          * matrix is not well supported.
          */
        IVCSC() {};

        // Private Helper Constructor for tranposing a IVSparse matrix
        template <typename indexT>
        IVCSC(std::unordered_map<T, std::vector<indexT>>* maps, uint32_t num_rows, uint32_t num_cols);


        /**
         * Empty Constructor \n \n
         * Takes in the number of rows and cols desired for an all zero matrix
         * of the specified size. All data will be set to nullptr.
         */
        IVCSC(uint32_t num_rows, uint32_t num_cols);

        /**
         * @param mat The Eigen Sparse Matrix to be compressed
         *
         * Eigen Sparse Matrix Constructor \n \n
         * This constructor takes an Eigen Sparse Matrix and compresses it into a
         * IVSparse matrix.
         */
        IVCSC(Eigen::SparseMatrix<T>& mat);

        /**
         * @param mat The Eigen Sparse Matrix to be compressed
         *
         * Eigen Sparse Matrix Constructor (Row Major) \n \n
         * Same as previous constructor but for Row Major Eigen Sparse Matrices.
         */
        IVCSC(Eigen::SparseMatrix<T, Eigen::RowMajor>& mat);

        /**
         * @tparam compressionLevel2 The compression level of the IVSparse matrix to
         * convert
         * @param mat The IVSparse matrix to convert
         *
         * Convert a IVSparse matrix of a different compression level to this
         * compression level. \n \n This constructor takes in a IVSparse matrix of the
         * same storage order, value, and index type and converts it to a different
         * compresion level. This is useful for converting between compression levels
         * without having to go through the CSC format.
         */
        template <typename indexT>
        IVCSC(IVSparse::VCSC<T, indexT, columnMajor>& other);

        /**
         * @param other The IVSparse matrix to be copied
         *
         * Deep Copy Constructor \n \n
         * This constructor takes in a IVSparse matrix and creates a deep copy of it.
         */
        IVCSC(const IVSparse::IVCSC<T, columnMajor>& other);

        /**
         * Raw CSC Constructor \n \n
         * This constructor takes in raw CSC storage format pointers and converts it
         * to a IVSparse matrix. One could also take this information and convert to
         * an Eigen Sparse Matrix and then to a IVSparse matrix.
         */
        template <typename T2, typename indexT>
        IVCSC(T2* vals, indexT* innerIndices, indexT* outerPtr, uint32_t num_rows, uint32_t num_cols, uint32_t nnz);

        /**
         * COO Tuples Constructor \n \n
         * This constructor takes in a list of tuples in COO format which can be
         * unsorted but without duplicates. The tuples are sorted and then converted
         * to a IVSparse matrix.
         *
         * @note COO is (row, col, value) format.
         *
         * @warning This constructor does not allow for duplicates but will sort the
         * tuples.
         */
        template <typename T2, typename indexT>
        IVCSC(std::vector<std::tuple<indexT, indexT, T2>>& entries, uint64_t num_rows, uint32_t num_cols, uint32_t nnz);

        /**
         * @param filename The filepath of the matrix to be read in
         *
         * File Constructor \n \n
         * Given a filepath to a IVSparse matrix written to file this constructor will
         * read in the matrix and construct it.
         */
        IVCSC(char* filename);

        /**
         * @brief Destroy the Sparse Matrix object
         */
        ~IVCSC();

        ///@}

        //* Getters *//
        /**
         * @name Getters
         */
         ///@{

         /**
          * @returns T The value at the specified row and column. Returns 0 if the
          * value is not found.
          *
          * Get the value at the specified row and column
          *
          * @note Users cannot update individual values in a IVSparse matrix.
          *
          * @warning This method is not efficient and should not be used in performance
          * critical code.
          */
        T coeff(uint32_t row, uint32_t col);

        /**
         * @returns true If the matrix is stored in column major format
         * @returns false If the matrix is stored in row major format
         *
         * See the storage order of the IVSparse matrix.
         */
        bool isColumnMajor() const;

        /**
         * @param vec The vector to get the pointer to
         * @returns void* The pointer to the vector
         *
         * Get a pointer to a vector in the IVSparse matrix such as the first column.
         *
         * @note Can only get vectors in the storage order of the matrix.
         */
        void* vectorPointer(uint32_t vec);

        /**
         * @param vec The vector to get the size of
         * @returns size_t The size of the vector in bytes
         *
         * Get the size of a vector in the IVSparse matrix in bytes.
         *
         * @note Can only get vectors in the storage order of the matrix.
         */
        size_t getVectorByteSize(uint32_t vec) const;

        ///@}

        //* Calculations *//
        /**
         * @name Calculations
         */
         ///@{

         /**
          * @returns A vector of the sum of each vector along the outer dimension.
          */
        inline Eigen::Matrix<T, -1, -1> colSum();

        /**
         * @returns A vector of the sum of each vector along the inner dimension.
         */
        inline Eigen::Matrix<T, -1, -1> rowSum();

        /**
         * Note: axis = 0 for a column sum and axis = 1 for row sum.
         *       For min coefficient in matrix, there is an overloaded
         *       method without a paramter.
         * 
         * @returns An Eigen::Matrix of the min value along specified axis
        */

        inline Eigen::Matrix<T, -1, -1> min(int axis);

        /**
         * @returns The min value in the matrix.
         */

        inline T min();

        /**
         * Note: axis = 0 for a column sum and axis = 1 for row sum.
         *       For max coefficient in matrix, there is an overloaded
         *       method without a paramter.
         * 
         * @returns An Eigen::Matrix of the max value along specified axis
        */

        inline Eigen::Matrix<T, -1, -1> max(int axis);

        /**
         * @returns The max value in the matrix.
         */

        inline T max();

        /**
         * @returns The trace of the matrix.
         *
         * @note Only works for square matrices.
         */
        template<typename T2 = T, std::enable_if_t<std::is_integral<T2>::value, bool> = true>
        inline int64_t trace();

        template<typename T2 = T, std::enable_if_t<std::is_floating_point<T2>::value, bool> = true>
        inline double trace();

        /**
         * @returns The sum of all the values in the matrix.
         */

        template<typename T2 = T, std::enable_if_t<std::is_integral<T2>::value, bool> = true>
        inline int64_t sum();

        template<typename T2 = T, std::enable_if_t<std::is_floating_point<T2>::value, bool> = true>
        inline double sum();

        /**
         * @returns The frobenius norm of the matrix.
         */
        inline double norm();

        /**
         * @returns Returns the length of the specified vector.
         */
        inline double vectorLength(uint32_t vec);

        ///@}

        //* Utility Methods *//
        /**
         * @name Utility Methods
         */
         ///@{

         /**
          * @param filename The filename of the matrix to write to
          *
          * This method writes the IVSparse matrix to a file in binary format.
          * This can then be read in later using the file constructor.
          * Currently .ivsparse is the perfered file extension.
          *
          * @note Useful to split a matrix up and then write each part separately.
          */
        void write(char* filename);


        /**
         * @param filename The filename of the matrix to read from
         * 
         * This method overwrites the current matrix with the matrix read in from the
         * file. The file must be written by the write method.
         * 
        */

        void read(char* filename);

        /**
         * Prints "IVSparse Matrix:" followed by the dense representation of the
         * matrix to the console.
         *
         * @note Useful for debugging but only goes up to 100 of either dimension.
         */
        void print();

        /**
         * @returns The current matrix as a VCSC Matrix.
         */
        template <typename indexT>
        IVSparse::VCSC<T, indexT, columnMajor> toVCSC();

        /**
         * @returns An Eigen Sparse Matrix constructed from the IVSparse matrix data.
         */
        Eigen::SparseMatrix<T, columnMajor ? Eigen::ColMajor : Eigen::RowMajor> toEigen();

        ///@}

        //* Matrix Manipulation Methods *//
        /**
         * @name Matrix Manipulation Methods
         */
         ///@{

         /**
          * @returns A transposed version of the IVSparse matrix.
          *
          * @warning This method is not very efficient for VCSC and IVCSC matrices.
          */
        IVSparse::IVCSC<T, columnMajor> transpose();

        /**
         * Transposes the matrix in place instead of returning a new matrix.
         *
         * @warning This method is not very efficient for VCSC and IVCSC matrices.
         */
        void inPlaceTranspose();

        /**
         * @param mat The matrix to append to the matrix in the correct storage order.
         *
         * Appends an IVSparse matrix to the current matrix in the storage order of the
         * matrix.
         */
        void append(IVCSC<T, columnMajor>& mat);

        /**
         * @param mat The matrix to append to the matrix in the correct storage order.
         *
         * Appends an Eigen::SparseMatrix to the current matrix in the storage order of the
         * matrix. This converts the Eigen::SparseMatrix to an IVSparse matrix.
         */

        inline void append(Eigen::SparseMatrix<T, columnMajor ? Eigen::ColMajor : Eigen::RowMajor>& mat);


        /**
         * @brief Appends a raw CSC matrix to the current matrix. Assumes correct storage order.
         * @tparam T2
         * @tparam indexT2
         * @param vals
         * @param innerIndices
         * @param outerPtr
         * @param num_rows
         * @param num_cols
         * @param nnz
         */
        template <typename T2, typename indexT>
        inline void append(T2* vals, indexT* innerIndices, indexT* outerPtr, uint32_t num_rows, uint32_t num_cols, uint32_t nnz);


        /**
         * @returns A matrix that represent a slice of the
         * IVSparse matrix.
         */
        IVSparse::IVCSC<T, columnMajor> slice(uint32_t start, uint32_t end);

        ///@}

        //* Operator Overloads *//

        friend std::ostream& operator<< (std::ostream& stream, IVSparse::IVCSC<T, columnMajor>& mat) {
            mat.printHelper(stream);
            return stream;
        }

        friend std::stringstream& operator<< (std::stringstream& stream, IVSparse::IVCSC<T, columnMajor>& mat) {
            mat.printHelper(stream);
            return stream;
        }
        // Assignment Operator
        IVSparse::IVCSC<T, columnMajor>& operator=(const IVSparse::IVCSC<T, columnMajor>& other);

        // Equality Operator
        bool operator==(const IVCSC<T, columnMajor>& other) const;

        // Inequality Operator
        bool operator!=(const IVCSC<T, columnMajor>& other);

        // Coefficient Access Operator
        T operator()(uint32_t row, uint32_t col);

        // Scalar Multiplication
        IVSparse::IVCSC<T, columnMajor> operator*(T scalar);

        // In Place Scalar Multiplication
        void operator*=(T scalar);

        // Matrix Vector Multiplication
        Eigen::Matrix<T, -1, 1> operator*(Eigen::Matrix<T, -1, 1>& vec);
        Eigen::Matrix<T, -1, 1> operator*(const Eigen::Ref<const Eigen::Matrix<T, -1, 1>>& mat);

        // Matrix Matrix Multiplication
        Eigen::Matrix<T, -1, -1> operator*(Eigen::Matrix<T, -1, -1>& mat);
        Eigen::Matrix<T, -1, -1> operator*(const Eigen::Ref<const Eigen::Matrix<T, -1, -1>>& mat);

    };  // End of SparseMatrix Class

}  // namespace IVSparse
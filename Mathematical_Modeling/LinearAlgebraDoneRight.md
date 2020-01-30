# A Personal Note of *Linear Algebra Done Right*🌠

```txt
Created Date: Thursday, January 30th 2020, 5:33:26 pm
Author: ZeFeng Zhu
```

## Preface for the Instructor

> Almost all linear algebra books use determinants to prove that every linear operator on a ﬁnite-dimensional complex vector space has an eigenvalue. Determinants are difﬁcult, nonintuitive, and often deﬁned without motivation.

 * To prove the theorem about existence of `eigenvalues` on `complex vector spaces`
   * most books must define `determinants`, prove that a linear map is not invertible if and only if its determinant equals 0
   * and then define the `characteristic polynomial`.

> This tortuous (torturous?) path gives students little feeling for why eigenvalues exist.

* In contrast, the simple determinant-free proofs presented here(for example, see 5.21) offer more insight
  * Once determinants have been banished to the **end** of the book, a new route opens to the main goal of linear algebra understanding the structure of `linear operators`

### Here is a chapter-by-chapter summary of the highlights of the book

* Chapter 1: `Vector spaces` are defined in this chapter, and their basic properties are developed
* Chapter 2: `Linear independence, span, basis, and dimension` are defined in this chapter, which presents the basic theory of finite-dimensional vector spaces
* Chapter 3: `Linear maps` are introduced in this chapter. The key result here is the Fundamental Theorem of Linear Maps (3.22): if $T$ is a linear map on $V$,then $\dim V = \dim \text{null}\, T +  \dim \text{range}\, T$. `Quotient spaces` and `duality` are topics in this chapter at a higher level of abstraction than other parts of the book; these topics can be skipped without running into problems elsewhere in the book
* Chapter 4: The part of the theory of `polynomials` that will be needed to understand linear operators is presented in this chapter. This chapter contains no linear algebra. It can be covered quickly, especially if your students are already familiar with these results
* Chapter 5: The idea of studying a linear operator by restricting it to small `subspaces` leads to eigenvectors in the early part of this chapter. **The highlight of this chapter is a simple proof that on complex vector spaces, eigenvalues always exist.** This result is then used to show that each linear operator on a complex vector space has an upper-triangular matrix with respect to some basis. All this is done without defining determinants or characteristic polynomials!
* Chapter 6: `Inner product spaces` are defined in this chapter, and their basic properties are developed along with standard tools such as `orthonormal bases` and the `Gram–Schmidt Procedure`. This chapter also shows how orthogonal projections can be used to solve certain minimization problems
* Chapter 7: `The Spectral Theorem`, which characterizes the linear operators for which there exists an orthonormal basis consisting of eigenvectors, is the highlight of this chapter. The work in earlier chapters **pays off** here with especially simple proofs. This chapter also deals with `positive operators`, `isometries`, the `Polar Decomposition`, and the `Singular Value Decomposition`
* Chapter 8: `Minimal polynomials`, `characteristic polynomials`, and `generalized eigenvectors` are introduced in this chapter. **The main achievement of this chapter is the description of a linear operator on a complex vector space in terms of its generalized eigenvectors.** This description enables one to prove many of the results usually proved using Jordan Form. For example, these tools are used to prove that every invertible linear operator on a complex vector space has a square root. The chapter concludes with a proof that every linear operator on a complex vector space can be put into Jordan Form.
* Chapter 9: Linear operators on real vector spaces occupy center stage in this chapter. Here the main technique is `complexification`,which is a natural extension of an operator on a real vector space to an operator on a complex vector space. **Complexification allows our results about complex vector spaces to be transferred easily to real vector spaces**. For example, this technique is used to show that every linear operator on a real vector space has an invariant subspace of dimension 1 or 2. As another example, we show that every linear operator on an odd-dimensional real vector space has an eigenvalue
* Chapter 10: The `trace` and `determinant` (on complex vector spaces) are defined in this chapter as the sum of the eigenvalues and the product of the eigenvalues, both counting multiplicity. **These easy-to-remember definitions would not be possible with the traditional approach to eigenvalues, because the traditional method uses determinants to prove that sufficient eigenvalues exist.** The standard theorems about determinants now become much clearer. The Polar Decomposition and the Real Spectral Theorem are used to derive the change of variables formula for multivariable integrals in a fashion that makes the appearance of the determinant there seem natural.

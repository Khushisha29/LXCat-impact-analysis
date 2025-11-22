Contents lists available at [ScienceDirect](http://www.ScienceDirect.com/)

# Journal of Computational Physics

[www.elsevier.com/locate/jcp](http://www.elsevier.com/locate/jcp)

# Numerical solution of the electron transport equation in the upper atmosphere ✩

M. Woods <sup>a</sup>*,*∗, W. Sailor a, M. Holmes <sup>b</sup>

- <sup>a</sup> *Department of Phenomenology and Sensor Science, Sandia National Laboratories, Albuquerque, NM 87185, United States of America*
- <sup>b</sup> *Department of Mathematical Sciences, Rensselaer Polytechnic Institute, Troy, NY 12180, United States of America*

#### a r t i c l e i n f o a b s t r a c t

*Article history:* Received 9 February 2018 Received in revised form 7 September 2018 Accepted 10 September 2018 Available online 2 October 2018

*Keywords:* Integro-differential equation Stiff boundary value problem Upwind difference method Electron transport Upper atmosphere

A new approach for solving the electron transport equation in the upper atmosphere is derived. The problem is a very stiff boundary value problem, and to obtain an accurate numerical solution, matrix factorizations are used to decouple the fast and slow modes. A stable finite difference method is applied to each mode. This solver is applied to a simplified problem for which an exact solution exists using various versions of the boundary conditions that might arise in a natural auroral display. The numerical and exact solutions are found to agree with each other, verifying the method.

© 2018 Elsevier Inc. All rights reserved.

# **1. Introduction**

The principle cause of the aurora is charged particles from the sun interacting with the earth's upper atmosphere. During a solar storm, the sun releases charged particles called the solar wind, which consists mostly of electrons and protons. Some of these particles reach the earth where they accelerate along the magnetic field lines which converge at the poles. Once the particles reach sufficiently low altitudes they scatter off atmospheric atoms and molecules. This scattering causes the atoms and molecules to enter excited states, and they return to their ground states via collisional quenching and fluorescence. Most of the auroral light is due to electron impact excitations, which is why we focus on electron transport. A more comprehensive explanation of how this occurs can be found in Rees [\[1\]](#page-14-0).

The electron transport problem can be modeled as an integro-differential equation. What is challenging about the problem is the unusual way the boundary conditions are split between the upper and lower limits of the atmosphere, and the pronounced boundary-layer structure of the solution due to the stiffness of the equation. Both Monte Carlo and deterministic methods have been used, but only the latter are more relevant to our study. The most well-known approach is due to Stamnes et al. [\[2\]](#page-14-0). This method subdivides the atmosphere into layers, and in each layer the problem is replaced by one with constant coefficients. The source term is approximated by an exponential, and the system of equations is solved exactly within each layer. These layers are patched together by requiring the solution to be continuous. This method has been used

*E-mail address:* [mcwood@sandia.gov](mailto:mcwood@sandia.gov) (M. Woods).

<sup>✩</sup> The authors gratefully acknowledge support from the Sandia National Laboratories Campus Executive Program, which is funded by the Laboratory Directed Research and Development (LDRD) Program.

<sup>\*</sup> Corresponding author.

<span id="page-1-0"></span>**Fig. 1.** An example electron intensity solution at 1.2 eV.

**Fig. 2.** The same intensity on a logarithmic scale.

in Stamnes [\[3\]](#page-14-0), Lummerzheim et al. [\[4\]](#page-15-0), Min et al. [\[5\]](#page-15-0), Lummerzheim and Lilensten [\[6\]](#page-15-0), and most recently in Lanchester and Gustavsson [\[7\]](#page-15-0).

What has been missed in the above and other numerical methods is an accurate accounting of the lower atmosphere. To explain, at the upper boundary a downward electron distribution is specified. Similarly, at some low altitude the upward electron distribution is set to zero. The top of the upper atmosphere is simply chosen to be an altitude where the density is relatively small and scattering effects are negligible. The bottom of the atmosphere is more troublesome. Theoretically, the ground (an altitude of zero) could be chosen because there are no free electrons at ground level. However, the electron transport equation has the property of becoming exponentially stiff at lower altitudes. This region can be avoided by prescribing a lower boundary that is far from ground level, but this yields a model which is not physically meaningful. On the other hand, if a more realistic lower boundary is used then standard numerical methods, such as collocation at Gaussian or Lobatto points, will produce negative and oscillating solutions due to the exponential stiffness.

Regardless of what low altitude is chosen, the solution must smoothly approach zero as the altitude decreases. Typical auroral electron intensities approach zero somewhere below 100 km where the exact altitude is dependent on the strength of the solar wind. This is exactly the region where the problem is exponentially stiff. A strong solar wind can give electron intensities on the order of 108 *e*<sup>−</sup> s−<sup>1</sup> cm−<sup>2</sup> eV−<sup>1</sup> sr−<sup>1</sup> or more (see Arnoldy and Lewis [\[8\]](#page-15-0) and Solomon et al. [\[9\]](#page-15-0)). This means that the numerical solution of the electron transport equation must drop many orders of magnitude over a few dozen km. The very rapid drop in intensity as the electrons approach the lower altitudes causes most solvers, even those designed for stiff problems, to overshoot or oscillate. The resulting negative intensities are physically meaningless, and the problem is unstable in such cases. In Figs. 1 and 2, we show an example of downward streaming electron intensities for 1*.*2 eV electrons (the curves come from solutions to a numerical example given in Section [5\)](#page-12-0). This energy was chosen because there is a greater abundance of low energy electrons, so the change in scale is readily apparent. The point, however, is that the numerical solution should approach zero as altitude decreases without overshoot or oscillation.

Fig. 3. The geometry of the electron transport problem.

For the most part, studies of the electron transport problem deemphasize the boundary conditions. Although they may be briefly mentioned, there is little discussion or explanation of the numerical complications they introduce. Some do not mention the boundary conditions at all (see Stamnes [3] for example) and some do not give enough detail to understand what exactly they used as a boundary condition (see Porter et al. [10] for example). In particular, almost all articles neglect to mention the consequences of how to handle the lower boundary. Only Mantas [11] discusses the difficulty of choosing the lower boundary and that negative intensities lead to instabilities and meaningless solutions. In a later article however, this same author uses an arbitrary reflecting lower boundary condition (see Mantas and Bowhill [12]). He forces 60% of all electrons reaching an altitude of 120 km back upward. The claim is made that although this is not realistic, the condition does not adversely affect the solution.

The computational algorithm developed here to solve the electron transport equation uses a generalized Legendre polynomial approximation for the elastic scattering integral followed by an eigenvalue decomposition to delineate the relevant scales needed to resolve the solution. To begin, in Section 2, the electron transport equation is described. In Section 3 the generalized Legendre polynomial approximation is used to reduce the electron transport equation to the form that is solved numerically. Section 4 provides the methodology for solving a stiff boundary value problem by adapting the work of Kreiss et al. [13]. Finally, in Section 5, our numerical solution is compared to a case where an exact solution is possible, showing the effectiveness of the numerical method.

#### 2. Mathematical model

In order to quantify electron transport, we use the electron intensity    where    is electron position in Cartesian coordinates,    is electron velocity in spherical coordinates, and t is time. Electron intensity is related to the electron distribution function, and its units are    (see Rees [1]). An equation for electron intensity can be derived from the continuity equation (see Woods [14] for the derivation). To obtain this equation, a few assumptions are made.

First, we consider the steady state problem. This is reasonable because the time it takes for an electron to penetrate the atmosphere is small compared to the time it takes for the aurora to change. The second assumption is that the atmosphere can be modeled as horizontally stratified. This is reasonable because the atmospheric density gradient in the local vertical direction is much larger than in any local horizontal direction. Finally, we assume a uniform magnetic field. For the altitudes we are considering, the curvature of the earth's magnetic field has a negligible effect, so we consider it to be uniform. A consequence of this final assumption is that the electron intensity is invariant under rotations about the magnetic field lines. This is because an electron travels in a helical path in a uniform magnetic field. With these assumptions, the electron intensity becomes a function of three variables: altitude z (which we take to be the local vertical direction), kinetic energy E, and the cosine of the pitch angle   . The geometry is shown in Fig. 3. We see that an electron travels in a helical path about the magnetic field lines, and once it scatters off an atom, it travels in a different helical path (i.e., a possibly different pitch angle and energy). The angle between the electron's velocity vector and the magnetic field is the pitch angle   , and the angle between the local horizontal and the magnetic field is the magnetic field in angle   . The magnetic field lines converge at the poles of the earth which is why auroras are only seen at high and low latitudes.

If we assume the only processes are in-scattering and out-scattering, then the electron transport equation is given by

<span id="page-3-0"></span>**Table 1**The functions of (1) are defined.

where the species under consideration are   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,   ,

Equation (1) describes how the electron intensity changes with respect to altitude. For every species, there is a chance for elastic scattering (second term on the right-hand-side), excitation scattering (third term on the right-hand-side), and single ionization scattering (final two terms on the right-hand-side). We model these events as the production of a new electron (or two new electrons in the case of single ionization). Although it is physically the same electron (except for the secondary electron produced in the ionization), it has a new pitch angle if the scattering was elastic or a new kinetic energy if the scattering was inelastic. The first term on the right-hand-side serves to remove the electron with the pre-scattering pitch angle and kinetic energy.

The elastic scattering probability density functions (also called the phase functions) are given by (see Rees [1])

(2)

where    is an energy dependent parameter that will be discussed in more detail along with (2) in Section 3. The ionization probability density functions are given by (see again Rees [1])

(3)

and

where the normalization functions    are determined from

 (5)

<span id="page-4-0"></span>Fig. 4. The atomic oxygen phase function at E = 10000 eV.

There exist sophisticated models of the atmosphere, and obtaining    for all species listed above except NO can be found in Hedin [15]. The number densities for NO can be found in Sharma et al. [16]. In addition, numerous scatting experiments and theoretical calculations have been performed that give the necessary cross sections. For this study, we used Laher and Gilmore [17], Itikawa and Ichimura [18], Salvat et al. [19], Pancheshnyi et al. [20], Morgan [21], Itikawa [22], Phelps [23], Biagi [24], Alves [25], Itikawa [26], Ionin et al. [27], Kim et al. [28], Hayashi [29], and Cartwright et al. [30].

Finally, the ranges for the electron kinetic energy E and pitch angle cosines    are

and the domain of equation (1) is

The boundary conditions are given by

 (8)

These conditions give the intensity entering at each end of the domain. Both endpoints must be chosen. The top of the atmosphere    can simply be chosen to be any altitude where the atmosphere is sufficiently thin so that scattering is negligible. We shall choose    km. The bottom of the atmosphere    is more difficult. This is an altitude where there is no upward intensity. We could simply choose the ground (  ), but this is not a good choice due to the extreme stiffness of the problem at low altitudes. This stiffness causes rapid oscillations and negative intensities (which are meaningless) in the numerical solution for most solvers unless a very large number of points are placed in the mesh. We will soon see that the number of points becomes so large that it is impractical. On the other hand, if    is chosen too high (say 100 km), then we will not find a true solution because we will be ignoring the physics of how the intensity decays to zero. The approach we will take is to choose an altitude where the electron intensity is clearly zero. Figs. 1 and 2 show that    km is adequate.

#### 3. The  -M method

In order to discretize (1), the integrals should be approximated by appropriate quadrature sums. Many quadrature techniques approximate the integrand by a low-order polynomial or a piecewise polynomial. The problem here is that the phase function for elastic scattering    is not well approximated by a low-order polynomial due to the fact that it contains sharp peaks at   . In Figs. 4 and 5, we show the phase function for atomic oxygen at E=10000 eV and E=10000 eV, respectively. We see that even at 10000 eV and E=1, the phase function is forward-peaked enough that a low order polynomial approximation is not adequate. The problem is much more pronounced at 100000 eV, and an inordinate number of points would be required to approximate it with polynomials. Fortunately, there is an idea called the   -M method, originally formulated by Wiscombe [31] for radiative transfer, that overcomes this difficulty. The formulas used here are slightly different than the original formulation, but the concepts are the same.

If we expand the phase function in an infinite series

(9)

where    is the mth degree Legendre polynomial and the    are the phase function moments, then it can be shown that (see Woods [14])

<span id="page-5-0"></span>**Fig. 5.** The atomic oxygen phase function at E = 100000 eV.

and the remaining moments are found through recursion

 (12)

As mentioned earlier, the phase function is not well approximated by a low-order polynomial due to the sharp peak at   . The idea behind the   -M method is to approximate    by a Dirac delta function and M Legendre polynomials. This way, the delta function can capture the sharp peak and the polynomials can capture the rest. Let our approximation be

(13)

where    is the "fraction" that represents the sharp peak and    are the modified moments. From this, we can find

(15)

Putting everything together, the electron transport equation is now given by

The power of the   -M method is that M does not need to be large to accurately approximate the elastic scattering integral. This means that a small number of points can be used, which greatly reduces the amount of computation.

<span id="page-6-0"></span>**Table 2**The largest eigenvalues of (17) for some representative cases.

#### 4. Numerical solution

Equations (16) and (8) together form a two-point linear boundary value problem (BVP). In order to write this in standard BVP form, we must discretize the equation in both energy and pitch angle cosine. Since upscattering is not possible, the system can be solved as a series of mono-energetic problems. The energy grid can then be specified between the high energies (100000 eV for auroral studies) and low energies (for this work, we went as low as 1 eV). The number of points used in the energy grid depends entirely on how rapidly the cross sections change. We found that for the higher energies, 20–30 points per decade and no more than 50 points per decade at lower energies worked well. As we will soon see, the BVP method we used is first order accurate, so we used a linear interpolation for approximating    and the trapezoid rule for the energy integrals.

For the angular discretization, we simply replace the integral over pitch angle cosine with a Gaussian quadrature sum. Following Stamnes and Swanson [32], we use the "double-Gauss" rule where the M point Gaussian quadrature is applied to each half of the interval (this is the same M that appears in equation (16)). That is, the M point Gaussian rule is applied to (-1,0) and the M point Gaussian rule is applied to (0,1). Some authors use the double-Gauss rule because it allows one to easily compute the upward or downward flux (integral of    over each half interval). We chose it simply because the electron intensity can be discontinuous across   . We found that M=10 was more than adequate for this study.

When we apply the above discretizations, we find

where    is the electron intensity vector,    is a matrix built from the angular discretization of the elastic scattering integral and    is a vector built from the inelastic scattering terms. The boundary conditions (8) are straightforward to discretize. A common method for solving this type of problem is either Gaussian or Lobatto collocation (see Ascher et al. [33]). The idea behind these methods is to choose a set of points in the domain (called the collocation points) and satisfy the differential equation at those points using piecewise polynomials of a certain degree. The difference between Gaussian and Lobatto collocation is the choice of collocation points. These methods are common because they are excellent for non-stiff and moderately stiff problems and software is freely available.

However, upon inspecting (16), we see that the atmospheric number density multiplies the entire right-hand-side, meaning that the eigenvalues of the system will be approximately proportional to the dominant density at every altitude. From Hedin [15], we know that at an altitude of 0 km, the density is on the order of    cm<sup>-3</sup> and at 1000 km, the density is on the order of    cm<sup>-3</sup>. Since these densities span many orders of magnitude, so do the eigenvalues of the system. Therefore at the lower altitudes, equation (16) is very stiff.

The stiffness of the problem can be characterized by the largest eigenvalues of the discretized system    in (17). The largest eigenvalues for some representative cases are shown in Table 2. We see that the eigenvalues indeed span many orders of magnitude. Using a low order BVP solver, it is not unreasonable to require that the product of the local step size and largest local eigenvalue be less than 2. It is well known that keeping this product small helps keep the error small (see Ascher and Petzold [34]). Table 2 shows that this is not a problem for the high altitudes. Step sizes on the order of kilometers are possible at all energies. However, at the low altitudes this requires step sizes on the order of centimeters for 100000 eV and microns for 10 eV. Clearly, if we wish to accurately solve the problem without using hundreds of thousands of points, something else must be done.

The problem under consideration qualifies as being a very stiff, or an exponentially stiff BVP. We make a distinction between a stiff and a very stiff BVP. For the latter, the relevant length scales change dramatically in the boundary layer with the result that standard stiff methods are not capable of accurately finding the solution. The fact that the electron transport equation qualifies as being very stiff is evident in Fig. 2. This is likely the reason why all previous numerical attempts at solving this problem have made spurious assumptions such as 60% of all electrons reaching 120 km are reflected back upward. Numerical methods for very stiff BVPs are not widely used or well-known. The purpose of this section is to describe an upwind numerical method that avoids these spurious assumptions.

#### <span id="page-7-0"></span>4.1. Overview of the upwind method

To explain what is done in the upwind method, consider the problem

(18)

with boundary conditions

where   ,   ,    and   ,   ,   . In Woods [14], it is shown how (16) can be reduced to this form. It turns out that the eigenvalues for the electron transport problem are real, so we will assume real eigenvalues throughout this section. The method we will use is originally from Kreiss et al. [13]. These authors were principally focused on proving error estimates and did not adequately explain its implementation. Consequently, we will here be focused on implementation.

Throughout this section, we will assume some mesh    with    for    and

In addition, all norms used denote the infinity norm unless otherwise specified. The notation

will be used throughout for the norm of a vector function    on an interval   .

As stated in Kreiss et al. [13], a function    is resolved on an interval    if

for    where   . The degree of smoothness p can vary with the BVP. The importance of using a mesh that resolves the solution follows from the error analysis for any finite difference method. For example, the local truncation error for the trapezoidal rule is bounded by   . For non-stiff BVPs,    can be made small enough so that this error is small. However, for a stiff BVP the derivatives of the solution can be very large so that the error is large unless if    is made prohibitively small. For this reason, a solution is only resolved if a number p of its derivatives are bounded by a constant K that is not too large (i.e.   ). Further, if    is resolved on    and   , then it is resolved on   . This means that we only need to worry about resolving    in the neighborhood of every point   .

The obvious problem with (22) is that in order to know if the mesh resolves the solution, it appears we need to already have the solution. It turns out that we can find a mesh that resolves the solution using only information about the BVP coefficients    and   . This means that an adequate mesh can be found before obtaining the solution.

**Definition 1.** Suppose a matrix function    can be partitioned into the form

(23)

where    for i, j = 1, 2, 3 and   .    is essentially diagonally dominant on    if    and    are strictly diagonally dominant,

for i = 1, 3 and i = 1, 2, 3, and

for j=1,2,3. Here    is the diagonal matrix containing the diagonal elements of    and   .

Note that in this definition, there is no requirement that    for i=1,3 and j=1,2,3 is small. As we will shortly see, the first and last row blocks will correspond to the stiff portion of the BVP. Also note that there is nothing special about submatrices    and   . The definition is written with those blocks being strictly diagonally dominant because the algorithm we will use to solve the BVP will put the system in this form. Now we are in a position to determine if a given mesh resolves the solution to our BVP.

<span id="page-8-0"></span>**Theorem 1** (Kreiss et al. [13]). Consider the BVP

 (26)

where    is partitioned as in (23). Let    and    be similarly partitioned so that   ,    for i = 1, 2, 3. If    is essentially diagonally dominant on    and there are constants    and    such that

 (27)

for i = 1, 3, j = 1, 2, 3, and v = 0, 1, ..., p;

for j = 1, 2, 3 and v = 0, 1, ..., p; and

 (29)

then    is resolved on   . Here again,    is the diagonal matrix containing the diagonal elements of   ,   , and   .

Theorem 1 requires the matrix of the BVP to be essentially diagonally dominant. This will not in general be the case. Thus, we must find a way to transform (18) to this form. Suppose we are able to find an invertible matrix function    such that

(30)

where    and   . Here, the eigenvalues of    are large and negative, the eigenvalues of    are large and positive, and the eigenvalues (both positive and negative) of    are small. Using (30), Equation (18) becomes

Let   . Then

where    (the prime denotes a derivative with respect to x) and   . With Theorem 1 in mind, suppose that    and    are strictly diagonally dominant. Now if    is small, then    is essentially diagonally dominant on   . Hence, the application of Theorem 1 relies on our ability to find an appropriate matrix function   .

Before we do this however, (30) and (32) are suggestive of a finite difference method. If an initial value problem (IVP) or a terminal value problem (TVP) have large eigenvalues, it is known that methods such as backward Euler work very well. If either an IVP or TVP has only small eigenvalues, then the trapezoidal rule is more accurate. With this in mind, let us use backward Euler for the    block integrating from a to b, the trapezoidal rule for the    block (integration direction does not matter since it is a symmetric method), and backward Euler for the    block integrating from b to a. This finite difference method gives us

for n = 1, 2, ..., N where    is the    identity matrix and   . Also, we use the shorthand    and similarly for    and   . This notation will be used throughout this section.

<span id="page-9-0"></span>To numerically solve (18), the finite difference equations (33) and the boundary conditions (19) are assembled into a system of equations of size M(N+1). This is a very sparse system. To solve it, we use an incomplete LU factorization as a preconditioner and a stabilized biconjugate gradient method.

Finally, for stability reasons, we consider an eigenvalue small if the product of itself and the local mesh spacing is less than 2. Otherwise, we consider the eigenvalue to be large.

#### 4.2. The Schur method

We now turn our attention to finding an appropriate   . From (30), we see that we need a similarity transform. One way to find    is to find a series of similarity transforms and construct    from those. At any mesh point    we can find the Schur decomposition of   . This is given by

(34)

where    is an orthogonal matrix and    is an upper triangular matrix. This implies that   ,   , and    are upper triangular, so the eigenvalues of    are on the diagonal of   . Further, the Schur decomposition can be done in such a way that the large negative eigenvalues are on the diagonal of   , the large positive eigenvalues are on the diagonal of   , and the small eigenvalues (both positive and negative) are on the diagonal of   .

Next, we zero out the remaining off-diagonal blocks. Let

(35)

so that we obtain

This will occur if   ,   , and    solve the Sylvester equations

Two algorithms for solving the Sylvester equation are the Bartels–Stewart algorithm and the Hessenberg–Schur algorithm, both of which are given in Golub et al. [35]. The Sylvester equation    has a unique solution if and only if    and    do not share any eigenvalues (see Golub et al. [35]), which is guaranteed due to how we have defined the blocks of   .

As stated above, the diagonal blocks of (36) are upper triangular, but    and    are not necessarily strictly diagonally dominant as required in Theorem 1. Fortunately, it is simple to find a similarity transform to make an upper triangular matrix strictly diagonally dominant. Let    be a diagonal matrix and    be an upper triangular matrix. Then the product

(40)

is strictly diagonally dominant if we choose    and

for i = m - 1, m - 2, ..., 1 and   . With this in mind, let

(42)

<span id="page-10-0"></span>where    and    are diagonal matrices with elements set according to (40) and (41) so that

We now have the desired block diagonal matrix    with strictly diagonally dominant matrices    and   . However, we still need    to be small. From (34), (36), and (43), let

Also define

for i = 1, 2, 3. Now let

(46)

so that

Note that this last similarity transform does not change   . It only has the effect of scaling    so that    is small. This scaling is effective because right-multiplying    by    normalizes the "column blocks" of   . This makes all elements of    of moderate size. Similarly, left-multiplying    by    normalizes the "row blocks" of   . Certainly, other choices of    may be better in this regard, but (47) has been found to be adequate for the electron transport problem.

Finally, we find using (34), (36), (43), and (47) that if we let

then we obtain the necessary similarity transformation for (30).

#### 4.3. The Riccati method

The Schur method would be expensive if calculated for every mesh point and does not guarantee a smooth   . However, if we already have   , then

(49)

can be viewed as a perturbation to    so long as    is sufficiently small. That is, the off-diagonal blocks should be small. If we can eliminate the off-diagonal blocks through similarity transforms, then we can avoid calculating the Schur decomposition of   .

Let us partition    so that

 (50)

Now let

(51)

<span id="page-11-0"></span>Then we obtain

 (52)

if    solves the algebraic Riccati equation

**Theorem 2** (Kreiss et al. [13]). Let    for i, j = 1, 2. Also let    where    is the    zero matrix. If    and    are sufficiently small, then the iteration

(54)

converges to a locally unique solution of

Theorem 2 states that under certain conditions the algebraic Riccati equation (53) can be solved by solving a series of Sylvester equations. We continue by letting

 (56)

Then we find that

 (57)

provided that    solves the Sylvester equation

From (50), (52), and (57) we find that

(59)

We now need to zero out the remaining off-diagonal blocks. We can let

(60)

so that

(61)

provided that    solves the algebraic Riccati equation

(62)

Similar to before, we can now let

(63)

With this, we obtain

 (64)

#### <span id="page-12-0"></span>**Algorithm 1** Implementation of the upwind method.

```
1: choose a preliminary mesh a = x_0 < x_1 < x_2 < \cdots < x_{N-1} < x_N = b that satisfies (29)
 2: use the Schur method to find \mathbf{V}(x_0) and \mathbf{\Lambda}(x_0) and calculate \mathbf{D}(x_0)
 3: set n = 1
 4: while x_n \neq b do
 5:
        use the Riccati method to find V(x_n) and \Lambda(x_n)
 6.
        if Riccati iteration (54) does not converge then
 7.
            replace \Delta x_n with \Delta x_n/\sqrt{2}, update x_n, and go to step 5
 8:
        else if block structure of \Lambda(x_n) and \Lambda(x_{n-1}) differs then
 9:
            use the Schur method to replace \mathbf{V}(x_{n-1}) and \mathbf{\Lambda}(x_{n-1}) with block structure forced to be the same as \mathbf{\Lambda}(x_n)
10:
        end if
11:
        calculate \mathbf{D}(x_n)
12.
        check smoothness with (27) and (28)
        if not smooth enough then
13:
            replace \Delta x_n with \Delta x_n/\sqrt{2}, update x_n, and go to step 5
14.
15:
16:
        accept \Delta x_n and adjust mesh accordingly
17:
        calculate finite difference matrices (33) and store
18.
        replace n with n+1
19: end while
20: assemble finite difference matrices (33) and boundary conditions (19) into a linear system
21: solve system to find solution \mathbf{u}_n \approx \mathbf{y}(x_n) for n = 0, 1, ..., N
```

if    solves the Sylvester equation

Finally, we find using (49), (59), (61), and (64) that

gives the necessary similarity transformation for (30).

There are two ways that the Riccati method can fail. The first is if the off-diagonal blocks of (49) are too large, so Theorem 2 does not apply. To fix this, we can simply decrease    until the off-diagonal blocks are small enough. Typically, we know that    is too large if too many iterations in (54) are used. The second way the Riccati method can fail is if the block structure of    changes from    to   . That is, if one or more eigenvalues of    go from being small to large or vice versa, then the size of the submatrices   ,   , and    (i.e. their dimensions   ,   , and   ) change. When this occurs, we simply resort to the Schur method.

## 4.4. Implementing the numerical solution

Before stating the algorithm, a few remarks should be made. First, in Theorem 1, we need to choose constants    for i = 1, 2 and the degree of smoothness p. For choosing   , we simply need   , so the choice of    is problem dependent. Regardless, the smaller    is, the more points the algorithm will use. As for p, it has been found to be sufficient to let p = 1. This way, when the derivatives needed in Theorem 1 are calculated, we can use a first order finite difference approximation with only two points. The procedure is summarized in Algorithm 1.

A few more remarks about Algorithm 1 are in order. First, the number of points N+1 changes as the algorithm proceeds. Also, this algorithm leaves open the possibility that there will be an abrupt change in mesh spacing. That is, either    or   . This can give spurious results in the numerical solution, but can be remedied by adding more points so that the ratio   . Lastly in step 9, we use the Schur method but alter how the blocking is done. That is, instead of setting the size of the blocks according to the size of the eigenvalues at   , we set the size of the blocks according to the size of the eigenvalues of    are its diagonal elements since it is essentially diagonally dominant.

#### 5. Numerical example

To see how well this numerical solution performs, we need to find a problem for which an exact solution exists. It turns out that if there only exists one species in the atmosphere, then an exact solution is indeed possible. Therefore, for this section we will assume all atoms and molecules in the atmosphere are atomic oxygen. We realize that this assumption is far from reality, but it will allow us to find an exact representation of the solution and see how well Algorithm 1 performs.

<span id="page-13-0"></span>Let us begin by rewriting (16) using the above simplification. We get

(67)

where    is the sum of all other terms in (16). We can write it this way because    only contains terms that depend on electron intensities at higher energies, which can be assumed to be known. Let us define the scattering depth to be

 (68)

where we have dropped the *E* dependency. If   , then our equation becomes

(69)

where

(71)

Under this change of variables, the boundary conditions become

 (72)

Notice that the top of the atmosphere is at    and the bottom of the atmosphere is at   . Hence, scattering depth (68) is a dimensionless measure of how far an electron has penetrated into the atmosphere.

The full details of how to find the exact solution to (69) are given in Woods [14]. The idea originally comes from Case and Zweifel [36]. We have simply applied those ideas to the electron transport equation. From Woods [14], the exact solution can be found using the boundary element method (BEM) and is given by

(73)

where we have dropped the hat notation and    is a fundamental solution.

In order to compare the two solutions, we will use a boundary condition given in Strickland et al. [37]. It is given by

 (74)

where

 (76)

<span id="page-14-0"></span>**Table 3** The relative difference between the upwind and boundary element solution at *E* = 10 eV for each combination of *E*<sup>0</sup> and *Q* .

Here, *E*<sup>0</sup> is the characteristic energy and *Q*<sup>0</sup> is related to the energy flux *Q* by

For a typical aurora, the energy flux is between 0 and 50 erg cm−<sup>2</sup> s−<sup>1</sup> (see Arnoldy and Lewis [\[8\]](#page-15-0) and Solomon et al. [\[9\]](#page-15-0)). For this reason, we will use *<sup>Q</sup>* = <sup>20</sup>*,* 50 erg cm−<sup>2</sup> <sup>s</sup>−<sup>1</sup> for each test included here. We will also use characteristic energies of *E*<sup>0</sup> = 5000*,* 8000*,* 10000 eV for each energy flux. For each combination of energy flux and characteristic energy, we have computed the relative difference using the formula

where both solutions are evaluated at *E* = 10 eV and · <sup>2</sup> denotes the *L*<sup>2</sup> norm. This norm was chosen because it incorporates all points in the domain. The relative differences are reported in Table 3.

Clearly, Table 3 shows that the upwind method and the boundary element method give close to the same solution. The relative differences are on the order of 10<sup>−</sup>4, which means that the solutions agree with each other. This demonstrates that the upwind method is correctly solving the single species problem. The boundary element method solution [\(73\)](#page-13-0) is exact, and the only error is in the numerical evaluation of its integrals. In order to evaluate [\(73\)](#page-13-0), we used half-range Gaussian quadrature for the *μ*<sup>0</sup> integrals (the "double-Gauss" rule mentioned earlier) with 20 points in each half interval and the trapezoid rule for the *τ*<sup>0</sup> integral using 500 points. Since Gaussian quadrature is known to be of order 2*M* where *M* is the number of points, the dominant error is clearly in the evaluation of the *τ*<sup>0</sup> integral. However, the trapezoid rule is a second order method and the upwind method described above is a first order method since it uses Euler's method. Care was taken to ensure that the integrands were well-resolved with both the *τ* and *μ* meshes. Since the error in the boundary element method is smaller than the upwind method, the comparison shows that we have verified our solution.

## **6. Conclusion**

We have demonstrated that the electron transport equation [\(1\)](#page-3-0) is a very stiff boundary value problem whose numerical solution cannot be found without a stiff solver unless unrealistic assumptions are made for the solution domain. To handle the exponential stiffness of the problem, the algorithm derived here incorporates analytic approximations involving a generalized Legendre polynomial approximation, along with an upwind scheme that uses an eigenvalue decomposition to delineate the relevant scales needed to resolve the solution. To demonstrate its effectiveness, in the case of a single species atmosphere, the exact solution can be written in terms of a fundamental solution, and then evaluated using a boundary element method. We showed that the two methods agree with each other, thereby verifying the upwind method.

One point not yet addressed is that our numerical method involved backward Euler, which is only first-order accurate. However, the method can be extended to arbitrarily high orders, and it is our recommendation to do so when seeking scientific results. The way to obtain higher order methods is shown in Brown and Lorenz [\[38\]](#page-15-0). Hence, we have demonstrated that the method works for a simplified version of the electron transport equation, and Brown and Lorenz [\[38\]](#page-15-0) have shown that the method can be extended to higher orders. Although we only demonstrated that the method works for a simplified version of the problem, we believe the method can also be used to solve the full electron transport equation (see Woods [\[14\]](#page-15-0)). There is not, however, an exact solution for the full multi-species problem (otherwise there is no purpose to a numerical method), and how to show that the upwind method gives the correct result in this case is the subject of future work.

### **References**

- [1] M.H. Rees, Physics and Chemistry of the Upper Atmosphere, Cambridge [Atmospheric](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib5265657331393839s1) and Space Science, Cambridge Univ. Press, New York, NY, 1989.
- [2] K. Stamnes, O. [Lie-Svendsen,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib5374616D6E657331393931s1) M.H. Rees, The linear Boltzmann equation in slab geometry: development and verification of a reliable and efficient solution, Planet. Space Sci. 39 (10) (1991) [1435–1463.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib5374616D6E657331393931s1)
- [3] K. Stamnes, Analytic approach to auroral electron transport and energy [degradation,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib5374616D6E657331393830s1) Planet. Space Sci. 28 (4) (1980) 427–441.

- <span id="page-15-0"></span>[4] D. [Lummerzheim,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C756D6D65727A6865696D31393839s1) M.H. Rees, H.R. Anderson, Angular dependent transport of auroral electrons in the upper atmosphere, Planet. Space Sci. 37 (1) (1989) [109–129.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C756D6D65727A6865696D31393839s1)
- [5] Q.L. Min, D. [Lummerzheim,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4D696E31393933s1) M.H. Rees, K. Stamnes, Effects of a parallel electric field and the geomagnetic field in the topside ionosphere on auroral and photoelectron energy distributions, J. Geophys. Res. 98 (11) (1993) [19223–19234.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4D696E31393933s1)
- [6] D. [Lummerzheim,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C756D6D65727A6865696D31393934s1) J. Lilensten, Electron transport and energy degradation in the ionosphere: evaluation of the numerical solution, comparison with laboratory experiments and auroral [observations,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C756D6D65727A6865696D31393934s1) Ann. Geophys. 12 (10/11) (1994) 1039–1051.
- [7] B. Lanchester, B. Gustavsson, Imaging of aurora to estimate the energy and flux of electron precipitation, in: Auroral [Phenomenology](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C616E6368657374657232303132s1) and Magnetospheric Processes: Earth and Other Planets, in: Geophysical Monograph Series, vol. 197, Amer. Geophys. Union, [Washington,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C616E6368657374657232303132s1) DC, 2012.
- [8] R.L. Arnoldy, P.B. Lewis, Correlation of ground-based and topside photometric observations with auroral electron spectra [measurements](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib41726E6F6C647931393737s1) and rocket altitudes, J. Geophys. Res. 82 (35) (1977) [5563–5572.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib41726E6F6C647931393737s1)
- [9] S.C. Solomon, P.B. Hays, V.J. Abreu, The auroral 6300 Å emission: [observations](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib536F6C6F6D6F6E31393838s1) and modeling, J. Geophys. Res. 93 (A9) (1988) 9867–9882.
- [10] H.S. Porter, F. Varosi, H.G. Mayr, Iterative solution of the [multistream](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib506F7274657231393837s1) electron transport equation. I: comparison with laboratory beam injection experiments, J. Geophys. Res. 92 (A6) (1987) [5933–5959.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib506F7274657231393837s1)
- [11] G.P. Mantas, Theory of photoelectron [thermalization](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4D616E7461733139373561s1) and transport in the ionosphere, Planet. Space Sci. 23 (2) (1975) 337–354.
- [12] G.P. Mantas, S.A. Bowhill, Calculated [photoelectron](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4D616E7461733139373562s1) pitch angle and energy spectra, Planet. Space Sci. 23 (2) (1975) 355–375.
- [13] H.O. Kreiss, N.K. Nichols, D.L. Brown, [Numerical](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4B726569737331393836s1) methods for stiff two-point boundary value problems, SIAM J. Numer. Anal. 23 (2) (1986) 325–368.
- [14] M. Woods, Numerical Solution of the Electron Transport Equation, Ph.D. thesis, Rensselaer [Polytechnic](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib576F6F647332303136s1) Institute, Troy, NY, 2016.
- [15] A.E. Hedin, Extension of the MSIS [thermospheric](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib486564696E31393931s1) model into the middle and lower atmosphere, J. Geophys. Res. 96 (A2) (1991) 1159–1172.
- [16] R.D. Sharma, J.H. Brown, A. Berk, P.K. Acharya, J. Gruninger, J.W. Duff, R.L. Sundberg, User's Manual for SAMM, SHARC and [MODTRAN](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib536861726D6131393936s1) Merged, Tech. Rep. [PL-TR-96-2090,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib536861726D6131393936s1) Phillips Lab., Hanscom AFB, MA, 1996.
- [17] R.R. Laher, F.R. Gilmore, Updated excitation and [ionization](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C6168657231393930s1) cross sections for electron impact on atomic oxygen, J. Phys. Chem. Ref. Data 19 (1) (1990) [277–305.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4C6168657231393930s1)
- [18] Y. Itikawa, A. [Ichimura,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4974696B61776131393930s1) Cross sections for collisions of electrons and photons with atomic oxygen, J. Phys. Chem. Ref. Data 19 (3) (1990) 637–651.
- [19] F. Salvat, A. Jablonski, C.J. Powell, ELSEPA Dirac [partial-wave](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib53616C76617432303035s1) calculation of elastic scattering of electrons and positrons by atoms, positive ions and [molecules,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib53616C76617432303035s1) Comput. Phys. Commun. 165 (2) (2005) 157–190.
- [20] S. [Pancheshnyi,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib50616E63686573686E796932303132s1) S. Biagi, M.C. Bordage, G.J.M. Hagelaar, W.L. Morgan, A.V. Phelps, L.C. Pitchford, The LXCat project: electron scattering cross sections and swarm parameters for low [temperature](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib50616E63686573686E796932303132s1) plasma modeling, Chem. Phys. 398 (4) (2012) 148–153.
- [21] W.L. Morgan, Electron collision data for plasma [chemistry](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4D6F7267616E32303030s1) modeling, Adv. At. Mol. Opt. Phys. 43 (1) (2000) 79–110.
- [22] Y. Itikawa, Cross sections for electron collisions with nitrogen [molecules,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4974696B61776132303036s1) J. Phys. Chem. Ref. Data 35 (1) (2006) 31–53.
- [23] A.V. Phelps, Collision cross sections for electrons with [atmospheric](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib5068656C707331393732s1) species, Ann. Geophys. 28 (3) (1972) 611–625.
- [24] S.F. Biagi, Monte Carlo [simulation](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib426961676931393939s1) of electron drift and diffusion in counting gases under the influence of electric and magnetic fields, Nucl. Instrum. Methods Phys. Res. A 421 (2) (1999) [234–240.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib426961676931393939s1)
- [25] L.L. Alves, The [IST-LISBON](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib416C76657332303134s1) database on LXCat, JPCS 565 (1) (2014) 1–10.
- [26] Y. Itikawa, Cross sections for electron collisions with oxygen [molecules,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4974696B61776132303039s1) J. Phys. Chem. Ref. Data 38 (1) (2009) 1–20.
- [27] A.A. Ionin, I.V. Kochetov, A.P. Napartovich, N.N. Yuryshev, Physics and engineering of singlet delta oxygen production in [low-temperature](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib496F6E696E32303037s1) plasma, J. Phys. D, Appl. Phys. 40 (2) (2007) [R25–R61.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib496F6E696E32303037s1)
- [28] Y.K. Kim, K.K. Irikura, M.E. Rudd, M.A. Ali, P.M. Stone, J. Chang, J.S. Coursey, R.A. Dragoset, A.R. Kishore, K.J. Olsen, A.M. Sansonetti, G.G. Wiersma, D.S. Zucker, M.A. Zucker, Electron-impact cross sections for ionization and excitation, Version 3.0, SRD 107, Nat. Inst. of Standards and Technol., 2004.
- [29] M. Hayashi, Nonequilibrium Processes in Partially Ionized Gases, NATO ASI Series, vol. 220, [Springer+Business](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4861796173686931393930s1) Media, LLC, New York, NY, 1990, [pp. 333–340,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4861796173686931393930s1) chap. 21.
- [30] D.C. [Cartwright,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4361727477726967687431393938s1) M.J. Brunger, L. Campbell, B. Mojarrabi, P.J.O. Teubner, Electron impact excitation of nitric oxide under auroral conditions, Geophys. Res. Lett. 25 (9) (1998) [1495–1498.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4361727477726967687431393938s1)
- [31] W.J. Wiscombe, The delta-M method: rapid yet accurate radiative flux [calculations](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib576973636F6D626531393737s1) for strongly asymmetric phase functions, J. Atmos. Sci. 34 (9) (1977) [1408–1422.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib576973636F6D626531393737s1)
- [32] K. Stamnes, R.A. Swanson, A new look at the discrete ordinate method for radiative transfer calculations in [anisotropically](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib5374616D6E65733139383162s1) scattering atmospheres, J. Atmos. Sci. 38 (2) (1981) [387–399.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib5374616D6E65733139383162s1)
- [33] U.M. Ascher, R.M. Mattheij, R.D. Russell, Numerical Solution of Boundary Value Problems for Ordinary [Differential](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib41736368657231393935s1) Equations, Soc. Ind. and Appl. Math., [Philadelphia,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib41736368657231393935s1) PA, 1995.
- [34] U.M. Ascher, L.R. Petzold, Computer Methods for Ordinary Differential Equations and [Differential-Algebraic](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib41736368657231393938s1) Equations, Soc. Ind. and Appl. Math., [Philadelphia,](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib41736368657231393938s1) PA, 1998.
- [35] G.H. Golub, S. Nash, C. Van Loan, A [Hessenberg–Schur](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib476F6C756231393739s1) method for the problem *A X* + *X B* = *C*, IEEE Trans. Autom. Control 24 (6) (1979) 909–913.
- [36] K.M. Case, P.F. Zweifel, Linear Transport Theory, [Addison–Wesley](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib4361736531393637s1) Publishing Company, Inc., Reading, MA, 1967.
- [37] D.J. Strickland, R.E.J. Daniell, J.R. Jasperse, B. Basu, Transport-theoretic model for the [electron–proton–hydrogen](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib53747269636B6C616E6431393933s1) atom aurora. II: model results, J. Geophys. Res. 98 (A12) (1993) [21533–21548.](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib53747269636B6C616E6431393933s1)
- [38] D.L. Brown, J. Lorenz, A [high-order](http://refhub.elsevier.com/S0021-9991(18)30630-2/bib42726F776E31393837s1) method for stiff boundary value problems with turning points, SIAM J. Sci. Stat. Comput. 8 (5) (1987) 790–805.
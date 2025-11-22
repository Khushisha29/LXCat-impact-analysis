#### **PAPER • OPEN ACCESS**

# Electron-neutral collision cross sections for H<sup>2</sup> O: II. Anisotropic scattering and assessment of the validity of the two-term approximation

To cite this article: Maik Budde et al 2023 J. Phys. D: Appl. Phys. 56 255201

View the [article online](https://doi.org/10.1088/1361-6463/accaf4) for updates and enhancements.

# You may also like

-

- [The LisbOn KInetics Boltzmann solver](/article/10.1088/1361-6595/ab0537) A Tejero-del-Caz, V Guerra, D Gonçalves et al. -
- [The 2021 release of the Quantemol](/article/10.1088/1361-6595/ac907e) [database \(QDB\) of plasma chemistries](/article/10.1088/1361-6595/ac907e) [and reactions](/article/10.1088/1361-6595/ac907e) -
- Jonathan Tennyson, Sebastian Mohr, M Hanicinec et al.

[Effect of anisotropic scattering for](/article/10.1088/1361-6595/ac0a4d)

[rotational collisions on electron transport](/article/10.1088/1361-6595/ac0a4d) [parameters in CO](/article/10.1088/1361-6595/ac0a4d) L Vialetto, A Ben Moussa, J van Dijk et al.

J. Phys. D: Appl. Phys. **56** (2023) 255201 (11pp) <https://doi.org/10.1088/1361-6463/accaf4>

# **Electron-neutral collision cross sections for H2O: II. Anisotropic scattering and assessment of the validity of the two-term approximation**

**Maik Budde**[1](#page-1-0)[,2](#page-1-1),*[∗](#page-1-2)***, Tiago Cunha Dias**[2](#page-1-1)**, Luca Vialetto**[3](#page-1-3)**, Nuno Pinh˜ao**[2](#page-1-1)**, Vasco Guerra**[2](#page-1-1) **and Tiago Silva**[2](#page-1-1)

E-mail: [m.budde@tue.nl](mailto:m.budde@tue.nl)

Received 6 December 2022, revised 26 March 2023 Accepted for publication 6 April 2023 Published 20 April 2023

#### **Abstract**

This work proposes a complete and consistent set of cross sections (CS) for electron collisions with water gas molecules to be published in the IST-Lisbon database on LXCat. The set is validated by the electron swarm analysis technique. The anisotropic angular distribution of electrons in rotational collisions is considered by means of the Born approximation in a two-term Boltzmann solver (LisbOn KInetics two-term Boltzmann solver (LoKI-B)) and a Monte Carlo simulations code (LoKI-MC), both freely available as open-source codes. The inclusion of electron anisotropic scattering in rotational collisions significantly improves the agreement between calculations and measurements of the electron drift velocity, reduced mobility, characteristic energy, reduced Townsend ionisation coefficient, reduced effective Townsend coefficient and reduced attachment coefficient. The MC simulations are deemed more accurate and shown to yield similar results as LoKI-B with the proposed set. The use of LoKI-MC also validates the set of CSs against parameters that cannot be obtained by LoKI-B, such as the longitudinal diffusion coefficient or the bulk transport coefficients.

Supplementary material for this article is available [online](https://doi.org/10.1088/1361-6463/accaf4)

Keywords: H2O, electron-neutral collision cross sections, electron swarm technique, two-term Boltzmann solver, Monte Carlo simulation, anisotropic scattering, molecular rotation

(Some figures may appear in colour only in the online journal)

<span id="page-1-2"></span>*<sup>∗</sup>* Author to whom any correspondence should be addressed.

Original Content from this work may be used under the terms of the [Creative Commons Attribution 4.0 licence](https://creativecommons.org/licenses/by/4.0/). Any

further distribution of this work must maintain attribution to the author(s) and the title of the work, journal citation and DOI.

<span id="page-1-0"></span><sup>1</sup> Department of Applied Physics, Eindhoven University of Technology, 5600 MB Eindhoven, The Netherlands

<span id="page-1-1"></span><sup>2</sup> Instituto de Plasmas e Fus˜ao Nuclear, Instituto Superior Técnico, Universidade de Lisboa, 1049-001 Lisbon, Portugal

<span id="page-1-3"></span><sup>3</sup> Theoretical Electrical Engineering, Faculty of Engineering, Kiel University, Kaiserstraße 2, 24143 Kiel, Germany

### <span id="page-2-1"></span>**1. Introduction**

From a scientific standpoint, the importance of water goes way beyond *merely* forming the foundation of life on Earth. For instance, water molecules (H2O) can serve as abundant hydrogen source in plasma gas conversion[[1,](#page-10-0) [2\]](#page-10-1) or surface functionalisation[[3\]](#page-10-2), as probe in atmospheric[[4\]](#page-10-3) or astronomic environments [\[5](#page-10-4)], as prominent constituent in primordial Earth's atmosphere [\[6](#page-10-5)] or as direct target of processing like water purification [\[7](#page-10-6)]. On top of that, water is an impurity present in many applications [\[8](#page-10-7), [9\]](#page-10-8). A common denominator of all mentioned situations is the importance of collisions between electrons and H2O.

Very complex environments are formed within which collisions between electrons and H2O induce various molecular processes like rotational, vibrational and electronic excitation, dissociation, electron attachment or ionisation, that must all be taken into account in an accurate and complete description. While experiments grant valuable insights into these environments, often simulations are vital for their interpretation and fundamental understanding [\[10](#page-11-0)]. In turn, the significance of simulation outcomes relies on the validity of input data.

Since the collision-induced processes dictate the overall behaviour of the system, electron-neutral collision cross sections (CSs) play an important part as simulation input. There has been a lot of discussion in the community on which H2O CSs to use, with many groups proposing different sets [\[11](#page-11-1)[–13](#page-11-2)], as extensively discussed in[[14\]](#page-11-3). Recently, we have also made available a CS set for electrons in H2O vapour[[14\]](#page-11-3) in the IST-Lisbon database [\[15](#page-11-4)] on LXCat[[16\]](#page-11-5). Under the assumption of isotropic scattering in inelastic collisions, the CSs have been optimised with the electron swarm analysis technique [\[17](#page-11-6)] using the LisbOn KInetics two-term Boltzmann solver (LoKI-B) [\[18](#page-11-7)] to obtain a complete CS set, in the following called the *isotropic set*, that is consistent with experiments.

The isotropic set comes with the advantage of compatibility with widely used space-homogeneous two-term Boltzmann solvers allowing for immediate improvement of existing lowtemperature plasma models.

In this paper, we extend the study in our previous work[[14\]](#page-11-3). Specifically, we test the impact of anisotropic scattering for rotational collisions and the validity of the electron-H2O collision CS set derived from LoKI-B beyond the two-term approximation, leading to what is henceforth called the *anisotropic set*.

Rotational collisions are known to be particularly important for low-energy electrons[[19\]](#page-11-8). In fact, the rotations of H2O are the main reason for the ongoing controversy in the community about which CSs to use. Different descriptions have been proposed [\[12](#page-11-9), [20,](#page-11-10) [21\]](#page-11-11) including either state-to-state transitions [\[12](#page-11-9)], lumped CSs [\[13](#page-11-2), [22](#page-11-12), [23\]](#page-11-13) or anisotropic rotational CSs [\[24](#page-11-14)]. In our isotropic set a large number of 147 rotational transitions is included to ensure an accurate description of the electron kinetics[[14\]](#page-11-3). A scaling factor of 0.3 and a cut-off beyond 12 eV are introduced in the calculation of the rotational CSs [\[25](#page-11-15)], so as to obtain agreement with experimental electron transport coefficients[4](#page-2-0) . In the present publication, a more thorough description of the rotations through inclusion of the anisotropy [\[26](#page-11-16)] of the scattering process is provided. The inclusion of anisotropic scattering is justified from our previous work on electrons in CO, where forward angular scattering for rotational collisions has been demonstrated to have a large impact in the calculations of electron transport coefficients for reduced electric fields *E/N* ⩽ 1Td (1Td = 1 *×* 10*−*<sup>21</sup> V m<sup>2</sup> ) [\[26](#page-11-16)], leading to an improved agreement with experiments.

Two-term electron Boltzmann solvers such as LoKI-B [\[18](#page-11-7)] or BOLSIG+ [\[27](#page-11-17)] are fast and reasonably accurate tools available to the community for the calculation of the electron energy distributions function (EEDF) [\[10](#page-11-0)]. Underlying assumptions, e.g. small anisotropy in the electron velocity distribution that allows for discarding the Legendre-polynomial development of the electron distribution function after the first order term, simplify the problem significantly. However, in the presence of significant inelastic collisions for electrons with molecules two-term Boltzmann solvers should be applied with care [\[28](#page-11-18)], due to the implied small anisotropy assumption for the electron velocity distribution function. Moreover, only socalled flux transport parameters have been considered in our previous study, whereas so-called bulk parameters[[29,](#page-11-19) [30](#page-11-20)] are considered here as well. The difference between bulk and flux is explained best by means of the drift velocity: the flux drift velocity is the average velocity of the electron swarm, while the bulk drift velocity is the change of the position of the centre of mass of the swarm[[29\]](#page-11-19). Differences between the two occur at *E/N* for which there is a significant contribution of non-conservative processes like attachment or ionisation[[28\]](#page-11-18). Codes based on density gradient expansion of the electron distribution function or the Monte Carlo (MC) simulation method are capable of providing bulk parameters though [\[31](#page-11-21)]. It is worth mentioning that two-term Boltzmann solvers are not the standard in the optimisation of CSs but often more precise methods like multi-term expansion or MC simulation codes are used. Using two-term-derived CSs in more exact calculations might lead to deviations. The consistent use of a two-term Boltzmann solver to first obtain those CSs and afterwards yield a correct EEDF using the CSs, see also figure [6,](#page-9-0) then might serve as basis for plasma modelling regardless[[32\]](#page-11-22).

Herein, we present a complete and consistent anisotropic set of electron-neutral collision CSs for electrons in water vapour to the community. Usability is ensured through the latest releases of the LisbOn KInetics open-source codes[[33\]](#page-11-23), namely the two-term Boltzmann solver LoKI-B [\[18](#page-11-7)] and the MC simulation tool LoKI-MC [\[34](#page-11-24)], both including anisotropic scattering. The latter validates the proposed anisotropic CS set at high *E/N* conditions where the two-term Boltzmann solver may fail and extend the comparison with experiment to bulk transport coefficients. The new set can significantly improve

<span id="page-2-0"></span><sup>4</sup> In our previous publication, we have been using the term swarm parameter instead of transport coefficient.

plasma models, which will promote the understanding and tailoring of experiments and applications.

The outline of this manuscript is as follows. Section 2 establishes anisotropic electron scattering by    in a general manner before detailing the implementation in a two-term Boltzmann solver and a MC simulation code. Section 3 presents the anisotropic CS set obtained and validated from the electron swarm analysis method, as demonstrated in section 4. Afterwards, section 5 elaborates on the effect of changing the gas temperature on the calculated electron transport coefficients for both isotropic and anisotropic sets of CSs. Finally, the most important findings of the study are summarised in section 6.

# <span id="page-3-0"></span>2. Anisotropic scattering in dipole rotational collisions

This section introduces the concept of anisotropic rotational collisions of electrons with water molecules and details how the anisotropy is included in the used codes, namely the two-term Boltzmann solver LoKI-B [18] and the MC simulations code LoKI-MC [34].

Before addressing anisotropic scattering, the proper notation of the rotational quantum state of    must be clarified. Since it has been introduced in a preceding paper [14], only a summary is given here. The    molecule is an asymmetrictop rotor whose rotational quantum state J is characterised by three quantum numbers: the principal rotational quantum number J (not to be confused with the notation of the rotational state itself J), K' and K'', which represent the projection of J along the axis of smallest and largest moment of inertia, respectively. The latter two are often combined to the pseudo-quantum number   . The rotational state is then given as    [14, 35].

# 2.1. Differential cross section (DCS) for rotational collisions of electrons in water vapour

The kinematics of a scattering event i is ruled by its DCS   , where    is the incident electron energy,    is the polar scattering angle and    is the differential solid angle, assuming symmetry regarding the azimuthal angle   . In the case of dipole transitions in asymmetric-top rotor molecules like water, Itikawa derived the following expression under the Born approximation [25, 36]

where primed quantities are after the collision, D = 0.728 is the dipole moment of water in atomic units and    is the line strength of the rotational transition [37], which is taken from King *et al* [38]. In fact, the Born approximation is a simplification as for instance short-range effects and the polar nature of    are neglected. As has been shown, the approximation is

however often still valid even for low electron energies since the effective interaction occurs distant from the molecule. The wave function of the incident electron is then only marginally distorted [26, 39, 40]. See particularly Vialetto *et al* for an indepth discussion [26].

By integrating the DCS over the solid angle and assuming azimuthal symmetry, we obtain the integral cross section (ICS):

<span id="page-3-2"></span>

where    is the absolute difference between the energies of the final and initial rotational states. Additionally, we can define the angular distribution function    by normalising the DCS with the ICS:

This function provides insight about the angular distribution of the scattered electrons, independently of the ICS of the collisional process. Taking into account equations (1) and (2), the angular distribution function in dipole-rotational collisions is written as

<span id="page-3-3"></span>

(4)

The angular distribution function given by equation (4) is plotted in figure 1 for the transition from    to   . The long-range dipole interaction yields a highly anisotropic angular distribution where small-angle scattering is dominant, with an increasing effect with electron energy.

Finally, using the classical definition of the momentum transfer cross section (MTCS) [41],

<span id="page-3-4"></span>

<span id="page-3-1"></span>for dipole rotational collisions in water, the MTCS is given by,

<span id="page-3-5"></span>

This component is important for the inclusion of anisotropic scattering in a two-term solver, as shown in the next section. Note that the MTCS definition is not unique and some

<span id="page-4-0"></span>**Figure 1.** Angular distribution function    from dipole-Born theory, for the rotational transition in water from    to   , whose threshold is    eV.

authors [42] consider a different formula for inelastic processes. This is extensively discussed in [26]. In this paper, whenever talking about momentum transfer, we refer to the definition (5).

#### 2.2. Anisotropic scattering in a two-term Boltzmann solver

The inclusion of anisotropic scattering in the two-term Boltzmann equation is detailed in [26]. Here, we focus on the main aspects.

Under azimuthal symmetry, similarly to what is done for the electron velocity distribution, the DCS can be expressed as an expansion in Legendre polynomials    [43],

where the terms    are the *j*th partial cross sections (PCSs), which can be obtained using the orthogonality relation of the Legendre polynomials:

Notice that the zeroth PCS is always equal to the ICS and the first PCS vanishes for isotropic processes. Moreover, the MTCS defined in (5) can be written as a function of the first two PCSs:

<span id="page-4-2"></span><span id="page-4-1"></span>

Using the two-term approximation, the anisotropic collisional effects can be considered by extending the total (effective) electron-neutral CS for momentum transfer in the following way:

where    is the fraction of molecules in state k,    is the first anisotropic component of the normalised electron velocity distribution and    is the absolute energy difference between the two involved states. The first group of terms represents, in order, the momentum transfer due to elastic collisions with molecules in state k, electron-impact excitations    and de-excitations   . This part is identical to what is implemented in most two-term Boltzmann solvers, describing the loss of momentum in isotropic collisions. The second and third group consist of the first order corrections due to the anisotropic nature of excitations and de-excitations, respectively.

Take note that the superelastic PCSs    are obtained through the microreversibility relation, expressing the principle of detailed balance [44]:

where    and    denote the statistical weights of the levels k and l, respectively.

As evidenced in figure 1, the angular distribution in rotational collisions of    is highly anisotropic and the extended total CS in equation (10) is required. However, the anisotropic terms can be further simplified for rotational collisions. Unless the incident electron energy is very low, the difference between the electron energies before and after rotational collisions can be neglected such that   . Consequently,    and the contribution of the rotational collisions for momentum transfer can be approximately written as

<span id="page-4-3"></span>

where in the last term equation (9) was used. In other words, in low-energy threshold processes such as rotational collisions, the anisotropy can be approximately considered by replacing the ICSs of rotational collisions by the MTCSs.

Expression (12) is implemented in the latest version of LoKI-B [18] and is used in the present simulations. Pay attention that in the case of other collisional processes, e.g. vibrational and electronic excitations/de-excitations, the original form in (10) should be used instead.

#### 2.3. Anisotropic scattering in a MC solver

The MC method used in LoKI-MC is described in [34]. In short, it simulates the accelerated electron transport in a background gas by following the stochastic trajectory of a representative ensemble of    electrons. Each electron performs a series of free flights interrupted by elastic, inelastic or superelastic collisions with gas molecules. The collision-free times and the collision dynamics are calculated by generating random numbers sampled from probability distributions based on the underlying physics. During the simulation, the information of the electrons is stored in order to calculate distribution functions, transport coefficients and other relevant quantities.

In the first code release, with the exception of ionisation, electron collisions are assumed isotropic. Here, we generalise its application to anisotropic scattering based on the work by Vialetto *et al* [26], to be included in the next release. The scattering angles after electron-molecule collisions can be sampled according to a theorem of probability [45], by inverting the following equation:

<span id="page-5-1"></span>

where    is a random number uniformly distributed between 0 and 1, and the scattering angle    is randomly distributed according to a probability distribution function    that is normalised to 1 in   . We should remark that this procedure is general and valid for any kind of electron-impact process. Contrarily to the two-term solution, no approximations are needed to include anisotropic scattering. Upon the knowledge of   , equation (13) can be inverted to obtain   .

For dipole-Born interactions, the substitution of equation (4) into (13) leads to [26]:

where the energy-dependent variable    is given by:

and the minus (plus) sign corresponds to the inelastic (superelastic) process. In this way, dipole-Born anisotropic scattering is rigorously included in the MC algorithm and we can quantify the accuracy of the approximations made in the twoterm Boltzmann solver.

### <span id="page-5-0"></span>3. Anisotropic CS set

The complete anisotropic CS set proposed in this paper is plotted against the electron energy    in figure 2. The CSs are grouped in conservative processes with a constant number of

<span id="page-5-2"></span>**Figure 2.** Proposed cross sections   , plotted against the electron energy   , divided into conservative and non-conservative collisional processes. ICS and MTCS (dashed lines) are the sums of all individual rotational cross sections weighted by the populations of the lower rotational levels assuming a Boltzmann distribution at 293 K. In the left-side panel, the elastic and rotational cross section extend down to sub-meV range which is not shown for better visibility of the remaining conservative collision cross sections. CSs are obtained from [22, 25, 48–56]. See the main text and [14] for more details.

electrons on the left and non-conservative processes, i.e. ionisation and attachment, on the right. With the exception of rotational processes, the anisotropic set is entirely equal to the isotropic set of [14]. For that reason, differences of the optimised CSs in the isotropic set with respect to the original references are only briefly addressed here before focusing on the rotational CSs and the reader is referred to [14] for details. In short, to improve the agreement with experimental transport coefficients with the isotropic set, in [14] the original CSs for   ,    and    are multiplied with a constant factor within their range of uncertainty, the high-energy tail of the elastic CS is slightly decreased and the effective excitation CS leading to    is introduced.

In the isotropic set, the rotational ICSs are decreased by a factor 0.3 relatively to equation (2) and set to zero after 12 eV, to compensate for the isotropic assumption. In that case, no additional MTCSs are needed since they are equal to the ICSs. In the anisotropic set proposed here, the ICSs and MTCSs are calculated entirely according to equations (2) and (6), with no modification. This approach leads to a significantly better agreement with experiments, as is shown in section 4. To put the proposed rotational CSs into perspective, figure 3 shows the CS for the rotational transition   . Dashed lines correspond to CSs that we propose in this publication (light blue lines) or in the previous isotropic set (grey line) [14], all based on the Born approximation. The dashdotted blue line is taken from [20] including a short-range correction to the Born approximation based on R-matrix calculations with a fixed-nuclei approximation. The solid green line is taken from the supplementary material of [13] that is in principle based on [20]. Note that [13] recommends only the highenergy part of the CS beyond the maximum. From figure 3, a

<span id="page-6-1"></span>**Figure 3.** Illustration of differences in rotational cross sections *σ* by means of the rotational transition (*JK′K ′ ′*) = (000) *→* (111). Dashed lines correspond to CSs that we recommend either here (light blue lines) or in our isotropic set (grey line)[[14\]](#page-11-3). The dash-dotted dark blue line is taken from Faure *et al* [\[21](#page-11-11)] and the solid green line from Song *et al* [\[13](#page-11-2)].

clear difference between the simple Born approximation and the more sophisticated approach is seen. The discussion of the best rotational CSs is ongoing and is not to be settled by the present study as the electron swarm analysis method yields an optimised set of CS but does not allow for conclusions about individual CSs. The conclusion that can be drawn though, is that our proposed anisotropic CS set yields excellent agreement with experimental electron transport coefficients as is shown in section [4](#page-6-0).

The inclusion of anisotropic scattering is limited to rotational collisions in the present set. We specifically decided to focus on anisotropic scattering in low-energy threshold rotational collisions for two reasons. On the one hand, this is motivated by the fact that anisotropic scattering in dipole rotational collisions has been demonstrated to have large effects on calculated electron transport coefficients [\[26](#page-11-16)]. On the other hand, it has been shown that the choice of the angular scattering model for higher energy threshold conservative collisions has only a minor influence on the calculated electron transport coefficients[[46,](#page-11-38) [47\]](#page-11-39). The present results confirm these observations from literature as good agreement between experimental and calculated transport coefficients for low *E/N* is obtained with only anisotropic rotational scattering while isotropic scattering is sufficient for the remaining collisional processes. It is worth mentioning however that equations [\(10](#page-4-1)) and([13\)](#page-5-1) are general and can principally be applied to any scattering process.

In summary, the anisotropic set includes one elastic[[48\]](#page-11-36), 147 rotational integral and 147 rotational momentum transfer [\[25](#page-11-15)], two vibrational [\[49](#page-11-40), [50\]](#page-11-41), three electronic excitation[[51,](#page-11-42) [52\]](#page-11-43), three dissociation [\[53](#page-11-44)[–55](#page-11-45)], three dissociative attachment[[22,](#page-11-12) [48](#page-11-36)] and five ionisation CSs[[56\]](#page-11-37). In figure [2](#page-5-2), the sum of all individual ICSs and MTCSs, see equations [\(2](#page-3-2)) and [\(6](#page-3-5)), weighted by the population of the lower rotational state is shown (dashed lines) for illustration. In total 310 CSs, where 294 = 2 *×* 147 = *n*ICS + *n*MTCS are rotational CSs, are included. However, note that the rotational MTCSs are not used for LoKI-MC calculations, since the anisotropic angular distribution is directly taken into account in the generation of the scattering angle, see section [2](#page-3-0). The reader is referred to [\[14](#page-11-3)] for more details on the CS set.

## <span id="page-6-0"></span>**4. Validation**

The complete CS set of figure [2](#page-5-2) is validated by the electron swarm technique using the two-term Boltzmann solver LoKI-B[[18\]](#page-11-7) and the MC simulation tool LoKI-MC[[34\]](#page-11-24), both freely available as open-source codes [\[33](#page-11-23)]. Anisotropic rotational scattering is included in both solvers through the methods described in section [2.](#page-3-0) The setup files required to run the codes are provided as supplementary material.

Contrarily to the recommendation in[[14\]](#page-11-3), where it is suggested to discretise the energy axis of the LoKI-B simulations in 2000 cells, as a good compromise between accuracy and computation time, here the energy axis is discretised in 8000 cells to facilitate the comparison between the isotropic and anisotropic sets. This large cell number assures an accurate treatment of the low-energy thresholds of the rotational CSs [\[14](#page-11-3)]. Note that the maximum energy of the grid is dynamically adjusted [\[18](#page-11-7)]. It is between 0.8 eV for lowest and 140 eV for highest *E/N* used, respectively, divided into the abovementioned number of equally sized cells. The LoKI-MC simulations follow the dynamics of an ensemble of 2 *×* 10<sup>5</sup> electrons. After the electron swarm relaxes to a stationary state, the transport coefficients are calculated by averaging over all electrons at 10<sup>5</sup> fixed time instants. The standard deviation for the coefficients shown in this work is always below 1%. For more details, see section 2.6 of [\[34](#page-11-24)].

The electron transport coefficients collected from literature have been presented already in a previous publication[[14\]](#page-11-3). Briefly, they are the electron drift velocity *v*<sup>D</sup> [\[57](#page-11-46)[–66](#page-11-47)], the reduced mobility *µN* [\[57](#page-11-46)], the characteristic energy *ε*char = *D*T*/µ* [[67,](#page-11-48) [68](#page-11-49)], the reduced Townsend coefficient *α/N* [[69,](#page-11-50) [70\]](#page-11-51), the reduced attachment coefficient *η/N* [\[67](#page-11-48), [69–](#page-11-50)[72\]](#page-11-52) and the reduced effective Townsend coefficient, defined as the difference of the latter two[[59,](#page-11-53) [69,](#page-11-50) [70](#page-11-51)]. Here, *N* is the total gas number density, *µ* the electron mobility, *D*<sup>T</sup> the transverse diffusion coefficient, *α* the Townsend coefficient and *η* the attachment coefficient. When not given explicitly, the reduced mobility is calculated from *µN* = *v*D*N/E* with *E* being the electric field. In contrast to the space-homogeneous two-term Boltzmann solver LoKI-B, MC and density gradient expansion codes can also provide the reduced longitudinal diffusion coefficient *D*L*N* [\[64](#page-11-54), [73](#page-11-55)], allowing to extend the validation to one more parameter, and bulk transport parameters for comparison with the experimental values for high *E/N* values.

Special attention should be taken on how the transport coefficients are measured to optimally compare them with calculations. On the one hand, in time-of-flight (TOF) experiments the electron number is growing in time. Drift velocity and diffusion coefficients are measured in TOF conditions. On the other hand, Townsend and attachment coefficients are usually measured in so-called steady state Townsend (SST) conditions, i.e. with the electron number growing in space. Both TOF and SST measurements usually yield bulk transport coefficients [29, 30], see also the discussion of flux and bulk coefficients in section 1<sup>5</sup>.

In the calculations, the measurements are emulated by making use of the concepts of *temporal/spatial growth* as introduced by Hagelaar and Pitchford [27], where first the energy dependence of the electron distribution function is separated from the time- and space-dependent electron density    before in a simplifying step it is either assumed that    grows exclusively in time with a net production frequency or in space with a constant net spatial grow rate [27]. These concepts are borrowed by LoKI-B [18]. On the contrary, the current version of LoKI-MC simulates only TOF configurations. However, the Townsend and attachment coefficients in SST conditions can be derived from the TOF bulk parameters using the following approximate relation in equation (16) deduced from [31, 74, 75]:

<span id="page-7-2"></span>

(16)

where    is the SST ionisation coefficient;    is the SST drift velocity;    is the effective ionisation rate-coefficient;    and    are the bulk components of the drift velocity and longitudinal diffusion coefficient, respectively, calculated in a TOF simulation. A similar expression for the attachment coefficient    is used, with    instead of   .

Figure 4 demonstrates the agreement between the calculated transport coefficients (lines) with the experimentally determined ones from literature (markers). Please pay attention that    and    (both y-axis labels on the right) are plotted linearly while all other parameters are presented in logarithmic scale. Whenever known, the uncertainty of the experimental electron transport coefficients is shown as error bars. From top to bottom,   ,   ,   ,   ,    and    are plotted. Note that compared to [14], the E/N range below 9 Td is not shown since no difference is observable there between the isotropic and anisotropic sets and for better visibility of the differences of the remaining data. We refer to [14] for a discussion of the electron transport coefficients. According to the discussion in the preceding paragraph and as indicated by the arrows in the centre two panels,   ,   and    are calculated under TOF conditions with temporal growth of the electron number while   ,    and   are calculated under SST conditions with spatial growth of the electron number.

In figure 4, we see how the good agreement of the calculation using the isotropic set in LoKI-B (solid green line) with the experimental values is further improved when the anisotropy of the rotational collisions is taken into account (dashed magenta line). In particular, excellent accordance is found now

in    and   . The calculated values of    and    agree very well with the experiment and are rather similar for both sets, except for a small shift in    for E/N below 70 Td, comparable with the dispersion of the experimental points. Moreover, it should be noted that effects of anisotropic scattering for rotational collisions appear to be relevant still for E/N > 80 Td. This is an important difference with respect to results obtained for electrons in CO [26], where anisotropic scattering is relevant only for E/N < 5 Td. It is related to the different dipole moment magnitude, i.e. 0.728 for H<sub>2</sub>O compared with 0.0432 for CO, and to the shape of elastic MTCSs for the two molecules.

A just as excellent agreement with experimental data can be seen in figure 4 when using LoKI-MC. In particular, the flux results from LoKI-MC (dash-dotted blue line) almost perfectly align with the anisotropic results obtained from LoKI-B.

When ionisation and attachment start to play a major role, the split between the flux and bulk components (dotted light blue line) can be evidenced from    for E/N > 100 Td in figure 4. In fact, within a careful analysis these details can be accounted for [23, 29]. However considering the overall spread of the experimental data, it is noted that both flux and bulk calculated components follow the experiments fairly well with about 20% difference between the two. In total, it is the agreement with the bulk parameters, despite the fact that they were not considered in the previous work, that should be emphasised.

The experimental longitudinal diffusion coefficient times gas number density    is plotted in figure 5 against the reduced electric field together with calculation results from LoKI-MC using both the anisotropic and isotropic sets. Although the results with the isotropic set are satisfactory, the rigorous inclusion of anisotropic scattering remarkably improves the agreement with experiment for E/N below 100 Td. Furthermore, it should be emphasised that the proposed CS set gives good agreement (i) with a transport coefficient that at no point has been used for the optimisation of the set as it is not accessible with the used two-term code and (ii) using the MC instead of the two-term approach. It is worth highlighting that the second point is not guaranteed when using a CS set optimised with the two-term approximation in a more accurate methodology like MC simulation [32]. In figure 6, we also show that the EEDFs for both calculation methods agree very well. This underlines the validity and wide applicability of the proposed CS set.

#### <span id="page-7-0"></span>5. Effect of the gas temperature

As elaborated in [14], experimental electron transport coefficients for    are only reliably provided close to room temperature. For that reason, it was sufficient to run all simulation up to this point at gas temperature   .

As the rotations are treated slightly different in isotropic and anisotropic CS set, it is worthwhile to compare how both sets behave with changing   . Specifically, with changing gas temperature the populations of rotational and vibrational

<span id="page-7-1"></span><sup>&</sup>lt;sup>5</sup> The arrival time-spectra drift velocity of Hasegawa *et al* [59] can be converted to bulk data following the corrections in [29].

<span id="page-8-0"></span>**Figure 4.** Comparison of experimental transport coefficients (markers), when known with error bars, with those obtained from LoKI-B or LoKI-MC simulations with the proposed isotropic[[14\]](#page-11-3) and anisotropic cross section sets (lines). References to the experimental transport coefficients can be found in the text. As indicated by the arrows in the centre two panels, *v*D, *µN* and *ε*char are calculated assuming temporal growth of the electron number while for *α/N* and *η/N* spatial growth is assumed. LoKI-B provides exclusively flux transport coefficients and all shown LoKI-MC results include anisotropic rotational scattering.

levels, both assumed to follow a Boltzmann distribution at *T*gas, are changing. The larger the population in a certain level is, the more important transitions starting from that level get

in shaping the EEDF. In turn, also the transport coefficients calculated from the EEDF change. For illustration, figure [7](#page-9-2) exemplarily shows *ε*char in panel (a) and *µN* in panel (b)

<span id="page-9-1"></span><span id="page-9-0"></span>**Figure 5.** Longitudinal diffusion coefficient times gas number density *D*L*N* against the reduced electric field *E/N* in water vapour from literature and calculations with Monte Carlo simulation tool LoKI-MC[[64,](#page-11-54) [73](#page-11-55)].

**Figure 6.** EEDFs of water vapour as calculated with the present cross sections using either LoKI-B (dashed) or LoKI-MC (solid) for four different reduced electric fields. The inset on the top right shows the very low energy part of the same EEDFs.

<span id="page-9-2"></span>**Figure 7.** Electron transport coefficients calculated with LoKI-B using either the isotropic (solid lines) or anisotropic CS set (dashed lines) for different temperatures according to the colour bar on the right. The characteristic energy is shown in (a) and the reduced mobility in (b). Details to the experimental transport coefficients (markers) can be found in the main text [\[57](#page-11-46)–[68\]](#page-11-49).

calculated with LoKI-B using the isotropic (solid lines) or anisotropic CS set (dashed lines) for different temperatures. The markers represent experimental transport coefficients, see section [4.](#page-6-0)

The blue lines in figure [7,](#page-9-2) exhibiting the best agreement with the experimental transport coefficients, correspond to the calculations at 293 K that are already plotted in figure [4](#page-8-0). Without going into too much detail, we note that (i) with changing *T*gas the lines start to deviate from the experiments at room temperature, as expected, and (ii) the discrepancy between the isotropic and anisotropic set also changes as a function of temperature. The second point is particularly well observed for the reduced mobility in figure [7](#page-9-2)(b) at high temperature (yellow), where there is a difference between the two calculations over the full *E/N*-range. This finding suggests that measurements of electron transport coefficients in H2O at different *T*gas are very much sought after to further validate the present set of electron-impact CSs. Finally, we should underline that a set with lumped rotational CSs would not be able to describe the same behaviour with *T*gas, since it would miss the important effect of the change in rotational populations.

### <span id="page-10-9"></span>**6. Conclusion**

Even though water molecules are frequently encountered in many innovative plasma applications, there is room for improvement of the H2O-electron collision CSs which are required for the determination of the EEDF. In particular, since water molecules are asymmetric-top rotors with permanent dipole moment, the rigorous inclusion of electron-impact rotational collisions is rather challenging.

In a previous work[[14\]](#page-11-3), we presented a complete CS set for H2O, under the typical isotropic assumption present in most electron Boltzmann two-term solvers. Since the rotational collisions in H2O are highly anisotropic, the corresponding CSs were artificially decreased in [\[14](#page-11-3)] so as to diminish the momentum transfer due to these processes. This approach was validated against experimental measurements, but there were still visible deviations between the calculations and the experimental data in the reduced mobility and the characteristic energy.

In this work, we pursued a different path and included the influence of anisotropic electron scattering in rotational collisions. Without modifying the CS of any other process besides rotations and using directly the rotational CSs from dipole-Born theory, the agreement with experiment for the mobility and the characteristic energy is now excellent as well.

The usage of the MC simulations code LoKI-MC allowed us to gain insight into the applicability of the present CS set that must be assumed *a priori* to be limited to two-term Boltzmann solvers as used for its derivation. First, we could verify that the electron transport coefficients calculated with the two-term Boltzmann solver LoKI-B agree very well with the MC solution, both when using the isotropic or the anisotropic sets. Note, that this agreement is somewhat coincidental and not due to a firm physical background. We conclude that there is a de facto *a posteriori* verification that the two-term approximation yields accurate results with the developed CS set for H2O and that the set is not exclusively suited for use in two-term Boltzmann solvers but also in the more accurate MC simulation method. Additionally, we could extend the validation to parameters that cannot be obtained by LoKI-B, such as the bulk transport coefficients or the longitudinal diffusion coefficient. The excellent agreement between LoKI-MC calculations and measurements of the latter, that were not considered in our previous analysis, is a further confirmation of the validity of the present CS set.

This work shows that the correct treatment of the angular distribution of the scattered electrons is essential to have an accurate description of electron swarms in water. This can be easily handled with the two open-source codes LoKI-B and LoKI-MC.

The CS set developed here will be available in the IST-Lisbon database on LXCat and can be used directly in LoKI-B and LoKI-MC to calculate more accurate electron distribution functions and the corresponding electron parameters leading to more refined plasma chemistry models. For codes where anisotropic scattering cannot be included, the CS set presented in our previous work[[14\]](#page-11-3) remains useful data to describe the electron kinetics in systems containing water vapour.

In a future work, we plan to quantify the importance of anisotropic scattering for the main gases of interest in the plasma community.

#### **Data availability statement**

The data cannot be made publicly available upon publication because no suitable repository exists for hosting data in this field of study. The data that support the findings of this study are available upon reasonable request from the authors.

### **Acknowledgment**

We acknowledge the valuable comments of Luís Lemos Alves. This work was partially supported by the European Union's Horizon 2020 research and innovation programme under grant agreement MSCA ITN 813393, by Portuguese FCT-Fundaç˜ao para a Ciˆencia e a Tecnologia, under Projects UIDB/50010/2020, UIDP/50010/2020 and PTDC/FIS-PLA/1616/2021 (PARADiSE), Grant PD/BD/ 150414/2019 (PD-F APPLAuSE), and EXPL/FIS-PLA/0076/2021. LV acknowledges fundings from Deutsche Forschungsgemeinschaft (DFG, German Research Foundation)—Project-ID 434434223—SFB 1461.

# **ORCID iDs**

Maik Budde <https://orcid.org/0000-0002-9084-4471> Tiago Cunha Dias <https://orcid.org/0000-0002-2179-1345> Luca Vialetto <https://orcid.org/0000-0003-3802-8001> Nuno Pinh˜ao <https://orcid.org/0000-0002-4185-2619> Vasco Guerra <https://orcid.org/0000-0002-6878-6850> Tiago Silva <https://orcid.org/0000-0001-9046-958X>

### **References**

- <span id="page-10-0"></span>[1] Damen M A, Martini L M and Engeln R 2020 *Plasma Sources Sci. Technol.* **[29](https://doi.org/10.1088/1361-6595/abad54)** [095017](https://doi.org/10.1088/1361-6595/abad54)
- <span id="page-10-1"></span>[2] Verheyen C, Silva T, Guerra V and Bogaerts A 2020 *Plasma Sources Sci. Technol.* **[29](https://doi.org/10.1088/1361-6595/aba1c8)** [095009](https://doi.org/10.1088/1361-6595/aba1c8)
- <span id="page-10-2"></span>[3] Médard N, Soutif J C and Poncin-Epaillard F 2002 *Langmuir* **[18](https://doi.org/10.1021/la011481i)** [2246–53](https://doi.org/10.1021/la011481i)
- <span id="page-10-3"></span>[4] Thorn P, Campbell L and Brunger M 2009 *PMC Phys.* B **[2](https://doi.org/10.1186/1754-0429-2-1)** [1](https://doi.org/10.1186/1754-0429-2-1)
- <span id="page-10-4"></span>[5] Bodewits D, Országh J, Noonan J, Durian M and Matejcˇík ˇ Sˇ 2019 *Astrophys. J.* **[885](https://doi.org/10.3847/1538-4357/ab43c9)** [167](https://doi.org/10.3847/1538-4357/ab43c9)
- <span id="page-10-5"></span>[6] Micca Longo G, Vialetto L, Diomede P, Longo S and Laporta V 2021 *Molecules* **[26](https://doi.org/10.3390/molecules26123663)** [3663](https://doi.org/10.3390/molecules26123663)
- <span id="page-10-6"></span>[7] Giardina A, Tampieri F, Biondo O, Marotta E and Paradisi C 2019 *Chem. Eng. J.* **[372](https://doi.org/10.1016/j.cej.2019.04.098)** [171–80](https://doi.org/10.1016/j.cej.2019.04.098)
- <span id="page-10-7"></span>[8] Meunier N, Laribi S, Dubois L, Thomas D and De Weireld G 2014 *Energy Proc.* **[63](https://doi.org/10.1016/j.egypro.2014.11.685)** [6492–503](https://doi.org/10.1016/j.egypro.2014.11.685)
- <span id="page-10-8"></span>[9] Chang Y, Mendrea B, Sterniak J and Bohac S V 2016 *J. Eng. Gas Turbines Power* **[139](https://doi.org/10.1115/1.4034966)** [023002](https://doi.org/10.1115/1.4034966)

- <span id="page-11-0"></span>[10] Alves L L, Bogaerts A, Guerra V and Turner M M 2018 Plasma Sources Sci. Technol. 27 023002
- <span id="page-11-1"></span>[11] Itikawa Y and Mason N 2005 J. Phys. Chem. Ref. Data 34 1–22
- <span id="page-11-9"></span>[12] Ness K F and Robson R E 1988 Phys. Rev. A 38 1446-56
- <span id="page-11-2"></span>[13] Song M Y, Cho H, Karwasz G P, Kokoouline V, Nakamura Y, Tennyson J, Faure A, Mason N J and Itikawa Y 2021 J. Phys. Chem. Ref. Data 50 023103
- <span id="page-11-3"></span>[14] Budde M, Dias T C, Vialetto L, Pinhão N, Guerra V and Silva T 2022 *J. Phys. D: Appl. Phys.* **55** 445205
- <span id="page-11-4"></span>[15] Alves L L 2014 J. Phys.: Conf. Ser. 565 012007
- <span id="page-11-5"></span>[16] Carbone E, Graef W, Hagelaar G, Boer D, Hopkins M M, Stephens J C, Yee B T, Pancheshnyi S, van Dijk J and Pitchford L 2021 Atoms 9 16
- <span id="page-11-6"></span>[17] Pitchford L C, McKoy B V, Chutjian A and Trajmar S 1987 Swarm studies and inelastic electron-molecule collisions: Proc. Meeting of the 4th Int. Swarm Seminar and the Inelastic Electron-Molecule Collisions Symp. (Tahoe City, California, USA) (New York: Springer)
- <span id="page-11-7"></span>[18] Tejero-del-Caz A, Guerra V, Gonçalves D, Silva M L d, Marques L, Pinhão N, Pintassilgo C D and Alves L L 2019 Plasma Sources Sci. Technol. 28 043001
- <span id="page-11-8"></span>[19] Hake R D and Phelps A V 1967 Phys. Rev. 158 70-84
- <span id="page-11-10"></span>[20] Faure A, Gorfinkiel J D and Tennyson J 2004 Mon. Not. R. Astron. Soc. 347 323–33
- <span id="page-11-11"></span>[21] Faure A, Gorfinkiel J D and Tennyson J 2004 J. Phys. B: At. Mol. Opt. Phys. 37 801–7
- <span id="page-11-12"></span>[22] Napartovich A P, Dyatko N A, Kochetov I V and Sukharev A G 2010 Triniti database (available at: www.lxcat.net/Triniti)
- <span id="page-11-13"></span>[23] Kawaguchi S, Takahashi K, Satoh K and Itoh H 2016 Japan. J. Appl. Phys. 55 07LD03
- <span id="page-11-14"></span>[24] Biagi S 1999 Nucl. Instrum. Methods Phys. Res. A 421 234–40
- <span id="page-11-15"></span>[25] Itikawa Y 1972 J. Phys. Soc. Japan. 32 217–26
- <span id="page-11-16"></span>[26] Vialetto L, Moussa A B, Dijk J v, Longo S, Diomede P, Guerra V and Alves L L 2021 Plasma Sources Sci. Technol. 30 075001
- <span id="page-11-17"></span>[27] Hagelaar G J M and Pitchford L C 2005 Plasma Sources Sci. Technol. 14 722–33
- <span id="page-11-18"></span>[28] Reid I D 1979 Aust. J. Phys. 32 231-54
- <span id="page-11-19"></span>[29] Ness K F, Robson R E, Brunger M J and White R D 2012 J. Chem. Phys. 136 024318
- <span id="page-11-20"></span>[30] Robson R E, White R D and Ness K F 2011 J. Chem. Phys. 134 064319
- <span id="page-11-21"></span>[31] Pinhão N, Loffhagen D, Vass M, Hartmann P, Korolov I, Dujko S, Bošnjaković D and Donkó Z 2020 Plasma Sources Sci. Technol. 29 045009
- <span id="page-11-22"></span>[32] Petrović Z L, Dujko S, Marić D, Malović G, Nikitović Ž Šašić O, Jovanović J, Stojanović V and Radmilović-Raenović M 2009 J. Phys. D: Appl. Phys. 42 194002
- <span id="page-11-23"></span>[33] Alves L L 2019 IST-Lisbon GitHub (available at: https://githubcom/IST-Lisbon)
- <span id="page-11-24"></span>[34] Dias T C, Tejero-del-Caz A, Alves L L and Guerra V 2023 Comput. Phys. Commun. 282 108554
- <span id="page-11-25"></span>[35] Šimečková M, Jacquemart D, Rothman L S, Gamache R R and Goldman A 2006 J. Quant. Spectrosc. Radiat. Transfer 98 130–55
- <span id="page-11-26"></span>[36] Gianturco F A and Jain A 1986 Phys. Rep. 143 347-425
- <span id="page-11-27"></span>[37] Crawford O H 1967 J. Chem. Phys. 47 1100-4
- <span id="page-11-28"></span>[38] King G W, Hainer R M and Cross P C 1947 *Phys. Rev.* 71 433–43
- <span id="page-11-29"></span>[39] Shimamura I and Takayanagi K 2013 *Electron-Molecule Collisions* (Berlin: Springer)
- <span id="page-11-30"></span>[40] Takayanagi K 1966 J. Phys. Soc. Japan 21 507–14
- <span id="page-11-31"></span>[41] Pitchford L C et al 2013 J. Phys. D: Appl. Phys. 46 334001

- <span id="page-11-32"></span>[42] Makabe T and White R 2015 J. Phys. D: Appl. Phys. 48 485205
- <span id="page-11-33"></span>[43] Makabe T and Petrović Z 2014 *Plasma Electronics:*Applications in Microelectronic Device Fabrication 2nd edn
  (Boca Raton, FL: CRC Press) pp 1–369
- <span id="page-11-34"></span>[44] Klein O and Rosseland S 1921 Z. Phys. 4 46–51
- <span id="page-11-35"></span>[45] Longo S 2000 Plasma Sources Sci. Technol. 9 468-76
- <span id="page-11-38"></span>[46] Phelps A and Pitchford L 1985 Phys. Rev. A 31 2932
- <span id="page-11-39"></span>[47] Janssen J, Pitchford L C, Hagelaar G and van Dijk J 2016 Plasma Sources Sci. Technol. 25 055026
- <span id="page-11-36"></span>[48] Biagi S Magboltz 11.9 1995 (available at: https://magboltz.web.cern.ch/magboltz/)
- <span id="page-11-40"></span>[49] Seng G and Linder F 1976 J. Phys. B: Atom. Mol. Phys. 9 2539–51
- <span id="page-11-41"></span>[50] Khakoo M A, Winstead C and McKoy V 2009 Phys. Rev. A 79 052711
- <span id="page-11-42"></span>[51] Ralphs K, Serna G, Hargreaves L R, Khakoo M A, Winstead C and McKoy V 2013 J. Phys. B: At. Mol. Opt. Phys. 46 125201
- <span id="page-11-43"></span>[52] Matsui M, Hoshino M, Kato H, da Silva F F, Limão-Vieira P and Tanaka H 2016 Eur. Phys. J. D 70 77
- <span id="page-11-44"></span>[53] Harb T, Kedzierski W and McConkey J W 2001 J. Chem. Phys. 115 5507–12
- [54] Beenakker C I M, de Heer F J, Krop H B and Möhlmann G R 1974 Chem. Phys. 6 445–54
- <span id="page-11-45"></span>[55] Kedzierski W, Derbyshire J, Malone C and McConkey J W 1998 J. Phys. B: At. Mol. Opt. Phys. 31 5361–8
- <span id="page-11-37"></span>[56] Itikawa Y 2012 Itikawa database (available at:www.lxcat.net/
- <span id="page-11-46"></span>[57] Cheung B and Elford M T 1990 The drift velocity of electrons in water vapour at low values of E/N Aust. J. Phys. 43 755–63
- [58] de Urquijo J, Basurto E, Juárez A M, Ness K F, Robson R E, Brunger M J and White R D 2014 J. Chem. Phys. 141 014308
- <span id="page-11-53"></span>[59] Hasegawa H, Date H and Shimozuma M 2007 J. Phys. D: Appl. Phys. 40 2495–8
- [60] Lowke J J and Rees J A 1963 Aust. J. Phys. 16 447–53
- [61] Pack J L, Voshall R E and Phelps A V 1962 Phys. Rev. 127 2084–9
- [62] Ruíz-Vargas G, Yousfi M and de Urquijo J 2010 J. Phys. D: Appl. Phys. 43 455201
- [63] Ryzko H 1965 Proc. Phys. Soc. 85 1283-95
- <span id="page-11-54"></span>[64] Wilson J F, Davis F J, Nelson D R, Compton R N and Crawford O H 1975 J. Chem. Phys. 62 4204–12
- [65] Christophorou L G and Christodoulides A A 1969 J. Phys. B: Atom. Mol. Phys. 2 71–85
- <span id="page-11-47"></span>[66] Bailey V A and Duncanson W E 1930 London, Edinburgh Dublin Phil. Mag. J. Sci. 10 145–60
- <span id="page-11-48"></span>[67] Elford M T 1987 Proc. XVIII Int. Conf. on the Phenomena in Ionized Gases (Swansea, Wales) (London: Hilger) p 130
- <span id="page-11-49"></span>[68] Crompton R W, Rees J A and Jory R L 1965 Aust. J. Phys. 18 541
- <span id="page-11-50"></span>[69] Risbud A V and Naidu M S 1979 *J. Phys. Colloq.* **40** C7-77–C7-78
- <span id="page-11-51"></span>[70] Prasad A N and Craggs J D 1960 Proc. Phys. Soc. 76 223–32
- [71] Kuffel E 1959 Proc. Phys. Soc. 74 297–308
- <span id="page-11-52"></span>[72] Parr J E and Moruzzi J L 1972 *J. Phys. D: Appl. Phys.* **5** 514–24
- <span id="page-11-55"></span>[73] Yousfi M, Bekstein A, Merbahi N, Eichwald O, Ducasse O, Benhenni M and Gardou J P 2010 Plasma Sources Sci. Technol. 19 034004
- <span id="page-11-56"></span>[74] Blevin H A and Fletcher J 1984 Aust. J. Phys. 37 593
- <span id="page-11-57"></span>[75] Dujko S, Bošnjaković D, Vass M, Hartmann P, Korolov I, Pinhão N R, Loffhagen D and Donkó Z 2023 Plasma Sources Sci. Technol. 32 025014
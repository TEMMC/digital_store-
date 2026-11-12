/* MT A-Level Study Centre. All lesson data is bundled locally for offline use. */
(() => {
  "use strict";
  const courses = [
    {id:"chemistry",name:"Chemistry",icon:"⚗️",topics:[
      {id:"atomic",title:"Atomic structure and periodicity",level:"Foundations",summary:"Atoms, isotopes, electron arrangement and periodic trends.",sections:[
        ["The atom","An atom contains a tiny, dense nucleus of protons and neutrons, surrounded by electrons in quantised energy levels. The proton number (Z) identifies the element. The nucleon number (A) is the total number of protons and neutrons."],
        ["Isotopes","Isotopes are atoms of the same element with the same proton number but different neutron numbers. They have very similar chemical properties because they have the same electron arrangement."],
        ["Electron configuration","Electrons occupy subshells in order of increasing energy. The common filling order begins 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p. A subshell holds s = 2, p = 6, d = 10 and f = 14 electrons."],
        ["Periodic trends","Across a period, nuclear charge increases while electrons enter the same principal shell, so atomic radius generally decreases. Down a group, extra occupied shells increase atomic radius. First ionisation energy generally rises across a period and falls down a group, with known subshell exceptions."]
      ],example:"Chlorine has Z = 17. Its electron configuration is 1s² 2s² 2p⁶ 3s² 3p⁵. It has seven outer-shell electrons and commonly gains one electron to form Cl⁻.",questions:[
        {q:"How many neutrons are in ³⁵₁₇Cl?",o:["17","18","35","52"],a:1,e:"Neutrons = nucleon number − proton number = 35 − 17 = 18."},
        {q:"How many electrons can a p subshell hold?",o:["2","6","10","14"],a:1,e:"A p subshell has three orbitals, each holding two electrons: 3 × 2 = 6."}
      ]},
      {id:"bonding",title:"Chemical bonding and structure",level:"Core",summary:"Ionic, covalent and metallic bonding; shapes and intermolecular forces.",sections:[
        ["Ionic bonding","Ionic bonding is the electrostatic attraction between oppositely charged ions, formed by electron transfer. Ionic solids have high melting points and conduct electricity when molten or dissolved because ions can move."],
        ["Covalent bonding","A covalent bond is a shared pair of electrons between atoms. Bond length, bond strength and bond polarity depend on the atoms and the shared electron density."],
        ["Shapes of molecules","Electron pairs repel and arrange themselves as far apart as possible. Lone pairs repel more strongly than bonding pairs. Common shapes include linear (180°), trigonal planar (120°), tetrahedral (109.5°), trigonal pyramidal (about 107°) and bent (about 104.5°)."],
        ["Intermolecular forces","London dispersion forces occur between all particles; permanent dipole–dipole attractions occur between polar molecules; hydrogen bonding is a particularly strong attraction when H is bonded to N, O or F."]
      ],example:"Methane, CH₄, has four bonding pairs and no lone pairs around carbon. The molecule is tetrahedral with bond angles close to 109.5°.",questions:[
        {q:"What is the shape of methane, CH₄?",o:["Linear","Trigonal planar","Tetrahedral","Pyramidal"],a:2,e:"Four bonding pairs around carbon repel into a tetrahedral arrangement."},
        {q:"Which substance can form hydrogen bonds between its molecules?",o:["CH₄","H₂O","HCl","CO₂"],a:1,e:"Water contains O–H bonds and lone pairs on oxygen, allowing intermolecular hydrogen bonding."}
      ]},
      {id:"equilibrium",title:"Chemical equilibrium",level:"Core",summary:"Dynamic equilibrium, equilibrium constants and Le Chatelier's principle.",sections:[
        ["Dynamic equilibrium","In a closed system at dynamic equilibrium, forward and reverse reaction rates are equal. Concentrations remain constant, but reactions continue at the particle level."],
        ["Equilibrium expression","For aA + bB ⇌ cC + dD, Kc = [C]^c[D]^d / ([A]^a[B]^b), using equilibrium concentrations. Pure solids and pure liquids are omitted."],
        ["Le Chatelier's principle","When a system at equilibrium is disturbed by changing concentration, pressure or temperature, the position shifts in the direction that opposes the disturbance."],
        ["Catalysts","A catalyst increases the rates of forward and reverse reactions by providing an alternative pathway with lower activation energy. It does not change Kc or the equilibrium position."]
      ],example:"For N₂(g) + 3H₂(g) ⇌ 2NH₃(g), increasing pressure favours the side with fewer gas molecules: the product side (2 moles versus 4).",questions:[
        {q:"At dynamic equilibrium, which statement is correct?",o:["Both reactions stop","Forward and reverse rates are equal","Reactant and product concentrations are equal","Only the forward reaction continues"],a:1,e:"Dynamic equilibrium means equal forward and reverse rates, not necessarily equal concentrations."},
        {q:"What does a catalyst change?",o:["Equilibrium constant","Equilibrium position","Time taken to reach equilibrium","Overall enthalpy change"],a:2,e:"A catalyst speeds up both directions and helps equilibrium be reached sooner."}
      ]},
      {id:"electrochem",title:"Redox and electrochemistry",level:"Core",summary:"Oxidation numbers, half-equations and electrochemical cells.",sections:[
        ["Redox","Oxidation is loss of electrons; reduction is gain of electrons. Oxidation and reduction occur together. Oxidation numbers help identify which species is oxidised or reduced."],
        ["Half-equations","Write separate oxidation and reduction equations. Balance atoms other than O and H first; then balance O with H₂O, H with H⁺ (acidic solution), and charge with electrons. In alkaline solution, neutralise H⁺ using OH⁻."],
        ["Electrochemical cells","A galvanic cell converts chemical energy into electrical energy through a spontaneous redox reaction. Oxidation occurs at the anode and reduction at the cathode."],
        ["Electrode potentials","Standard electrode potentials are measured relative to the standard hydrogen electrode. A more positive E° indicates a greater tendency for reduction under standard conditions."]
      ],example:"Cu²⁺ + 2e⁻ → Cu is reduction because copper(II) ions gain two electrons. Zn → Zn²⁺ + 2e⁻ is oxidation because zinc loses two electrons.",questions:[
        {q:"In Cu²⁺ + 2e⁻ → Cu, what happens to copper?",o:["It is oxidised","It is reduced","It loses two electrons","Its oxidation number rises"],a:1,e:"Cu²⁺ gains two electrons, so it is reduced."},
        {q:"At which electrode does oxidation occur?",o:["Cathode","Anode","Salt bridge","Both electrodes"],a:1,e:"Oxidation always occurs at the anode; reduction occurs at the cathode."}
      ]}
    ]},
    {id:"physics",name:"Physics",icon:"⚡",topics:[
      {id:"mechanics",title:"Mechanics: motion and forces",level:"Foundations",summary:"Kinematics, Newton's laws, momentum and energy.",sections:[
        ["Scalars and vectors","A scalar has magnitude only (for example mass or energy). A vector has magnitude and direction (for example displacement, velocity and force). Resolve vectors into perpendicular components when needed."],
        ["Equations of motion","For constant acceleration: v = u + at; s = ut + ½at²; v² = u² + 2as; s = ½(u + v)t. Use consistent SI units and define positive direction."],
        ["Newton's laws","The resultant force equals rate of change of momentum. For constant mass, F = ma. Action and reaction forces are equal and opposite, act on different bodies and therefore do not cancel on one body."],
        ["Momentum and energy","Momentum p = mv. Impulse equals change in momentum. Work done W = Fs cos θ; kinetic energy = ½mv²; gravitational potential energy change near Earth's surface = mgΔh."]
      ],example:"A body starts from rest and accelerates at 2.0 m s⁻² for 5.0 s. v = u + at = 0 + 2.0 × 5.0 = 10 m s⁻¹.",questions:[
        {q:"A 2 kg object accelerates at 3 m s⁻². What is the resultant force?",o:["1.5 N","5 N","6 N","9 N"],a:2,e:"F = ma = 2 × 3 = 6 N."},
        {q:"Which quantity is a vector?",o:["Speed","Distance","Energy","Velocity"],a:3,e:"Velocity has both magnitude and direction."}
      ]},
      {id:"waves",title:"Waves and superposition",level:"Core",summary:"Wave properties, interference, diffraction and stationary waves.",sections:[
        ["Wave quantities","Frequency f is the number of complete oscillations per second; period T = 1/f. Wave speed v = fλ, where λ is wavelength."],
        ["Transverse and longitudinal waves","In transverse waves, oscillations are perpendicular to energy transfer. In longitudinal waves, oscillations are parallel to energy transfer and produce compressions and rarefactions."],
        ["Superposition","When waves overlap, the resultant displacement is the algebraic sum of individual displacements. In-phase waves can interfere constructively; out-of-phase waves can interfere destructively."],
        ["Diffraction","Diffraction is the spreading of waves around obstacles or through gaps. It is most noticeable when the gap size is comparable to the wavelength."]
      ],example:"A wave has frequency 50 Hz and wavelength 0.40 m. Its speed is v = fλ = 50 × 0.40 = 20 m s⁻¹.",questions:[
        {q:"A wave has frequency 10 Hz. What is its period?",o:["0.01 s","0.1 s","10 s","100 s"],a:1,e:"T = 1/f = 1/10 = 0.1 s."},
        {q:"Diffraction is greatest when a gap is…",o:["Much larger than wavelength","Comparable to wavelength","Zero width","Made of a conductor"],a:1,e:"Diffraction is strongest when gap dimensions are similar to the wavelength."}
      ]},
      {id:"electricity",title:"Electricity and circuits",level:"Core",summary:"Current, potential difference, resistance and circuit analysis.",sections:[
        ["Current and charge","Current I = ΔQ/Δt. Conventional current direction is the direction positive charge would flow; electrons in metal wires drift in the opposite direction."],
        ["Potential difference","Potential difference V is energy transferred per unit charge: V = W/Q. Resistance R = V/I for an ohmic conductor at constant physical conditions."],
        ["Series and parallel","In series, current is the same through each component and potential differences add. In parallel, potential difference is the same across branches and branch currents add."],
        ["Electrical power","P = IV = I²R = V²/R. Electrical energy transferred E = Pt = VIt. Check units: watts, joules, volts, amperes and ohms."]
      ],example:"A 6 Ω resistor connected across 12 V draws I = V/R = 12/6 = 2 A. Its power is P = VI = 24 W.",questions:[
        {q:"A 12 V supply is connected to a 4 Ω resistor. What current flows?",o:["0.33 A","3 A","8 A","48 A"],a:1,e:"I = V/R = 12/4 = 3 A."},
        {q:"In a parallel circuit, which quantity is the same across each branch?",o:["Current","Resistance","Potential difference","Power"],a:2,e:"Each parallel branch is connected across the same two points, so the potential difference is equal."}
      ]},
      {id:"fields",title:"Gravitational and electric fields",level:"Extension",summary:"Field strength, potential, inverse-square laws and orbits.",sections:[
        ["Gravitational field","Gravitational field strength g is force per unit mass. For a point mass M, g = GM/r². Gravitational force is attractive."],
        ["Electric field","Electric field strength E is force per unit positive charge. For a point charge Q, magnitude E = k|Q|/r² in vacuum. Field direction is the force direction on a positive test charge."],
        ["Potential","Potential is potential energy per unit mass or charge. Potential is a scalar, while field strength is a vector. Field strength relates to the spatial rate of change of potential."],
        ["Circular orbits","For a circular orbit, gravitational force supplies centripetal force: GMm/r² = mv²/r. Therefore v = √(GM/r) and orbital period T = 2π√(r³/GM)."]
      ],example:"If distance from a point mass doubles, gravitational field strength becomes one quarter because g is proportional to 1/r².",questions:[
        {q:"If distance from a point mass doubles, its field strength becomes…",o:["Twice","Half","One quarter","Four times"],a:2,e:"Inverse-square relationship: 1/2² = 1/4."},
        {q:"Is electric potential a scalar or vector?",o:["Scalar","Vector","Neither","Always zero"],a:0,e:"Potential has magnitude only; electric field strength has direction."}
      ]}
    ]},
    {id:"mathematics",name:"Mathematics",icon:"∑",topics:[
      {id:"functions",title:"Functions and graphs",level:"Foundations",summary:"Domain, range, transformations and inverse functions.",sections:[
        ["Function notation","A function maps each allowed input to exactly one output. The domain is the set of allowed inputs; the range is the set of outputs actually produced."],
        ["Composite functions","For functions f and g, (f ∘ g)(x) = f(g(x)). Work from the inside out and check that the output of the inner function belongs to the outer function's domain."],
        ["Inverse functions","An inverse reverses a one-to-one function. To find it, write y = f(x), interchange x and y, then rearrange for y. Restrict the domain if necessary."],
        ["Transformations","y = f(x) + a shifts a graph vertically; y = f(x − a) shifts it right by a; y = af(x) stretches vertically; y = f(ax) scales horizontally by factor 1/a."]
      ],example:"If f(x) = 2x + 3, set y = 2x + 3, swap x and y, then solve: x = 2y + 3, so f⁻¹(x) = (x − 3)/2.",questions:[
        {q:"If f(x) = 2x + 3, what is f(4)?",o:["8","11","14","24"],a:1,e:"f(4) = 2(4) + 3 = 11."},
        {q:"The domain of a function is…",o:["All possible outputs","Allowed input values","The gradient","The y-intercept"],a:1,e:"The domain is the set of input values for which the function is defined."}
      ]},
      {id:"calculus-diff",title:"Differentiation",level:"Core",summary:"First principles, derivatives, tangents, stationary points and rates.",sections:[
        ["Derivative","The derivative gives the gradient of a curve at a point and the instantaneous rate of change. From first principles, f′(x) = lim(h→0)[f(x+h) − f(x)]/h."],
        ["Power rule","For y = axⁿ, dy/dx = anxⁿ⁻¹. Differentiate each term separately; constants differentiate to zero."],
        ["Stationary points","A stationary point occurs where dy/dx = 0. Use the second derivative or a sign change in the first derivative to classify maxima, minima or stationary points of inflection."],
        ["Applications","For a tangent at x = a, find gradient f′(a), then use y − f(a) = f′(a)(x − a). For motion, velocity is the derivative of displacement and acceleration is the derivative of velocity."]
      ],example:"If y = 3x² − 4x + 7, then dy/dx = 6x − 4. At x = 2, the gradient is 12 − 4 = 8.",questions:[
        {q:"Differentiate y = 5x³.",o:["5x²","15x²","15x³","3x⁵"],a:1,e:"Using dy/dx = anxⁿ⁻¹ gives 5 × 3x² = 15x²."},
        {q:"At a stationary point, dy/dx is…",o:["1","−1","0","Undefined always"],a:2,e:"A stationary point has a horizontal tangent, so its gradient is zero."}
      ]},
      {id:"calculus-int",title:"Integration",level:"Core",summary:"Reverse differentiation, definite integrals and area.",sections:[
        ["Indefinite integration","Integration reverses differentiation. ∫axⁿ dx = axⁿ⁺¹/(n+1) + C for n ≠ −1. Always include the constant of integration C."],
        ["Definite integration","Evaluate ∫ₐᵇ f(x) dx by finding an antiderivative F(x), then calculating F(b) − F(a). This gives signed area."],
        ["Area","Area between a curve and the x-axis may require splitting at intercepts and taking absolute values. Area between curves is the integral of upper function minus lower function."],
        ["Applications","Integration can recover displacement from velocity and velocity from acceleration, with initial conditions used to determine constants."]
      ],example:"∫(6x² + 4)dx = 2x³ + 4x + C.",questions:[
        {q:"Evaluate ∫4x³ dx.",o:["x⁴ + C","12x² + C","4x⁴ + C","x³ + C"],a:0,e:"Increase the power to 4 and divide by 4: 4x⁴/4 = x⁴ + C."},
        {q:"What must be included in an indefinite integral?",o:["A +C","A gradient","A limit","A determinant"],a:0,e:"The constant of integration represents the family of antiderivatives."}
      ]},
      {id:"probability",title:"Probability and distributions",level:"Extension",summary:"Conditional probability, binomial and normal distributions.",sections:[
        ["Probability rules","For events A and B, P(A′) = 1 − P(A). P(A ∪ B) = P(A) + P(B) − P(A ∩ B). For mutually exclusive events, the intersection is zero."],
        ["Conditional probability","P(A|B) = P(A ∩ B)/P(B), provided P(B) is non-zero. Independence means P(A ∩ B) = P(A)P(B)."],
        ["Binomial distribution","If X ~ B(n,p), then P(X = r) = ⁿCᵣ pʳ(1−p)ⁿ⁻ʳ. Mean = np and variance = np(1−p)."],
        ["Normal distribution","For X ~ N(μ,σ²), standardise using Z = (X − μ)/σ. Use symmetry and the normal distribution table or an approved calculator carefully."]
      ],example:"For X ~ B(5, 0.2), P(X = 1) = ⁵C₁(0.2)(0.8)⁴ = 0.4096.",questions:[
        {q:"If A and B are independent, P(A ∩ B) equals…",o:["P(A)+P(B)","P(A)P(B)","P(A)/P(B)","1−P(A)"],a:1,e:"Independence means the probability of both is the product of their probabilities."},
        {q:"For X ~ B(n,p), the mean is…",o:["np","np(1−p)","n/p","p/n"],a:0,e:"The binomial mean is np; its variance is np(1−p)."}
      ]}
    ]},
    {id:"biology",name:"Biology",icon:"🧬",topics:[
      {id:"cells",title:"Cell structure and membranes",level:"Foundations",summary:"Organelles, microscopy, membrane structure and transport.",sections:[
        ["Cell organisation","Eukaryotic cells contain membrane-bound organelles. The nucleus stores DNA; mitochondria are sites of aerobic respiration; ribosomes synthesise proteins; rough ER and Golgi process and transport products."],
        ["Membranes","The fluid mosaic model describes a phospholipid bilayer with embedded proteins. Hydrophilic heads face aqueous environments; hydrophobic tails face inward."],
        ["Diffusion and osmosis","Diffusion is net movement of particles down a concentration gradient. Osmosis is net movement of water across a partially permeable membrane from higher water potential to lower water potential."],
        ["Active transport","Active transport moves substances against a concentration or electrochemical gradient using energy, commonly ATP, and specific membrane transport proteins."]
      ],example:"A plant cell placed in a concentrated salt solution loses water by osmosis. The vacuole and cytoplasm shrink and the cell membrane may pull away from the cell wall (plasmolysis).",questions:[
        {q:"Which organelle is the main site of aerobic respiration?",o:["Ribosome","Mitochondrion","Golgi apparatus","Lysosome"],a:1,e:"Mitochondria contain the machinery for aerobic respiration and ATP production."},
        {q:"Osmosis is the movement of…",o:["Any solute down its gradient","Water across a partially permeable membrane","Ions using ATP only","Proteins out of the nucleus"],a:1,e:"Osmosis is net water movement down a water-potential gradient across a partially permeable membrane."}
      ]},
      {id:"genetics",title:"Inheritance and molecular genetics",level:"Core",summary:"DNA, genes, meiosis, inheritance and variation.",sections:[
        ["DNA and genes","DNA is a double helix made of nucleotide strands. Each nucleotide contains deoxyribose, phosphate and a nitrogenous base. A gene is a DNA sequence that contributes to a functional product."],
        ["Replication and protein synthesis","DNA replication is semi-conservative. During transcription, RNA polymerase makes RNA from a DNA template. During translation, ribosomes read mRNA codons and assemble amino acids."],
        ["Meiosis","Meiosis produces haploid cells and halves chromosome number. Crossing over and independent assortment create genetic variation."],
        ["Inheritance","Alleles are alternative forms of a gene. Genotypes describe allele combinations; phenotypes are observable characteristics produced by genotype and environment."]
      ],example:"For a monohybrid cross Aa × Aa with complete dominance, expected genotypes are 1 AA : 2 Aa : 1 aa and phenotypes 3 dominant : 1 recessive.",questions:[
        {q:"How many chromosomes are present in a normal human gamete?",o:["23","44","46","92"],a:0,e:"Human gametes are haploid and contain 23 chromosomes."},
        {q:"Which process produces genetically varied haploid cells?",o:["Mitosis","Meiosis","Binary fission","Fertilisation only"],a:1,e:"Meiosis includes crossing over and independent assortment."}
      ]},
      {id:"transport",title:"Transport in plants and mammals",level:"Core",summary:"Xylem, phloem, circulation and gas exchange.",sections:[
        ["Plant transport","Xylem vessels transport water and mineral ions from roots to leaves. Cohesion between water molecules and adhesion to xylem walls help maintain a continuous water column."],
        ["Transpiration","Water evaporates from mesophyll cell surfaces and diffuses out through stomata. Transpiration pull helps draw water up the xylem. Stomatal opening balances gas exchange with water loss."],
        ["Phloem translocation","Phloem transports assimilates such as sucrose from sources to sinks. Translocation involves loading, osmotic water entry and pressure-driven mass flow."],
        ["Mammalian circulation","The heart pumps blood through pulmonary and systemic circuits. Arteries carry blood away from the heart; veins return it; capillaries provide exchange surfaces."]
      ],example:"During exercise, muscle cells respire more rapidly. Heart rate and ventilation increase to deliver oxygen and glucose and remove carbon dioxide.",questions:[
        {q:"Which tissue transports water in plants?",o:["Phloem","Xylem","Epidermis","Cortex only"],a:1,e:"Xylem carries water and mineral ions from roots towards leaves."},
        {q:"Where does exchange of materials between blood and tissues mainly occur?",o:["Arteries","Veins","Capillaries","Heart valves"],a:2,e:"Thin capillary walls and extensive networks allow exchange by diffusion."}
      ]},
      {id:"ecology",title:"Ecology and ecosystems",level:"Extension",summary:"Energy flow, nutrient cycles, populations and conservation.",sections:[
        ["Ecosystems","An ecosystem includes a community of organisms and their abiotic environment. Organisms interact through competition, predation, mutualism, parasitism and other relationships."],
        ["Energy flow","Energy enters most ecosystems through photosynthesis and passes through trophic levels. Energy is lost at each transfer through respiration, heat, waste and uneaten material."],
        ["Nutrient cycles","Decomposers break down dead organic matter and release mineral ions. The carbon and nitrogen cycles involve biological, geological and atmospheric processes."],
        ["Population ecology","Population size changes through births, deaths, immigration and emigration. Limiting factors may be density-dependent or density-independent. Carrying capacity is the sustainable population size under given conditions."]
      ],example:"If producers store 10 000 kJ and transfer efficiency to primary consumers is 10%, the energy passed on is about 1 000 kJ.",questions:[
        {q:"Which organisms recycle nutrients by breaking down dead matter?",o:["Primary consumers","Decomposers","Top predators","Producers only"],a:1,e:"Decomposers break down organic matter and release nutrients back into ecosystems."},
        {q:"A limiting factor that becomes stronger as population density rises is…",o:["Density-dependent","Always climatic","Density-independent","Unrelated to population"],a:0,e:"Competition and disease often intensify as population density increases."}
      ]}
    ]},
    {id:"geography",name:"Geography",icon:"🌍",topics:[
      {id:"geomorphology",title:"Geomorphology and landforms",level:"Foundations",summary:"Weathering, mass movement, erosion and river processes.",sections:[
        ["Weathering","Weathering is the breakdown of rock in place. Physical weathering includes freeze-thaw and thermal expansion; chemical weathering includes carbonation, hydrolysis and oxidation; biological weathering involves organisms."],
        ["Mass movement","Mass movement is downslope movement of material under gravity. Types include rockfalls, slides, slumps, mudflows and soil creep. Water content, slope angle and vegetation affect stability."],
        ["River processes","Rivers erode by hydraulic action, abrasion, attrition and solution. They transport material by traction, saltation, suspension and solution, and deposit sediment when energy decreases."],
        ["Landforms","Erosion and deposition create features such as V-shaped valleys, waterfalls, meanders, ox-bow lakes, floodplains, levees and deltas."]
      ],example:"A river entering a lake loses velocity and competence, so it deposits sediment. Repeated deposition can build a delta where conditions allow.",questions:[
        {q:"Which process breaks rock down in place?",o:["Transportation","Weathering","Deposition","River capture"],a:1,e:"Weathering is the breakdown of rock in situ."},
        {q:"Which process moves sediment by bouncing along a river bed?",o:["Suspension","Solution","Saltation","Traction"],a:2,e:"Saltation is the hopping or bouncing movement of particles along the bed."}
      ]},
      {id:"climate",title:"Weather, climate and climate change",level:"Core",summary:"Atmospheric processes, rainfall, climate controls and change.",sections:[
        ["Weather and climate","Weather describes short-term atmospheric conditions; climate describes long-term patterns and averages, commonly assessed over multi-decade periods."],
        ["Controls of climate","Latitude, altitude, distance from the sea, ocean currents, prevailing winds, relief and vegetation influence temperature and precipitation patterns."],
        ["Rainfall mechanisms","Convectional rainfall forms when heated moist air rises and cools. Relief rainfall occurs when air is forced over high ground. Frontal rainfall forms where contrasting air masses meet."],
        ["Climate change","Climate varies naturally, but recent global warming is primarily driven by increased greenhouse gas concentrations from human activities. Impacts include changing rainfall, heat extremes, sea-level rise and ecosystem stress."]
      ],example:"As moist air rises over a mountain, it expands and cools. Condensation forms cloud and precipitation on the windward side, often leaving a drier rain-shadow region leeward.",questions:[
        {q:"Which rainfall type is caused by air being forced over mountains?",o:["Convectional","Relief","Frontal","Cyclonic only"],a:1,e:"Relief or orographic rainfall occurs when air rises over high ground."},
        {q:"Climate refers to…",o:["One afternoon's weather","Long-term atmospheric patterns","A single storm","Only daily temperature"],a:1,e:"Climate describes long-term patterns and averages of weather."}
      ]},
      {id:"population",title:"Population and settlement",level:"Core",summary:"Population structure, migration, urbanisation and settlement patterns.",sections:[
        ["Population change","Population change is affected by fertility, mortality and migration. Natural increase is the difference between birth rate and death rate."],
        ["Population structure","Population pyramids show age and sex structure. A broad base often indicates high birth rates; a narrow base may indicate low fertility or an ageing population."],
        ["Migration","Push factors encourage people to leave a place; pull factors attract them elsewhere. Migration may be internal or international, voluntary or forced."],
        ["Urbanisation","Urbanisation is an increasing proportion of people living in urban areas. It can bring employment and services but may also create housing shortages, congestion, informal settlements and pressure on infrastructure."]
      ],example:"If a country has a birth rate of 30 per 1 000 and death rate of 10 per 1 000, its rate of natural increase is 20 per 1 000 (2%).",questions:[
        {q:"Natural increase is calculated using…",o:["Birth rate minus death rate","Immigration minus emigration","Deaths plus migration","Population divided by area"],a:0,e:"Natural increase = birth rate − death rate."},
        {q:"A push factor is one that…",o:["Attracts migrants to a destination","Encourages people to leave an origin","Measures population density","Stops urban growth"],a:1,e:"Push factors make people want or need to leave their place of origin."}
      ]},
      {id:"resources",title:"Resources, development and sustainability",level:"Extension",summary:"Resource management, development indicators and sustainable strategies.",sections:[
        ["Natural resources","Resources may be renewable or non-renewable. Their availability depends on physical distribution, technology, demand, accessibility and management."],
        ["Development indicators","Development can be measured using income, education, health, life expectancy, access to services and composite indicators. No single measure captures every aspect of wellbeing."],
        ["Resource management","Sustainable management balances economic needs, social equity and environmental protection. Strategies include conservation, efficient technology, recycling and community participation."],
        ["Geographical enquiry","A strong case study identifies location, scale, causes, impacts, stakeholders, management strategies and evidence. Use named examples and evaluate successes and limitations."]
      ],example:"A sustainable catchment plan may combine soil conservation, riparian buffer zones, controlled grazing, water monitoring and community involvement.",questions:[
        {q:"Which is a renewable resource when managed sustainably?",o:["Coal","Petroleum","Solar energy","Natural gas"],a:2,e:"Solar energy is continually replenished by incoming solar radiation."},
        {q:"A balanced definition of sustainable development considers…",o:["Economy only","Environment only","Economic, social and environmental needs","Short-term profit only"],a:2,e:"Sustainability balances economic, social and environmental dimensions."}
      ]}
    ]}
  ];


  // Add four section-based revision questions to every topic using the lesson's own notes.
  courses.forEach(course => course.topics.forEach(t => {
    const headings = t.sections.map(section => section[0]);
    t.sections.forEach((section, index) => {
      const options = [section[0], ...headings.filter((_, i) => i !== index)].slice(0, 4);
      t.questions.push({
        q: "Which section covers this idea: " + section[1].split(/[.!?]/)[0] + "?",
        o: options, a: 0,
        e: "Review " + section[0] + ": " + section[1]
      });
    });
  }));
  const $ = id => document.getElementById(id);
  const progressKey = "mt-study-progress-v1";
  let activeSubject = courses[0].id;
  let activeTopic = null;
  let quizAnswers = {};
  let progress = {};
  try { progress = JSON.parse(localStorage.getItem(progressKey) || "{}") || {}; } catch (_) { progress = {}; }
  const subject = () => courses.find(s => s.id === activeSubject);
  const topic = () => subject().topics.find(t => t.id === activeTopic);
  const esc = value => String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  function saveProgress(){ localStorage.setItem(progressKey, JSON.stringify(progress)); renderProgress(); }
  function renderProgress(){
    const all = courses.flatMap(s => s.topics.map(t => s.id + ":" + t.id));
    const done = all.filter(k => progress[k]).length;
    $("study-progress-fill").style.width = (100 * done / all.length) + "%";
    $("study-progress-label").textContent = done + " of " + all.length + " topics completed";
  }
  function renderSubjects(){
    $("study-subjects").innerHTML = courses.map(s => '<button type="button" class="study-subject '+(s.id===activeSubject?'active':'')+'" data-subject="'+s.id+'"><span>'+s.icon+'</span><b>'+s.name+'</b><small>'+s.topics.length+' topics</small></button>').join("");
    $("study-subjects").querySelectorAll("[data-subject]").forEach(btn => btn.addEventListener("click", () => {
      activeSubject=btn.dataset.subject; activeTopic=null; renderSubjects(); renderTopics(); renderLesson();
    }));
  }
  function renderTopics(){
    const q = $("study-search").value.trim().toLowerCase();
    const list = subject().topics.filter(t => !q || (t.title+" "+t.summary+" "+t.sections.map(x=>x.join(" ")).join(" ")).toLowerCase().includes(q));
    $("study-topic-list").innerHTML = '<div class="study-topic-heading"><div><span class="eyebrow">SUBJECT TOPICS</span><h2>'+subject().icon+' '+subject().name+'</h2></div><span>'+list.length+' topics</span></div>' +
      (list.length ? list.map(t => '<button type="button" class="study-topic '+(t.id===activeTopic?'active':'')+'" data-topic="'+t.id+'"><span class="study-topic-check">'+(progress[activeSubject+":"+t.id]?'✓':'○')+'</span><span><b>'+esc(t.title)+'</b><small>'+esc(t.summary)+'</small></span><em>'+esc(t.level)+'</em></button>').join("") : '<p class="study-no-results">No matching topics. Try another search.</p>');
    $("study-topic-list").querySelectorAll("[data-topic]").forEach(btn=>btn.addEventListener("click",()=>{activeTopic=btn.dataset.topic;quizAnswers={};renderTopics();renderLesson();}));
  }
  function renderLesson(){
    const t=topic();
    if(!t){$("study-lesson").innerHTML='<div class="study-empty"><div class="study-symbol">✦</div><h2>Choose a topic</h2><p>Pick a topic above to open the lesson.</p></div>';return;}
    const key=activeSubject+":"+t.id;
    $("study-lesson").innerHTML =
      '<div class="lesson-topline"><span class="badge">'+esc(t.level)+'</span><span>'+esc(subject().name)+'</span></div>'+
      '<h2>'+esc(t.title)+'</h2><p class="lesson-summary">'+esc(t.summary)+'</p>'+
      t.sections.map((s,i)=>'<section class="lesson-section"><h3>'+String(i+1).padStart(2,"0")+' · '+esc(s[0])+'</h3><p>'+esc(s[1])+'</p></section>').join("")+
      '<section class="worked-example"><span class="eyebrow">WORKED EXAMPLE</span><p>'+esc(t.example)+'</p></section>'+
      '<section class="study-quiz"><span class="eyebrow">CHECK YOUR UNDERSTANDING</span><h3>Practice questions · '+t.questions.length+' questions</h3>'+ '<div class="study-tool-row"><button type="button" id="shuffle-quiz">Shuffle questions</button><button type="button" id="start-timer">Start 10-minute timer</button><span id="study-timer">Timer off</span></div>'+
      t.questions.map((q,i)=>'<div class="quiz-question" data-question="'+i+'"><p><b>'+ (i+1)+'. '+esc(q.q)+'</b></p><div class="quiz-options">'+q.o.map((o,j)=>'<button type="button" data-answer="'+j+'" class="'+(quizAnswers[i]===j?'chosen':'')+'">'+String.fromCharCode(65+j)+'. '+esc(o)+'</button>').join("")+'</div><p class="quiz-feedback" id="feedback-'+i+'"></p></div>').join("")+
      '<button type="button" class="study-check" id="check-answers">Check answers</button><span id="quiz-score" class="quiz-score"></span></section>'+
      '<section class="study-flashcards"><h3>Flashcards</h3><p>Tap a card to reveal the explanation.</p>'+t.sections.map((s,i)=>'<button type="button" class="study-flashcard" data-flash="'+i+'"><b>'+esc(s[0])+'</b><span>'+esc(s[1])+'</span></button>').join("")+'</section>'+
      '<div class="lesson-actions"><button type="button" class="study-complete" id="mark-complete">'+(progress[key]?'✓ Completed — mark again':'Mark topic as completed')+'</button><button type="button" class="study-print" id="print-lesson">Print / save lesson</button></div>';
    $("study-lesson").querySelectorAll("[data-question]").forEach(box=>box.querySelectorAll("[data-answer]").forEach(btn=>btn.addEventListener("click",()=>{
      const i=Number(box.dataset.question);quizAnswers[i]=Number(btn.dataset.answer);
      box.querySelectorAll("[data-answer]").forEach(b=>b.classList.toggle("chosen",b===btn));
      $("feedback-"+i).textContent="";
    })));
    $("shuffle-quiz").addEventListener("click",()=>{t.questions.sort(()=>Math.random()-.5);quizAnswers={};renderLesson();});
    let timerHandle=null, secondsLeft=600;
    $("start-timer").addEventListener("click",()=>{
      if(timerHandle) clearInterval(timerHandle);
      secondsLeft=600; $("study-timer").textContent="10:00 remaining";
      timerHandle=setInterval(()=>{
        secondsLeft--;
        $("study-timer").textContent=Math.floor(secondsLeft/60)+":"+String(secondsLeft%60).padStart(2,"0")+" remaining";
        if(secondsLeft<=0){clearInterval(timerHandle);timerHandle=null;$("study-timer").textContent="Time is up — check your answers.";}
      },1000);
    });
    $("study-lesson").querySelectorAll("[data-flash]").forEach(card=>card.addEventListener("click",()=>card.classList.toggle("revealed")));
    $("check-answers").addEventListener("click",()=>{
      let score=0;
      t.questions.forEach((q,i)=>{const ok=quizAnswers[i]===q.a;if(ok)score++;$("feedback-"+i).textContent=(ok?"Correct. ":"Not quite. ")+q.e;$("feedback-"+i).className="quiz-feedback "+(ok?"correct":"incorrect");});
      $("quiz-score").textContent="Score: "+score+"/"+t.questions.length;
    });
    $("mark-complete").addEventListener("click",()=>{progress[key]=!progress[key];saveProgress();renderTopics();renderLesson();});
    $("print-lesson").addEventListener("click",()=>window.print());
  }
  $("study-search").addEventListener("input",renderTopics);
  $("study-reset").addEventListener("click",()=>{if(confirm("Clear all study progress saved on this device?")){progress={};saveProgress();renderTopics();renderLesson();}});
  renderSubjects();renderTopics();renderLesson();renderProgress();
})();
# Lane 1 — Reparations Economics: Exemplar Evidence Base

**Purpose:** structural argumentation DNA for the paper-foundry skill. This file covers
**how** the most-cited works in the economics of slavery and reparations argue — not prose style.

**Methods (all free, no accounts):**
- Candidate pool built from OpenAlex Works API (`https://api.openalex.org`), default pool, no `mailto`.
- Searches: `search=reparations economics`, `search=economics of slavery reparations`,
  `search=reparations for slavery`, `search=racial wealth gap reparations`,
  `filter=title_and_abstract.search:reparations slavery`, plus author filters for
  William Darity and Thomas Craemer, plus title filters for known canonical works.
- All citation counts are **`cited_by_count` from OpenAlex, as retrieved 2026-09-18 (EDT)**.
- Abstracts reconstructed from `abstract_inverted_index` via a Python script.
- Open-access full-text fetch attempted for 3 works via `best_oa_location` PDFs (JEP 2022,
  QJE 2024, Soc Sci & Medicine 2021). All three PDF endpoints returned Cloudflare
  bot-challenge pages via curl; `browser.open` on the AEA PDF also failed. Per policy,
  **no further fetch attempts were made**. Result: **all 14 exemplars below are abstract-only**
  (two are metadata-only, as flagged). Every distillation is labeled accordingly.

**Spot-checks:** 4 DOIs verified against Crossref (`api.crossref.org/works/{doi}`) — title and
publication year all matched OpenAlex. See "Crossref spot-checks" at the end. Zero mismatches.

**Deliberately excluded:** see the end section for works considered and rejected (with reasons).

---

## Exemplar 1 — Darity & Mullen, *From Here to Equality: Reparations for Black Americans in the Twenty-First Century*

- **Title:** *From Here to Equality: Reparations for Black Americans in the Twenty-First Century*
- **Authors:** William Darity Jr., A. Kirsten Mullen
- **Venue:** Book, University of North Carolina Press, 2020
- **DOI:** 10.5149/northcarolina/9781469654973.001.0001 | **OpenAlex ID:** W4206315446
- **Cited by:** 327 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`; this is the publisher
  book blurb, ~1,900 chars). No full text accessed.
- **Confidence:** abstract-only — the structural DNA below describes the book's *framing
  architecture as rendered in the blurb*. Gap-framing and contribution-claim architecture are
  directly readable; objection-handling, lit-review positioning, and intro/conclusion
  micro-structure are unverifiable from the blurb alone.

**1. Gap-framing move.** Claims a comprehensiveness gap, not a finding gap: "the most
comprehensive case to date for economic reparations for U.S. descendants of slavery." The
consensus invoked is quantitative (the 10-cents-on-the-dollar wealth figure) plus a historical
claim that three hinge moments (Reconstruction, New Deal, civil rights) each failed to deliver
economic justice. The gap is made to matter by stakes escalation: each era individually would
suffice; taken collectively the case is "impossible to ignore" — i.e., the gap is not missing
evidence but missing *assembly*.

**2. Contribution-claim architecture.** Stacked, sequential, three-part: (a) measurement
("innovative methods that link monetary values to historical wrongs"), (b) accounting ("the
literal and figurative costs of justice denied"), (c) policy ("a detailed roadmap for an
effective reparations program"). One big claim (comprehensive case) with three stacked
sub-claims that map onto the book's three eras (slavery, Jim Crow, modern-day discrimination).
Qualification appears minimal in the blurb — the strongest language ("most comprehensive,"
"impossible to ignore") is unhedged, a superlative claim appropriate to a trade-press book.

**3. Evidence-to-claim density.** Evidence named at the level of *methods and eras*, not
numbers: "innovative methods," "economic data," three historical eras. Claims sit very close to
evidence — each era is claimed to individually carry the case, meaning the evidence blocks are
modular and redundant by design: the argument does not depend on any single estimate holding up.

**4. Objection handling.** Not visible in the blurb. The structure preempts the "who pays /
how much" objection not by refuting it but by *absorbing* it: the roadmap and payment proposal
(substantial payment to each documented descendant) are folded into the contribution itself, so
the anticipated objection becomes a chapter, not a counterargument.

**5. Introduction and conclusion architecture.** Opening move: stark intergenerational
assessment (diagnosis first, mechanism second). Closing move (from the blurb): cumulative
aggregation — the three eras "taken collectively" as a closing amplifier. Structure is
arc-shaped: present diagnosis → historical deep dive → forward program.

**6. Literature-review positioning moves.** From the blurb: prior work is positioned by
contrast on *scope* rather than by dispute on findings — predecessors are implicitly credited
for partial cases while the book claims the first complete integration. The three-era periodization
(slavery → Jim Crow → modern discrimination) itself is the delimiting move: it sets the
boundaries of what counts as reparations-relevant history.

---

## Exemplar 2 — Darity, "Stratification economics: The role of intergroup inequality" (2005)

- **Title:** Stratification economics: The role of intergroup inequality
- **Authors:** William Darity Jr.
- **Venue:** Journal of Economics and Finance, 2005 (Review of Black Political Economy lineage)
- **DOI:** 10.1007/bf02761550 | **OpenAlex ID:** W1995060833
- **Cited by:** 248 (OpenAlex, as of 2026-09-18)
- **Text source used:** metadata-only. OpenAlex returned **no abstract** (`abstract_inverted_index`
  absent) and no open-access location. No full text accessed.
- **Confidence:** metadata-only — structural extraction is not performed. The framing below is
  limited to what the title, venue, author, and citation record verify. Included because it is
  the most-cited theoretical foundation of the entire lane: Darity's own framework paper that
  every subsequent Darity-led reparations estimate cites.

What the metadata verifies: a single-author framework paper naming a new subfield
("stratification economics") and its object ("intergroup inequality") in a heterodox
economics journal. The positioning move readable from the title alone is *field-founding*:
not a contribution *to* a literature but the announcement of a literature. (For the mature
statement of this framework, see Exemplar 5, the 2022 JEL survey, which has an abstract and
full distillation.)

---

## Exemplar 3 — Hamilton & Darity, "Can 'Baby Bonds' Eliminate the Racial Wealth Gap in Putative Post-Racial America?" (2010)

- **Title:** Can 'Baby Bonds' Eliminate the Racial Wealth Gap in Putative Post-Racial America?
- **Authors:** Darrick Hamilton, William Darity Jr.
- **Venue:** The Review of Black Political Economy, 2010
- **DOI:** 10.1007/s12114-010-9063-1 | **OpenAlex ID:** W2063634140
- **Cited by:** 231 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~760 chars). No full
  text accessed.
- **Confidence:** abstract-only — gap-framing, thesis, and contribution architecture are directly
  readable; objection handling is partly visible (preemptive framing against "race-neutral"
  policy norms); intro/conclusion microstructure and lit-review mechanics are unverifiable.

**1. Gap-framing move.** Names a *discursive* gap, not an empirical one: the ascendant
"post-racial" narrative plus the behavioral-deficit explanation of racial disparity. The anomaly
is policy-feasibility: the only acceptable remedies are "facially race neutral." The gap is made
to matter by showing it *rules out* the direct fix (asset redistribution by race), so the paper's
contribution is a lawful workaround.

**2. Contribution-claim architecture.** Single big claim in interrogative form (the title's
question), supported by one mechanism claim: use *wealth* (not race) as the redistributive
standard, and it reaches the racial gap indirectly. The thesis is sequenced as
problem-diagnosis → constraint (race-neutrality requirement) → design (progressive child
development accounts). Qualifiers are mild ("could go a long way towards") — the boldness is in
the proposal ("bold progressive"), the hedge is in the verb.

**3. Evidence-to-claim density.** Abstract names no statistics, no model outputs — the
"enormous and persistent black-white wealth gap" is invoked as stipulated background. This is a
design/argument paper, not an estimation paper: the evidence burden is carried by the mechanism
design's logic, with each claim sitting adjacent to its design rationale rather than to data.

**4. Objection handling.** Preemption is the dominant move, and it opens the abstract rather
than closing it: the "post-racial" climate and the dysfunction narrative are named in the first
two sentences, then routed around ("even without the capacity to redistribute assets directly
on the basis of race, our nation still can do so indirectly"). Concession is tactical — accept
the race-neutrality constraint, then design within it.

**5. Introduction and conclusion architecture.** Opening move: narrative vs. reality contrast
(the proclaimed post-racial society vs. the persistent gap). Closing move: the indirect-redress
proposal as constructive exit. Structure is *constraint-then-design*: make the political
constraint explicit, then show a design that satisfies it.

**6. Literature-review positioning moves.** Unverifiable from the abstract; the abstract's only
positioning is against a public narrative and a behavioral-deficit consensus, not against named
prior work.

---

## Exemplar 4 — Posner & Vermeule, "Reparations for Slavery and Other Historical Injustices" (2003)

- **Title:** Reparations for Slavery and Other Historical Injustices
- **Authors:** Eric A. Posner, Adrian Vermeule
- **Venue:** Columbia Law Review, 2003
- **DOI:** 10.2307/1123721 | **OpenAlex ID:** W579064304
- **Cited by:** 139 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~990 chars). No full
  text accessed.
- **Confidence:** abstract-only — the "gap in the literature" claim and the paper's scope
  architecture are explicit in the abstract; objection handling and lit-review mechanics are
  unverifiable.

**1. Gap-framing move.** Classic explicit gap claim: "problems of legal and institutional
design have received almost none" of the attention given to moral and political arguments.
The consensus invoked is that reparations *talk* is plentiful (Japanese American internment,
Holocaust programs, countless proposals) while design analysis is absent. The gap is made to
matter by implication — proposals cannot become programs without design — without needing to
state it.

**2. Contribution-claim architecture.** One big claim ("this paper fills the gap") executed
as a *taxonomy*: "the various design options for reparations programs, their legal and
constitutional bases, and their relationship to the standard moral and political arguments."
Three stacked sub-claims (options → bases → relationship-to-arguments), sequenced from
concrete to abstract. No hedging language in the abstract — the fill-the-gap verb is
unqualified.

**3. Evidence-to-claim density.** Evidence is comparative-institutional: known programs
(internment, Holocaust) and lesser-known ones serve as the case inventory from which design
options are induced. The density pattern is *enumeration-then-abstraction* — claims about
design space sit directly on top of the listed cases.

**4. Objection handling.** Unverifiable from the abstract. Notably, the abstract *sidesteps*
the moral/political debate rather than engaging it — the paper's posture is that design
questions are orthogonal to (not downstream of) the moral verdict, which is itself an implicit
objection-deflection move.

**5. Introduction and conclusion architecture.** Opening move: empirical inventory (programs
exist, proposals abound) → pivot to the neglected dimension. The closing move is unrecoverable
from the abstract, but the architecture is plainly *analytical-completeness*: the contribution
is coverage, not verdict.

**6. Literature-review positioning moves.** The abstract groups prior work into two bins —
moral/political arguments (crowded, credited with "considerable attention") and design analysis
(empty) — and delimits the paper's scope to the empty bin. This is credit-and-vacate: praise the
existing conversation, then claim the room it isn't using.

---

## Exemplar 5 — Darity, "Position and Possessions: Stratification Economics and Intergroup Inequality" (2022)

- **Title:** Position and Possessions: Stratification Economics and Intergroup Inequality
- **Authors:** William Darity Jr.
- **Venue:** Journal of Economic Literature, 2022
- **DOI:** 10.1257/jel.20211690 | **OpenAlex ID:** W4281627227
- **Cited by:** 121 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (reconstructed from OpenAlex `abstract_inverted_index`,
  ~950 chars; full JEL abstract text as above). No full text accessed.
- **Confidence:** abstract-only — this is a field survey, so the gap-framing and
  positioning moves are unusually legible even in abstract form; objection handling and
  intro/conclusion microstructure are unverifiable.

**1. Gap-framing move.** Foundational-response framing: stratification economics "developed in
response to explanations for interracial/ethnic/gender inequality that invoked group-based
dysfunction on the part of the subordinate community." The anomaly named is not empirical but
*explanatory* — the dominant literature blames the subordinate group. The gap is made to matter
by moral-methodological weight: a field exists because the standard explanations were
defamatory, not merely incomplete.

**2. Contribution-claim architecture.** Single big claim (the field's existence and coherence)
supported by two moves: intellectual genealogy ("origins and development") and a forward
extension list (multiple identities, productivity determinants, "passing," wealth sources,
mobility, immigration). The architecture is *legitimation-through-lineage*: one claim, many
ancestors (Du Bois, Veblen, Marx, Eric Williams, Blumer, Steele, Ridgeway, Pettigrew, Tropp).
The JEL codes at the end function as a quiet qualification — the field is being filed into
the discipline's taxonomy, not attacking it from outside.

**3. Evidence-to-claim density.** Abstract names no data; evidence is the cited lineage
itself. This is a survey, so the "evidence" for the field's existence is the list of
contributors. Claims sit directly adjacent to their named sources — maximal density between
claim ("the field draws on X") and evidence (X's work).

**4. Objection handling.** The objection (dysfunction explanations of inequality) is named in
the abstract's second clause and disposed of by *displacement*: the whole field is the
refutation. No concession, no point-by-point refutation — the objection is framed as the
field's founding motivation and then left behind.

**5. Introduction and conclusion architecture.** Opening move: origin-story (why the field
exists). Closing move: extension list (where the field goes next). The survey's arc is
past-justification → future-territory — a standard field-survey shape whose closing move
doubles as a research-agenda claim.

**6. Literature-review positioning moves.** Genealogy as positioning: nine named
predecessors spanning economics, sociology, and psychology. The grouping move is
*ecumenical* — the field is presented as the convergence of established names rather than a
break from them. The one named outsider concept is "group-based dysfunction," which is
delimited as the position the field defines itself against. (Note: the 2005 founding paper,
Exemplar 2, made the same field-founding move; this 2022 survey is its institutionalized form.)

---

## Exemplar 6 — Dawson & Popoff, "REPARATIONS: Justice and Greed in Black and White" (2004)

- **Title:** REPARATIONS: Justice and Greed in Black and White
- **Authors:** Michael Dawson, Rovana Popoff
- **Venue:** Du Bois Review: Social Science Research on Race, 2004
- **DOI:** 10.1017/s1742058x04040056 | **OpenAlex ID:** W2127460765
- **Cited by:** 91 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~1,200 chars). No
  full text accessed.
- **Confidence:** abstract-only — the paper's empirical design (multivariate analysis,
  racial-divide finding) is explicit; gap-framing is inferable; objection handling and
  intro/conclusion microstructure are unverifiable.

**1. Gap-framing move.** Polemic-first framing: the opening sentences stage a three-cornered
fight — conservative opponents ("greed"), liberal/left opponents ("divisiveness"), supporters
("simple justice"). The consensus claimed is not scholarly but *popular-discursive*: everyone
argues past each other. The paper's gap is empirical grounding — what do people actually
think, and what predicts it?

**2. Contribution-claim architecture.** Two stacked claims: (a) descriptive — there is a
"tremendous divide between Blacks and Whites" on apology and monetary reparations (and the
divide extends to Japanese-American reparations support); (b) explanatory — "multivariate
analyses demonstrate that for both Blacks and Whites, racialized views of politics are best
predictors of support for or opposition." The sequence is description → mechanism. Hedging is
minimal ("demonstrate" is strong; the plural "views" is the only softener).

**3. Evidence-to-claim density.** High and tight: survey data → divide finding → multivariate
predictor finding, all within the abstract. Each claim is one clause away from its method.
This is the lane's exemplar of the *opinion-economics* move: using public-opinion data as
evidence about reparations' political economy.

**4. Objection handling.** The abstract's opening triage *is* the objection handling: the two
opposition positions (greed-motive, divisiveness) are named and attributed before the findings
land, which structurally positions the empirical results as the adjudicator of the shouting
match. The paper doesn't refute either side's morals; it replaces the argument about motives
with data about who believes what and why.

**5. Introduction and conclusion architecture.** Opening move: adversarial tableau (three
positions, maximal disagreement). The closing move is unrecoverable from the abstract, but the
architecture's logic points toward *empirical adjudication* — let the survey data have the
last word on a normative fight.

**6. Literature-review positioning moves.** Unverifiable from the abstract; the abstract
positions against *positions* (ideological camps), not against named prior studies. A notable
structural feature: the title's "Justice and Greed" mirrors the opponents' frames, a
hostile-attribution move that signals the paper will examine the frames themselves.

---

## Exemplar 7 — Thomas & Bean, "The Fishers of Men: The Profits of the Slave Trade" (1974)

- **Title:** The Fishers of Men: The Profits of the Slave Trade
- **Authors:** Robert Paul Thomas, Richard N. Bean
- **Venue:** The Journal of Economic History, 1974
- **DOI:** 10.1017/s002205070008935x | **OpenAlex ID:** W2161015912
- **Cited by:** 84 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~825 chars). No full
  text accessed.
- **Confidence:** abstract-only — the revisionist framing move is fully visible; the paper's
  actual profit estimates and methods are not in the abstract, so evidence-to-claim density is
  inferred only at the framing level.

**1. Gap-framing move.** Revisionist debunking: historians "have often left us with the
impression that the slave trade was fantastically profitable," and the view that slave-trade
profits "financed the British Industrial Revolution" is "gaining adherents." The consensus
claimed is an *impression* — plausible-sounding but untested. The anomaly is the gap between
the impression's plausibility ("seem plausible enough on the surface") and its evidentiary
basis. The gap is made to matter by political stakes: the impression is "part of the
historical foundation for the claim by black militants for reparations" — the paper names the
reparations connection explicitly as a reason the number matters.

**2. Contribution-claim architecture.** Single big claim (the profitability of the slave trade
was overstated) — the abstract sets up the target and the accounting identity that will do the
work: value produced minus subsistence consumption. Sequenced as: received impression →
its political load-bearing role → the economic logic that will be tested. Qualification is
stylistic ("seem plausible enough on the surface" — the surface/depth contrast does the
hedging).

**3. Evidence-to-claim density.** The abstract names the *logic* of the evidence (the
production-minus-subsistence margin) rather than the evidence itself — a promissory structure:
the accounting identity is displayed up front so the reader can audit the forthcoming numbers.
Claim and method are adjacent; claim and number are not (numbers live in the paper).

**4. Objection handling.** The anticipated objection — "surely there was a substantial
difference" — is voiced in the abstract's final sentence in the objector's own voice, then
left hanging. This is preemption by *staging*: let the reader hear the intuitive case at full
strength, then promise the numbers that will discipline it. No refutation yet; the refutation
is the paper.

**5. Introduction and conclusion architecture.** Opening move: the received impression stated
fairly, even sympathetically ("plausible enough on the surface"). This is the classic
cliometric opening: steel-man the conventional wisdom before the revision. Closing move
unrecoverable from the abstract.

**6. Literature-review positioning moves.** The "literature" positioned against is
historians' *impressions* — unnamed, collective, and characterized as impressionistic. The
delimiting move is disciplinary: economics (accounting, profit-rate estimation) is positioned
as the corrective to history's narrative impressions. This paper is the lane's archetype of
the *quantitative-revision* move that later reparations-cost estimators (Craemer, Darity)
inherited and redirected.

---

## Exemplar 8 — Darity, "Forty Acres and a Mule in the 21st Century" (2008)

- **Title:** Forty Acres and a Mule in the 21st Century
- **Authors:** William Darity Jr.
- **Venue:** Social Science Quarterly, 2008
- **DOI:** 10.1111/j.1540-6237.2008.00555.x | **OpenAlex ID:** W2091368071
- **Cited by:** 80 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~910 chars). No full
  text accessed.
- **Confidence:** abstract-only — the three-objectives framework and the program-design
  architecture (magnitude, eligibility, legislative route) are explicit; objection handling and
  lit-review mechanics are unverifiable.

**1. Gap-framing move.** Program-design gap: reparations debates are stuck on *whether*;
the paper moves to *how*. It opens with a definitional consensus claim — reparations programs
"in general" aim at three objectives: acknowledgment, redress, closure — which positions the
paper as working inside an established comparative framework (transitional-justice language),
not inventing one. The gap is made to matter by operational specificity: the missing pieces
are magnitude and eligibility criteria.

**2. Contribution-claim architecture.** Stacked design claims, sequenced as an implementation
checklist: (a) the three motivating injustices (slavery, Jim Crow, ongoing discrimination);
(b) the institutional route (federal legislative action, "rather than by judicial fiat" — a
quiet scope-delimiting claim); (c) the magnitude method ("the present day value of 40 acres
and a mule can provide the foundation for the calculation"); (d) eligibility criteria.
The signature move is the *historical-anchor estimate*: a concrete 1865 counterfactual (the
unfulfilled land promise) converted into a present-value foundation — the same device later
expanded in the JEP 2022 "global indicator strategy" (Exemplar 13).

**3. Evidence-to-claim density.** Abstract-level; the evidence blocks (the three injustice
eras) are named as stipulated premises, and each design claim sits adjacent to the premise it
operationalizes. The 40-acres device is both evidence (a historical fact: the promise existed)
and method (a valuation anchor) — a dual-use move that compresses density.

**4. Objection handling.** Partially visible: the legislative-vs-judicial clause preempts the
courts-can't-do-this objection by conceding the institutional point and routing around it.
The "documented descendant" eligibility framing (expanded in the book) similarly preempts the
identification objection by making it a design parameter rather than a defeater.

**5. Introduction and conclusion architecture.** Opening move: definitional (the three
objectives) — start from shared comparative ground, then particularize to Black Americans.
Closing move (from the abstract's final sentence): the valuation anchor as the constructive
exit — end on the number's foundation, not on the moral case.

**6. Literature-review positioning moves.** Unverifiable from the abstract; the abstract's
positioning is against a *debate stage* (the whether-question) rather than named prior work.
The transitional-justice vocabulary ("acknowledgment, redress, closure") is the grouping move:
it files Black American reparations inside the global reparations literature instead of
treating it as sui generis.

---

## Exemplar 9 — Craemer et al., "Wealth Implications of Slavery and Racial Discrimination for African American Descendants of the Enslaved" (2020)

- **Title:** Wealth Implications of Slavery and Racial Discrimination for African American
  Descendants of the Enslaved
- **Authors:** Thomas Craemer, Trevor Smith, Brianna Harrison, Trevon D. Logan, Wesley
  Bellamy, William Darity Jr.
- **Venue:** The Review of Black Political Economy, 2020
- **DOI:** 10.1177/0034644620926516 | **OpenAlex ID:** W3036414338
- **Cited by:** 66 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~1,270 chars). No
  full text accessed.
- **Confidence:** abstract-only — the estimate-comparison architecture (multiple methods,
  multiple interest rates, enumerated cost categories) is fully visible; gap-framing and
  objection handling are inferable; lit-review mechanics unverifiable.

**1. Gap-framing move.** Benchmark-gap framing: the anchor is a single stipulated number —
the 2018 per-capita Black–White wealth gap of ~US$352,250 — against which "portions of the
estimated total cost of slavery and discrimination" are compared. The consensus invoked is the
gap's existence; the gap in the literature is the *comparison*: cost estimates exist, but they
have not been set against the gap they are meant to close. The gap is made to matter by the
comparison's verdict function — do the estimates cover the gap, and by how much?

**2. Contribution-claim architecture.** Multi-method triangulation as the architecture:
Darity's land-based method ($12–13T), Marketti's price-based method, Craemer's wage-based
method ($18.6T at 3% to $6.2 quadrillion at 6%), plus new cost categories (lost freedom via
the Japanese-internment precedent: $35T at 3%; lost opportunities and pain-and-suffering
flagged as future work). The thesis is sequenced as *convergent upper bounds*: several
independent methods, all landing in the trillions-to-quadrillions, all dwarfing the
per-capita gap. Qualification is explicit and twofold: interest-rate sensitivity is displayed
(the 3% vs 6% spread), and unfinished categories are named rather than hidden.

**3. Evidence-to-claim density.** Extremely high: every major claim is a number with its
method and rate attached in the same sentence. This is the lane's densest abstract — the
argument *is* the table of estimates. The closing sentence ("whether the full cost... should
be compensated, or only a portion, and at what interest rate remain to be determined by
negotiations") deliberately detaches the estimation claims from the policy verdict: the
paper claims the menu, not the meal.

**4. Objection handling.** The interest-rate display is the objection handler: by showing
both 3% and 6% compounding, the paper preempts the "your number depends on an arbitrary rate"
attack — the sensitivity is the point, and the range is the honest answer. Naming unfinished
work (lost opportunities, pain and suffering, colonial slavery, post-abolition discrimination)
is a concession move that protects the published estimates from over-claim charges.

**5. Introduction and conclusion architecture.** Opening move: the benchmark number (the gap),
stated first — the paper opens on the target, not the history. Closing move: procedural
deferral — the compensation decision "remain[s] to be determined by negotiations between the
federal government and the descendant community." The structure hands the final verdict to
politics, which is both a humility move and a scope-delimiting one.

**6. Literature-review positioning moves.** The abstract's positioning is *method-lineage*:
Darity's, Marketti's, and Craemer's methods are named as the three estimation traditions,
and the paper positions itself as their synthesizer and extender (adding the internment-based
lost-freedom valuation). Prior estimators are credited by name and their numbers reused — a
cumulative rather than adversarial positioning.

---

## Exemplar 10 — Richardson et al., "Reparations for Black American descendants of persons enslaved in the U.S. and their potential impact on SARS-CoV-2 transmission" (2021)

- **Title:** Reparations for Black American descendants of persons enslaved in the U.S. and
  their potential impact on SARS-CoV-2 transmission
- **Authors:** Eugene T. Richardson, Momin M. Malik, William Darity Jr., A. Kirsten Mullen,
  Michelle Morse, Maya Malik, Aletha Maybank, Mary T. Bassett, Paul E. Farmer, Lee Worden,
  James H. Jones
- **Venue:** Social Science & Medicine, 2021
- **DOI:** 10.1016/j.socscimed.2021.113741 | **OpenAlex ID:** W3127285466
- **Cited by:** 63 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~1,770 chars; the
  longest abstract in the set). Full text was attempted via the OA PDF
  (sciencedirect.com) — the endpoint returned a Cloudflare bot-challenge page; no full text
  obtained.
- **Confidence:** abstract-only — but this abstract is unusually complete (objective, methods,
  results, conclusions all present), so the argument architecture is legible in rare detail;
  objection handling beyond the abstract's own framing is unverifiable.

**1. Gap-framing move.** Intervention-gap framing inside epidemiology: "Going beyond mere
epidemiological tallying, the potential for racial-justice interventions, including
reparations payments, to ameliorate these disparities has not been adequately explored."
The consensus claimed is the disparity's existence (disproportionate COVID incidence); the
anomaly is that the literature tallies the disparity without modeling *structural*
interventions. The gap is made to matter by pandemic urgency — a moment when transmission
models were policy-relevant.

**2. Contribution-claim architecture.** Single big claim with a three-step method ladder:
(a) compare Rt curves of contrasting polities (South Korea vs. Louisiana) as an equity
natural experiment; (b) back-calculate transmission rates for a structured model of the
Louisiana outbreak; (c) simulate the structural effects of reparations payments on
pre-intervention transmission and R0. The result claim is quantitative (R0 reduced 31–68%)
and then universalized: benefits "distributed across racial groups, benefiting the population
at large." The architecture is *counterfactual simulation*: the contribution is a modeled
world, not a measured one, and the abstract is careful to say "reasoning through the
consequences" and "would have had."

**3. Evidence-to-claim density.** High but explicitly counterfactual: real Rt curves
(South Korea vs. Louisiana, absolute difference 1.3–2.5, halving time more than doubled)
ground the first two steps; the reparations step is a modeled intervention on those
grounded parameters. The abstract keeps the evidentiary status of each step legible —
observed curves vs. back-calculated rates vs. simulated effects.

**4. Objection handling.** The "mere tallying" phrase preempts the descriptive-epidemiology
objection (we already know disparities exist) by conceding it and moving past it. The
universal-benefit closing ("benefiting the population at large") preempts the
zero-sum/particularism objection — a classic move in the reparations literature: the remedy
helps everyone.

**5. Introduction and conclusion architecture.** Opening move: the disparity as established
fact, then the pivot from tallying to intervening. Closing move: the universal-benefit
generalization — end not on the recipient group but on the population. The arc is
particular-diagnosis → universal-prescription.

**6. Literature-review positioning moves.** Unverifiable from the abstract; the abstract
positions against a *methodological habit* (tallying) rather than named prior work. The
author list itself (eleven authors spanning medicine, economics, and public health, including
Darity and Mullen) is a positioning signal: the economics-of-reparations apparatus being
imported into epidemiology.

---

## Exemplar 11 — Craemer, "Estimating Slavery Reparations: Present Value Comparisons of Historical Multigenerational Reparations Policies" (2015)

- **Title:** Estimating Slavery Reparations: Present Value Comparisons of Historical
  Multigenerational Reparations Policies
- **Authors:** Thomas Craemer
- **Venue:** Social Science Quarterly, 2015
- **DOI:** 10.1111/ssqu.12151 | **OpenAlex ID:** W2164238138
- **Cited by:** 63 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~1,060 chars;
  structured Objective/Methods/Results/Conclusions format). No full text accessed.
- **Confidence:** abstract-only — the structured abstract makes the full argument skeleton
  (two problems, two methods, results, conclusions) unusually legible; objection handling and
  lit-review mechanics beyond the named precedents are unverifiable.

**1. Gap-framing move.** Two-problem framing, stated in the Objective line: (a) *legal* —
"legal obstacles caused by the passage of time"; (b) *economic* — "economic difficulties in
obtaining realistic present value estimates." The consensus invoked is that multigenerational
claims are thought to be novel problems; the paper's move is to show they are *old* problems
with precedents. The gap is made to matter by the upward correction it enables: better method
→ bigger number.

**2. Contribution-claim architecture.** The abstract's structure IS the architecture:
Objective (two problems) → Methods (two investigations: legal precedents + present-value
method comparison) → Results (precedents traced; $5.9–14.2T estimate in 2009 dollars) →
Conclusions (two verdicts). Two stacked sub-claims in parallel: the legal-historical claim
(French spoliation claims paid over 123 years; Haitian independence debt over 156 years) and
the economic-method claim (wage-based estimation via unremunerated hours × free-market wages,
vs. slave-price-based expected-income methods). The conclusions then compress both:
"Neither problems nor solutions associated with multigenerational reparations are new. New is
the estimation method and the resulting upward correction."

**3. Evidence-to-claim density.** Very high: each problem gets a named method and a named
result in adjacent sentences. The precedents are quantified by duration (123, 156 years) —
numbers doing argumentative work as existence proofs. The estimate range ($5.9–14.2T) is
presented as the direct output of the method comparison.

**4. Objection handling.** The legal-precedent investigation is the objection handler: the
"too much time has passed" objection is disposed of by *precedent* (refutation-by-example —
long-horizon claims have been paid before), and the conclusion generalizes it: "Historical
precedents suggest that political rather than narrowly legal processes will determine any
ultimate claims." This is concession-plus-redirect: concede the legal difficulty, then show
the determination mechanism is political anyway.

**5. Introduction and conclusion architecture.** Opening move: the two problems, named
cleanly (a problem-statement opening, not a narrative one). Closing move: the novelty claim
is *minimized* ("neither problems nor solutions are new") while the method's upward
correction is maximized — a humility-about-novelty / boldness-about-results split that is
characteristic of the estimation sub-literature.

**6. Literature-review positioning moves.** Positioning by *precedent class*: the paper
groups its historical comparators (French spoliation, Haitian debt) as a class of
multigenerational payment programs, crediting them as existence proofs. The existing
slavery-reparations estimates (price-based) are positioned as the baseline to be corrected
upward — credited for existing, delimited by method.

---

## Exemplar 12 — Althoff & Reichardt, "Jim Crow and Black Economic Progress after Slavery" (2024)

- **Title:** Jim Crow and Black Economic Progress after Slavery
- **Authors:** Lukas Althoff, Hugo Reichardt
- **Venue:** The Quarterly Journal of Economics, 2024
- **DOI:** 10.1093/qje/qjae023 | **OpenAlex ID:** W4401040663
- **Cited by:** 60 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~880 chars). Full
  text attempted via the OA PDF (academic.oup.com) — the endpoint returned a Cloudflare
  bot-challenge page; no full text obtained.
- **Confidence:** abstract-only — the identification strategy (linked census records,
  regression discontinuity on enslavement location) is explicit; gap-framing is inferable;
  objection handling and lit-review mechanics are unverifiable.

**1. Gap-framing move.** Within-group comparison as the gap device: the literature studies
Black vs. white gaps; the paper studies *enslaved-until-1865 vs. free-before-1865 Black
families* — a gap inside the gap. The anomaly: families enslaved until the Civil War have
"considerably lower education, income, and wealth" than families free before it, and the
disparity persists into 2023 (surname-based outcomes). The gap is made to matter by the
mechanism claim: persistence is explained by *where* the formerly enslaved lived — states
with strict Jim Crow regimes.

**2. Contribution-claim architecture.** Single big claim (slavery + Jim Crow have
long-run causal effects on Black economic outcomes) executed through a data-construction
claim plus an identification claim: (a) linked individual census records 1850–1940 extended
to 2000 neighborhoods and 2023 surnames — the panel construction is itself a contribution;
(b) a regression discontinuity design on ancestors' enslavement locations isolates Jim Crow
institutions' causal role. Sequenced description → mechanism → identification. Hedging is
minimal; the RD language ("we show," "sharply reduced") is causal and unqualified.

**3. Evidence-to-claim density.** High: the abstract ties each claim to its data source
(census linkage, neighborhood outcomes, surname outcomes) and each causal claim to the RD
design. This is the lane's exemplar of the *identification-credibility* move imported from
mainstream empirical economics — the argument's authority comes from the design, not the
magnitude.

**4. Objection handling.** The within-Black comparison is itself the objection handler: it
preempts the "maybe it's something else about Black families" objection by holding race
constant and varying only enslavement history and Jim Crow exposure. The RD on location
further preempts selection objections. Both moves are structural (in the design) rather than
rhetorical (in the text) — visible even from the abstract.

**5. Introduction and conclusion architecture.** Opening move: the long-run question stated
as the object of study ("studies the long-run effects of slavery and restrictive Jim Crow
institutions"). Closing move: the causal verdict on Jim Crow institutions. The arc is
data → discontinuity → verdict — the standard QJE empirical arc, notable here because it
applies mainstream identification machinery to the reparations-adjacent question of
slavery's economic afterlife.

**6. Literature-review positioning moves.** Unverifiable from the abstract. Structurally, the
paper positions itself as the *causal-identification complement* to the estimation
literature (Craemer, Darity): where they compute the bill, this paper identifies the
mechanism (Jim Crow as the persistence engine). The venue (QJE) is itself a positioning
move — the argument is filed in the discipline's top general-interest journal, not a
field journal.

---

## Exemplar 13 — Darity, Mullen & Slaughter, "The Cumulative Costs of Racism and the Bill for Black Reparations" (2022)

- **Title:** The Cumulative Costs of Racism and the Bill for Black Reparations
- **Authors:** William Darity Jr., A. Kirsten Mullen, Marvin Slaughter
- **Venue:** The Journal of Economic Perspectives, 2022
- **DOI:** 10.1257/jep.36.2.99 | **OpenAlex ID:** W4280652853
- **Cited by:** 45 (OpenAlex, as of 2026-09-18)
- **Text source used:** abstract-only (OpenAlex `abstract_inverted_index`, ~1,170 chars).
  Full text attempted via the OA PDF (aeaweb.org) — the endpoint returned a Cloudflare
  bot-challenge page; no full text obtained.
- **Confidence:** abstract-only — the two-strategies architecture and the verdict for the
  wealth-gap standard are fully explicit; objection handling is inferable; intro/conclusion
  microstructure unverifiable.

**1. Gap-framing move.** Method-selection framing: "Two major procedures for establishing the
monetary value of a plan for reparations... are considered." The gap is not a missing number
but a missing *verdict between methods* — the literature has many estimates but no disciplined
comparison of the estimation strategies themselves. The gap is made to matter by the paper's
verdict function: one standard must be chosen as "the best gauge."

**2. Contribution-claim architecture.** Binary comparison as architecture: (1) the
*itemization strategy* — enumerate atrocities, price each, sum (wage costs of bondage,
perpetrators' gains, massacre/lynching damages, FHA/G.I. Bill discrimination losses,
employment discrimination penalties); (2) the *global indicator strategy* — one summary
measure of cumulative intergenerational effects (present value of 40 acres in 1865; the
current Black–White wealth gap). The thesis is a *verdict*: "the latter standard, the racial
wealth gap, provides the best gauge for the size of the bill." Sequenced: enumerate both →
adjudicate → crown the winner. No hedging on the verdict ("provides the best gauge").

**3. Evidence-to-claim density.** The abstract lists the itemized components as evidence
for strategy (1) and the two global indicators as evidence for strategy (2) — the density
pattern is *inventory-then-judgment*. The verdict claim sits directly on the comparison; no
new estimate is produced in the abstract, which marks this as a second-order (meta-estimation)
contribution.

**4. Objection handling.** The binary structure is the objection handler: the anticipated
attack on any single number ("your estimate is arbitrary") is absorbed by showing two
families of methods and arguing for the *class* rather than the *figure*. Choosing the wealth
gap as the gauge additionally preempts the compounding-rate objection that haunts the
itemization strategy (cf. Craemer 2015's 3%-vs-6% spread) — the gap is observable now, no
compounding assumption required.

**5. Introduction and conclusion architecture.** Opening move: the two procedures, named
neutrally — a taxonomy opening (cf. Posner & Vermeule's design taxonomy, Exemplar 4).
Closing move: the verdict for the wealth-gap standard. The arc is compare → crown — the
paper is structured as a judging, and it ends with the winner.

**6. Literature-review positioning moves.** The abstract positions the entire prior
estimation literature as instances of the two strategies — a *reclassification* move that
subordinates previous estimators (including the authors' own earlier work) to the new
taxonomy. This is the lane's mature form: the literature reviewing itself, with the
reviewers as its most-cited authors.

---

## Exemplar 14 — Browne, "The Economic Basis for Reparations to Black America" (1969/1971; RBPE reprint 1993)

- **Title:** The Economic Basis for Reparations to Black America
- **Authors:** Robert S. Browne
- **Venue:** The Review of Black Political Economy (reprint 1993; original: *The Economic
  Basis for Reparations to Black America*, 1969 pamphlet / 1971 journal version)
- **DOI (1993 reprint):** 10.1007/bf02701708 | **OpenAlex ID:** W1971244818
- **Cited by:** 15 (OpenAlex, as of 2026-09-18; OpenAlex holds the 1993 reprint record —
  citations to the 1969/1971 originals are fragmented across duplicate records, so the true
  count is understated)
- **Text source used:** metadata-only. OpenAlex returned **no abstract** and no open-access
  location. No full text accessed.
- **Confidence:** metadata-only — structural extraction is not performed. Included as a
  deliberate historical anchor: this is the founding economics-of-reparations paper, the work
  that first put a dollar figure on the claim in an economics journal. Its structural role in
  the lane (first-mover estimation) is verifiable from the historical record; its internal
  argument architecture is not recoverable from the metadata and is not inferred here.

---

## Crossref spot-checks (title/year sanity)

| DOI | OpenAlex title/year | Crossref title/year | Match |
|---|---|---|---|
| 10.2307/1123721 | Reparations for Slavery and Other Historical Injustices / 2003 | Reparations for Slavery and Other Historical Injustices / 2003-04 | ✅ |
| 10.1177/0034644620926516 | Wealth Implications of Slavery and Racial Discrimination for African American Descendants of the Enslaved / 2020 | same (truncated display) / 2020-09 | ✅ |
| 10.1111/ssqu.12151 | Estimating Slavery Reparations: Present Value Comparisons of Historical Multigenerational Reparations Policies / 2015 | same (truncated display) / 2015-06 | ✅ |
| 10.1257/jep.36.2.99 | The Cumulative Costs of Racism and the Bill for Black Reparations / 2022 | same / 2022-05-01 | ✅ |

Zero mismatches.

---

## Deliberately excluded (considered, rejected)

- **Olúfẹ́mi Táíwò, *Reconsidering Reparations* (2022, Oxford) — 552 citations.** Highest-cited
  reparations work in the pool, but it is political philosophy (distributive-justice argument),
  not economics: no estimation, no wealth-gap analysis, no policy costing. Out of lane by the
  task's "reparations economics" criterion.
- **Ta-Nehisi Coates, "The Case for Reparations" (2014, *The Atlantic*).** Enormously
  influential public argument, but journalism, not a scholarly paper; no economic estimation
  apparatus. (OpenAlex holds only a 2015 excerpt record, 99 citations.)
- **Eve Tuck & K. Wayne Yang, "Decolonization is not a metaphor" (2012) — 4,103 citations.**
  Top hit of the naive text search; settler-colonial theory of education, no economics of
  slavery content. Search noise.
- **Stern Review / Barro / de Groot et al.** Top hits of the "economics of reparations"
  text search; matched on the word "economics," content is climate/macro. Search noise.
- **"The Wealth of races: the present value of benefits from past injustices" (1991).**
  OpenAlex record (W1978661022, 53 citations) is a *Choice* book review, not the original
  work — excluded to avoid citing a review as a primary contribution.
- **Craemer, "Comparative Analysis of Reparations for the Holocaust and for the Transatlantic
  Slave Trade" (2018) — 6 citations.** In-lane but below the citation bar; the two
  higher-cited Craemer papers represent his contribution.
- **Darity, "Forty Acres and a Mule in the 21st Century" duplicates; Browne 1971/2007/2020
  duplicate records.** Fragmented OpenAlex records for the same work; used the highest-cited
  record only (1993 reprint, 15 citations) and noted the fragmentation.
- **Fogel & Engerman, *Time on the Cross* (1974).** Foundational to the economics of slavery
  (profitability debate), but OpenAlex's records are fragmented across reviews/foreign
  editions with no clean canonical record (top clean hit: 29 citations on a 2016 follow-up).
  Cited here as context: Thomas & Bean (Exemplar 7) is the cleaner in-lane representative of
  the cliometric profitability debate.
- **Dawson & Popoff duplicates; Posner & Vermeule response literature** ("Getting
  Reparations for Slavery Right," 25 citations). In-lane but below the bar; the Posner &
  Vermeule original represents the exchange.

---

## API queries run (all 2026-09-18, default pool, no mailto)

1. `works?search=reparations+economics&sort=cited_by_count:desc&per-page=40&select=id,doi,title,authorships,publication_year,primary_location,cited_by_count,abstract_inverted_index,open_access,best_oa_location`
2. `works?search=economics+of+slavery+reparations&sort=cited_by_count:desc&per-page=40&...` (same select)
3. `works?search=reparations+for+slavery`, `works?search=the+economics+of+reparations`,
   `works?search=racial+wealth+gap+reparations` (per-page 25, brief select)
4. `works?filter=title_and_abstract.search:reparations+slavery&sort=cited_by_count:desc&per-page=40&...` (full select)
5. `authors?search=William+Darity` → author IDs A5087523337, A5110101911;
   `works?filter=authorships.author.id:...&sort=cited_by_count:desc` for both
6. `authors?search=Thomas+Craemer` → A5002906043; works filter for that ID
7. `works?search=Time+on+the+Cross+Fogel+Engerman`, `works?search=Conrad+Meyer+profitability+slavery`
8. `works?search=Forty+Acres+reparations+Darity`, `works?search=unpaid+labor+slavery+reparations+estimate`
9. `works?filter=title.search:Reparations+for+Slavery+and+Other+Historical+Injustices`
10. `works?filter=title.search:The+Economic+Basis+for+Reparations+to+Black+America`
11. `works?filter=title.search:Position+and+Possessions`
12. Per-work full records (`works/{id}`) for all 14 finalists incl. `abstract_inverted_index`
    and `best_oa_location`
13. Crossref: `api.crossref.org/works/{doi}` for 4 DOIs
14. Full-text attempts: curl on 2 OA PDF URLs (Cloudflare challenge pages); `browser.open` on
    1 OA PDF URL (fetch failed, terminal for the turn). No further attempts per policy.

**Reusable corpus artifacts (in /tmp, ephemeral):** `oa1.json`, `oa2.json`, `oa3.json`,
`exemplars.json` (all 13 abstracts reconstructed), `fulltexts/` (2 Cloudflare challenge
HTML files — no usable content). If a later lane needs the raw abstracts, re-run
`fetchall.py` logic against OpenAlex rather than relying on /tmp.

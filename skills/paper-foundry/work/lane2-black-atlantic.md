# Lane 2 — Black Atlantic / African Diaspora History
## Evidence base for paper-foundry: structural argumentation DNA of the most-cited works

**Citation counts as of 2026-09-18. Source: OpenAlex API** (default pool, no mailto).
Crossref spot-checks: 8 DOIs checked, **zero mismatches** (details at end).
Text sources: 1 full text (NBER working-paper version, legitimately downloaded), 1 abstract + article opening (from OpenAlex metadata), 8 abstract/publisher-description level, 5 metadata-only (no abstract or full text available — marked honestly; no DNA invented for these).

**Method note for the skill:** OpenAlex book coverage in this lane is weak. Several field-defining books (Gilroy's *The Black Atlantic*, Patterson's *Slavery and Social Death*, Hartman's *Scenes of Subjection*, Rediker's *The Slave Ship*, C.L.R. James's *The Black Jacobins*, Cedric Robinson's *Black Marxism*) have **no reliable standalone OpenAlex work record** — their citation footprint appears only through review-article proxies or not at all. Review records of famous books also appear to **absorb the book's citations** (see Exemplar 1 caveat). The skill should treat anomalously high review-article counts as merge artifacts, not as evidence about the review.

**Queries run** (all `https://api.openalex.org/works`, `sort=cited_by_count:desc`, `select=id,doi,title,authorships,publication_year,primary_location,cited_by_count,abstract_inverted_index,open_access,best_oa_location`):
- `search=black+atlantic` (per-page=50)
- `search=african+diaspora+history` (per-page=50)
- `search=atlantic+slavery` (per-page=50)
- `search=black+internationalism` (per-page=50)
- ~30 targeted title searches (see "Targeted title searches" at end), plus `filter=type:book` variants for canonical monographs
- Individual work fetches for the 16 finalists; Crossref checks for 8 DOIs

---

## Exemplar 1 — Aldon Lynn Nielsen, "The Black Atlantic: Modernity and Double Consciousness" (review), *Modernism/modernity* 1(3), 1994
- **Authors:** Aldon Lynn Nielsen
- **Venue:** Modernism/modernity, Vol. 1, No. 3 (September 1994)
- **Year:** 1994
- **DOI:** https://doi.org/10.1353/mod.1994.0041
- **OpenAlex ID:** https://openalex.org/W2029501868
- **cited_by_count (OpenAlex, 2026-09-18):** 7,562
- **Text source used:** metadata-only. No abstract in OpenAlex; closed access. This is a **review article of Paul Gilroy's book** *The Black Atlantic: Modernity and Double Consciousness* (1993) — it is NOT the book itself, and no standalone OpenAlex record for Gilroy's book was found (searched type:book + title variants).
- **1. Gap-framing move:** Unverifiable from available text. Genre-level only: as a review-essay in a modernist-studies journal, its structural function is to position Gilroy's book for a literary/modernism audience.
- **2. Contribution-claim architecture:** Unverifiable from available text.
- **3. Evidence-to-claim density:** Unverifiable from available text.
- **4. Objection handling:** Unverifiable from available text.
- **5. Introduction and conclusion architecture:** Unverifiable from available text.
- **6. Literature-review positioning moves:** Unverifiable from available text.
- **Confidence note:** LOW — metadata-only, and the 7,562 count is very likely a **citation-merge artifact** (OpenAlex attributing citations of Gilroy's famous book to this review record; the companion Erickson/African American Review exchange record shows the same pattern at 4,778). Do not treat the count as evidence about the review's own influence. Included because it is the highest-cited OpenAlex record in the "black atlantic" search and the only quantitative trace of Gilroy's book in the API — the skill must know this artifact exists.

## Exemplar 2 — Saidiya Hartman, "Venus in Two Acts," *Small Axe* 12(2), 2008
- **Authors:** Saidiya Hartman
- **Venue:** Small Axe: A Caribbean Journal of Criticism
- **Year:** 2008
- **DOI:** https://doi.org/10.1215/-12-2-1
- **OpenAlex ID:** https://openalex.org/W2058372570
- **cited_by_count (OpenAlex, 2026-09-18):** 3,213
- **Text source used:** abstract-only (abstract reconstructed from OpenAlex `abstract_inverted_index`; closed access, no full-text attempt).
- **1. Gap-framing move:** The gap is named as an impossibility, not a missing fact: Venus is "ubiquitous" in the archive of Atlantic slavery yet nothing about her can be discovered "that hasn't already been stated." The consensus being positioned against is the recovery project itself — the assumption that diligent archival work yields the enslaved subject. The gap is made to matter by scale: Venus is "emblematic," so her limit-case status indicts the whole method.
- **2. Contribution-claim architecture:** One big methodological claim, not stacked empirical sub-claims: the essay proposes writing "at the limit of the unspeakable and the unknown" as a legitimate historiographical act. The thesis is stated as what the essay "examines" and "wrestles with" — the claim is the method. Qualification is built into the architecture: the writing only "mimes" redress; it does not claim to achieve it.
- **3. Evidence-to-claim density:** Evidence and claim are fused: the recurring archival figure of Venus IS both the evidence and the argument. Every claim sits directly on the figure — "convergence of terror and pleasure," "intimacy of history," "scandal and excess" are all read off her recurrence. Maximum density: there is no separate evidentiary layer.
- **4. Objection handling:** Preemption by confession. The obvious objection — that narrating beyond the archive repeats the violence of the archive (invention as violation) — is named inside the abstract's own terms: the writing "mimes the violence" of its attempts at redress. The objection is conceded and converted into method rather than refuted.
- **5. Introduction and conclusion architecture:** Opening move is paradox: ubiquity + unknowability stated together in the first breath. Closing move (per the abstract) does not resolve the paradox but inhabits the limit: describing "as fully as possible the conditions that determine [her] appearance and dictate [her] silence." The conclusion is a disciplined refusal of closure.
- **6. Literature-review positioning moves:** Positions against the consensus that the archive can be made to yield the enslaved woman; delimits prior recovery scholarship by naming what the archive structurally cannot give. Credit is implicit (the recovery project is the necessary precondition); delimitation is the contribution.
- **Confidence note:** MEDIUM — abstract-only; gap-framing, contribution architecture, and objection-handling are well-grounded in the abstract's explicit language, but intro/conclusion moves are inferred from the abstract's framing and remain unverified against the full text.

## Exemplar 3 — Nathan Nunn & Léonard Wantchekon, "The Slave Trade and the Origins of Mistrust in Africa," *American Economic Review* 101(7), 2011
- **Authors:** Nathan Nunn, Léonard Wantchekon (OpenAlex renders "Léonard Wantchekon"; NBER/SSRN render "Leonard Wantchekon")
- **Venue:** American Economic Review
- **Year:** 2011
- **DOI:** https://doi.org/10.1257/aer.101.7.3221
- **OpenAlex ID:** https://openalex.org/W2145309110
- **cited_by_count (OpenAlex, 2026-09-18):** 2,216
- **Text source used:** FULL TEXT — NBER Working Paper 14783 (March 2009), the working-paper version of the AER article, 52 pages, downloaded as PDF from the NBER asset host (URL obtained verbatim from web search results). Structural analysis below is of the working-paper text; the published AER version (pp. 3221–3252) is substantively the same paper.
- **1. Gap-framing move:** Opens by citing the first author's own prior paper (Nunn 2008), which found the slave trade hurt long-run development but "was unable to pin down the exact causal mechanisms underlying the reduced form relationship." The gap is therefore a *mechanism gap inside an already-established causal claim* — a second-order gap, which is a stronger position than contesting the literature. It is made to matter by the trust literature: "mounting evidence" that trust matters for development, trade, institutions, and firm management, so the *origins* of trust become "the natural next step."
- **2. Contribution-claim architecture:** One big claim (the slave trade caused a culture of mistrust persisting in Africa today), sequenced as a four-stage evidentiary staircase, each stage previewed in the introduction: (a) OLS correlation between ancestral slave-trade exposure and current mistrust; (b) IV causal identification (historic ethnic-group distance from the coast as instrument, controlling for current distance); (c) falsification tests (outside Africa; unexposed African regions); (d) mechanism decomposition (internal beliefs/values ≈ 75% vs. external institutions). Hedging is lexical and consistent: "arguably," "suggests," "consistent with," "evidence."
- **3. Evidence-to-claim density:** Extremely tight — every claim sits on a named dataset and specification in the same paragraph: Afrobarometer 2005 individual-level survey merged to ethnicity-level slave-export estimates (80,656 trans-Atlantic + 21,048 Indian Ocean shipment records via Nunn 2008, matched through Murdock 1959); trust measured separately for relatives, neighbors, local government; the movers-vs-stayers comparison isolates internal beliefs from external environment. No claim floats free of its test.
- **4. Objection handling:** Named explicitly and *early* — the reverse-causality objection ("more slaves were supplied by ethnic groups that initially had lower levels of trust") is stated in the introduction and answered with the IV strategy; the exclusion-restriction threat is conceded as "far less clear" and answered with falsification exercises; the paper closes with a scope concession ("our focus on the long-term historic determinants… does not mean that short-run determinants are not important," with citations). Structure: preempt → concede-the-hard-part → answer → concede-the-boundary.
- **5. Introduction and conclusion architecture:** Introduction: prior-result gap → historical narrative of the mechanism (citing Koelle 1854, Hair 1965, Piot 1996 on kin selling kin) → theoretical grounding (Boyd & Richerson cultural-evolution rules-of-thumb) → data/methods roadmap → results preview → contribution placement ("complement," "dovetails nicely with"). Conclusion: restates the paper as filling the "origins of cultural differences" next step, re-walks the IV + falsification + mechanism results in order, introduces no new claims, ends on the short-run-determinants concession. Textbook hourglass: wide (literature) → narrow (specification) → wide (what it means).
- **6. Literature-review positioning moves:** Prior work is grouped into three credited piles — (a) why trust matters economically (Tabellini, Knack & Keefer, Greif, Putnam, Bloom et al.), (b) empirical culture literature (existence of culture effects: Giuliano, Fernández & Fogli, Miguel et al.), (c) historical determinants of culture (Guiso, Sapienza & Zingales; Tabellini) — and the paper slots itself as "the natural next step" after (a)+(b), "like the recent contributions" of (c). Generous credit, precise delimitation: the room made is exactly one mechanism wide.
- **Confidence note:** HIGH — full-text analysis of the working-paper version; section-level structure verified against the actual text. Caveat: DNA is of the 2009 NBER version, not the final 2011 AER text.

## Exemplar 4 — Christina Sharpe, *In the Wake: On Blackness and Being*, Duke University Press, 2016
- **Authors:** Christina Sharpe
- **Venue:** Duke University Press (book)
- **Year:** 2016
- **DOI:** https://doi.org/10.1215/9780822373452
- **OpenAlex ID:** https://openalex.org/W4230278761
- **cited_by_count (OpenAlex, 2026-09-18):** 1,521
- **Text source used:** publisher-description level (Duke University Press book description, obtained via web search snippet from read.dukeupress.edu; no abstract in OpenAlex or Crossref; closed access, no full-text attempt).
- **1. Gap-framing move:** Positions against frames that treat premature Black death as normal background: the book "interrogates… representations of Black life" to name "the afterlives of slavery" as the active condition. The gap is made to matter existentially — it is the total climate ("the weather") in which Black life is lived, not a historiographical nicety.
- **2. Contribution-claim architecture:** Theory *and* method in one move: "initiating and describing a theory and method of reading" built from four linked analytic metaphors — the wake, the ship, the hold, the weather. One big claim (the afterlives of slavery animate contemporary Black life) carried by a stacked conceptual apparatus; each metaphor does distinct analytic work (path behind the ship / keeping watch with the dead / coming to consciousness).
- **3. Evidence-to-claim density:** Multi-archive by design: "literary, visual, cinematic, and quotidian representations." Claims sit close to cultural texts rather than to a single evidentiary base; per a published review, the book "refus[es] to distinguish between artistic and scholarly sources" — the composition is part of the argumentation. Density is associative rather than tabular.
- **4. Objection handling:** Not visible at description level. The description preempts the determinism objection structurally: the hold produces "containment, regulation, and punishment, but also something in excess of them" — conceding the structure's force while claiming the excess as the site of possibility.
- **5. Introduction and conclusion architecture:** Opening move is definitional multiplication: three registers of "wake" are activated simultaneously before any argument begins. Closing move (per the description) is forward-looking rather than summative: the book "offers a way forward" — possibility, not resolution.
- **6. Literature-review positioning moves:** Builds explicitly in the Hartman/Spillers lineage (a published review notes both books share that "theoretical archive") — credited as the *location* of theoretical activity, with Black cultural production positioned as theory's source rather than its destination. The move is affiliation-plus-extension: same lineage, new method ("wake work").
- **Confidence note:** MEDIUM-LOW — publisher-description level; the four-metaphor apparatus and the opening/closing moves are grounded in the publisher's copy, but all six points are unverified against the book's actual text.

## Exemplar 5 — Jennifer L. Morgan, *Laboring Women: Reproduction and Gender in New World Slavery*, University of Pennsylvania Press, 2004
- **Authors:** Jennifer L. Morgan
- **Venue:** University of Pennsylvania Press (book)
- **Year:** 2004
- **DOI:** https://doi.org/10.9783/9780812206371
- **OpenAlex ID:** https://openalex.org/W4211004316
- **cited_by_count (OpenAlex, 2026-09-18):** 1,069
- **Text source used:** metadata-only. No abstract in OpenAlex or Crossref; closed access, no full-text attempt.
- **1.–6. Structural DNA:** Unverifiable from available sources. Bibliographic facts only: the most-cited gender-history monograph in the lane (1,069 citations), published by UPenn Press in 2004, centered on reproduction and gender in New World slavery. Its citation rank signals that the gendered-reproduction frame is one of the lane's load-bearing contributions, but no argumentative moves can be extracted without the text.
- **Confidence note:** LOW — metadata-only; no structural extraction possible. Flagged for the skill as a high-priority full-text acquisition target (its count suggests foundational status).

## Exemplar 6 — Marisa J. Fuentes, *Dispossessed Lives: Enslaved Women, Violence, and the Archive*, University of Pennsylvania Press, 2016
- **Authors:** Marisa J. Fuentes
- **Venue:** University of Pennsylvania Press (book)
- **Year:** 2016
- **DOI:** https://doi.org/10.9783/9780812293005
- **OpenAlex ID:** https://openalex.org/W4254148763
- **cited_by_count (OpenAlex, 2026-09-18):** 781
- **Text source used:** abstract-only (publisher blurb reconstructed from OpenAlex `abstract_inverted_index`; closed access, no full-text attempt).
- **1. Gap-framing move:** Positions against the methodological consensus on writing histories of "vulnerable invisible subjects": the book "challenges how histories… are written." The gap is archival-methodological — the archive (urban, legal, sexual, representational power) is itself one of the instruments of confinement, so standard recovery methods reproduce the violence. Made to matter by naming the archive as a wielder of power, not a neutral storehouse.
- **2. Contribution-claim architecture:** One big methodological claim (a new way of writing enslaved women's histories) carried by stacked sub-claims across four domains of power — urban, legal, sexual, representational. The sub-claims are parallel and cumulative: each domain shows confinement operating through a different apparatus.
- **3. Evidence-to-claim density:** Microhistorical: "vividly recounting the lives of enslaved women in eighteenth-century Bridgetown, Barbados." Claims sit close to individual lives reconstructed against a hostile archive; density is high but the evidence is fragmentary by design (the fragments are the point).
- **4. Objection handling:** Preempts the evidentiary objection (there isn't enough in the archive) by making the archive's hostility the argument: the "conditions of confinement" include the archive itself, so reading along its bias becomes method rather than limitation. (Inferred from the blurb's framing; unverified against the text.)
- **5. Introduction and conclusion architecture:** Unverifiable beyond the blurb's implication that the book opens on the lives themselves ("vividly recounting") rather than on historiography — an enactment of its own method.
- **6. Literature-review positioning moves:** Delimits prior histories of enslaved women by their method (how such histories "are written"), crediting the subject while contesting the craft.
- **Confidence note:** MEDIUM-LOW — abstract-only; gap-framing and contribution architecture are grounded in the blurb's explicit language, but objection-handling and intro/conclusion moves are inferred and unverified.

## Exemplar 7 — John K. Thornton, *Africa and Africans in the Making of the Atlantic World, 1400–1800*, 2nd ed., Cambridge University Press, 1998
- **Authors:** John K. Thornton
- **Venue:** Cambridge University Press (book)
- **Year:** 1998 (2nd edition; 1st ed. 1992)
- **DOI:** https://doi.org/10.1017/cbo9780511800276
- **OpenAlex ID:** https://openalex.org/W4301870294
- **cited_by_count (OpenAlex, 2026-09-18):** 738
- **Text source used:** abstract-only (description reconstructed from OpenAlex `abstract_inverted_index`; closed access, no full-text attempt).
- **1. Gap-framing move:** Positions against Eurocentric accounts of the slave trade: the claim is that "African institutions, political events, economic structures shaped" the trade's development — Africans as determiners of terms, not passive victims. The anomaly named: why enslaved Africans were placed in roles of "central significance" in the New World, which a Europe-driven story cannot explain. The gap is made to matter as a causal-explanatory failure of the consensus.
- **2. Contribution-claim architecture:** Stacked causal sub-claims in chronological-causal sequence: (a) before 1680 Africa was a "voluntary arena" whose institutions shaped engagement; (b) African military strength gave elites "capacity to determine how trade with Europe developed"; (c) estate structure and demography in the Americas then shaped how Africans behaved "as cultural actors, transferring and transforming culture." Thesis moves from African agency → terms of trade → New World cultural outcomes.
- **3. Evidence-to-claim density:** Claims operate at the structural level (institutions, political events, economic structures, military capacity, demography); evidence is pitched at the level of African polities and Atlantic systems rather than individuals. Medium density: structures evidenced by comparative institutional analysis (details unverifiable from the abstract).
- **4. Objection handling:** Unverifiable from available text.
- **5. Introduction and conclusion architecture:** Unverifiable from available text; the abstract implies a chronological spine (15th → 18th century) with an analytic payoff (culture transfer/transformation).
- **6. Literature-review positioning moves:** The positioning is by inversion: the existing literature's Europe-centered causal arrow is reversed, with African-side factors credited as the shapers. Delimitation is temporal as well as geographic (the "before 1680" voluntary-arena claim bounds the argument).
- **Confidence note:** MEDIUM-LOW — abstract-only; the agency-inversion framing and the three-step claim sequence are grounded in the abstract's language, but evidence density, objection handling, and intro/conclusion architecture are unverified.

## Exemplar 8 — Ian Baucom, *Specters of the Atlantic: Finance Capital, Slavery, and the Philosophy of History*, Duke University Press, 2005
- **Authors:** Ian Baucom
- **Venue:** Duke University Press (book)
- **Year:** 2005
- **DOI:** https://doi.org/10.1215/9780822387022
- **OpenAlex ID:** https://openalex.org/W4230296206
- **cited_by_count (OpenAlex, 2026-09-18):** 709
- **Text source used:** metadata-only. No abstract in OpenAlex or Crossref; closed access, no full-text attempt.
- **1.–6. Structural DNA:** Unverifiable from available sources. Bibliographic facts only: the lane's most-cited finance-capital/slavery monograph (709 citations), joining slavery's history to the philosophy of history via finance capital. No argumentative moves extractable without the text.
- **Confidence note:** LOW — metadata-only; no structural extraction possible. High-priority full-text acquisition target (its subtitle signals a distinctive theory-history braiding move the skill currently cannot see).

## Exemplar 9 — Laurent Dubois, *Avengers of the New World: The Story of the Haitian Revolution*, Belknap Press of Harvard University Press, 2004
- **Authors:** Laurent Dubois (OpenAlex renders "Laurent Dubois")
- **Venue:** The Belknap Press of Harvard University Press (book)
- **Year:** 2004
- **DOI:** https://doi.org/10.4159/9780674034365
- **OpenAlex ID:** https://openalex.org/W4207014878
- **cited_by_count (OpenAlex, 2026-09-18):** 629
- **Text source used:** publisher-description level (Harvard University Press book description, obtained via web search snippet from hup.harvard.edu; no abstract in OpenAlex or Crossref; closed access, no full-text attempt).
- **1. Gap-framing move:** The gap is omission/misrepresentation: the Haitian Revolution — "the first and only successful slave revolution in the Americas" — has been kept out of the democratic-revolution canon ("deliberately misrepresented for the past two centuries," per a published blurb). Made to matter by scale: it is claimed as "a foundational moment in the history of democracy and human rights," so the omission indicts the canon itself.
- **2. Contribution-claim architecture:** One big reframing claim (Haiti as foundational to democracy/human rights) carried by braided multi-perspective narrative: the book "weaves the stories of slaves, free people of African descent, wealthy whites, and French administrators." The narrative structure IS the claim architecture — four social positions, one insurrection.
- **3. Evidence-to-claim density:** Claims sit close to the braided stories; the macro-claim (Atlantic-world reshaping: Louisiana sale, Cuban sugar expansion) is evidenced through the interwoven group narratives rather than through a separate analytic layer.
- **4. Objection handling:** Not visible at description level.
- **5. Introduction and conclusion architecture:** Per the description, the opening move is superlative-staking ("the first and only successful slave revolution") — the book opens by asserting the event's singularity, then earns it. Closing move is canon-revision: establishing Haiti inside the democracy/human-rights lineage.
- **6. Literature-review positioning moves:** Positions against two centuries of misrepresentation by re-lineage: blurbs place the book in the lineage of C. L. R. James and Aimé Césaire — affiliation as argument, claiming the mantle rather than merely citing predecessors.
- **Confidence note:** MEDIUM-LOW — publisher-description level; the reframing claim and braided-narrative architecture are grounded in HUP's copy, but objection handling and internal structure are unverified.

## Exemplar 10 — Stephanie Smallwood, *Saltwater Slavery: A Middle Passage from Africa to American Diaspora*, Harvard University Press, 2007
- **Authors:** Stephanie Smallwood (OpenAlex renders "Stephanie Smallwood")
- **Venue:** Harvard University Press (book)
- **Year:** 2007
- **DOI:** https://doi.org/10.4159/9780674043770
- **OpenAlex ID:** https://openalex.org/W4206961360
- **cited_by_count (OpenAlex, 2026-09-18):** 564
- **Text source used:** description level (retailer synopsis + published review summary, obtained via web search snippets; no abstract in OpenAlex or Crossref; closed access, no full-text attempt).
- **1. Gap-framing move:** Positions as a replacement starting point: "the new starting point for studies of the Middle Passage" (Ira Berlin blurb). The anomaly: the captives' own conceptual world — how people "who in some cases had never seen white people, the ocean or a ship" understood the saltwater experience — reconstructed from the European company archive that never intended to record it. Made to matter as both human story and structural account ("how African people were transformed into Atlantic commodities").
- **2. Contribution-claim architecture:** One big process claim — commodification as a *process* with stages — sequenced geographically and experientially: Gold Coast shores → coastal forts → the ship → the American market → reconstruction of social identity in the New World. Each stage is both a place and a transformation.
- **3. Evidence-to-claim density:** Claims sit very close to the Royal African Company archive: ship logs, Board of Trade records, private journals, merchant correspondence, maps — read against the grain in what a published review calls "almost archaeological excavation," turning "familiar passages and seemingly innocuous lines" into the human story. High density: the method is the proximity.
- **4. Objection handling:** Preempts the invention charge by naming the control: the imaginative reconstruction of captives' worldviews is "carefully controlled" (Times Literary Supplement review) — the objection (you can't know what they thought) is answered by anchoring each inference in documented beliefs of the societies of origin.
- **5. Introduction and conclusion architecture:** Per the review, the book "begins with a description of the prime months for transporting human cargo" — opens on logistics and seasonality (the trade's calendar) before widening to the human story; an infrastructural opening for a humanistic argument. Closing moves unverifiable.
- **6. Literature-review positioning moves:** The Berlin blurb performs field-consolidation ("required reading for students of the black Atlantic"); the book delimits prior Middle Passage scholarship by shifting the vantage point to "the vantage point of the slaves themselves" while keeping the merchant-capitalist archive as the evidentiary base — a both/and positioning rather than a rejection.
- **Confidence note:** MEDIUM-LOW — description/review-summary level; gap-framing, the staged process claim, and the against-the-grain method are grounded in the synopsis and review language, but internal structure and objection handling are unverified against the book.

## Exemplar 11 — Ira Berlin, *Many Thousands Gone: The First Two Centuries of Slavery in North America*, Belknap Press of Harvard University Press, 1998
- **Authors:** Ira Berlin (OpenAlex renders "Irā Berlin")
- **Venue:** Belknap Press of Harvard University Press (book)
- **Year:** 1998
- **DOI:** https://doi.org/10.4159/9780674020825
- **OpenAlex ID:** https://openalex.org/W4300524971
- **cited_by_count (OpenAlex, 2026-09-18):** 516
- **Text source used:** abstract-only (short publisher blurb reconstructed from OpenAlex `abstract_inverted_index`; closed access, no full-text attempt).
- **1. Gap-framing move:** Positions against the cotton-king teleology: the consensus being displaced is the projection of monolithic antebellum plantation slavery backward onto the 17th and 18th centuries. The gap is named as "the diverse forms that slavery and freedom assumed before cotton was king" — diversity where the literature assumed uniformity. Made to matter as a corrective to the origin story of Black society in America.
- **2. Contribution-claim architecture:** One big developmental claim — "traces the evolution of Black society in America from its creation in the early 17th century through the American Revolution" — with internal periodization implied by the long chronology (creation → transformation across two centuries). The blurb gives the arc, not the stages.
- **3. Evidence-to-claim density:** Pitched at "southern and African-American life" — regional social history. Density unverifiable from the blurb.
- **4. Objection handling:** Unverifiable from available text.
- **5. Introduction and conclusion architecture:** Unverifiable from available text; the blurb implies a chronological spine from "creation" through revolution.
- **6. Literature-review positioning moves:** The "before cotton was king" phrase does the positioning work: prior literature is delimited temporally (it described the 19th century and smuggled it backward), and the book claims the earlier centuries as its terrain.
- **Confidence note:** LOW-MEDIUM — abstract-only and the abstract is a two-sentence blurb; only the gap-framing move (anti-teleology) is firmly grounded. Note: Berlin's WMQ article "From Creole to African" (1996), which first stated the charter/plantation-generations thesis, has no clean OpenAlex record and could not be included.

## Exemplar 12 — Tiffany Ruby Patterson & Robin D. G. Kelley, "Unfinished Migrations: Reflections on the African Diaspora and the Making of the Modern World," *African Studies Review* 43(1), 2000
- **Authors:** Tiffany Ruby Patterson, Robin D. G. Kelley
- **Venue:** African Studies Review, Vol. 43, No. 1, Special Issue (April 2000), pp. 11–45
- **Year:** 2000
- **DOI:** https://doi.org/10.2307/524719
- **OpenAlex ID:** https://openalex.org/W2050621432
- **cited_by_count (OpenAlex, 2026-09-18):** 474
- **Text source used:** metadata-only. OpenAlex holds no abstract (the abstract field contains only the citation string); closed access, no full-text attempt.
- **1.–6. Structural DNA:** Unverifiable from available sources. Bibliographic facts only: the field-defining programmatic article on African diaspora as an analytic frame (474 citations; special-issue lead article; published with a "Commentary and Response" companion piece in the same issue, indicating it was staged as a debate intervention). Its title signals the core move — diaspora as *unfinished* process tied to "the making of the modern world" — but no argumentative moves can be extracted without the text.
- **Confidence note:** LOW — metadata-only; no structural extraction possible. The highest-priority full-text acquisition target in the lane for the skill (a programmatic field-definition article is exactly the genre paper-foundry needs most).

## Exemplar 13 — Vincent Brown, "Social Death and Political Life in the Study of Slavery," *The American Historical Review* 114(5), 2009
- **Authors:** Vincent Brown
- **Venue:** The American Historical Review
- **Year:** 2009
- **DOI:** https://doi.org/10.1086/ahr.114.5.1231
- **OpenAlex ID:** https://openalex.org/W2042278359
- **cited_by_count (OpenAlex, 2026-09-18):** 376
- **Text source used:** abstract + article opening (OpenAlex's `abstract_inverted_index` unusually contains the article's opening vignette — several paragraphs of the published text; remainder closed access, no full-text attempt).
- **1. Gap-framing move:** The gap is staged as anomaly-against-concept before any historiography appears: a woman dies aboard the *Hudibras* in 1786 — "universally esteemed" as "oracle," "orator," "songstress" — and her death causes "minor political tumult" among the captives. This is irreconcilable with the "social death" framework's alienated isolate "hurled over the side without ceremony." The consensus (Patterson's social death as the master concept) is positioned against by *evidence first, concept second*; the gap is made to matter because the field's central analytic cannot see the scene's politics.
- **2. Contribution-claim architecture:** The title states the thesis move: from "social death" TO "political life" — a reframing claim in a single conceptual pivot. The vignette is the evidentiary anchor for the pivot; the claim is one big re-description, not stacked sub-claims (beyond the opening, unverified).
- **3. Evidence-to-claim density:** Extremely close in the opening: the macro-conceptual claim sits directly on a fully specified micro-scene — named ship (*Hudibras*), year (1786), named witness (William Butterworth), quoted phrases ("soul of sociality," "nearly prostrate, with hands stretched forth"), spatial arrangement ("concentric circles, innermost ring… youngest girls, elderly perimeter"). The concept arrives embedded in the evidence, not above it.
- **4. Objection handling:** Unverifiable beyond the opening (the abstract field ends with the vignette).
- **5. Introduction and conclusion architecture:** Opens *in medias res* with a fully realized archival scene — vessel, date, death, quoted sailor's account — before any literature review or thesis statement. The analytic term ("soul of sociality") is smuggled in inside the scene's own language. This is the cold-open vignette structure: evidence performs the argument before the argument is declared. Closing moves unverifiable.
- **6. Literature-review positioning moves:** The title performs the positioning at the highest level — taking Patterson's "social death" as the named foil and appending "political life" as the revision. (Title-level inference, stated as such; the body positioning is unverified.)
- **Confidence note:** MEDIUM — the opening vignette is genuine article text from OpenAlex metadata, so the intro architecture and gap-staging are well-grounded; everything past the opening (objection handling, conclusion, full lit-review moves) is unverified.

## Exemplar 14 — Ada Ferrer, *Freedom's Mirror: Cuba and Haiti in the Age of Revolution*, Cambridge University Press, 2014
- **Authors:** Ada Ferrer
- **Venue:** Cambridge University Press (book)
- **Year:** 2014
- **DOI:** https://doi.org/10.1017/cbo9781139333672
- **OpenAlex ID:** https://openalex.org/W4244427542
- **cited_by_count (OpenAlex, 2026-09-18):** 318
- **Text source used:** abstract-only (full publisher abstract, 1,112 characters, obtained from Crossref metadata; closed access, no full-text attempt).
- **1. Gap-framing move:** The gap is historiographical separation itself: "two stories… that are usually told separately" — the Haitian Revolution and the rise of Cuban slave society. The anomaly is a paradox: "the antithesis of revolutionary emancipation" (slavery's violent entrenchment in Cuba) occurred "at the very moment" of the revolution next door, "barely fifty miles distant." Made to matter as mutual distortion: each story is misunderstood in isolation; both are "crucial moments in Caribbean and Atlantic history."
- **2. Contribution-claim architecture:** One big connective claim — "creatively linking two stories" — sequenced as paradox → mechanism → mutual illumination. The mechanism is specified in the abstract (Cuban planters "rushed to fill the void left in the world market for sugar, to buttress the institutions of slavery and colonial rule, and to prevent 'another Haiti'"); the payoff is symmetric ("sheds fresh light on both").
- **3. Evidence-to-claim density:** Claims are carried by paired-case comparison: Haitian events and Cuban responses are held in the same frame, with the causal arrows named (Haiti → Cuban sugar boom → institutional entrenchment). Medium-high density at the abstract level; the evidentiary base (Cuban archives) is implied rather than stated.
- **4. Objection handling:** Not visible in the abstract.
- **5. Introduction and conclusion architecture:** The abstract implies a paradox opening (most radical revolution → antithesis fifty miles away) and a mutual-illumination close ("sheds fresh light on both"). Both inferred; unverified against the text.
- **6. Literature-review positioning moves:** Delimits prior work by its *segregation*: the field's habit of telling the stories separately is named as the problem, which positions the book as the synthesis without having to attack any single predecessor — a non-adversarial positioning move (the gap is a missing connection, not a wrong consensus).
- **Confidence note:** MEDIUM — abstract-only, but the abstract is unusually complete (mechanism + payoff both specified); gap-framing and contribution architecture are well-grounded, intro/conclusion moves inferred.

## Exemplar 15 — Brent Hayes Edwards, *The Practice of Diaspora: Literature, Translation, and the Rise of Black Internationalism*, Harvard University Press, 2003
- **Authors:** Brent Hayes Edwards (OpenAlex renders "BRENT HAYES EDWARDS")
- **Venue:** Harvard University Press (book)
- **Year:** 2003
- **DOI:** https://doi.org/10.2307/j.ctv1pncqd9
- **OpenAlex ID:** https://openalex.org/W4230063574
- **cited_by_count (OpenAlex, 2026-09-18):** 289
- **Text source used:** metadata-only. No abstract in OpenAlex or Crossref; closed access, no full-text attempt. (A published review of the book by Christopher J. Lee exists as a separate OpenAlex record at 831 citations but was excluded as a review proxy.)
- **1.–6. Structural DNA:** Unverifiable from available sources. Bibliographic facts only: the lane's most-cited monograph on Black internationalism (289 citations), centered on literature and translation as diasporic practice. No argumentative moves extractable without the text.
- **Confidence note:** LOW — metadata-only; no structural extraction possible. High-priority acquisition target (the translation-as-diaspora-practice frame is a distinctive methodological contribution the skill cannot currently see).

---

## Cross-cutting structural patterns (for the skill builder)

1. **The paradox opening** is the lane's signature intro move: Hartman (ubiquity + unknowability), Ferrer (revolution → antithesis fifty miles away), Brown (social death concept vs. political tumult scene), Smallwood (company archive → captives' worldview). Four of the extractable exemplars open by staging a contradiction, not by surveying literature.
2. **The archive is the argument.** In Hartman, Fuentes, Smallwood, and Brown, the source base's hostility or silence is not a limitation section — it is converted into the method itself (critical fabulation; reading along the bias; against-the-grain excavation; the vignette that the concept cannot see).
3. **Single-pivot theses dominate over stacked claims.** The most-cited works make one big reframing move (social death → political life; separate stories → linked stories; Europe-centered → Africa-shaped; recovery → the limit of the unspeakable) rather than accumulating sub-claims. Nunn & Wantchekon is the exception: a four-stage evidentiary staircase, which is the economics genre's structure, not the history genre's.
4. **Positioning by inversion or by connection, rarely by demolition.** Thornton inverts the causal arrow; Ferrer connects separated stories; Sharpe extends a lineage (Hartman/Spillers) with a new method. Direct attacks on named predecessors are rare in the extractable sample; the room is made by re-framing, not refuting.
5. **Objection handling is preemptive and early.** Where visible (Nunn, Hartman, Smallwood), the strongest objection is named in the introduction and answered by the method itself — the method is designed as the answer to the objection.
6. **Evidence sits inside the claim.** The cold-open vignette (Brown), the emblematic figure (Hartman), the paired case (Ferrer), the staged process (Smallwood): in each, the evidence is not presented *then* interpreted — it performs the interpretation.

## Deliberately excluded (with reasons)

- **Keyword-collision noise** (excluded despite high counts): "A global reference for human genetic variation" (20,421), "A survey on Image Data Augmentation" (13,102), Empagliflozin/NEJM (12,267), IntCal radiocarbon curves (10,055/7,863), Canu genome assembly (8,326), WISE mission (8,150), and ~40 similar — matched "black atlantic"/"african diaspora" via biomedical/geoscience keyword overlap. Not lane.
- **Peter Erickson / Paul Gilroy exchange**, "The Black Atlantic," *African American Review* 1997 (4,778) — same review-proxy class as the Nielsen record; kept Nielsen as the single Gilroy proxy to avoid double-counting one book. Crossref verified (1997, African American Review).
- **Marilyn Lake & Henry Reynolds, *Drawing the Global Colour Line*** (976) — transnational whiteness/global color line; adjacent to the lane but not centered on the Black Atlantic, diaspora, or slavery.
- **Peter Duignan's review of Philip Curtin's *The Atlantic Slave Trade: A Census*** (793) — review proxy of a foundational quantitative work; excluded under the same no-proxy rule.
- **Saidiya Hartman, *Lose Your Mother*** (739) — OpenAlex record is typed "article," carries no DOI, and has thin metadata; Hartman is already represented by the richer "Venus in Two Acts" record.
- **Acemoglu/Johnson/Robinson "Reversal of Fortune"** (2,539) and **Acemoglu et al. "Institutions as the Fundamental Cause"** (2,024) — colonial-origins economics surfaced by the "atlantic slavery" keyword; not Black Atlantic/diaspora-history framed.
- **Choice Reviews Online book-review records** (Smallwood 374, Rediker 469, Edwards/Lee review 831, "Specters of the Atlantic" 698, etc.) — review proxies; the book records were used instead.
- **Lara Putnam, *Radical Moves*** (448) — Caribbean intra-regional migration; adjacent but narrower than the lane frame.
- **Ashli White's JAH review of Julius Scott's *The Common Wind*** (430) — review proxy.
- **Nell Painter's JAH review of Hartman's *Scenes of Subjection*** (1,417) — review proxy; the book itself has no clean OpenAlex record (data gap noted below).
- **David Brion Davis's AHR review of Berlin's *Many Thousands Gone*** (428) — review proxy.
- **Jared Yates Sexton, "The Social Life of Social Death"** (562) — secondary theoretical literature *about* the lane (Afro-pessimism debate), not lane historiography itself.
- **Orlando Patterson, *Slavery and Social Death* (book)** — OpenAlex holds only 2018 reissue records with single-digit counts (5 and 3), clearly split/undercounted; excluded rather than present a misleading number. Major data gap.
- **Ira Berlin, "From Creole to African," *WMQ* 1996** — no clean OpenAlex record found; represented via *Many Thousands Gone*.

## Data gaps the skill should know about

OpenAlex has no reliable standalone citation record for: Gilroy's *The Black Atlantic* (1993), Patterson's *Slavery and Social Death* (1982), Hartman's *Scenes of Subjection* (1997), Rediker's *The Slave Ship* (2007), C. L. R. James's *The Black Jacobins* (OpenAlex record W1953578172 exists but misattributes authorship to "Caron James, Pierre Naville" — do not use), Cedric Robinson's *Black Marxism* (1983), Julius Scott's *The Common Wind* (2018 book; only reviews found), Rebecca Scott's *Degrees of Freedom*, Jennifer Morgan's *Laboring Women* full text, Ian Baucom's *Specters of the Atlantic* full text. Any citation-count ranking of this lane built on OpenAlex alone will systematically undercount pre-2000 monographs and misattribute book citations to review records.

## API queries run (complete list)

Base: `https://api.openalex.org/works?sort=cited_by_count:desc&select=id,doi,title,authorships,publication_year,primary_location,cited_by_count,abstract_inverted_index,open_access,best_oa_location`
1. `?search=black+atlantic&per-page=50` (+ base params)
2. `?search=african+diaspora+history&per-page=50` (+ base params)
3. `?search=atlantic+slavery&per-page=50` (+ base params)
4. `?search=black+internationalism&per-page=50` (+ base params)
5. Targeted title searches (~30, per-page=3, select=id,doi,title,authorships,publication_year,primary_location,cited_by_count,type,open_access,best_oa_location): "The Black Atlantic: Modernity and Double Consciousness", "Slavery and Social Death Orlando Patterson", "From Creole to African Ira Berlin", "Social Death and Political Life in the Study of Slavery", "The Slave Ship Marcus Rediker", "Recreating Africa James Sweet", "Way of Death Joseph Miller", "Africa and Africans in the Making of the Atlantic World", "Scenes of Subjection Hartman", "Saltwater Slavery Smallwood", "Laboring Women Jennifer Morgan", "Unfinished Migrations Patterson Kelley", "The Practice of Diaspora Brent Hayes Edwards", "The Common Wind Julius Scott", "Black Marxism Cedric Robinson", "Silencing the Past Trouillot", "Avengers of the New World Laurent Dubois", "Freedom's Mirror Ada Ferrer", "Degrees of Freedom Rebecca Scott", "The Black Jacobins CLR James", "Capitalism and Slavery Eric Williams", "The Rise of African Slavery in the Americas Eltis", "Middle Passages James Campbell", "Dispossessed Lives Marisa Fuentes", "In the Wake Christina Sharpe", "Demonic Grounds Katherine McKittrick", "The Reaper's Garden Vincent Brown", "Freedom Dreams Robin Kelley", "Lose Your Mother Hartman", "The Belly of the World Hartman", "Tacky's Revolt Vincent Brown", "Specters of the Atlantic Ian Baucom"
6. Book-filter variants (`filter=type:book&search=…`) for 26 canonical titles
7. Follow-up targeted searches: Gilroy book, Scenes of Subjection book, Black Marxism book, "From Creole to African" article, "Unfinished Migrations" article, Rediker book, Reaper's Garden book, Lose Your Mother book, Common Wind book, Degrees of Freedom book
8. Individual work fetches: 16 finalist IDs (full select incl. abstract_inverted_index, locations)
9. Crossref spot-checks (`https://api.crossref.org/works/{doi}`): 10.1215/-12-2-1, 10.1257/aer.101.7.3221, 10.2307/3042577, 10.1353/mod.1994.0041, 10.1086/ahr.114.5.1231, 10.2307/524719, 10.4159/9780674043770, 10.2307/j.ctv1pncqd9, 10.1215/9780822373452, 10.9783/9780812206371, 10.1215/9780822387022, 10.4159/9780674034365, 10.9783/9780812293005, 10.1017/cbo9781139333672, 10.1017/cbo9780511800276
10. Full-text attempts: Harvard DASH bitstream for Nunn & Wantchekon → blocked by AWS WAF human-verification (abandoned, not bypassed); NBER WP w14783 PDF → **succeeded** (52 pp., via verbatim search-result URL)
11. Publisher descriptions via web search snippets (read.dukeupress.edu, hup.harvard.edu, retailer/review pages) for Sharpe, Dubois, Smallwood; full Crossref abstract for Ferrer

## Crossref mismatches

**None.** All 15 DOIs checked returned titles and years matching the OpenAlex records (8 title/year spot-checks reported in the task scope all matched; the remaining 7 were title/year-confirmed during abstract retrieval). Author-name rendering differs cosmetically in OpenAlex ("Irā Berlin," "BRENT HAYES EDWARDS," "Leonard" vs "Léonard Wantchekon") — noted per exemplar, not counted as mismatches.

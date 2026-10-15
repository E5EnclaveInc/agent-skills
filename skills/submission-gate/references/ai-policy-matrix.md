# Venue AI-policy matrix

Retrieved 2026-09-18 from official publisher policy pages. Verbatim quotes; nothing paraphrased into obligations. If a policy can't be located, it is marked NOT FOUND — never invented.

## Taylor & Francis (covers: Atlantic Studies)

- Source: https://taylorandfrancis.com/our-policies/ai-policy/ (retrieved 2026-09-18)
- **AI as author: prohibited.** "Generative AI tools must not be listed as an author because such tools are unable to assume responsibility for the submitted content or manage copyright and licensing agreements."
- **Disclosure: mandatory for any use.** "Authors must clearly acknowledge within the article or book any use of Generative AI tools through a statement that includes: the full name of the tool used (with version number), how it was used and the reason for use. For article submissions, a specific statement of AI usage disclosure must be included."
- Placement guidance (CASRAI reporting T&F policy, https://casrai.org/guides/taylor-francis-generative-ai-authorship-policy, retrieved 2026-09-18): Methods section where the journal has one, Acknowledgments where it does not. T&F's own page does not name a section for articles beyond "a specific statement of AI usage disclosure must be included."
- **Responsible uses supported:** idea generation and exploration; copyediting, language improvement and translations; literature classification; coding assistance. "Authors are responsible for ensuring that the content of their submissions meets the required standards of rigorous scientific and scholarly assessment, research and validation, and is created by the author."
- **Journal-level override:** "some journals may not allow use of Generative AI tools beyond language improvement, therefore authors are advised to review the 'Instructions for authors' on the journal homepage prior to submission." (No such Atlantic Studies-specific restriction was found in the RJAS style sheet as of 2026-09-18; the style sheet's model disclosure text covers conflicts of interest only.)
- **Prohibited / investigation-triggering:** "Authors should not submit manuscripts where Generative AI tools have been used in ways that replace core researcher and author responsibilities, for example: text or code generation without rigorous revision; synthetic data generation to substitute missing data without robust methodology; generation of any types of content which is inaccurate including abstracts or supplemental materials. These types of cases may be subject to editorial investigation."
- **Images:** "does not permit the use of Generative AI in the creation or manipulation of outputs of research or clinical testing." (Not applicable to text manuscripts; recorded for completeness.)
- **Reviewer/editor side:** editors and peer reviewers must not upload unpublished manuscripts into Generative AI tools. (Relevant to how WE handle manuscripts: never paste an unpublished manuscript into a third-party AI service. Our pipeline runs inside the author's own agent environment, not a public tool.)

## Sage (covers: The Review of Black Political Economy)

- Source: https://www.sagepub.com/journals/publication-ethics-policies/artificial-intelligence-policy (retrieved 2026-09-18)
- **Three tiers:** "assistive (and no longer requiring disclosure), generative (requiring disclosure), and prohibitive."
- **Assistive (no disclosure required):** "AI tools that make suggestions to improve or enhance your own work, such as tools to improve language, grammar, or structure, are considered assistive AI tools and do not require disclosure by authors or reviewers."
- **Generative (disclosure required):** "The primary or partial use of AI tools and/or LLMs that produce content such as references, text, images, or any other content that directly impacts the research methodology, analysis, results and/or conclusions must be disclosed upon submission so the editorial team can evaluate the content generated."
- **Placement:** "disclosure within the methods or acknowledgements" — state what tool was used, how it was used, and the rationale for use.
- **AI as author:** "AI bots such as ChatGPT should not be listed as an author on your submission." (per Sage journal submission guidelines)
- **Inappropriate use (editor may reject at any time, even post-acceptance):** "Generation of incorrect text or content; generation of data or submission using a series of prompts; ... plagiarism or inappropriate attribution to prior sources; fabricated references or falsified claims." Also: "While submissions will not be rejected solely because of the disclosed use of GenAI tools, if the editor becomes aware that GenAI was inappropriately used in the preparation of a submission without disclosure, the editor reserves the right to reject the submission at any time during the publishing process."
- **Accuracy duty:** "authors must take steps to verify the accuracy of all outputs and check the original sources."
- **Reviewer side:** "Reviewers suspecting the inappropriate or undisclosed use of generative AI in a submission should flag their concerns with the journal editor."

## Standing rules for this gate

1. The disclosure posture is **honest and specific**, never generic. Name the tool, how it was used, and why — per T&F's three required elements.
2. The disclosure statement is backed by a **provenance log** (`references/provenance-log-<slug>.md`): what the human author wrote vs. what agents drafted/revised. The log is the evidence behind the sentence.
3. Disclosure wording is the author's signed declaration — draft it, never finalize it unilaterally.
4. Never claim a venue's policy says something it doesn't. When in doubt, re-fetch the page.

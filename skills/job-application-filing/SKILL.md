---
name: job-application-filing
description: "File complete, truthful job applications with minimum hand-backs: verify a posting is live on the employer's own site, build a tailored resume and cover-letter package from the applicant's verified record, file through ATS portals (Workday, Greenhouse, Ashby, ADP, and others), and capture the confirmation. Use when an applicant commissions a filing run or approves a new target. Facts are never invented, and filing requires the applicant's approval."
license: MIT
metadata:
  version: 1.0.0
---

# Job Application Filing

## Purpose
File complete, truthful job applications for one applicant with minimum hand-backs: verify the posting, build a tailored package, file through the portal, capture the confirmation. Every fact on every form comes from the applicant's verified record — never invented.

## Setup
Before the first run, create the applicant's canonical-answers file from `references/canonical-answers.md` (a blank template in this export — fill it from the applicant's verified record and keep the filled copy private, never in a public repo). The template's fields are the questions agents otherwise re-ask on every application.

## Workflow
1. **Verify the posting first.** Confirm it is LIVE on the official employer/careers site (aggregator mirrors do not count — stale mirrors are the top cause of wasted filings). Confirm the location terms the applicant requires (e.g. strict-remote), still accepting applications, and an exact role match. Dead, closed, expired, or location-mismatched → skip, log it, no substitution. Never file a different role than the one approved.
2. **Read the canonical answers.** Never re-ask the applicant for anything in that file.
3. **Build the package** in a per-run workspace:
   - Tailored ATS résumé PDF from the applicant's base source.
   - One-page cover letter PDF in the applicant's voice (executive, high-signal, direct, never sycophantic, no flattery) — but ONLY if the form has a cover-letter field; never force one.
   - Never put working notes, deltas, or draft text in PDF sources — a "resume deltas" note leaking into a shipped résumé is a hard, common failure. Verify every PDF: text-extractable (`pdftotext`) and free of working-note strings. If your builder treats a bare `---` line as a document break, never let one appear in a source.
4. **File via a browser session.** Attach file grants FRESH on every browser session (successor sessions lose prior grants — always re-attach). Steer in stages: form fill → document attach → review → submit.
5. **Portal handling.**
   - Account required → create the account with a password the applicant can recover (their password manager or vault flow); account creation is never a barrier, but never store a password in the filing log or package files.
   - Email verification code → if the agent has authorized access to the applicant's mailbox, pull the code and relay it to the browser session, single-use for that step only. NEVER put codes in chat logs, memory, or files. If the code arrives by SMS, hand that one step to the applicant.
   - CAPTCHA on a job form → follow the applicant's standing instruction for CAPTCHAs (solve, or hand back); record which applied.
   - Application questions → answer from canonical answers only. AI-use disclosure line when the form asks (an approved framing belongs in the canonical answers). Compensation field → follow the applicant's documented compensation strategy (see references).
6. **Capture the confirmation.** Record the exact on-screen confirmation text, any reference number, and the portal's "My Applications" status. Screenshot the confirmation page. Log the filing in the run's status file the same session.
7. **Report after.** After-action form: filed (with confirmation) / skipped (with reason) / failed (with reason). One screen, TL;DR first.

## Output Contract
Per target: status (submitted / skipped / failed), exact confirmation text or skip/fail reason, package filenames built, whether a portal account was created, verification-code relays used. Durable state goes in the run workspace (status log + packages), never only in chat.

## Package quality bar (independent review)
- Every NEW package is graded by an independent reviewer (a second agent or a rubric script) BEFORE filing.
- Floor: overall COMPETITIVE or better, narrative ≥ 6/10, no dimension below 5/10. Failures get one rewrite pass against the reviewer's top-3 fixes, then re-graded.
- The four systematic fixes independent reviews keep finding: (1) the profile's first line states the career arc as intentional — what the applicant builds, across which domains; (2) every bullet carries a truthful scale marker (dollars, headcount, scope, timeframe) — metric density is the cheapest score lift; (3) first line = level + domain + scale proof for the 6-second skim; (4) JD-term coverage pass — mirror the posting's own phrases naturally in summary + bullets.
- Never weaken the rubric to pass a package. If the rubric is wrong, version it (v2) with a written reason — don't tune prompts per package.

## Operating Rules
1. **Check-first rule:** before asking the applicant ANY question, exhaust the sources already available — their saved notes and memory, the résumé source files, prior application filings, their public profile, the canonical-answers file. Ask only when the sources genuinely don't hold it.
2. Never invent facts, dates, metrics, employers, or credentials. Required personal-story/voice essays are ghostwritten in the applicant's voice, grounded ONLY in their verified record. Never invent experiences or a political/values stance. If a question demands a stance or experience genuinely absent from the record, park that single question and hand it back.
3. Location terms are strict. If the applicant's rule is remote-only, no hybrid, no office-proximity, no relocation-required — regardless of how good the fit looks.
4. Filing requires the applicant's approval: a standing pre-approval order with a named window, or explicit per-target approval. Staged (unapproved) targets are never auto-filed.
5. Don't touch items parked awaiting the applicant (manual takeover steps, a factual answer only they can give) unless they give fresh instruction. Essay questions are NOT in this category — ghostwrite them per rule 2, subject to any approval gate the applicant sets on essay text.
6. Cost defaults to $0. Never pay for a "priority application" upsell, premium job-board tier, or background-check add-on without the applicant's word.

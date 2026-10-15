# ATS Portal Notes (field-learned)

Platform behavior worth knowing before a filing run. Employers are not named:
the same platform behaves the same way for every tenant.

- **Workday:** the Education section may have NO graduation-year field — the degree dropdown plus school name suffices. Work Experience entries need start month/year and carry an "I currently work here" checkbox. Account creation is required before applying.
- **Greenhouse:** email verification via a short code sent to the applicant's mailbox — pull it through the authorized mailbox lane and relay it to the browser session (single-use, expires fast). Invisible reCAPTCHA may pass silently.
- **Ashby:** résumé-only forms exist (no cover-letter field) — do not force a cover letter; note it in the log.
- **ADP:** verification codes expire fast and sessions restart — re-pull a fresh code, don't reuse.
- **Rippling:** repeated résumé-upload rejection has been observed as a portal defect, not a user error — after documented attempts, log it and move on.
- **Hidden file inputs:** some custom forms hide the real file control behind a styled button — the résumé "Browse" box may need a manual attach. If three attempts fail, hand back for manual takeover with precise instructions (which box, what file), then resume on the applicant's go.
- **File grants:** every successor browser session loses prior file grants — re-attach files on every steer. This is the #1 avoidable stall.
- **Essay questions:** long-form answers (250–500 words) need the applicant's words — draft from their verified record where the standing rules allow ghostwriting, and honor any approval gate the applicant sets on essay text before submitting.

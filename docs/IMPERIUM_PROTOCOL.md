# Imperium Protocol — Public CV Governance

**Scope:** All tracked and generated CV repository artifacts, including CV sources, research status, data manifests, scripts, workflow outputs, job objects, and downloadable packages. The root `README.md` is a plain-language visitor entrypoint, not an Imperium-scored artifact. Files whose sole function is to point upstream to source evidence are source references, not newly evaluated evidence; preserve their links and authority.

**Source of governance:** [imperium-aeterna governance](https://github.com/pskeffington/imperium-aeterna/blob/main/docs/governance.md). This document restates safe, public-facing boundaries only; the private repository is not a runtime dependency.

## Mandatory rules

1. **Evidence before assertion.** Attribute each substantive claim to an auditable public source, retain its maturity/release state, and never upgrade an unverified or developing claim to an awarded credential, publication, appointment, or production deployment.
2. **Provenance and versioning.** Derived objects retain their source repository/path, source type, evidence confidence, method or generator version, and review status when those attributes exist. Unresolved claims remain unresolved.
3. **Human review.** Scores, classifications, role-fit assessments, and generated language are provisional aids for editorial review; they cannot make employment, admission, promotion, compensation, eligibility, military readiness, or other consequential person-level decisions.
4. **Protected attributes.** Do not use religion, ancestry, ethnicity, race, sex, gender identity, disability, age, political belief, property, wealth, or private belief to rate, rank, exclude, or recommend an individual.
5. **No modern status by historical analogy.** Historical rank, vocation, precedence, or title models are research representations, not credentials, institutional authority, merit determinations, or present-day hiring criteria.
6. **Public-release gate.** Maintain the existing allowlist, sanitization, claim validation, and private/public separation. Never import operational or personal data from a private governance repository into this public one.
7. **No automatic score publication.** Internal evidence scores and assessment metadata may inform private review but must not appear as definitive ratings in public CVs or downloadable artifacts.

## Explicit exceptions

- `README.md`: visitor-facing orientation and navigation; it links here but carries no Imperium scoring or source-object metadata requirement.
- **Upstream pointers:** link-only source references, citation indexes, and immutable pointers retain their external provenance without being rewritten, decorated, or treated as local scored content. If a file mixes upstream pointers with locally authored conclusions, the authored portion remains in scope.
- Generated PDFs and LaTeX outputs: governance attaches to the upstream generation and validation workflow; do not stamp these files with intrusive metadata or break their rendering.

## Required release checks

For any changed in-scope artifact, verify that public release guards pass; claims correspond to released sources; historical or model-derived ratings are not presented as credentials; and protected traits are not used for suitability scoring. A failure blocks publication pending human correction. See `scripts/check_imperium_protocol.py` for automated baseline checks. Static checks are a defense-in-depth gate, not proof of compliance.

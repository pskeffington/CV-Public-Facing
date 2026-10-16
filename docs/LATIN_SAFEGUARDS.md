<!-- lingua: la -->
# Norma linguae Latinae — Protocolum Imperii

**Regula principalis.** Omnia documenta auctoris propria, quae non sunt fontes ad alios fontes dirigentes, Latine conscribenda sunt. `README.md` in radice exceptum est, ut lectoribus pateat.

## Ambitus

- Documenta investigationis, interpretationes, descriptiones operum, relationes, aestimationes et commentarii ad publicum destinati Latine scribantur.
- Documenta quae solum ad fontes superiores ducunt (*feeder*, indices citationum, nexus immutabiles) servantur sine mutatione.
- Codex exsecutabilis, claves JSON, nomina variabilium, schema, URL, DOI, tituli proprii, citationes verbatim, mandata terminalia et syntaxis LaTeX non vertantur; ne officia vel compilationes corrumpantur.
- Summaria e fontibus externis desumpta, si propria sunt, Latine reddantur, dum verba fontium in citationibus integra manent.
- Documenta generata ex exemplaribus idem praeceptum sequantur; translatio in fonte generationis potius quam in effectu fiat.

## Fides et tutela

1. Quaeque affirmatio substantialis fontem publicum verificabilem habeat.
2. Status probationis, auctoritas fontis, versio methodi et dubitationes serventur.
3. Nulla classis historica aut nota computata iudicium de hominis dignitate, officio, mercede, admissione aut iure efficiat.
4. Proprietates personales tutas ne ad homines ordinandos adhibeantur.
5. Ante editionem, custodia publica, index fontium permissorum et recognitio humana necessaria sunt.

## Transitus et examinatio

Instrumentum `scripts/check_latin_safeguards.py` documenta nova Markdown, quae non sunt mera indicia ad fontes ducentia, examinat, et documenta vetera nondum translata recenset. Signum `<!-- lingua: la -->` tantum post translationem re vera absolutam adhibeatur. Instrumentum verba Anglica manifesto retenta quaerit, sed ipsum signum neque probationes vocabularii qualitatem Latinitatis per se confirmant. Documenta priora quae nondum translata sunt aperte enumerantur nec pro conformibus habentur. Ratio antiqua non statim rumpatur: res veteres per partes transferantur, servatis testibus compilationis atque integritate citationum.

**Exceptio:** `README.md` fundamentale, nexus ad fontes superiores, et textus machinis necessarii.

## Recognitio Latinitatis

Ad emendationem grammaticae et sermonis Latini normae philologicae repositorii [`trans-latin`](https://github.com/pskeffington/trans-latin) consulantur, praesertim rationes de [normalizatione](https://github.com/pskeffington/trans-latin/blob/main/docs/methodology/latin_normalization_policy.md) et [transcriptione](https://github.com/pskeffington/trans-latin/blob/main/docs/methodology/latin_transcription_policy.md). Scriptura Latina recens ad usum professionalem recognoscenda est, non quasi transcriptio testis antiqui tractanda. Emendationes grammaticae et stili ab homine diiudicandae sunt; programmata automatica solam probationem subsidialem praebent. Nomina propria, citationes, sigla technica et testimonia fontium ne tacite mutentur.

## Examen et transitus residuus

Exsequenda sunt `python3 scripts/test_latin_safeguards.py` et `python3 scripts/check_latin_safeguards.py`. Regulae nunc documenta Markdown scripta examinant; fontes LaTeX, campi narrationis JSON, commentarii codicis et textus ab instrumentis generatus adhuc translationem accuratam in fontibus suis requirunt. Quae restant in relatione probationis aperte indicentur. Exceptio nexuum ad fontes superiores manet, etiam si tituli citationum Anglice servantur.

<!-- lingua: la -->
# Norma linguae Latinae — Protocolum Imperii

**Regula principalis.** Omnia documenta auctoris propria, quae non sunt fontes ad alios fontes dirigentes, Latine conscribenda sunt. `README.md` in radice exceptum est, ut lectoribus pateat.

## Ambitus

- Documenta investigationis, interpretationes, descriptiones operum, relationes, aestimationes et commentarii ad publicum destinati Latine scribantur.
- Documenta quae solum ad fontes superiores ducunt (*feeder*, indices citationum, nexus immutabiles) servantur sine mutatione.
- Codex exsecutabilis, claves JSON, nomina variabilium, schema, URL, DOI, tituli proprii, citationes verbatim, mandata terminalia et syntax LaTeX non vertantur; ne officia vel compilationes corrumpantur.
- Summaria e fontibus externis desumpta, si propria sunt, Latine reddantur, dum verba fontium in citationibus integra manent.
- Documenta generata ex exemplaribus idem praeceptum sequantur; translatio in fonte generationis potius quam in effectu fiat.

## Fides et tutela

1. Quaeque affirmatio substantialis fontem publicum verificabilem habeat.
2. Status probationis, auctoritas fontis, versio methodi et dubitationes serventur.
3. Nulla classis historica aut nota computata iudicium de hominis dignitate, officio, mercede, admissione aut iure efficiat.
4. Proprietates personales tutas ne ad homines ordinandos adhibeantur.
5. Ante editionem, custodia publica, index fontium permissorum et recognitio humana necessaria sunt.

## Transitus et examinatio

Instrumentum `scripts/check_latin_safeguards.py` documenta nova Markdown non directa coercet, et documenta vetera nondum translata recenset. Signum `<!-- lingua: la -->` adhibetur tantum post translationem veram; signum ipsum translationem non probat. Ratio antiqua non statim rumpatur: res veteres per partes transferantur, servatis testibus compilationis atque integritate citationum.

**Exceptio:** `README.md` fundamentale, nexus ad fontes superiores, et textus machinis necessarii.

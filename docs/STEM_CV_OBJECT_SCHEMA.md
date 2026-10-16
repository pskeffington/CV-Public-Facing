<!-- lingua: la -->
# Schema rerum STEM in curriculo vitae

Hoc documentum structuram rerum a curatore curriculi vitae publico generatarum et regulas maturitatis eis applicandas describit.

## Fasciculus effectus

```text
data/stem_cv_objects.json
```

Hic fasciculus est effectus temporarius generationis, non fons principalis in historia versionum conservandus. `scripts/run_stem_cv_curator.py` eum ante probationem structurae iterum generat. Git eum ignorat, ne exemplaria antiqua fortuito in historiam committantur. Status operum diuturnus in `data/pipeline_repos.json` et fontibus publicis ibi indicatis servandus est.

## Structura summa

```json
{
  "schema": "stem-cv-curator/v0.3",
  "run": {},
  "repositories": [],
  "projects": [],
  "claims": [],
  "sections": [],
  "render_targets": [],
  "blocked_release_records": []
}
```

Instrumentum separatum `scripts/stem_presence.py` mensuram `stem_presence` ex scriptis, documentis `README`, relationibus de statu et excerptis publicis computare potest.

## Res Run

```json
{
  "run_time": "2026-08-21 00:00:00 UTC",
  "trigger": "local",
  "scanned_repositories": 10,
  "active_project_objects": 10
}
```

**Usus:** ostendit quomodo et quando curator res generaverit.

## RepositoryObject

```json
{
  "repo_full_name": "owner/repo",
  "repo_name": "repo",
  "owner": "owner",
  "url": "https://github.com/owner/repo",
  "visibility": "public",
  "default_branch": "main",
  "archived": false,
  "active_status": "active",
  "last_observed_at": "2026-08-21 00:00:00 UTC",
  "topics": [],
  "detected_domains": ["biomedical_data"]
}
```

**Usus:** repositorium GitHub pro fonte curatoris CV describit. Ante finem generationis visibilitas publica separatim verificanda est.

## ProjectObject

```json
{
  "project_id": "cart-trace",
  "title": "Longitudinal CAR T-cell care-trajectory reconstruction",
  "repository": {},
  "maturity": "synthetic_freeze",
  "cv_section": "biomedical_data",
  "public_summary": "Synthetic-first translational health data-science framework.",
  "near_term_needs": "Preserve the frozen capstone and separately govern extensions.",
  "source_surfaces": [],
  "keywords": ["biomedical_data"],
  "include_in_cv": true,
  "include_in_resume": true,
  "display_priority": 0,
  "curated": true,
  "public_release": "public"
}
```

**Usus:** testimonia repositorii in rem curriculo vitae aptam convertit, servatis tamen finibus maturitatis investigationis.

## ClaimObject

Assertiones a statu repositorii separantur; vias testimoniorum et signa permissionis divulgationis continent. Repositorium maturum per se assertiones clinicas, causales, operativas aut aliter non probatas non permittit.

## Valores maturitatis

Probatio structurae vocabula sequentia admittit. Valores graduum probationis a `scripts/maturity_policy.py` generantur; veteres ad convenientiam retroversam adhuc admittuntur.

| Maturitas | Usus |
|---|---|
| `synthetic_freeze` | Fasciculus investigationis syntheticae stabilitus et intra fines datos interne validatus |
| `pre_submission` | Scriptum ante submissionem emendatur, citationes et tabulae conferuntur, vel fasciculus caecus recognoscitur |
| `benchmark_freeze_pending` | Via probationis exsecutabilis exstat, sed comparatio nondum definitive comprobata |
| `pre_analysis` | Protocollum vel exemplar ante analysim empiricam validatam exstat |
| `source_validation` | Fontes et variabiles examinantur, vel reproductibilitas praeparatur |
| `active_research` | Investigatio activa finibus definitis, sed statu maturitatis specialiore carens |
| `submitted` | Scriptum submissum vel sub recognitione; propter convenientiam veterem retinetur |
| `publication_ready` | Res ad editionem parata; propter convenientiam veterem retinetur |
| `active_manuscript` | Scriptum scientificum in apparatu; propter convenientiam veterem retinetur |
| `active_scaffold` | Repositorium activum cum ratione operis clara; propter convenientiam veterem retinetur |
| `early_stage` | Methodus vel argumentum in prima evolutione; propter convenientiam veterem retinetur |
| `validation_gated` | Fortiores assertiones verificationem requirunt; propter convenientiam veterem retinetur |
| `intake` | Repositorium nuper repertum quod curam et recognitionem requirit |

Si valor ignotus est aut deest, probatio rerum generatarum deficit.

## Classes praesentiae STEM

| Classis | Intervallum | Usus |
|---|---:|---|
| `core_stem` | 75–100 | Argumenta fortia disciplinarum STEM, methodorum, reproductionis et progressus |
| `stem_adjacent` | 55–74 | Connexio STEM manifesta, sed probatio ad nucleum disciplinarum adhuc impar |
| `mixed_or_transitional` | 35–54 | Argumenta STEM partialia vel documenta adhuc rudia |
| `low_stem_presence` | 0–34 | Argumenta STEM tenuia vel declinatio magna a progressu disciplinarum |

## Partes curriculi vitae

| Clavis partis | Titulus adhibitus in instrumento |
|---|---|
| `publications` | Submitted and Publication-Oriented Work |
| `machine_learning` | Machine Learning and Reproducible Research Tools |
| `public_health` | Public Health, Infrastructure, and Environmental Evidence |
| `biomedical_data` | Biomedical Data and Signal/Imaging Methods |
| `methods` | Computational Methods and Validation |
| `archive_history` | Archive and Public-History Indexing |
| `intake` | Discovered Repository Intake |

Tituli Anglici in hac tabula sunt valores exsecutionis adhuc vigentes; non sunt versiones Latinae ad publicum conversae.

# First Test - Job CV Package Action

## Purpose

This note prepares the first manual test of the public-facing job CV package workflow.

The workflow builds the neutral public CV package and then creates a selected public-safe job package from the dropdown job object. It does not pull private job packets or private evidence.

## Workflow

```text
.github/workflows/build-public-research-status.yml
```

Displayed name:

```text
Build Public CV Package
```

## First test target

Use the neutral object first:

```text
neutral
```

Then test the Harvard Chan object:

```text
harvard-chan-director-data-analytics
```

## Manual test steps

1. Open the repository on GitHub.
2. Go to `Actions`.
3. Select `Build Public CV Package`.
4. Click `Run workflow`.
5. Choose `neutral` from the `Public-safe job object to package` dropdown.
6. Run the workflow from `main`.
7. Confirm the workflow completes.
8. Download artifacts.
9. Repeat with `harvard-chan-director-data-analytics`.

## Expected artifacts

For the neutral test:

```text
public-cv-package-neutral
selected-job-cv-package-neutral
generated-living-cv-sources-neutral
```

For the Harvard Chan test:

```text
public-cv-package-harvard-chan-director-data-analytics
selected-job-cv-package-harvard-chan-director-data-analytics
generated-living-cv-sources-harvard-chan-director-data-analytics
```

## Expected selected package contents

The selected job package artifact should include:

```text
dist/job_cv_packages/<selected-job>/Paul_A_Skeffington_Academic_CV_Public.pdf
dist/job_cv_packages/<selected-job>/Paul_A_Skeffington_One_Page_Profile_Public.pdf
dist/job_cv_packages/<selected-job>/Index_Safe_Public_Upload_CV.pdf
dist/job_cv_packages/<selected-job>/Paul_A_Skeffington_Research_Status_Public.pdf
dist/job_cv_packages/<selected-job>/PUBLIC_SAFE_JOB_BRIEF.md
dist/job_cv_packages/<selected-job>/manifest.json
```

## Preflight checks now enforced

The workflow runs:

```bash
make job-cv-package JOB_OBJECT="<selected>"
```

That target runs the normal public package build and validates:

- job object registry exists;
- selected job object exists;
- every job object has required fields;
- dropdown options match registry keys;
- first dropdown option matches the default job object;
- public package PDFs exist before selected packaging.

## Pass condition

A first test passes when:

- the workflow completes without error;
- all three artifacts are present;
- `selected-job-cv-package-*` includes `PUBLIC_SAFE_JOB_BRIEF.md` and `manifest.json`;
- no private job packet text appears in the public artifact;
- PDF outputs match the neutral public package unless a later tailored LaTeX variant is intentionally added.

## Boundary

This workflow packages public-safe outputs for a selected job object. It is not yet a full tailored-LaTeX renderer. The current test validates safe selection, package creation, artifact naming, manifest creation, and role-facing public-safe brief generation.

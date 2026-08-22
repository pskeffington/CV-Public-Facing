LATEXMK = latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -file-line-error
PYTHON = python3
CV_DIR = cv
RESEARCH_DIR = research
DOCUMENTS_DIR = documents
JOB_OBJECT ?= neutral

.PHONY: all stem-cv living-cv stem-presence-report stem-presence-check maturity-contract public-manifest-check public-visibility-check job-cv-object-check safety-surface-check citation-check doi-normalization-check reference-metadata-parser-check url-policy-check paper-evaluator-check paper-review-check stem-object-contract stem-report-contract preflight sanitize polish-public-cv align-public-positioning public-package job-cv-package academic-cv one-page-profile public-upload-cv research-status clean

all: public-package

stem-cv: public-manifest-check safety-surface-check maturity-contract
	$(PYTHON) scripts/run_stem_cv_curator.py

stem-presence-report: stem-cv safety-surface-check
	$(PYTHON) scripts/write_stem_presence_report.py

living-cv: stem-presence-report safety-surface-check

stem-presence-check:
	$(PYTHON) -m py_compile scripts/stem_presence.py scripts/stem_cv_curator.py scripts/run_stem_cv_curator.py scripts/maturity_policy.py scripts/check_maturity_contract.py scripts/check_stem_presence.py scripts/check_stem_object_contract.py scripts/write_stem_presence_report.py scripts/check_stem_presence_report.py scripts/stem_citation_verifier.py scripts/check_stem_citation_verifier.py scripts/check_doi_normalization.py scripts/check_reference_metadata_parsers.py scripts/check_url_policy.py scripts/stem_paper_evaluator.py scripts/check_stem_paper_evaluator.py scripts/check_stem_paper_evaluator_contract.py scripts/write_stem_paper_review.py scripts/check_stem_paper_review.py scripts/build_job_cv_package.py scripts/check_job_cv_objects.py scripts/public_release_guard.py scripts/check_public_release_guard.py scripts/check_public_manifest_contract.py scripts/check_public_allowlist_visibility.py scripts/polish_public_cv_sections.py scripts/align_public_cv_positioning.py
	$(PYTHON) scripts/check_stem_presence.py
	$(PYTHON) scripts/check_maturity_contract.py

maturity-contract:
	$(PYTHON) scripts/check_maturity_contract.py

public-manifest-check:
	$(PYTHON) scripts/check_public_manifest_contract.py

public-visibility-check: public-manifest-check
	$(PYTHON) scripts/check_public_allowlist_visibility.py

job-cv-object-check:
	$(PYTHON) scripts/check_job_cv_objects.py

safety-surface-check:
	$(PYTHON) scripts/check_public_release_guard.py

doi-normalization-check:
	$(PYTHON) scripts/check_doi_normalization.py

reference-metadata-parser-check:
	$(PYTHON) scripts/check_reference_metadata_parsers.py

url-policy-check:
	$(PYTHON) scripts/check_url_policy.py

citation-check: doi-normalization-check reference-metadata-parser-check url-policy-check
	$(PYTHON) scripts/check_stem_citation_verifier.py

paper-evaluator-check:
	$(PYTHON) scripts/check_stem_paper_evaluator.py
	$(PYTHON) scripts/check_stem_paper_evaluator_contract.py

paper-review-check:
	$(PYTHON) scripts/check_stem_paper_review.py

stem-object-contract: living-cv stem-presence-check public-manifest-check public-visibility-check job-cv-object-check safety-surface-check citation-check paper-evaluator-check paper-review-check maturity-contract
	$(PYTHON) scripts/check_stem_object_contract.py

stem-report-contract: stem-object-contract safety-surface-check
	$(PYTHON) scripts/check_stem_presence_report.py

preflight: stem-report-contract public-visibility-check safety-surface-check
	bash scripts/preflight_public_package.sh

sanitize: safety-surface-check
	bash scripts/check_public_sanitization.sh

polish-public-cv: preflight
	$(PYTHON) scripts/polish_public_cv_sections.py
	$(PYTHON) scripts/check_public_release_guard.py

align-public-positioning: polish-public-cv
	$(PYTHON) scripts/align_public_cv_positioning.py
	$(PYTHON) scripts/check_public_release_guard.py

public-package: safety-surface-check align-public-positioning academic-cv one-page-profile public-upload-cv research-status
	$(PYTHON) scripts/check_public_release_guard.py

job-cv-package: public-package job-cv-object-check safety-surface-check
	$(PYTHON) scripts/build_job_cv_package.py $(JOB_OBJECT)
	$(PYTHON) scripts/check_public_release_guard.py

# Every directly invokable public render target is preflight-gated. This prevents
# callers from bypassing manifest, visibility, release, and evidence-state checks
# by rendering a single PDF target outside the normal public-package path.
academic-cv: preflight
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) academic_cv_public.tex
	cp $(CV_DIR)/academic_cv_public.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_Academic_CV_Public.pdf

one-page-profile: preflight
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) one_page_profile_public.tex
	cp $(CV_DIR)/one_page_profile_public.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_One_Page_Profile_Public.pdf

public-upload-cv: preflight
	bash scripts/check_index_safe_upload.sh $(CV_DIR)/public_upload_cv.tex
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) public_upload_cv.tex
	cp $(CV_DIR)/public_upload_cv.pdf $(DOCUMENTS_DIR)/Index_Safe_Public_Upload_CV.pdf

research-status: preflight
	mkdir -p $(DOCUMENTS_DIR)
	cd $(RESEARCH_DIR) && $(LATEXMK) $(LATEXFLAGS) research_status.tex
	cp $(RESEARCH_DIR)/research_status.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf

clean:
	cd $(CV_DIR) && $(LATEXMK) -C academic_cv_public.tex one_page_profile_public.tex public_upload_cv.tex
	cd $(RESEARCH_DIR) && $(LATEXMK) -C research_status.tex
	rm -f $(RESEARCH_DIR)/stem_presence_report.md
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_Academic_CV_Public.pdf
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_One_Page_Profile_Public.pdf
	rm -f $(DOCUMENTS_DIR)/Index_Safe_Public_Upload_CV.pdf
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf
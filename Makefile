LATEXMK = latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -file-line-error
PYTHON = python3
CV_DIR = cv
RESEARCH_DIR = research
DOCUMENTS_DIR = documents

.PHONY: all stem-cv living-cv stem-presence-check stem-object-contract preflight sanitize public-package academic-cv one-page-profile public-upload-cv research-status clean

all: public-package

stem-cv:
	$(PYTHON) scripts/stem_cv_curator.py

living-cv: stem-cv

stem-presence-check:
	$(PYTHON) -m py_compile scripts/stem_presence.py scripts/stem_cv_curator.py scripts/check_stem_presence.py scripts/check_stem_object_contract.py
	$(PYTHON) scripts/check_stem_presence.py

stem-object-contract: living-cv stem-presence-check
	$(PYTHON) scripts/check_stem_object_contract.py

preflight: stem-object-contract
	bash scripts/preflight_public_package.sh

sanitize:
	bash scripts/check_public_sanitization.sh

public-package: preflight academic-cv one-page-profile public-upload-cv research-status

academic-cv:
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) academic_cv_public.tex
	cp $(CV_DIR)/academic_cv_public.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_Academic_CV_Public.pdf

one-page-profile:
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) one_page_profile_public.tex
	cp $(CV_DIR)/one_page_profile_public.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_One_Page_Profile_Public.pdf

public-upload-cv:
	bash scripts/check_index_safe_upload.sh $(CV_DIR)/public_upload_cv.tex
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) public_upload_cv.tex
	cp $(CV_DIR)/public_upload_cv.pdf $(DOCUMENTS_DIR)/Index_Safe_Public_Upload_CV.pdf

research-status:
	mkdir -p $(DOCUMENTS_DIR)
	cd $(RESEARCH_DIR) && $(LATEXMK) $(LATEXFLAGS) research_status.tex
	cp $(RESEARCH_DIR)/research_status.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf

clean:
	cd $(CV_DIR) && $(LATEXMK) -C academic_cv_public.tex one_page_profile_public.tex public_upload_cv.tex
	cd $(RESEARCH_DIR) && $(LATEXMK) -C research_status.tex
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_Academic_CV_Public.pdf
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_One_Page_Profile_Public.pdf
	rm -f $(DOCUMENTS_DIR)/Index_Safe_Public_Upload_CV.pdf
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf

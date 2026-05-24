LATEXMK = latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -file-line-error
CV_DIR = cv
RESEARCH_DIR = research
DOCUMENTS_DIR = documents

.PHONY: all public-package academic-cv one-page-profile research-status clean

all: public-package

public-package: academic-cv one-page-profile research-status

academic-cv:
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) academic_cv_public.tex
	cp $(CV_DIR)/academic_cv_public.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_Academic_CV_Public.pdf

one-page-profile:
	mkdir -p $(DOCUMENTS_DIR)
	cd $(CV_DIR) && $(LATEXMK) $(LATEXFLAGS) one_page_profile_public.tex
	cp $(CV_DIR)/one_page_profile_public.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_One_Page_Profile_Public.pdf

research-status:
	mkdir -p $(DOCUMENTS_DIR)
	cd $(RESEARCH_DIR) && $(LATEXMK) $(LATEXFLAGS) research_status.tex
	cp $(RESEARCH_DIR)/research_status.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf

clean:
	cd $(CV_DIR) && $(LATEXMK) -C academic_cv_public.tex one_page_profile_public.tex
	cd $(RESEARCH_DIR) && $(LATEXMK) -C research_status.tex
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_Academic_CV_Public.pdf
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_One_Page_Profile_Public.pdf
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf

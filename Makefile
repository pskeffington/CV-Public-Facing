LATEXMK = latexmk
LATEXFLAGS = -pdf -interaction=nonstopmode -halt-on-error -file-line-error
RESEARCH_DIR = research
DOCUMENTS_DIR = documents

.PHONY: all research-status clean

all: research-status

research-status:
	mkdir -p $(DOCUMENTS_DIR)
	cd $(RESEARCH_DIR) && $(LATEXMK) $(LATEXFLAGS) research_status.tex
	cp $(RESEARCH_DIR)/research_status.pdf $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf

clean:
	cd $(RESEARCH_DIR) && $(LATEXMK) -C research_status.tex
	rm -f $(DOCUMENTS_DIR)/Paul_A_Skeffington_Research_Status_Public.pdf

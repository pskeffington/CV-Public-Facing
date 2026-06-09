#!/usr/bin/env python3
"""Apply final public-CV polish after object generation.

The STEM CV curator writes object-derived files for validation and ledgers. This
step keeps the rendered public CV package aligned with a Dartmouth-style CV
structure by replacing the visible research-experience section with concise,
public-facing entries.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CV_PROJECTS_PATH = ROOT / "cv" / "current_projects_public.tex"

POLISHED_RESEARCH_EXPERIENCE = r"""\section*{Research Experience}
\begin{samepage}
\cvrole{Family economics, financial literacy, and fertility}{Under peer review}
\cvplace{Longitudinal NLSY79 manuscript project}
\begin{itemize}[leftmargin=2.0em,labelsep=0.55em,topsep=1pt,itemsep=0pt,parsep=0pt]
    \item Analyzed family, fertility, and economic outcomes with reproducible modeling and table review to support source-to-claim manuscript development.
\end{itemize}
\end{samepage}

\begin{samepage}
\cvrole{Rural and global health systems}{In preparation}
\cvplace{Public-health infrastructure and WASH research}
\begin{itemize}[leftmargin=2.0em,labelsep=0.55em,topsep=1pt,itemsep=0pt,parsep=0pt]
    \item Organized WASH, water and wastewater infrastructure, terrain, access, and environmental-health evidence to support rural and global health risk assessment.
\end{itemize}
\end{samepage}

\begin{samepage}
\cvrole{Maternal, child, reproductive, and life-course health}{Developing}
\cvplace{Population-health research direction}
\begin{itemize}[leftmargin=2.0em,labelsep=0.55em,topsep=1pt,itemsep=0pt,parsep=0pt]
    \item Connected family economics, fertility, household context, and reproductive outcomes to clarify maternal-child and life-course research questions.
\end{itemize}
\end{samepage}

\begin{samepage}
\cvrole{Cancer outcomes and end-of-life care}{Developing}
\cvplace{Open-data outcomes and care-quality methods}
\begin{itemize}[leftmargin=2.0em,labelsep=0.55em,topsep=1pt,itemsep=0pt,parsep=0pt]
    \item Developed cancer end-of-life typology concepts around place-of-death patterns and care-quality variation to guide reproducible study design.
\end{itemize}
\end{samepage}

\begin{samepage}
\cvrole{Biomedical data science methods}{Developing}
\cvplace{Signal, imaging, and machine-learning methods}
\begin{itemize}[leftmargin=2.0em,labelsep=0.55em,topsep=1pt,itemsep=0pt,parsep=0pt]
    \item Built ECG signal-quality, PET imaging robustness, and responsible machine-learning evaluation scaffolds to support public-data biomedical methods work.
\end{itemize}
\end{samepage}

\begin{samepage}
\cvrole{Public-history and archival indexing}{Developing}
\cvplace{Catholic archive and material-culture indexing}
\begin{itemize}[leftmargin=2.0em,labelsep=0.55em,topsep=1pt,itemsep=0pt,parsep=0pt]
    \item Applied transcription, entity modeling, provenance notes, and uncertainty flags to improve public-history archive structure and interpretability.
\end{itemize}
\end{samepage}
"""


def main() -> int:
    CV_PROJECTS_PATH.write_text(POLISHED_RESEARCH_EXPERIENCE.rstrip() + "\n", encoding="utf-8")
    print("Public CV sections polished for final render.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

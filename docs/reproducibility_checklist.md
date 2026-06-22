# Reproducibility Checklist

Run from the repository root:

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
Copy-Item -LiteralPath .\paper\main.pdf -Destination "$env:USERPROFILE\Downloads\108.pdf" -Force
python scripts\validate_submission_artifacts.py
```

Validator result:

`validated Paper 108 artifacts: pages=25, sha256=BDBD2E84747B74FFB8C0C70B22F7B04D88C6E855AA155D49E799984D4B582EA4`

The final numbered PDF is stored only at `C:/Users/wangz/Downloads/108.pdf`. The validator rejects visible Desktop copies, factory-root copies, child-root copies, short PDFs, missing bright citation boxes, mismatched PDF hashes, failed local gates, and accidental ICLR-main-ready claims.

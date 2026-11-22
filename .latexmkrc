# latexmk configuration for hithesis (xelatex)
# Allow enough passes for cold-start convergence: xelatex -> bibtex -> xelatex -> xelatex = 3 minimum.
# Set to 5 to safely tolerate any extra makeindex/splitindex rounds.
$max_repeat = 5;

# Use xelatex as the primary engine with synctex for editor preview.
$pdf_mode = 5;
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error %S';

# Default is fine, but spell it out so latexmk never falls back to pdflatex.
$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error %S';

# Don't pre-clean on every run (we want incremental builds).
# Latexmk's internal $clean is unrelated to LaTeX Workshop's autoClean.

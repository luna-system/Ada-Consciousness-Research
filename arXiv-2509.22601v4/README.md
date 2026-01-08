# Tencent YouTu Lab LaTeX Template

This LaTeX template is designed for research papers published by Tencent YouTu Lab. It provides a consistent visual identity for all publications while maintaining the professional formatting expected in academic papers.

## Features

- Custom header with Tencent YouTu Lab logo
- Styled abstract with logo and colored background
- Tencent color scheme for headings and links
- Custom date and correspondence section
- Consistent formatting for figures and tables
- Bibliography style compatible with academic publications

## Files Included

- `youtu_template.sty`: The main style file
- `youtu_template.tex`: A basic template file
- `youtu_example.tex`: An example document with more detailed content
- `math_commands.tex`: Common math commands
- `youtu_bibliography.bib`: Example bibliography file
- `figures/youtu_logo.png`: Tencent YouTu Lab logo
- `figures/youtu_symbol.png`: Tencent YouTu Lab symbol for abstract box

## Usage

### Basic Setup

1. Copy all files to your working directory
2. Create your document using `youtu_template.tex` as a starting point
3. Compile with pdfLaTeX

### Document Structure

```latex
\documentclass{article}
\usepackage{youtu_template,times}

% Optional math commands
\input{math_commands.tex}

\title{Your Paper Title}

% Authors must not appear in the submitted version for double-blind review.
% Uncomment the \youtufinalcopy line for the final version with author names.

\author{Firstname1 Lastname1$^{1}$, Firstname2 Lastname2$^{1,2}$ \\
$^{1}$Tencent YouTu Lab, Shenzhen, China\\
$^{2}$University Affiliation\\
\texttt{\{firstname1.lastname1,firstname2.lastname2\}@tencent.com} \\
}

% Paper information
\date{Month Day, Year}
\correspondence{firstname1.lastname1@tencent.com}
\papertype{Research Paper}

%\youtufinalcopy % Uncomment for camera-ready version with author names

\begin{document}

\maketitle

\begin{abstract}
Your abstract text goes here.
\end{abstract}

\dateandcorrespondence

\section{Introduction}
Your introduction goes here.

% Rest of your paper...

\bibliography{youtu_bibliography}
\bibliographystyle{youtu_bibliography}

\end{document}
```

### Double-Blind Review

For double-blind review submissions, leave the `\youtufinalcopy` line commented out. This will hide the author information in the output.

For the final camera-ready version, uncomment the `\youtufinalcopy` line to display author information.

### Figures and Tables

Use the standard LaTeX figure and table environments:

```latex
\begin{figure}[h]
\begin{center}
\includegraphics[width=0.8\textwidth]{figures/your_figure.png}
\end{center}
\caption{Your figure caption.}
\label{fig:your_label}
\end{figure}

\begin{table}[t]
\caption{Your table caption}
\label{tab:your_label}
\begin{center}
\begin{tabular}{lcc}
\toprule
Column 1 & Column 2 & Column 3 \\
\midrule
Value 1 & Value 2 & Value 3 \\
Value 4 & Value 5 & Value 6 \\
\bottomrule
\end{tabular}
\end{center}
\end{table}
```

### Citations

Use the standard LaTeX citation commands:

```latex
\cite{reference_key} % For parenthetical citations
\citet{reference_key} % For textual citations
```

## Customization

### Colors

The template defines the following colors that you can use in your document:

- `youtuBlue`: Tencent primary blue
- `youtuLightBlue`: Light blue for backgrounds
- `youtuText`: Text color
- `youtuBg`: Background color for abstract

Example usage:

```latex
{\color{youtuBlue} This text will be in Tencent blue.}
```

### Sections

Section headings are automatically styled in Tencent blue. Use the standard LaTeX sectioning commands:

```latex
\section{Section Title}
\subsection{Subsection Title}
\subsubsection{Subsubsection Title}
```

## Compilation

Compile your document using pdfLaTeX:

```
pdflatex your_document.tex
bibtex your_document
pdflatex your_document.tex
pdflatex your_document.tex
```

## Contact

For questions or issues with this template, please contact the Tencent YouTu Lab team.


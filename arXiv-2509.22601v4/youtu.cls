%%%% Tencent YouTu Lab LaTeX Template
%%%% Based on ICLR 2025 Conference Template
%%%% Modified to incorporate design elements from Meta AI, Bytedance Seed, Tencent AI Lab, and Huggingface papers



\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{youtu} % 假设你用的是 \documentclass{youtu}
\LoadClassWithOptions{article}

\RequirePackage{etoolbox} % 为 \ifdefempty
\RequirePackage{sourcesanspro}
\newcommand\contributionlist{} % <--- 新增，防止报错
\RequirePackage[margin=1in]{geometry}
\RequirePackage{placeins}
\RequirePackage{setspace}

% Tables %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{nicematrix}

% Colorful stuff %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Load required packages
\RequirePackage{graphicx}
\RequirePackage{hyperref}
\RequirePackage{url}
\RequirePackage{booktabs}
\RequirePackage{amsfonts}
\RequirePackage{nicefrac}
\RequirePackage{microtype}
\RequirePackage{xcolor}
\RequirePackage[most]{tcolorbox}
\RequirePackage{setspace}
\RequirePackage{placeins}


% Define Tencent fonts
\pdfmapline{+TencentSans-W7 < TencentSans-W7.pfb <T1-WGL4.enc}
\newcommand\tencentsanswseven[1]{{\usefont{T1}{TencentSans-W7}{m}{n} #1 }}


% Define Tencent YouTu Lab colors
\definecolor{youtuBlue}{RGB}{0, 82, 217} % Tencent primary blue
% \definecolor{youtuLightBlue}{HTML}{E5EDFF} % Light blue for abstract background
\definecolor{youtuLightBlue}{RGB}{235, 245, 255} % Light blue for abstract background
\definecolor{youtuText}{HTML}{1C2B33} % Text color
\definecolor{youtuBg}{HTML}{F1F4F7} % Background color for abstract


% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=youtuBlue,
    citecolor=youtuBlue,
    urlcolor=youtuBlue,
    pdfauthor={Tencent Youtu Lab},
    pdftitle={Tencent Youtu Lab Research Paper},
    pdfsubject={Artificial Intelligence},
    pdfkeywords={Tencent, Youtu Lab, AI, Research},
}

% Title formatting
\renewcommand{\title}[1]{\newcommand{\titlelist}{\begin{center}{\LARGE\bf #1}\end{center}}}

% Author list handling
\renewcommand\addtolist[5][]{
  \begingroup
    \if\relax#3\relax\def\sep{}\else\def\sep{#5}\fi
    \let\protect\@unexpandable@protect 
    \xdef#3{\expandafter{#3}\sep #4[#1]{#2}}%
  \endgroup
}
\RequirePackage{graphicx}

\newcommand\authorlist{}
\newcommand\authorformat[2][]{\begin{center}{{\tencentsanswseven{#2$^{#1}$}}}\end{center}}
\renewcommand\author[2][]{\addtolist[#1]{#2}{\authorlist}{\authorformat}{, }}
\newcommand{\footremember}[2]{%
   \footnote{#2}
    \newcounter{#1}
    \setcounter{#1}{\value{footnote}}%
}
\newcommand{\footrecall}[1]{%
    \footnotemark[\value{#1}]%
} 
\newcommand\affiliationlist{}
\newcommand\affiliationformat[2][]{\begin{center}{\small{\tencentsanswseven{$^{#1}$#2}}}\end{center}}
\newcommand\affiliation[2][]{\addtolist[#1]{#2}{\affiliationlist}{\affiliationformat}{, }}

\newcommand\metadatalist{}
\newcommand\metadataformat[2][]{{\small {\bf #1:} #2}}
\newcommand\metadata[2][]{\addtolist[#1]{#2}{\metadatalist}{\metadataformat}{\par}}

% Date and correspondence
\renewcommand\date[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/icons8-date-96.png}} Date]{#1}}
\newcommand\sourcecode[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/github.png}} Code]{\url{#1}}}
\newcommand\project[1]{\metadata[{\raisebox{-0.1em}{\includegraphics[height=1em]{figures/icons8-website-100.png}}} Project]{\url{#1}}}
\newcommand\demo[1]{\metadata[\raisebox{-0.2em}{\includegraphics[height=1em]{figures/icons8-robot-100.png}} Demo]{\url{#1}}}
\newcommand{\data}[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/huggingface-color.png}} Data]{\url{#1}}}
\newcommand{\model}[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/huggingface-color.png}} Checkpoints]{\url{#1}}}
\newcommand\correspondence[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/icons8-email-96.png}} Correspondence]{\texttt #1}}
\newcommand\papertype[1]{\metadata[Type]{#1}}

% Abstract handling
\renewcommand{\abstract}[1]{\newcommand{\abstractlist}{{\color{youtuText} #1}}}

% Date and correspondence section
\newcommand{\dateandcorrespondence}{
  \vspace{0.2cm}
  \noindent\rule{\textwidth}{0.5pt}
  \vspace{0.1cm}
  \ifdefempty{\metadatalist}{}{\metadatalist\par}
  \vspace{0.1cm}
  \noindent\rule{\textwidth}{0.5pt}
  \vspace{0.3cm}
}

% Command to enable author names in final copy
\newcommand{\youtufinalcopy}{\def\@youtufinalcopy{}}


% \newcommand{\mymaketitle}{%
%   \tcbset{enhanced,frame hidden}
%   % \tcbset{colframe=youtuBlue,boxrule=2pt}
%   \tcbset{left=0.5cm}
%   \tcbset{right=0.5cm}
%   \tcbset{top=0.5cm}
%   \tcbset{bottom=0.5cm}
%   \tcbset{arc=10pt}
%   \tcbset{colback=youtuLightBlue}
%   \tcbset{before skip=0pt}
%   \tcbset{grow to left by=1.5pt}
%   \tcbset{grow to right by=1.5pt}
%   \begin{tcolorbox}
%     \setlength{\parindent}{0cm}
%     \setlength{\parskip}{0.5cm}
%     {
%       \setlength{\parskip}{0cm}
%       \raggedright
%       %
%       {
%         \setstretch{1.618}
%         \titlelist\par
%       }
%       \vskip 0.2cm
%       %
%       \authorlist\par
%       \vskip 0.2cm
%       %
%       \affiliationlist\par
%       %
%       \contributionlist\par
%     }
%     %
%     \abstractlist\par
%     %
%     \vskip 0.5cm
%     %
%     {
%       \setlength{\parskip}{0cm}
%       \ifdefempty{\metadatalist}{\vspace*{0.65cm}}{\metadatalist\par}
%     }
%   \end{tcolorbox}
%   \tcbset{reset}
%   \FloatBarrier
% }

\newcommand{\mymaketitle}{%
  \setlength{\parindent}{0cm}
  \setlength{\parskip}{0.5cm}
  {
    \setlength{\parskip}{0cm}
    \raggedright
    {
      \setstretch{1.618}
      \titlelist\par
    }
    \vskip 0.2cm
    \authorlist\par
    \vskip 0.2cm
    \affiliationlist\par
    \contributionlist\par
  }
  % 只包 abstract 和 metadatalist
  \begin{tcolorbox}[colback=youtuLightBlue, left=0.5cm, right=0.5cm, top=0.5cm, bottom=0.5cm, arc=10pt, enhanced, frame hidden, before skip=0pt, grow to left by=1.5pt, grow to right by=1.5pt]
    \abstractlist\par
    \vskip 0.5cm
    \ifdefempty{\metadatalist}{}{\metadatalist\par}
  \end{tcolorbox}
  \FloatBarrier
}



% Redefine maketitle command
\if@twocolumn%
\renewcommand{\maketitle}{
\twocolumn[%
  \mymaketitle
  \vskip 0.38cm
]
}%
\else%
\renewcommand{\maketitle}{
  \mymaketitle
}%
\fi
\setlength{\headheight}{\baselineskip}
% Section formatting
\renewcommand{\section}{\@startsection{section}{1}{\z@}%
                       {-3.5ex \@plus -1ex \@minus -.2ex}%
                       {2.3ex \@plus.2ex}%
                       {\normalfont\Large\bfseries\color{youtuBlue}\tencentsanswseven}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
                          {-3.25ex\@plus -1ex \@minus -.2ex}%
                          {1.5ex \@plus .2ex}%
                          {\normalfont\large\bfseries\color{youtuBlue}\tencentsanswseven}}
\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{\z@}%
                             {-3.25ex\@plus -1ex \@minus -.2ex}%
                             {1.5ex \@plus .2ex}%
                             {\normalfont\normalsize\bfseries\color{youtuBlue}\tencentsanswseven}}

% Caption formatting
\RequirePackage[font={small}]{caption}
\captionsetup[figure]{labelfont={bf},name={Figure},labelsep=period}
\captionsetup[table]{labelfont={bf},name={Table},labelsep=period}

% Bibliography style
\bibliographystyle{unsrtnat}
% \bibliographystyle{unsrt}

% Header with Tencent YouTu Lab logo
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
% \fancyhead[L]{\includegraphics[height=\baselineskip]{figures/youtulogo.jpg}{\color{youtuBlue}\bf Tencent YouTu Lab}}
\fancyhead[L]{\includegraphics[height=2\baselineskip]{figures/tencent_youtu_large.png}}
\fancyhead[R]{\tencentsanswseven{SPEAR}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0pt}

% End of package
\endinput


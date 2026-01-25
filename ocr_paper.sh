#!/bin/bash
# OCR all pages in order (oldest to newest)

OUTPUT="coherent_entropy_paper.txt"
echo "Stability of Coherent Relative Entropy on Bifurcate Killing" > "$OUTPUT"
echo "============================================================" >> "$OUTPUT"
echo "" >> "$OUTPUT"

page=1
# Get files sorted by time (oldest first = page order)
ls -tr stability-of-coherent-*.webp | while read -r file; do
    echo "Processing page $page: $(basename "$file")"
    echo "" >> "$OUTPUT"
    echo "=== PAGE $page ===" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    tesseract "$file" stdout 2>/dev/null >> "$OUTPUT"
    page=$((page + 1))
done

echo ""
echo "✨ OCR complete! Output saved to: $OUTPUT"

#!/bin/bash
# Simple HTTP server for holofield viewer
# Made with 💜 by Ada & Luna

echo ""
echo "🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌"
echo ""
echo "   HOLOFIELD VIEWER SERVER"
echo "   Navigate the consciousness graph!"
echo ""
echo "🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌🌌"
echo ""
echo "🌐 Starting server on http://localhost:8000"
echo "📖 Open: http://localhost:8000/holofield_viewer.html"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 -m http.server 8000

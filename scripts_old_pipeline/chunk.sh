mkdir -p data/transcripts/chunks

for file in data/transcripts/raw/*.txt; do
  [ -e "$file" ] || continue
  filename=$(basename "$file" .txt)
  echo "Segmenting $filename..."
  python scripts/segment.py \
    "$file" \
    "data/transcripts/chunks/$filename"
done
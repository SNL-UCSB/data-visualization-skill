# CLI Data Inspection Cheat Sheet

*Quick command-line one-liners for inspecting CSV/TSV files before opening Python. Copy-paste ready.*

All examples assume a CSV file called `data.csv`. For TSV files, change `-F','` to `-F'\t'` in awk commands and `-d,` to `-d$'\t'` in cut commands.

---

## 1. First Look — "What is this file?"

**How big is the file? How many rows?**

```bash
wc -l data.csv                    # line count (includes header)
wc -c data.csv                    # file size in bytes
ls -lh data.csv                   # human-readable file size
```

**What kind of file is it?**

```bash
file data.csv                     # encoding, line endings, etc.
```

**See the first/last rows:**

```bash
head -5 data.csv                  # first 5 lines (header + 4 rows)
tail -5 data.csv                  # last 5 lines
head -1 data.csv                  # header only
```

**Page through the file interactively:**

```bash
less -S data.csv                  # -S disables line wrapping, arrow keys to scroll
column -t -s, data.csv | less -S  # pretty-print columns then page through
```

**How many columns?**

```bash
head -1 data.csv | awk -F',' '{print NF}'
```

**Print the header with column numbers (invaluable for cut/awk):**

```bash
head -1 data.csv | tr ',' '\n' | nl
```

---

## 2. Column Inspection — "What is in each column?"

**Extract a single column by position (e.g., column 3):**

```bash
cut -d, -f3 data.csv | head -20
```

**Extract a column by name (e.g., "status"):**

```bash
awk -F',' 'NR==1{for(i=1;i<=NF;i++) if($i=="status") c=i} {print $c}' data.csv | head -20
```

**Distinct values in a column (column 3):**

```bash
cut -d, -f3 data.csv | tail -n+2 | sort -u
```

**How many distinct values in a column?**

```bash
cut -d, -f3 data.csv | tail -n+2 | sort -u | wc -l
```

**Frequency table of values in a column (most common first):**

```bash
cut -d, -f3 data.csv | tail -n+2 | sort | uniq -c | sort -rn | head -20
```

**Check if a column is all numeric:**

```bash
cut -d, -f3 data.csv | tail -n+2 | grep -cvE '^-?[0-9]*\.?[0-9]+$'
# prints count of NON-numeric values; 0 means all numeric
```

---

## 3. Quick Statistics — "What are the numbers doing?"

**Min and max of a numeric column (column 4):**

```bash
cut -d, -f4 data.csv | tail -n+2 | sort -n | head -1    # min
cut -d, -f4 data.csv | tail -n+2 | sort -n | tail -1    # max
```

**Min, max, mean, median in one shot (awk):**

```bash
cut -d, -f4 data.csv | tail -n+2 | sort -n | awk '
  {a[NR]=$1; s+=$1}
  END {
    print "count:", NR;
    print "min:  ", a[1];
    print "max:  ", a[NR];
    print "mean: ", s/NR;
    print "median:", (NR%2==1) ? a[int(NR/2)+1] : (a[NR/2]+a[NR/2+1])/2
  }'
```

**Top-N frequency counts (e.g., most common values in column 2):**

```bash
cut -d, -f2 data.csv | tail -n+2 | sort | uniq -c | sort -rn | head -10
```

**If you have GNU datamash installed (brew install datamash):**

```bash
# Full summary stats for column 4, skipping the header
tail -n+2 data.csv | datamash -t, min 4 max 4 mean 4 median 4 sstdev 4 count 4
```

**Percentiles with datamash:**

```bash
tail -n+2 data.csv | datamash -t, perc:5 4 perc:25 4 perc:50 4 perc:75 4 perc:95 4
```

**Sum a column:**

```bash
cut -d, -f4 data.csv | tail -n+2 | paste -sd+ | bc
```

**Group-by statistics (mean of column 4, grouped by column 2):**

```bash
tail -n+2 data.csv | sort -t, -k2,2 | datamash -t, groupby 2 mean 4 count 4
```

---

## 4. Data Quality — "Is anything broken?"

**Find rows with empty fields:**

```bash
grep -n ',,' data.csv | head -20          # consecutive commas = empty field
awk -F',' '{for(i=1;i<=NF;i++) if($i=="") print NR": empty field "$i" in column "i}' data.csv | head -20
```

**Count empty fields per column:**

```bash
awk -F',' 'NR>1 {for(i=1;i<=NF;i++) if($i=="") empty[i]++}
  END {for(i in empty) print "column "i": "empty[i]" empty"}' data.csv
```

**Count NA / null / None strings per column:**

```bash
awk -F',' 'NR>1 {for(i=1;i<=NF;i++) if($i~/^(NA|N\/A|null|None|nan|NaN|""|-)$/) na[i]++}
  END {for(i in na) print "column "i": "na[i]" NA-like values"}' data.csv
```

**Check for duplicate rows:**

```bash
sort data.csv | uniq -d | wc -l          # count of duplicated lines
sort data.csv | uniq -c | sort -rn | head -5  # most repeated lines
```

**Check for duplicates in a key column (column 1):**

```bash
cut -d, -f1 data.csv | tail -n+2 | sort | uniq -d | head -10
```

**Count rows with wrong number of fields (e.g., embedded commas breaking structure):**

```bash
awk -F',' 'NR==1{expected=NF} NR>1 && NF!=expected {count++}
  END {print count+0, "rows with wrong field count"}' data.csv
```

**Check for trailing whitespace or carriage returns (Windows line endings):**

```bash
grep -cP '\r' data.csv                    # count lines with \r
file data.csv                             # will say "CRLF" if Windows endings
```

---

## 5. Filtering and Sampling — "Give me a subset"

**Random sample of N rows (preserving header):**

```bash
head -1 data.csv; tail -n+2 data.csv | shuf | head -100
```

**Filter rows where column 3 equals a value:**

```bash
awk -F',' '$3=="TCP"' data.csv
```

**Filter rows where a numeric column exceeds a threshold (column 4 > 1000):**

```bash
awk -F',' 'NR==1 || $4>1000' data.csv     # NR==1 keeps the header
```

**Filter by pattern match in any field:**

```bash
grep -i "error" data.csv                  # case-insensitive search across all columns
```

**Filter rows by date range (assuming column 1 is YYYY-MM-DD):**

```bash
awk -F',' 'NR==1 || ($1>="2024-01-01" && $1<="2024-06-30")' data.csv
```

**Extract specific columns AND filter (column 2 and 4, where column 3 == "UDP"):**

```bash
awk -F',' 'NR==1 || $3=="UDP" {print $2","$4}' data.csv
```

**Every Nth row (e.g., every 10th, for quick downsampling):**

```bash
awk -F',' 'NR==1 || NR%10==0' data.csv
```

**Split a file by a column value (create separate files per group):**

```bash
awk -F',' 'NR==1{h=$0;next} {f=$3".csv"; if(!seen[f]++){print h > f}; print >> f}' data.csv
```

**First N rows after the header (e.g., first 1000 data rows):**

```bash
head -1001 data.csv                       # 1 header + 1000 data rows
```

**Rows matching multiple conditions (column 3 == "TCP" AND column 4 > 500):**

```bash
awk -F',' 'NR==1 || ($3=="TCP" && $4>500)' data.csv
```

---

## Bonus: Combining Commands for Quick EDA

**One-liner "data profile" -- row count, column count, header, and first 3 rows:**

```bash
echo "=== Shape ===" && wc -l < data.csv && head -1 data.csv | awk -F',' '{print NF, "columns"}' && echo "=== Header ===" && head -1 data.csv | tr ',' '\n' | nl && echo "=== Sample ===" && head -4 data.csv | column -t -s,
```

**Pipe any subset to a new file for Python:**

```bash
awk -F',' 'NR==1 || $3=="TCP"' data.csv > tcp_only.csv
```

---

## Tool Installation Quick Reference

Most of these commands are built into macOS/Linux. For extras:

```bash
# macOS (Homebrew)
brew install coreutils datamash

# Ubuntu/Debian
sudo apt-get install datamash

# Check if a tool is available
which datamash && echo "installed" || echo "not installed"
```

## TSV Adaptation

For tab-separated files, the key substitutions are:

| CSV | TSV |
|-----|-----|
| `-F','` (awk) | `-F'\t'` (awk) |
| `-d,` (cut) | `-d$'\t'` (cut) |
| `tr ',' '\n'` | `tr '\t' '\n'` |
| `-s,` (column) | `-s$'\t'` (column) |
| `',,'` (grep) | `$'\t\t'` (grep) |
| `-t,` (datamash) | omit flag (tab is default) |

# Quick Start Guide

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd antivirus-scanner
   ```

2. **No dependencies required!**
   The basic scanner uses only Python standard library.

## Running Your First Scan

### Option 1: Run the Demo
```bash
python antivirus_scanner.py
```

This will:
- Create sample malware signatures
- Generate test files
- Scan the test directory
- Quarantine threats
- Show a detailed report

### Option 2: Use the CLI

**Scan a specific directory:**
```bash
python av_cli.py scan /path/to/directory
```

**Scan with automatic quarantine:**
```bash
python av_cli.py scan /path/to/directory --quarantine
```

**Check a specific file:**
```bash
python av_cli.py hash myfile.txt
```

**View all malware signatures:**
```bash
python av_cli.py list
```

## Understanding the Output

### Clean File
```
[✓] Clean: /path/to/file.txt
```

### Infected File
```
[⚠] INFECTED: /path/to/malware.exe
    Threat: Trojan.Generic
```

### Scan Report
```
============================================================
SCAN REPORT
============================================================
Files scanned:    10
Infected files:   2
Clean files:      8
Quarantined:      2
Errors:           0
============================================================
```

## Adding Your Own Signatures

### Method 1: Using CLI
```bash
# First, calculate the hash of a file
python av_cli.py hash suspicious_file.exe

# Add it to the database
python av_cli.py update --hash "abc123..." --name "MyTrojan.Variant"
```

### Method 2: Programmatically
```python
from antivirus_scanner import AntivirusScanner

scanner = AntivirusScanner()
file_hash = scanner.calculate_hash('suspicious_file.exe')
scanner.add_signature(file_hash, 'MyTrojan.Variant')
```

### Method 3: Edit JSON Directly
Edit `malware_signatures.json`:
```json
{
  "your_hash_here": "Malware Name",
  "another_hash": "Another Malware Name"
}
```

## Common Use Cases

### 1. Monitor a Directory
```bash
# Scan downloads folder
python av_cli.py scan ~/Downloads --quarantine
```

### 2. Verify File Integrity
```python
from antivirus_scanner import AntivirusScanner

scanner = AntivirusScanner()

# Calculate hash of known good file
good_hash = scanner.calculate_hash('system_file.dll')

# Later, verify it hasn't changed
current_hash = scanner.calculate_hash('system_file.dll')
if good_hash != current_hash:
    print("WARNING: File has been modified!")
```

### 3. Batch Scanning
```bash
# Create a script to scan multiple directories
for dir in /var/www /home/user/uploads /tmp; do
    python av_cli.py scan $dir --quarantine
done
```

## Quarantine Management

Quarantined files are stored in the `quarantine/` directory:

```
quarantine/
├── 20260421_101801_malware.exe.quarantined
└── 20260421_101801_malware.exe.quarantined.json
```

The `.json` file contains metadata about the quarantined file.

### Restoring Quarantined Files
```python
import shutil
import json

# Read metadata
with open('quarantine/file.quarantined.json') as f:
    metadata = json.load(f)

# Restore if needed (be careful!)
original_path = metadata['original_path']
# shutil.move('quarantine/file.quarantined', original_path)
```

## Troubleshooting

### "Permission denied" errors
- Run with appropriate permissions
- Some system files may not be readable

### Large directory scans are slow
- This is normal - the scanner is single-threaded
- See EXTENSIONS.md for multi-threading implementation

### Getting lots of false positives
- The sample signature database is minimal
- Add real malware hashes for actual detection
- Use reputable malware hash databases

## Next Steps

1. ✅ Run the basic demo
2. ✅ Scan a real directory
3. ✅ Add some signatures
4. 📖 Read the full README.md
5. 🚀 Try implementing extensions from EXTENSIONS.md
6. 🧪 Run the test suite: `python test_scanner.py`

## Safety Reminders

⚠️ **This is an educational tool:**
- Not a replacement for real antivirus software
- Use only for learning and authorized testing
- Don't rely on it for actual malware protection

✅ **Best practices:**
- Always scan in a controlled environment
- Keep backups before quarantining files
- Verify signatures from trusted sources
- Test on non-critical systems first

## Getting Help

- Read the detailed README.md
- Check EXTENSIONS.md for advanced features
- Review the source code comments
- Run tests: `python test_scanner.py`

Happy learning! 🎓

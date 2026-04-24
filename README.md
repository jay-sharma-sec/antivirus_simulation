# Basic Antivirus Simulation (Signature Scanner)

An educational Python-based antivirus scanner that demonstrates how signature-based malware detection works.

## 🎯 Purpose

This project is designed for **educational and ethical use only** to help understand:

- How signature-based antivirus engines work
- Cryptographic fundamentals (file hashing and signature comparison)
- How to detect unauthorized or modified files in restricted environments
- Real-world security automation concepts

**⚠️ Important:** This tool will NOT detect real malware unless real signatures are added. It demonstrates the concepts used by antivirus systems.

## 🔍 How It Works

1. **Hashing**: Calculates cryptographic hash (SHA-256, MD5, or SHA-1) of files
2. **Signature Comparison**: Compares file hashes against a known malware database
3. **Detection**: Flags files that match known malware signatures
4. **Quarantine**: Optionally moves infected files to a quarantine folder

## 📋 Features

- ✅ Fast file scanning with cryptographic hashing
- ✅ Recursive directory scanning
- ✅ Malware signature database (JSON format)
- ✅ Automatic quarantine functionality
- ✅ Detailed scan reports
- ✅ Command-line interface (CLI)
- ✅ Support for multiple hash algorithms (MD5, SHA1, SHA256)
- ✅ Easy signature updates

## 🚀 Quick Start

### Basic Usage

Run the demonstration:

```bash
python antivirus_scanner.py
```

This will:
1. Create a sample malware signature database
2. Generate test files
3. Scan the test directory
4. Quarantine any detected threats
5. Display a detailed report

### CLI Usage

#### Scan a directory:
```bash
python av_cli.py scan /path/to/directory
```

#### Scan with auto-quarantine:
```bash
python av_cli.py scan /path/to/directory --quarantine
```

#### Calculate file hash:
```bash
python av_cli.py hash myfile.txt
python av_cli.py hash myfile.txt --algorithm md5
```

#### Add new malware signature:
```bash
python av_cli.py update --hash "abc123def456..." --name "Trojan.Example"
```

#### List all signatures:
```bash
python av_cli.py list
```

## 📁 Project Structure

```
antivirus-scanner/
├── antivirus_scanner.py    # Main scanner class
├── av_cli.py              # Command-line interface
├── malware_signatures.json # Signature database
├── quarantine/            # Quarantined files directory
├── test_files/            # Test files directory
└── README.md              # This file
```

## 🔧 How to Use

### 1. Initialize Scanner

```python
from antivirus_scanner import AntivirusScanner

scanner = AntivirusScanner()
```

### 2. Scan a Directory

```python
infected_files = scanner.scan_directory('/path/to/scan', recursive=True)
```

### 3. Quarantine Infected Files

```python
for file_path, malware_name in infected_files:
    scanner.quarantine_file(file_path)
```

### 4. Print Report

```python
scanner.print_scan_report()
```

## 📊 Signature Database Format

The signature database is stored in JSON format:

```json
{
  "file_hash_1": "Malware Name 1",
  "file_hash_2": "Malware Name 2",
  "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Suspicious Empty File"
}
```

## 🧪 Testing

The project includes the EICAR test file string - a standard antivirus test file that is NOT actual malware but is recognized by most antivirus software.

**EICAR Test String:**
```
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
```

## 🔐 Security Concepts Demonstrated

### 1. **Signature-Based Detection**
   - Files are identified by their cryptographic hash
   - Known malware hashes are stored in a database
   - Fast and efficient for known threats

### 2. **Cryptographic Hashing**
   - SHA-256: Most secure, recommended for production
   - MD5: Faster but less secure (deprecated for security use)
   - SHA-1: Middle ground (also deprecated for security)

### 3. **Quarantine Logic**
   - Isolates suspected files
   - Preserves metadata for investigation
   - Prevents accidental execution

### 4. **File Integrity**
   - Detect unauthorized modifications
   - Compare against known good hashes
   - Useful for monitoring restricted directories

## ⚙️ Advanced Usage

### Custom Signature Database

```python
scanner = AntivirusScanner(signatures_file='custom_signatures.json')
```

### Add Signatures Programmatically

```python
# Calculate hash of a known malware file
malware_hash = scanner.calculate_hash('/path/to/malware/sample')

# Add to database
scanner.add_signature(malware_hash, "Trojan.CustomThreat")
```

### Scan Specific File

```python
is_infected, malware_name, file_hash = scanner.scan_file('/path/to/file')

if is_infected:
    print(f"Infected with {malware_name}")
    scanner.quarantine_file('/path/to/file')
```

## 📚 Educational Value

This project teaches:

1. **How antivirus software works** at a fundamental level
2. **Cryptographic hashing** for file identification
3. **File system operations** in Python
4. **Security automation** concepts
5. **Pattern matching** and signature databases
6. **Quarantine and incident response** procedures

## ⚠️ Limitations

This is a **basic educational tool** with limitations:

- ❌ Only detects files with exact hash matches
- ❌ Cannot detect new/unknown malware (zero-day threats)
- ❌ No heuristic or behavioral analysis
- ❌ No packed/encrypted malware detection
- ❌ No real-time protection
- ❌ Single-threaded (slower on large directories)

Real antivirus solutions use:
- Machine learning and AI
- Behavioral analysis
- Sandboxing
- Cloud-based threat intelligence
- Heuristic detection
- Real-time monitoring

## 🎓 Learning Challenges

Try extending this project:

1. **Multi-threading**: Scan files in parallel for better performance
2. **File type detection**: Scan only executable/suspicious file types
3. **Hash caching**: Store hashes of clean files to speed up rescans
4. **Whitelisting**: Maintain a database of known-good files
5. **Reporting**: Generate HTML or PDF scan reports
6. **Scheduled scans**: Add cron/task scheduler integration
7. **Real-time monitoring**: Watch directories for new files
8. **Web interface**: Build a Flask/Django dashboard

## 📖 References

- [SHA-256 Hash Function](https://en.wikipedia.org/wiki/SHA-2)
- [EICAR Test File](https://www.eicar.org/download-anti-malware-testfile/)
- [Signature-Based Detection](https://en.wikipedia.org/wiki/Antivirus_software#Signature-based_detection)

## ⚖️ Legal & Ethical Notice

This tool is for:
- ✅ Educational purposes
- ✅ Learning cybersecurity concepts
- ✅ Authorized security testing
- ✅ Personal file integrity monitoring

Do NOT use for:
- ❌ Scanning systems without authorization
- ❌ Distributing malware signatures for actual malware
- ❌ Any illegal activities

## 📄 License

This is an educational project. Use responsibly and ethically.

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new features
- Improve performance
- Enhance documentation
- Share your extensions

---

**Remember**: This demonstrates antivirus concepts but is not a replacement for professional security software. Always use reputable antivirus solutions for real protection.

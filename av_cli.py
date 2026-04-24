#!/usr/bin/env python3
"""
Advanced Antivirus Scanner CLI
Interactive command-line interface for the signature-based scanner
"""

import argparse
import sys
from antivirus_scanner import AntivirusScanner


def scan_command(args):
    """Handle scan command."""
    scanner = AntivirusScanner(args.signatures)
    
    infected = scanner.scan_directory(args.path, recursive=args.recursive)
    
    if args.quarantine and infected:
        print(f"\n[*] Quarantining {len(infected)} infected file(s)...")
        for file_path, malware_name in infected:
            scanner.quarantine_file(file_path, args.quarantine_dir)
    
    scanner.print_scan_report()
    
    # Return exit code based on findings
    return 1 if infected else 0


def update_command(args):
    """Handle signature update command."""
    scanner = AntivirusScanner(args.signatures)
    
    if args.hash and args.name:
        scanner.add_signature(args.hash, args.name)
        print(f"[✓] Signature database updated")
    else:
        print("[!] Both --hash and --name are required for updates")
        return 1
    
    return 0


def hash_command(args):
    """Handle hash calculation command."""
    scanner = AntivirusScanner()
    
    print(f"[*] Calculating hash for: {args.file}")
    file_hash = scanner.calculate_hash(args.file, args.algorithm)
    
    if file_hash:
        print(f"\n{args.algorithm.upper()}: {file_hash}")
        
        # Check if it matches any known signature
        is_malware, malware_name = scanner.check_signature(file_hash)
        if is_malware:
            print(f"\n[⚠] WARNING: This file matches known malware: {malware_name}")
        else:
            print(f"\n[✓] No match in malware database")
    
    return 0


def list_command(args):
    """Handle list signatures command."""
    scanner = AntivirusScanner(args.signatures)
    
    print(f"\n[*] Malware Signatures Database")
    print("=" * 60)
    print(f"Total signatures: {len(scanner.malware_db)}\n")
    
    for hash_val, name in scanner.malware_db.items():
        print(f"{name}:")
        print(f"  Hash: {hash_val}")
        print()
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Basic Antivirus Scanner - Educational Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a directory
  python av_cli.py scan /path/to/scan
  
  # Scan and auto-quarantine infected files
  python av_cli.py scan /path/to/scan --quarantine
  
  # Calculate hash of a file
  python av_cli.py hash myfile.txt
  
  # Add new malware signature
  python av_cli.py update --hash abc123... --name "Trojan.Example"
  
  # List all signatures
  python av_cli.py list
        """
    )
    
    parser.add_argument(
        '--signatures',
        default='malware_signatures.json',
        help='Path to signatures database (default: malware_signatures.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan files or directories')
    scan_parser.add_argument('path', help='Path to file or directory to scan')
    scan_parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        default=True,
        help='Scan subdirectories recursively (default: True)'
    )
    scan_parser.add_argument(
        '--no-recursive',
        action='store_false',
        dest='recursive',
        help='Do not scan subdirectories'
    )
    scan_parser.add_argument(
        '-q', '--quarantine',
        action='store_true',
        help='Automatically quarantine infected files'
    )
    scan_parser.add_argument(
        '--quarantine-dir',
        default='quarantine',
        help='Quarantine directory path (default: quarantine)'
    )
    
    # Hash command
    hash_parser = subparsers.add_parser('hash', help='Calculate file hash')
    hash_parser.add_argument('file', help='File to hash')
    hash_parser.add_argument(
        '-a', '--algorithm',
        choices=['md5', 'sha1', 'sha256'],
        default='sha256',
        help='Hash algorithm (default: sha256)'
    )
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update signature database')
    update_parser.add_argument('--hash', help='Malware file hash')
    update_parser.add_argument('--name', help='Malware name/description')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all signatures')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == 'scan':
        return scan_command(args)
    elif args.command == 'hash':
        return hash_command(args)
    elif args.command == 'update':
        return update_command(args)
    elif args.command == 'list':
        return list_command(args)


if __name__ == "__main__":
    sys.exit(main())

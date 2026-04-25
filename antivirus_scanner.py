#!/usr/bin/env python3
"""
Basic Antivirus Simulation (Signature Scanner)
Educational tool demonstrating signature-based malware detection
"""

import os
import hashlib
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple


class AntivirusScanner:
    """
    A basic signature-based antivirus scanner that detects files
    by comparing their cryptographic hashes against a known malware database.
    """
    
    def __init__(self, signatures_file: str = "malware_signatures.json"):
        """
        Initialize the antivirus scanner.
        
        Args:
            signatures_file: Path to the malware signatures database
        """
        self.signatures_file = signatures_file
        self.malware_db: Dict[str, str] = {}
        self.scan_results = {
            'scanned': 0,
            'infected': 0,
            'clean': 0,
            'quarantined': 0,
            'errors': 0
        }
        self.detected_files: List[Tuple[str, str]] = []
        
        # Load malware signatures
        self.load_signatures()
    
    def load_signatures(self):
        """Load malware signatures from database file."""
        if os.path.exists(self.signatures_file):
            try:
                with open(self.signatures_file, 'r') as f:
                    self.malware_db = json.load(f)
                print(f"[✓] Loaded {len(self.malware_db)} malware signatures")
            except Exception as e:
                print(f"[!] Error loading signatures: {e}")
                self.malware_db = {}
        else:
            print(f"[!] Signatures file not found. Creating new database...")
            self.create_sample_signatures()
    
    def create_sample_signatures(self):
        """Create a sample malware signatures database."""
        # These are example hashes - in reality, these would be actual malware hashes
        self.malware_db = {
            "44d88612fea8a8f36de82e1278abb02f": "EICAR Test File",
            "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f": "Trojan.Generic",
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Suspicious Empty File",
        }
        
        # Save to file
        with open(self.signatures_file, 'w') as f:
            json.dump(self.malware_db, f, indent=2)
        print(f"[✓] Created sample signatures database with {len(self.malware_db)} entries")
    
    def calculate_hash(self, file_path: str, algorithm: str = 'sha256') -> str:
        """
        Calculate cryptographic hash of a file.
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm to use (md5, sha1, sha256)
            
        Returns:
            Hexadecimal hash string
        """
        hash_func = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                # Read file in chunks to handle large files efficiently
                while chunk := f.read(8192):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            print(f"[!] Error hashing {file_path}: {e}")
            return ""
    
    def check_signature(self, file_hash: str) -> Tuple[bool, str]:
        """
        Check if a file hash matches any known malware signature.
        
        Args:
            file_hash: Hash of the file to check
            
        Returns:
            Tuple of (is_malware, malware_name)
        """
        if file_hash in self.malware_db:
            return True, self.malware_db[file_hash]
        return False, ""
    
    def scan_file(self, file_path: str) -> Tuple[bool, str, str]:
        """
        Scan a single file for malware.
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            Tuple of (is_infected, malware_name, file_hash)
        """
        try:
            # Calculate file hash
            file_hash = self.calculate_hash(file_path)
            
            if not file_hash:
                self.scan_results['errors'] += 1
                return False, "", ""
            
            # Check against malware database
            is_malware, malware_name = self.check_signature(file_hash)
            
            self.scan_results['scanned'] += 1
            
            if is_malware:
                self.scan_results['infected'] += 1
                self.detected_files.append((file_path, malware_name))
                return True, malware_name, file_hash
            else:
                self.scan_results['clean'] += 1
                return False, "", file_hash
                
        except Exception as e:
            print(f"[!] Error scanning {file_path}: {e}")
            self.scan_results['errors'] += 1
            return False, "", ""
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[Tuple[str, str]]:
        """
        Scan a directory for malware.
        
        Args:
            directory: Path to directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of infected files and their malware names
        """
        print(f"\n[*] Starting scan of: {directory}")
        print(f"[*] Recursive scan: {recursive}")
        print("-" * 60)
        
        infected_files = []
        
        if recursive:
            # Walk through all subdirectories
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    is_infected, malware_name, _ = self.scan_file(file_path)
                    
                    if is_infected:
                        print(f"[⚠] INFECTED: {file_path}")
                        print(f"    Threat: {malware_name}")
                        infected_files.append((file_path, malware_name))
                    else:
                        print(f"[✓] Clean: {file_path}")
        else:
            # Scan only files in the specified directory
            for item in os.listdir(directory):
                file_path = os.path.join(directory, item)
                if os.path.isfile(file_path):
                    is_infected, malware_name, _ = self.scan_file(file_path)
                    
                    if is_infected:
                        print(f"[⚠] INFECTED: {file_path}")
                        print(f"    Threat: {malware_name}")
                        infected_files.append((file_path, malware_name))
                    else:
                        print(f"[✓] Clean: {file_path}")
        
        return infected_files
    
    def quarantine_file(self, file_path: str, quarantine_dir: str = "quarantine"):
        """
        Move infected file to quarantine directory.
        
        Args:
            file_path: Path to the infected file
            quarantine_dir: Path to quarantine directory
        """
        try:
            # Create quarantine directory if it doesn't exist
            os.makedirs(quarantine_dir, exist_ok=True)
            
            # Generate unique quarantine filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = os.path.basename(file_path)
            quarantine_name = f"{timestamp}_{original_name}.quarantined"
            quarantine_path = os.path.join(quarantine_dir, quarantine_name)
            
            # Move file to quarantine
            shutil.move(file_path, quarantine_path)
            
            # Create metadata file
            metadata = {
                'original_path': file_path,
                'quarantine_date': timestamp,
                'original_name': original_name
            }
            
            metadata_path = f"{quarantine_path}.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.scan_results['quarantined'] += 1
            print(f"[✓] Quarantined: {file_path} -> {quarantine_path}")
            
        except Exception as e:
            print(f"[!] Error quarantining {file_path}: {e}")
    
    def print_scan_report(self):
        """Print detailed scan report."""
        print("\n" + "=" * 60)
        print("SCAN REPORT")
        print("=" * 60)
        print(f"Files scanned:    {self.scan_results['scanned']}")
        print(f"Infected files:   {self.scan_results['infected']}")
        print(f"Clean files:      {self.scan_results['clean']}")
        print(f"Quarantined:      {self.scan_results['quarantined']}")
        print(f"Errors:           {self.scan_results['errors']}")
        print("=" * 60)
        
        if self.detected_files:
            print("\nDETECTED THREATS:")
            print("-" * 60)
            for file_path, malware_name in self.detected_files:
                print(f"  {malware_name}: {file_path}")
    
    def add_signature(self, file_hash: str, malware_name: str):
        """
        Add a new malware signature to the database.
        
        Args:
            file_hash: Hash of the malware file
            malware_name: Name/description of the malware
        """
        self.malware_db[file_hash] = malware_name
        
        # Save to file
        with open(self.signatures_file, 'w') as f:
            json.dump(self.malware_db, f, indent=2)
        
        print(f"[✓] Added signature: {malware_name}")


def main():
    """Main function to demonstrate the antivirus scanner."""
    print("=" * 60)
    print("Basic Antivirus Simulation (Signature Scanner)")
    print("=" * 60)
    
    # Initialize scanner
    scanner = AntivirusScanner()
    
    # Create test directory with sample files
    test_dir = "test_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create some test files
    print("\n[*] Creating test files...")
    
    # Clean file
    with open(os.path.join(test_dir, "clean_file.txt"), 'w') as f:
        f.write("This is a clean file with normal content.")
    
    # EICAR test file (standard antivirus test file - NOT actual malware)
    with open(os.path.join(test_dir, "eicar.txt"), 'w') as f:
        f.write("X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")
    
    # Another clean file
    with open(os.path.join(test_dir, "document.txt"), 'w') as f:
        f.write("Important document with sensitive information.")
    
    print(f"[✓] Created test files in '{test_dir}' directory")
    
    # Perform scan
    infected = scanner.scan_directory(test_dir, recursive=True)
    
    # Quarantine infected files
    if infected:
        print("\n[*] Quarantining infected files...")
        for file_path, malware_name in infected:
            scanner.quarantine_file(file_path)
    
    # Print report
    scanner.print_scan_report()
    
    print("\n[*] Scan complete!")

if __name__ == "__main__":
    main()

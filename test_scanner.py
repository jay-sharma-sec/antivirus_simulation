#!/usr/bin/env python3
"""
Test Suite for Antivirus Scanner
Demonstrates various features and edge cases
"""

import os
import tempfile
import shutil
from antivirus_scanner import AntivirusScanner


def test_basic_scanning():
    """Test basic file scanning functionality."""
    print("\n" + "="*60)
    print("TEST 1: Basic File Scanning")
    print("="*60)
    
    scanner = AntivirusScanner()
    
    # Create temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        clean_file = os.path.join(tmpdir, "clean.txt")
        with open(clean_file, 'w') as f:
            f.write("This is clean content.")
        
        # Scan the file
        is_infected, malware_name, file_hash = scanner.scan_file(clean_file)
        
        print(f"File: {clean_file}")
        print(f"Hash: {file_hash}")
        print(f"Status: {'INFECTED' if is_infected else 'CLEAN'}")
        
        assert not is_infected, "Clean file should not be detected as infected"
        print("\n✓ Test passed: Clean file correctly identified")


def test_hash_algorithms():
    """Test different hash algorithms."""
    print("\n" + "="*60)
    print("TEST 2: Multiple Hash Algorithms")
    print("="*60)
    
    scanner = AntivirusScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Test content for hashing")
        
        for algorithm in ['md5', 'sha1', 'sha256']:
            file_hash = scanner.calculate_hash(test_file, algorithm)
            print(f"{algorithm.upper()}: {file_hash}")
            assert file_hash, f"{algorithm} hash should not be empty"
    
    print("\n✓ Test passed: All hash algorithms working")


def test_signature_detection():
    """Test malware signature detection."""
    print("\n" + "="*60)
    print("TEST 3: Signature Detection")
    print("="*60)
    
    scanner = AntivirusScanner()
    
    # Add a test signature
    test_hash = "testHashValue123456"
    test_malware = "Test.Malware"
    scanner.add_signature(test_hash, test_malware)
    
    # Check detection
    is_malware, name = scanner.check_signature(test_hash)
    
    print(f"Hash: {test_hash}")
    print(f"Detected: {is_malware}")
    print(f"Name: {name}")
    
    assert is_malware, "Test signature should be detected"
    assert name == test_malware, "Malware name should match"
    
    print("\n✓ Test passed: Signature detection working")


def test_directory_scanning():
    """Test recursive directory scanning."""
    print("\n" + "="*60)
    print("TEST 4: Directory Scanning")
    print("="*60)
    
    scanner = AntivirusScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create nested directory structure
        subdir = os.path.join(tmpdir, "subdir")
        os.makedirs(subdir)
        
        # Create files in different directories
        for i, path in enumerate([tmpdir, subdir]):
            file_path = os.path.join(path, f"file{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"Content {i}")
        
        # Scan directory
        infected = scanner.scan_directory(tmpdir, recursive=True)
        
        print(f"\nFiles scanned: {scanner.scan_results['scanned']}")
        print(f"Infected: {scanner.scan_results['infected']}")
        print(f"Clean: {scanner.scan_results['clean']}")
        
        assert scanner.scan_results['scanned'] >= 2, "Should scan multiple files"
    
    print("\n✓ Test passed: Directory scanning working")


def test_quarantine():
    """Test quarantine functionality."""
    print("\n" + "="*60)
    print("TEST 5: Quarantine Functionality")
    print("="*60)
    
    scanner = AntivirusScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test file
        test_file = os.path.join(tmpdir, "infected.txt")
        with open(test_file, 'w') as f:
            f.write("Malicious content")
        
        # Create quarantine directory
        quarantine_dir = os.path.join(tmpdir, "quarantine")
        
        # Quarantine the file
        scanner.quarantine_file(test_file, quarantine_dir)
        
        # Check if file was moved
        assert not os.path.exists(test_file), "Original file should be removed"
        assert os.path.exists(quarantine_dir), "Quarantine directory should exist"
        
        # Check quarantine contents
        quarantined_files = os.listdir(quarantine_dir)
        print(f"Quarantined files: {len([f for f in quarantined_files if not f.endswith('.json')])}")
        print(f"Metadata files: {len([f for f in quarantined_files if f.endswith('.json')])}")
        
        assert len(quarantined_files) >= 2, "Should have file and metadata"
    
    print("\n✓ Test passed: Quarantine working correctly")


def test_large_file_handling():
    """Test handling of large files."""
    print("\n" + "="*60)
    print("TEST 6: Large File Handling")
    print("="*60)
    
    scanner = AntivirusScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a larger file (1MB)
        large_file = os.path.join(tmpdir, "large.bin")
        with open(large_file, 'wb') as f:
            f.write(b'X' * (1024 * 1024))  # 1MB of data
        
        # Calculate hash
        file_hash = scanner.calculate_hash(large_file)
        
        print(f"File size: {os.path.getsize(large_file) / 1024:.2f} KB")
        print(f"Hash: {file_hash[:32]}...")
        
        assert file_hash, "Should be able to hash large files"
    
    print("\n✓ Test passed: Large file handling working")


def test_empty_file():
    """Test handling of empty files."""
    print("\n" + "="*60)
    print("TEST 7: Empty File Handling")
    print("="*60)
    
    scanner = AntivirusScanner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        empty_file = os.path.join(tmpdir, "empty.txt")
        open(empty_file, 'w').close()  # Create empty file
        
        file_hash = scanner.calculate_hash(empty_file)
        
        print(f"Empty file hash: {file_hash}")
        print(f"Expected (SHA256 of empty): e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        
        # SHA256 of empty file is known
        expected_empty_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert file_hash == expected_empty_hash, "Empty file hash should match expected"
    
    print("\n✓ Test passed: Empty file handling correct")


def run_all_tests():
    """Run all test cases."""
    print("\n" + "#"*60)
    print("# ANTIVIRUS SCANNER TEST SUITE")
    print("#"*60)
    
    tests = [
        test_basic_scanning,
        test_hash_algorithms,
        test_signature_detection,
        test_directory_scanning,
        test_quarantine,
        test_large_file_handling,
        test_empty_file
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ Test error: {e}")
            failed += 1
    
    print("\n" + "#"*60)
    print(f"# TEST RESULTS: {passed} passed, {failed} failed")
    print("#"*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

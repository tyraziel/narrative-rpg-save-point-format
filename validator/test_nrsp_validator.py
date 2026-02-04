#!/usr/bin/env python3
"""
Tests for NRSP Format Validator

Run with: python -m pytest test_nrsp_validator.py -v
Or: python test_nrsp_validator.py
"""

import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from nrsp_validator import NRSPValidator, FileType, Version, ValidationResult


class TestVersionDetection(unittest.TestCase):
    """Test version detection strategies"""

    def setUp(self):
        self.validator = NRSPValidator()

    def test_detect_version_from_filename_v040(self):
        """Test v0.4.0 filename detection"""
        test_cases = [
            "my_save_v0.4.0.NRSP.md",
            "save_v0_4_0.NRSP.md",
            "save_v040.NRSP.md",
            "save_v0.4.NRSP.md",
        ]
        for filename in test_cases:
            path = Path(filename)
            version = self.validator.detect_version_from_filename(path)
            self.assertEqual(version, Version.V0_4, f"Failed to detect v0.4 from {filename}")

    def test_detect_version_from_filename_v03(self):
        """Test v0.3 filename detection"""
        test_cases = [
            "GEMINI-v031.NRSP.md",
            "save_v0.3.NRSP.md",
            "save_v0_3.NRSP.md",
        ]
        for filename in test_cases:
            path = Path(filename)
            version = self.validator.detect_version_from_filename(path)
            self.assertEqual(version, Version.V0_3, f"Failed to detect v0.3 from {filename}")

    def test_detect_version_from_yaml_explicit(self):
        """Test explicit NRSPFormat field detection"""
        content = "---\nTitle: Test\nNRSPFormat: 0.4.0\n---\n## Test"
        yaml_data = {"Title": "Test", "NRSPFormat": "0.4.0"}
        version = self.validator.detect_version_from_content(content, yaml_data)
        self.assertEqual(version, Version.V0_4)

        yaml_data_v03 = {"Title": "Test", "NRSPFormat": "0.3"}
        version = self.validator.detect_version_from_content(content, yaml_data_v03)
        self.assertEqual(version, Version.V0_3)

    def test_detect_version_from_structure_v04(self):
        """Test v0.4 structure detection"""
        content = "---\nTitle: Test\n---\n## Party State\nContent"
        yaml_data = {"Title": "Test"}
        version = self.validator.detect_version_from_content(content, yaml_data)
        self.assertEqual(version, Version.V0_4)

    def test_detect_version_from_structure_v03(self):
        """Test v0.3 structure detection (T.md reference)"""
        content = "---\nTitle: Test\n---\n## Location\nSee Bramblebend.T.md"
        yaml_data = {"Title": "Test"}
        version = self.validator.detect_version_from_content(content, yaml_data)
        self.assertEqual(version, Version.V0_3)

    def test_default_version(self):
        """Test default to latest version"""
        content = "---\nTitle: Test\n---\n## Some Section"
        yaml_data = {"Title": "Test"}
        version = self.validator.detect_version_from_content(content, yaml_data)
        self.assertEqual(version, Version.V0_4)


class TestFileTypeDetection(unittest.TestCase):
    """Test file type detection from extensions"""

    def setUp(self):
        self.validator = NRSPValidator()

    def test_nrsp_file_type(self):
        """Test NRSP file type detection"""
        path = Path("test.NRSP.md")
        file_type = self.validator.detect_file_type(path)
        self.assertEqual(file_type, FileType.NRSP)

    def test_sld_file_type(self):
        """Test SLD file type detection"""
        path = Path("test.SLD.md")
        file_type = self.validator.detect_file_type(path)
        self.assertEqual(file_type, FileType.SLD)

    def test_cs_file_type(self):
        """Test CS file type detection"""
        path = Path("test.CS.md")
        file_type = self.validator.detect_file_type(path)
        self.assertEqual(file_type, FileType.CS)

    def test_ls_file_type(self):
        """Test LS file type detection"""
        path = Path("test.LS.md")
        file_type = self.validator.detect_file_type(path)
        self.assertEqual(file_type, FileType.LS)

    def test_t_file_type(self):
        """Test T.md (v0.3 town) maps to LS"""
        path = Path("test.T.md")
        file_type = self.validator.detect_file_type(path)
        self.assertEqual(file_type, FileType.LS)

    def test_npc_file_type(self):
        """Test NPC file type detection"""
        path = Path("test.NPC.md")
        file_type = self.validator.detect_file_type(path)
        self.assertEqual(file_type, FileType.NPC)

    def test_lgm_file_type(self):
        """Test LGM file type detection"""
        path = Path("test.LGM.md")
        file_type = self.validator.detect_file_type(path)
        self.assertEqual(file_type, FileType.LGM)

    def test_unknown_file_type(self):
        """Test unknown file type"""
        path = Path("test.txt")
        file_type = self.validator.detect_file_type(path)
        self.assertIsNone(file_type)


class TestYAMLValidation(unittest.TestCase):
    """Test YAML frontmatter validation"""

    def setUp(self):
        self.validator = NRSPValidator()

    def test_valid_nrsp_yaml(self):
        """Test valid NRSP YAML"""
        yaml_data = {
            "Title": "Test Save Point",
            "TimelineType": "Mainline",
            "ArcID": "TEST-01"
        }
        errors, warnings = self.validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertEqual(len(errors), 0)

    def test_missing_required_field(self):
        """Test missing required field"""
        yaml_data = {"ArcID": "TEST-01"}
        errors, warnings = self.validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Title" in error for error in errors))

    def test_invalid_timeline_type(self):
        """Test invalid TimelineType value"""
        yaml_data = {
            "Title": "Test",
            "TimelineType": "CustomType"
        }
        errors, warnings = self.validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("TimelineType" in error for error in errors))

    def test_unknown_field_warning(self):
        """Test unknown field generates warning in normal mode"""
        yaml_data = {
            "Title": "Test",
            "UnknownField": "value"
        }
        errors, warnings = self.validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertGreater(len(warnings), 0)
        self.assertEqual(len(errors), 0)

    def test_unknown_field_strict(self):
        """Test unknown field generates error in strict mode"""
        validator = NRSPValidator(strict=True)
        yaml_data = {
            "Title": "Test",
            "UnknownField": "value"
        }
        errors, warnings = validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertGreater(len(errors), 0)

    def test_missing_nrspformat_warning(self):
        """Test missing NRSPFormat generates warning in normal mode"""
        yaml_data = {
            "Title": "Test"
        }
        errors, warnings = self.validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertGreater(len(warnings), 0)
        self.assertTrue(any("NRSPFormat" in warning for warning in warnings))
        self.assertEqual(len(errors), 0)

    def test_missing_nrspformat_strict(self):
        """Test missing NRSPFormat generates error in strict mode"""
        validator = NRSPValidator(strict=True)
        yaml_data = {
            "Title": "Test"
        }
        errors, warnings = validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("NRSPFormat" in error for error in errors))

    def test_with_nrspformat_no_warning(self):
        """Test that files with NRSPFormat don't get warnings"""
        yaml_data = {
            "Title": "Test",
            "NRSPFormat": "0.4.0"
        }
        errors, warnings = self.validator.validate_yaml_fields(yaml_data, FileType.NRSP, Version.V0_4)
        self.assertEqual(len(errors), 0)
        # Should not have NRSPFormat warning
        self.assertFalse(any("NRSPFormat" in warning for warning in warnings))


class TestFileValidation(unittest.TestCase):
    """Test complete file validation"""

    def setUp(self):
        self.validator = NRSPValidator()
        self.temp_dir = tempfile.mkdtemp()

    def create_temp_file(self, filename, content):
        """Helper to create temporary test files"""
        path = Path(self.temp_dir) / filename
        path.write_text(content, encoding='utf-8')
        return path

    def test_valid_nrsp_file(self):
        """Test validation of valid NRSP file"""
        content = """---
Title: Test Save Point
TimelineType: Mainline
---

## Narrative Context

This is a test save point.

## Character Snapshots

### Character: TestChar
- Level: 1
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)
        self.assertEqual(result.file_type, FileType.NRSP)

    def test_missing_frontmatter(self):
        """Test file missing frontmatter"""
        content = "## Section\nContent"
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("frontmatter" in error.lower() for error in result.errors))

    def test_malformed_yaml(self):
        """Test file with malformed YAML"""
        content = """---
Title: Test
InvalidYAML: [unclosed
---

## Section
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)

    def test_empty_body(self):
        """Test NRSP file with empty body"""
        content = """---
Title: Test Save Point
---
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("empty" in error.lower() for error in result.errors))

    def test_valid_sld_file(self):
        """Test validation of valid SLD file"""
        content = """---
SessionLogTitle: Test Session
SavePoint: TestSave.NRSP.md
SessionDate: 2025-01-23
---

## Session Narrative

This is a test session log.
"""
        path = self.create_temp_file("test.SLD.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)
        self.assertEqual(result.file_type, FileType.SLD)

    def test_valid_character_sheet(self):
        """Test validation of valid character sheet"""
        content = """---
Name: Test Character
Type: PC
---

## Character Stats

- Level: 5
- HP: 20
"""
        path = self.create_temp_file("test.CS.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)
        self.assertEqual(result.file_type, FileType.CS)

    def test_explicit_version_override(self):
        """Test explicit version override"""
        content = """---
Title: Test
---

## Section
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path, explicit_version=Version.V0_3)
        self.assertEqual(result.detected_version, Version.V0_3)

    def test_file_without_nrspformat_has_warning(self):
        """Test that files without NRSPFormat get warning in normal mode"""
        content = """---
Title: Test Save Point
---

## Narrative Context

Test content.
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)  # Still valid
        self.assertGreater(len(result.warnings), 0)
        self.assertTrue(any("NRSPFormat" in w for w in result.warnings))

    def test_file_without_nrspformat_strict_mode(self):
        """Test that files without NRSPFormat fail in strict mode"""
        validator = NRSPValidator(strict=True)
        content = """---
Title: Test Save Point
---

## Narrative Context

Test content.
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = validator.validate_file(path)
        self.assertFalse(result.valid)  # Invalid in strict mode
        self.assertGreater(len(result.errors), 0)
        self.assertTrue(any("NRSPFormat" in e for e in result.errors))

    def test_file_with_nrspformat_no_warning(self):
        """Test that files with NRSPFormat don't get warning"""
        content = """---
Title: Test Save Point
NRSPFormat: 0.4.0
---

## Narrative Context

Test content.
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)
        # Should not have NRSPFormat warning
        self.assertFalse(any("NRSPFormat" in w for w in result.warnings))

    def test_fix_adds_nrspformat(self):
        """Test that fix_file adds NRSPFormat to a file"""
        content = """---
Title: Test Save Point
---

## Narrative Context

Test content.
"""
        path = self.create_temp_file("test_fix.NRSP.md", content)

        # Verify it's missing NRSPFormat
        result_before = self.validator.validate_file(path)
        self.assertTrue(any("NRSPFormat" in w for w in result_before.warnings))

        # Fix the file
        success = self.validator.fix_file(path, Version.V0_4)
        self.assertTrue(success)

        # Verify it now has NRSPFormat
        result_after = self.validator.validate_file(path)
        self.assertFalse(any("NRSPFormat" in w for w in result_after.warnings))

        # Verify the field was actually added
        fixed_content = path.read_text(encoding='utf-8')
        self.assertIn("NRSPFormat:", fixed_content)
        self.assertIn("0.4.0", fixed_content)

    def test_fix_preserves_existing_nrspformat(self):
        """Test that fix_file doesn't overwrite existing NRSPFormat"""
        content = """---
Title: Test Save Point
NRSPFormat: 0.4.0
---

## Narrative Context

Test content.
"""
        path = self.create_temp_file("test_no_fix.NRSP.md", content)

        # Try to fix (should do nothing)
        success = self.validator.fix_file(path, Version.V0_4)
        self.assertTrue(success)

        # Verify content unchanged
        fixed_content = path.read_text(encoding='utf-8')
        self.assertIn("NRSPFormat: 0.4.0", fixed_content)


class TestDirectoryValidation(unittest.TestCase):
    """Test directory validation"""

    def setUp(self):
        self.validator = NRSPValidator()
        self.temp_dir = tempfile.mkdtemp()

    def create_temp_file(self, subdir, filename, content):
        """Helper to create temporary test files in subdirectories"""
        dir_path = Path(self.temp_dir) / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        path = dir_path / filename
        path.write_text(content, encoding='utf-8')
        return path

    def test_directory_validation_non_recursive(self):
        """Test non-recursive directory validation"""
        # Create files in root
        self.create_temp_file(".", "test1.NRSP.md", "---\nTitle: Test1\n---\n## Section")
        self.create_temp_file(".", "test2.NRSP.md", "---\nTitle: Test2\n---\n## Section")

        # Create file in subdirectory (should be ignored)
        self.create_temp_file("subdir", "test3.NRSP.md", "---\nTitle: Test3\n---\n## Section")

        results = self.validator.validate_directory(Path(self.temp_dir), recursive=False)
        self.assertEqual(len(results), 2)

    def test_directory_validation_recursive(self):
        """Test recursive directory validation"""
        # Create files in root
        self.create_temp_file(".", "test1.NRSP.md", "---\nTitle: Test1\n---\n## Section")

        # Create file in subdirectory
        self.create_temp_file("subdir", "test2.NRSP.md", "---\nTitle: Test2\n---\n## Section")

        results = self.validator.validate_directory(Path(self.temp_dir), recursive=True)
        self.assertEqual(len(results), 2)


class TestValidationResult(unittest.TestCase):
    """Test ValidationResult output formatting"""

    def test_valid_result_string(self):
        """Test string representation of valid result"""
        result = ValidationResult(
            valid=True,
            file_path="test.NRSP.md",
            file_type=FileType.NRSP,
            detected_version=Version.V0_4,
            errors=[],
            warnings=[]
        )
        output = str(result)
        self.assertIn("✓ VALID", output)
        self.assertIn("test.NRSP.md", output)
        self.assertIn("NRSP", output)
        self.assertIn("0.4.0", output)

    def test_invalid_result_string(self):
        """Test string representation of invalid result"""
        result = ValidationResult(
            valid=False,
            file_path="test.NRSP.md",
            file_type=FileType.NRSP,
            detected_version=Version.V0_4,
            errors=["Missing required field: Title"],
            warnings=["Unknown field: CustomField"]
        )
        output = str(result)
        self.assertIn("✗ INVALID", output)
        self.assertIn("Missing required field", output)
        self.assertIn("Unknown field", output)


class TestErrorHandling(unittest.TestCase):
    """Test error handling paths"""

    def setUp(self):
        self.validator = NRSPValidator()
        self.temp_dir = tempfile.mkdtemp()

    def create_temp_file(self, filename, content):
        """Helper to create temporary test files"""
        path = Path(self.temp_dir) / filename
        path.write_text(content, encoding='utf-8')
        return path

    def test_file_not_found(self):
        """Test validation of non-existent file"""
        path = Path(self.temp_dir) / "nonexistent.NRSP.md"
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("not found" in error.lower() for error in result.errors))

    def test_malformed_yaml_unclosed_bracket(self):
        """Test file with malformed YAML (unclosed bracket)"""
        content = """---
Title: Test
InvalidList: [unclosed
---

## Section
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("YAML" in error for error in result.errors))

    def test_malformed_yaml_not_dict(self):
        """Test YAML that's not a dictionary"""
        content = """---
- Item 1
- Item 2
---

## Section
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("dictionary" in error.lower() for error in result.errors))

    def test_empty_sld_body(self):
        """Test SLD file with empty body"""
        content = """---
SessionLogTitle: Test Session
SavePoint: test.NRSP.md
---
"""
        path = self.create_temp_file("test.SLD.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("empty" in error.lower() for error in result.errors))

    def test_no_section_headers_warning(self):
        """Test file with no section headers generates warning"""
        content = """---
Title: Test Save Point
NRSPFormat: 0.4.0
---

Just some plain text with no headers.
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)
        self.assertTrue(any("section" in warning.lower() for warning in result.warnings))

    def test_fix_file_no_frontmatter(self):
        """Test fix_file on file without frontmatter"""
        content = "## Section\n\nNo frontmatter here"
        path = self.create_temp_file("test.NRSP.md", content)
        success = self.validator.fix_file(path, Version.V0_4)
        self.assertFalse(success)

    def test_fix_file_malformed_frontmatter(self):
        """Test fix_file on file with malformed frontmatter"""
        content = "---\nTitle: Test\n"  # Missing closing ---
        path = self.create_temp_file("test.NRSP.md", content)
        success = self.validator.fix_file(path, Version.V0_4)
        self.assertFalse(success)

    def test_fix_file_invalid_yaml(self):
        """Test fix_file on file with invalid YAML"""
        content = """---
Title: Test
Invalid: [unclosed
---

## Section
"""
        path = self.create_temp_file("test.NRSP.md", content)
        success = self.validator.fix_file(path, Version.V0_4)
        self.assertFalse(success)

    def test_fix_file_readonly(self):
        """Test fix_file on read-only file"""
        import os
        content = """---
Title: Test Save Point
---

## Section
"""
        path = self.create_temp_file("readonly.NRSP.md", content)
        # Make file read-only
        os.chmod(path, 0o444)
        try:
            success = self.validator.fix_file(path, Version.V0_4)
            # Depending on the system, this might fail or succeed
            # Just ensure it doesn't crash
            self.assertIsNotNone(success)
        finally:
            # Restore write permissions for cleanup
            os.chmod(path, 0o644)

    def test_empty_cs_file(self):
        """Test CS file with empty body (should be valid with warning)"""
        content = """---
Name: Test Character
---
"""
        path = self.create_temp_file("test.CS.md", content)
        result = self.validator.validate_file(path)
        # CS files can have empty bodies (not an error like NRSP/SLD)
        self.assertTrue(result.valid)

    def test_missing_narrative_context_warning(self):
        """Test NRSP file missing Narrative Context section"""
        content = """---
Title: Test Save Point
NRSPFormat: 0.4.0
---

## Some Other Section

Content without Narrative Context.
"""
        path = self.create_temp_file("test.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)
        self.assertTrue(any("Narrative Context" in warning for warning in result.warnings))

    def test_file_read_error(self):
        """Test file read error handling"""
        import os
        content = """---
Title: Test
NRSPFormat: 0.4.0
---

## Section
"""
        path = self.create_temp_file("unreadable.NRSP.md", content)
        # Make file unreadable
        os.chmod(path, 0o000)
        try:
            # Skip if running as root (can read anything)
            if os.geteuid() == 0:
                self.skipTest("Running as root, cannot test permission errors")
            result = self.validator.validate_file(path)
            # Should handle read error gracefully
            self.assertFalse(result.valid)
        finally:
            # Restore permissions for cleanup
            os.chmod(path, 0o644)

    def test_fix_file_read_error(self):
        """Test fix_file with file read error"""
        import os
        content = """---
Title: Test
---

## Section
"""
        path = self.create_temp_file("unreadable_fix.NRSP.md", content)
        # Make file unreadable
        os.chmod(path, 0o000)
        try:
            # Skip if running as root (can read anything)
            if os.geteuid() == 0:
                self.skipTest("Running as root, cannot test permission errors")
            success = self.validator.fix_file(path, Version.V0_4)
            self.assertFalse(success)
        finally:
            # Restore permissions for cleanup
            os.chmod(path, 0o644)

    def test_unknown_file_type_validation(self):
        """Test validation of file with unknown extension"""
        content = """---
Title: Test
---

## Section
"""
        path = self.create_temp_file("test.txt", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("Unknown file type" in error for error in result.errors))

    def test_empty_yaml_frontmatter(self):
        """Test file with empty YAML frontmatter"""
        content = """---
---

## Section
"""
        path = self.create_temp_file("empty_yaml.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("Title" in error for error in result.errors))

    def test_ls_file_no_section_headers(self):
        """Test LS file with no section headers generates warning"""
        content = """---
Name: Test Location
NRSPFormat: 0.4.0
---

Just some plain text with no headers.
"""
        path = self.create_temp_file("test.LS.md", content)
        result = self.validator.validate_file(path)
        self.assertTrue(result.valid)
        # Should have warning about no section headers
        self.assertTrue(any("section" in warning.lower() for warning in result.warnings))

    def test_npc_file_empty_body(self):
        """Test NPC file with empty body (should be valid, may have warnings)"""
        content = """---
Name: Test NPC
NRSPFormat: 0.4.0
---
"""
        path = self.create_temp_file("test.NPC.md", content)
        result = self.validator.validate_file(path)
        # NPC files can have empty bodies
        self.assertTrue(result.valid)

    def test_yaml_scalar_value(self):
        """Test YAML parsing with scalar value instead of dict"""
        content = """---
just a string
---

## Section
"""
        path = self.create_temp_file("scalar.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        self.assertTrue(any("dictionary" in error.lower() for error in result.errors))

    def test_yaml_null_value(self):
        """Test YAML parsing with null value"""
        content = """---
---

## Section
"""
        path = self.create_temp_file("null_yaml.NRSP.md", content)
        result = self.validator.validate_file(path)
        self.assertFalse(result.valid)
        # Should fail due to missing required Title field
        self.assertTrue(any("Title" in error for error in result.errors))


class TestCLI(unittest.TestCase):
    """Test command-line interface"""

    def setUp(self):
        self.validator = NRSPValidator()
        self.temp_dir = tempfile.mkdtemp()

    def create_temp_file(self, filename, content):
        """Helper to create temporary test files"""
        path = Path(self.temp_dir) / filename
        path.write_text(content, encoding='utf-8')
        return path

    def test_cli_single_file(self):
        """Test CLI validation of single file"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
Title: Test Save Point
NRSPFormat: 0.4.0
---

## Narrative Context

Test content.
"""
        path = self.create_temp_file("test.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', str(path)]
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

            output = sys.stdout.getvalue()
            self.assertIn("VALID", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_single_file_with_fix(self):
        """Test CLI with --fix option"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
Title: Test Save Point
---

## Narrative Context

Test content.
"""
        path = self.create_temp_file("test_fix_cli.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', str(path), '--fix']
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

            output = sys.stdout.getvalue()
            self.assertIn("Added NRSPFormat", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_directory(self):
        """Test CLI validation of directory"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
Title: Test
NRSPFormat: 0.4.0
---

## Section
"""
        self.create_temp_file("test1.NRSP.md", content)
        self.create_temp_file("test2.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', '--directory', str(self.temp_dir)]
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

            output = sys.stdout.getvalue()
            self.assertIn("Summary:", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_directory_with_fix(self):
        """Test CLI directory validation with --fix"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
Title: Test
---

## Section
"""
        self.create_temp_file("test1.NRSP.md", content)
        self.create_temp_file("test2.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', '--directory', str(self.temp_dir), '--fix']
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

            output = sys.stdout.getvalue()
            self.assertIn("Fixed", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_nonexistent_directory(self):
        """Test CLI with non-existent directory"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        # Mock sys.argv
        old_argv = sys.argv
        old_stderr = sys.stderr
        sys.stderr = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', '--directory', '/nonexistent/path']
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 1)

            output = sys.stderr.getvalue()
            self.assertIn("Not a directory", output)
        finally:
            sys.argv = old_argv
            sys.stderr = old_stderr

    def test_cli_empty_directory(self):
        """Test CLI with directory containing no NRSP files"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        empty_dir = Path(self.temp_dir) / "empty"
        empty_dir.mkdir()

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', '--directory', str(empty_dir)]
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

            output = sys.stdout.getvalue()
            self.assertIn("No NRSP files found", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_invalid_file(self):
        """Test CLI with invalid file"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
InvalidYAML: [unclosed
---
"""
        path = self.create_temp_file("invalid.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', str(path)]
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 1)

            output = sys.stdout.getvalue()
            self.assertIn("INVALID", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_strict_mode(self):
        """Test CLI with --strict mode"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
Title: Test
---

## Section
"""
        path = self.create_temp_file("test_strict.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', str(path), '--strict']
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 1)  # Should fail in strict mode

            output = sys.stdout.getvalue()
            self.assertIn("NRSPFormat", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_explicit_version(self):
        """Test CLI with explicit --version argument"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
Title: Test
---

## Section
"""
        path = self.create_temp_file("test_version.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', str(path), '--version', '0.4.0']
            try:
                main()
            except SystemExit as e:
                # Will have warnings but should not crash
                pass

            output = sys.stdout.getvalue()
            self.assertIn("0.4.0", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_recursive_flag(self):
        """Test CLI with --recursive flag"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = """---
Title: Test
NRSPFormat: 0.4.0
---

## Section
"""
        # Create nested structure
        subdir = Path(self.temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "test.NRSP.md").write_text(content, encoding='utf-8')

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', '--directory', str(self.temp_dir), '--recursive']
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 0)

            output = sys.stdout.getvalue()
            self.assertIn("Summary:", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_cli_fix_fails_gracefully(self):
        """Test CLI --fix when fix fails"""
        import sys
        from io import StringIO
        from nrsp_validator import main

        content = "No frontmatter"
        path = self.create_temp_file("no_yaml.NRSP.md", content)

        # Mock sys.argv
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            sys.argv = ['nrsp_validator.py', str(path), '--fix']
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 1)

            output = sys.stdout.getvalue()
            self.assertIn("INVALID", output)
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout


class TestScriptExecution(unittest.TestCase):
    """Test running the script directly"""

    def test_script_runs_directly(self):
        """Test that script can be run directly"""
        import subprocess
        import sys

        # Create a temp file to validate
        temp_dir = tempfile.mkdtemp()
        test_file = Path(temp_dir) / "test.NRSP.md"
        test_file.write_text("""---
Title: Test
NRSPFormat: 0.4.0
---

## Section
""", encoding='utf-8')

        try:
            # Run the validator script directly
            result = subprocess.run(
                [sys.executable, "nrsp_validator.py", str(test_file)],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Should succeed (exit code 0)
            self.assertEqual(result.returncode, 0)
            self.assertIn("VALID", result.stdout)
        except subprocess.TimeoutExpired:
            self.skipTest("Script execution timed out")
        except FileNotFoundError:
            self.skipTest("nrsp_validator.py not found in current directory")


class TestExceptionHandling(unittest.TestCase):
    """Test exception handling with mocks"""

    def setUp(self):
        self.validator = NRSPValidator()
        self.temp_dir = tempfile.mkdtemp()

    def create_temp_file(self, filename, content):
        """Helper to create temporary test files"""
        path = Path(self.temp_dir) / filename
        path.write_text(content, encoding='utf-8')
        return path

    def test_validate_file_exception_in_content_read(self):
        """Test validation when file reading raises unexpected exception"""
        content = """---
Title: Test
---

## Section
"""
        path = self.create_temp_file("test.NRSP.md", content)

        # Mock Path.read_text to raise an exception
        with patch.object(Path, 'read_text', side_effect=IOError("Simulated IO error")):
            result = self.validator.validate_file(path)
            self.assertFalse(result.valid)
            self.assertTrue(any("error" in error.lower() for error in result.errors))

    def test_fix_file_exception_during_write(self):
        """Test fix_file when writing raises exception"""
        content = """---
Title: Test
---

## Section
"""
        path = self.create_temp_file("test.NRSP.md", content)

        # Mock write_text to raise an exception
        with patch.object(Path, 'write_text', side_effect=IOError("Simulated write error")):
            success = self.validator.fix_file(path, Version.V0_4)
            self.assertFalse(success)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)

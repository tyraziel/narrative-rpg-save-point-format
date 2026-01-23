#!/usr/bin/env python3
"""
Tests for NRSP Format Validator

Run with: python -m pytest test_nrsp_validator.py -v
Or: python test_nrsp_validator.py
"""

import unittest
import tempfile
from pathlib import Path
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


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)

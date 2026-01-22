#!/usr/bin/env python3
"""
NRSP Format Validator

Validates Narrative RPG Save Point Format files (.NRSP.md, .SLD.md, .CS.md, .LS.md, .NPC.md, .LGM.md)
with automatic version detection.

Version detection strategies:
1. Explicit FormatVersion field in YAML frontmatter (optional)
2. Filename patterns (e.g., v0.4.0, v0_4, v031)
3. Structural analysis (section headers, file extension references)
4. Default to latest version (0.4.0) if ambiguous

Usage:
    python nrsp_validator.py <file_path> [--version VERSION] [--strict]
    python nrsp_validator.py --directory <dir_path> [--recursive]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


class FileType(Enum):
    """NRSP file types"""
    NRSP = "NRSP"  # Narrative RPG Save Point
    SLD = "SLD"    # Session Log Document
    CS = "CS"      # Character Sheet
    LS = "LS"      # Location Sheet
    NPC = "NPC"    # Non-Player Character
    LGM = "LGM"    # Location Game Master Information


class Version(Enum):
    """Format versions"""
    V0_3 = "0.3"
    V0_4 = "0.4.0"
    UNKNOWN = "unknown"


@dataclass
class ValidationResult:
    """Result of validation"""
    valid: bool
    file_path: str
    file_type: Optional[FileType]
    detected_version: Optional[Version]
    errors: List[str]
    warnings: List[str]

    def __str__(self):
        status = "✓ VALID" if self.valid else "✗ INVALID"
        output = [f"{status}: {self.file_path}"]

        if self.file_type:
            output.append(f"  File Type: {self.file_type.value}")
        if self.detected_version:
            output.append(f"  Detected Version: {self.detected_version.value}")

        if self.warnings:
            output.append(f"  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                output.append(f"    ⚠ {warning}")

        if self.errors:
            output.append(f"  Errors ({len(self.errors)}):")
            for error in self.errors:
                output.append(f"    ✗ {error}")

        return "\n".join(output)


class NRSPValidator:
    """Validates NRSP format files"""

    # Version detection patterns
    VERSION_PATTERNS = [
        (re.compile(r'v?0[._-]?4[._-]?0'), Version.V0_4),
        (re.compile(r'v?0[._-]?4(?:[._-]0)?'), Version.V0_4),
        (re.compile(r'v?0[._-]?3[._-]?[0-9]*'), Version.V0_3),
    ]

    # File type detection
    FILE_EXTENSION_MAP = {
        '.NRSP.md': FileType.NRSP,
        '.SLD.md': FileType.SLD,
        '.CS.md': FileType.CS,
        '.LS.md': FileType.LS,
        '.L.md': FileType.LS,  # Alternate extension
        '.NPC.md': FileType.NPC,
        '.LGM.md': FileType.LGM,
        '.T.md': FileType.LS,  # v0.3 Town extension (maps to Location)
    }

    # Required YAML fields by file type (v0.4.0)
    REQUIRED_YAML_FIELDS = {
        FileType.NRSP: ['Title'],
        FileType.SLD: ['SessionLogTitle', 'SavePoint'],
        FileType.CS: ['Name'],
        FileType.LS: ['Name'],
        FileType.NPC: ['Name'],
        FileType.LGM: ['Name'],
    }

    # Optional YAML fields by file type (v0.4.0)
    OPTIONAL_YAML_FIELDS = {
        FileType.NRSP: ['System', 'PreviousSavePoint', 'NextSavePoint', 'AlternateNext',
                        'TimelineType', 'ArcID', 'TimelineNote', 'SLD', 'Tags', 'FormatVersion'],
        FileType.SLD: ['InGameDate', 'SessionDate', 'SessionDuration', 'SessionNumber',
                       'System', 'Tags', 'FormatVersion'],
        FileType.CS: ['Type', 'NPCSheet', 'System', 'IntroducedIn', 'CurrentAsOf',
                      'Supersedes', 'SupersededBy', 'Status', 'Tags', 'FormatVersion'],
        FileType.LS: ['Type', 'GMSheet', 'System', 'IntroducedIn', 'CurrentAsOf',
                      'Supersedes', 'SupersededBy', 'Status', 'Tags', 'FormatVersion'],
        FileType.NPC: ['Type', 'System', 'IntroducedIn', 'CurrentAsOf', 'Supersedes',
                       'SupersededBy', 'Status', 'Tags', 'FormatVersion'],
        FileType.LGM: ['Type', 'System', 'IntroducedIn', 'CurrentAsOf', 'Supersedes',
                       'SupersededBy', 'Status', 'Tags', 'FormatVersion'],
    }

    # Version-specific sections
    V0_4_SECTIONS = {
        FileType.NRSP: ['Party State', 'Linked Files'],  # New in v0.4
    }

    V0_3_INDICATORS = {
        'file_refs': ['.T.md'],  # Old town extension
    }

    def __init__(self, strict: bool = False):
        self.strict = strict

    def detect_file_type(self, file_path: Path) -> Optional[FileType]:
        """Detect file type from extension"""
        file_str = str(file_path)
        for ext, file_type in self.FILE_EXTENSION_MAP.items():
            if file_str.endswith(ext):
                return file_type
        return None

    def detect_version_from_filename(self, file_path: Path) -> Optional[Version]:
        """Detect version from filename"""
        filename = file_path.name
        for pattern, version in self.VERSION_PATTERNS:
            if pattern.search(filename):
                return version
        return None

    def detect_version_from_content(self, content: str, yaml_data: Dict) -> Optional[Version]:
        """Detect version from content structure"""
        # Check for explicit version field
        if 'FormatVersion' in yaml_data:
            version_str = str(yaml_data['FormatVersion'])
            if '0.4' in version_str or '0_4' in version_str:
                return Version.V0_4
            elif '0.3' in version_str or '0_3' in version_str:
                return Version.V0_3

        # Check for v0.3 indicators
        for indicator in self.V0_3_INDICATORS['file_refs']:
            if indicator in content:
                return Version.V0_3

        # Check for v0.4 sections
        for section in self.V0_4_SECTIONS.get(FileType.NRSP, []):
            if f"## {section}" in content or f"## 🧑‍🤝‍🧑 {section}" in content or f"## 🔗 {section}" in content:
                return Version.V0_4

        # Default to latest version
        return Version.V0_4

    def extract_yaml_frontmatter(self, content: str) -> Tuple[Optional[Dict], List[str]]:
        """Extract and parse YAML frontmatter"""
        errors = []

        # Check for frontmatter
        if not content.startswith('---'):
            errors.append("Missing YAML frontmatter (must start with '---')")
            return None, errors

        # Extract frontmatter content
        parts = content.split('---', 2)
        if len(parts) < 3:
            errors.append("Malformed YAML frontmatter (missing closing '---')")
            return None, errors

        yaml_content = parts[1].strip()

        # Parse YAML
        try:
            yaml_data = yaml.safe_load(yaml_content)
            if yaml_data is None:
                yaml_data = {}
            if not isinstance(yaml_data, dict):
                errors.append(f"YAML frontmatter must be a dictionary, got {type(yaml_data).__name__}")
                return None, errors
            return yaml_data, errors
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML syntax: {e}")
            return None, errors

    def validate_yaml_fields(self, yaml_data: Dict, file_type: FileType, version: Version) -> Tuple[List[str], List[str]]:
        """Validate YAML fields for the given file type and version"""
        errors = []
        warnings = []

        # Check required fields
        required_fields = self.REQUIRED_YAML_FIELDS.get(file_type, [])
        for field in required_fields:
            if field not in yaml_data:
                errors.append(f"Missing required YAML field: '{field}'")

        # Check for unknown fields (warning in non-strict mode, error in strict mode)
        if version == Version.V0_4:
            known_fields = set(required_fields + self.OPTIONAL_YAML_FIELDS.get(file_type, []))
            unknown_fields = set(yaml_data.keys()) - known_fields

            for field in unknown_fields:
                msg = f"Unknown YAML field: '{field}'"
                if self.strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)

        # Validate specific field types
        if 'TimelineType' in yaml_data:
            valid_types = ['Mainline', 'Branch', 'WhatIf']
            if yaml_data['TimelineType'] not in valid_types:
                errors.append(f"Invalid TimelineType: '{yaml_data['TimelineType']}' (must be one of {valid_types})")

        if 'Type' in yaml_data and file_type == FileType.CS:
            valid_types = ['PC', 'Companion', 'NPC', 'Entity']
            if yaml_data['Type'] not in valid_types:
                warnings.append(f"Unexpected character Type: '{yaml_data['Type']}' (common types: {valid_types})")

        return errors, warnings

    def validate_content_structure(self, content: str, file_type: FileType, version: Version) -> Tuple[List[str], List[str]]:
        """Validate content structure (sections, etc.)"""
        errors = []
        warnings = []

        # Extract body (after YAML frontmatter)
        parts = content.split('---', 2)
        if len(parts) < 3:
            return errors, warnings

        body = parts[2].strip()

        # Check that body is not empty
        if not body:
            if file_type == FileType.NRSP:
                errors.append("Save Point body is empty (must contain at least one section)")
            elif file_type == FileType.SLD:
                errors.append("Session Log body is empty (must contain at least one section)")

        # Check for at least one section header
        if body and not re.search(r'^##\s+', body, re.MULTILINE):
            warnings.append("No section headers found (recommend using '## Section Name' format)")

        # Check for common v0.4 NRSP sections
        if file_type == FileType.NRSP and version == Version.V0_4:
            if not re.search(r'##\s+.*Narrative Context', body, re.IGNORECASE):
                warnings.append("Missing recommended section: 'Narrative Context'")

        return errors, warnings

    def validate_file(self, file_path: Path, explicit_version: Optional[Version] = None) -> ValidationResult:
        """Validate a single NRSP file"""
        errors = []
        warnings = []

        # Check file exists
        if not file_path.exists():
            errors.append(f"File not found: {file_path}")
            return ValidationResult(False, str(file_path), None, None, errors, warnings)

        # Detect file type
        file_type = self.detect_file_type(file_path)
        if file_type is None:
            errors.append(f"Unknown file type (must end with .NRSP.md, .SLD.md, .CS.md, .LS.md, .NPC.md, or .LGM.md)")
            return ValidationResult(False, str(file_path), None, None, errors, warnings)

        # Read file
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"Error reading file: {e}")
            return ValidationResult(False, str(file_path), file_type, None, errors, warnings)

        # Extract YAML frontmatter
        yaml_data, yaml_errors = self.extract_yaml_frontmatter(content)
        errors.extend(yaml_errors)

        if yaml_data is None:
            return ValidationResult(False, str(file_path), file_type, None, errors, warnings)

        # Detect version
        detected_version = explicit_version
        if detected_version is None:
            detected_version = self.detect_version_from_filename(file_path)
        if detected_version is None:
            detected_version = self.detect_version_from_content(content, yaml_data)

        # Validate YAML fields
        field_errors, field_warnings = self.validate_yaml_fields(yaml_data, file_type, detected_version)
        errors.extend(field_errors)
        warnings.extend(field_warnings)

        # Validate content structure
        structure_errors, structure_warnings = self.validate_content_structure(content, file_type, detected_version)
        errors.extend(structure_errors)
        warnings.extend(structure_warnings)

        # Determine overall validity
        valid = len(errors) == 0

        return ValidationResult(valid, str(file_path), file_type, detected_version, errors, warnings)

    def validate_directory(self, dir_path: Path, recursive: bool = False) -> List[ValidationResult]:
        """Validate all NRSP files in a directory"""
        results = []

        # Find all NRSP files
        patterns = ['**/*.NRSP.md', '**/*.SLD.md', '**/*.CS.md', '**/*.LS.md',
                    '**/*.L.md', '**/*.NPC.md', '**/*.LGM.md', '**/*.T.md']

        files_to_validate = set()
        for pattern in patterns:
            if recursive:
                files_to_validate.update(dir_path.glob(pattern))
            else:
                files_to_validate.update(dir_path.glob(pattern.lstrip('**/')))

        # Validate each file
        for file_path in sorted(files_to_validate):
            result = self.validate_file(file_path)
            results.append(result)

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Validate Narrative RPG Save Point Format files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python nrsp_validator.py my_save_point.NRSP.md
  python nrsp_validator.py my_save_point.NRSP.md --version 0.4.0
  python nrsp_validator.py --directory ./examples --recursive
  python nrsp_validator.py my_save_point.NRSP.md --strict
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('file', nargs='?', type=Path, help='Path to NRSP file to validate')
    group.add_argument('--directory', '-d', type=Path, help='Validate all NRSP files in directory')

    parser.add_argument('--version', '-v', choices=['0.3', '0.4.0'], help='Explicitly specify format version')
    parser.add_argument('--strict', '-s', action='store_true', help='Strict mode (unknown fields are errors)')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively search directory for NRSP files')

    args = parser.parse_args()

    # Create validator
    validator = NRSPValidator(strict=args.strict)

    # Parse explicit version if provided
    explicit_version = None
    if args.version:
        explicit_version = Version.V0_4 if args.version == '0.4.0' else Version.V0_3

    # Validate
    if args.file:
        # Validate single file
        result = validator.validate_file(args.file, explicit_version)
        print(result)
        sys.exit(0 if result.valid else 1)

    elif args.directory:
        # Validate directory
        if not args.directory.is_dir():
            print(f"Error: Not a directory: {args.directory}", file=sys.stderr)
            sys.exit(1)

        results = validator.validate_directory(args.directory, args.recursive)

        if not results:
            print(f"No NRSP files found in {args.directory}")
            sys.exit(0)

        # Print results
        for result in results:
            print(result)
            print()

        # Print summary
        valid_count = sum(1 for r in results if r.valid)
        total_count = len(results)
        print(f"Summary: {valid_count}/{total_count} files valid")

        sys.exit(0 if valid_count == total_count else 1)


if __name__ == '__main__':
    main()

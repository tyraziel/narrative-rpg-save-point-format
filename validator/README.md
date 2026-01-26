# NRSP Format Validator

A Python validator for the Narrative RPG Save Point Format (NRSP) with automatic version detection.

## Features

- **Multi-format support**: Validates `.NRSP.md`, `.SLD.md`, `.CS.md`, `.LS.md`, `.NPC.md`, and `.LGM.md` files
- **Automatic version detection**: Detects format version (0.3, 0.4.0) from filename, content, or explicit declaration
- **Comprehensive validation**: Checks YAML frontmatter, required fields, section structure, and format compliance
- **Clear error reporting**: Provides detailed errors and warnings with file location context
- **Batch validation**: Validate entire directories recursively
- **Strict mode**: Optional strict validation for production use

## Version Detection Strategy

The validator uses multiple strategies to detect the format version:

1. **Explicit declaration**: `NRSPFormat` field in YAML frontmatter (recommended)
2. **Filename patterns**: Detects version from patterns like `v0.4.0`, `v0_4`, `v031`
3. **Structural analysis**:
   - Checks for v0.4-specific sections (Party State, Linked Files)
   - Detects v0.3 file references (`.T.md` vs `.LS.md`)
4. **Default**: Assumes latest version (0.4.0) if ambiguous

### NRSPFormat Field Behavior

- **Normal mode**: Missing `NRSPFormat` generates a **warning** (file is still valid)
- **Strict mode** (`--strict`): Missing `NRSPFormat` generates an **error** (file is invalid)
- **Fix mode** (`--fix`): Automatically adds `NRSPFormat` with the detected version

**Recommendation**: Always include `NRSPFormat` in your files to avoid ambiguity and ensure future compatibility.

## Installation

### Requirements

- Python 3.7+
- PyYAML

### Install dependencies

```bash
pip install pyyaml
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Validate a single file

```bash
python nrsp_validator.py my_save_point.NRSP.md
```

### Validate with explicit version

```bash
python nrsp_validator.py my_save_point.NRSP.md --version 0.4.0
```

### Validate all files in a directory

```bash
python nrsp_validator.py --directory ./examples
```

### Validate recursively

```bash
python nrsp_validator.py --directory ./my_campaign --recursive
```

### Strict mode (missing NRSPFormat and unknown fields are errors)

```bash
python nrsp_validator.py my_save_point.NRSP.md --strict
```

### Fix missing NRSPFormat fields

```bash
# Fix a single file
python nrsp_validator.py my_save_point.NRSP.md --fix

# Fix all files in a directory
python nrsp_validator.py --directory ./my_campaign --recursive --fix
```

## Output Examples

### Valid file

```
✓ VALID: examples/CLAUDE-040.NRSP.md
  File Type: NRSP
  Detected Version: 0.4.0
```

### File with warnings

```
✓ VALID: examples/my_save.NRSP.md
  File Type: NRSP
  Detected Version: 0.4.0
  Warnings (2):
    ⚠ Missing recommended field 'NRSPFormat' (detected version: 0.4.0)
    ⚠ Unknown YAML field: 'CustomField'
```

### Using --fix to add NRSPFormat

```bash
$ python nrsp_validator.py my_save.NRSP.md --fix
Fixing my_save.NRSP.md...
✓ Added NRSPFormat: 0.4.0
✓ VALID: my_save.NRSP.md
  File Type: NRSP
  Detected Version: 0.4.0
```

### Invalid file

```
✗ INVALID: examples/broken.NRSP.md
  File Type: NRSP
  Detected Version: 0.4.0
  Errors (2):
    ✗ Missing required YAML field: 'Title'
    ✗ Invalid TimelineType: 'Custom' (must be one of ['Mainline', 'Branch', 'WhatIf'])
```

### Directory validation summary

```
Summary: 15/17 files valid
```

## Validation Rules

### YAML Frontmatter

All NRSP files **must** start with YAML frontmatter:

```markdown
---
Title: My Save Point
---
```

#### Required fields by file type (v0.4.0)

- **NRSP**: `Title`
- **SLD**: `SessionLogTitle`, `SavePoint`
- **CS**: `Name`
- **LS**: `Name`
- **NPC**: `Name`
- **LGM**: `Name`

#### Recommended fields

- **NRSPFormat**: Format version (e.g., `0.4.0`). Highly recommended to avoid version ambiguity.

#### Optional fields

See the [specification files](./spec/) for complete lists of optional fields.

### Content Structure

- Files should contain at least one markdown section (`## Section Name`)
- NRSP files should include a "Narrative Context" section (warning if missing)
- Empty bodies trigger errors for NRSP and SLD files

### Field Validation

- `TimelineType`: Must be `Mainline`, `Branch`, or `WhatIf`
- Character `Type`: Should be `PC`, `Companion`, `NPC`, or `Entity` (warning for others)

## Command-Line Options

```
usage: nrsp_validator.py [-h] [--directory DIRECTORY] [--version {0.3,0.4.0}]
                         [--strict] [--recursive]
                         [file]

Validate Narrative RPG Save Point Format files

positional arguments:
  file                  Path to NRSP file to validate

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        Validate all NRSP files in directory
  --version {0.3,0.4.0}, -v {0.3,0.4.0}
                        Explicitly specify format version
  --strict, -s          Strict mode (missing NRSPFormat and unknown fields are errors)
  --recursive, -r       Recursively search directory for NRSP files
  --fix, -f             Automatically add NRSPFormat field to files missing it
```

## Exit Codes

- `0`: All files valid
- `1`: One or more files invalid or validation error

## Testing

### Run Tests

The validator includes a comprehensive test suite covering all functionality.

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest test_nrsp_validator.py -v

# Run with coverage report
python -m pytest test_nrsp_validator.py -v --cov=nrsp_validator --cov-report=term-missing

# Run tests using unittest directly
python test_nrsp_validator.py
```

### Test Coverage

The test suite includes 38 tests covering:
- Version detection (filename, content structure, explicit declaration)
- File type detection from extensions
- YAML frontmatter validation
- Content structure validation
- Full file validation (with and without NRSPFormat)
- Directory validation (recursive and non-recursive)
- Strict mode behavior (NRSPFormat enforcement)
- Auto-fix functionality (adding missing NRSPFormat)
- Error and warning reporting

## Integration

### CI/CD Integration

This project includes a GitHub Actions workflow (`.github/workflows/validate.yml`) that:
- Runs unit tests on Python 3.8-3.12
- Validates example files
- Lints code with flake8 and black

Add to your own project's GitHub Actions workflow:

```yaml
- name: Validate NRSP files
  run: |
    pip install pyyaml
    python nrsp_validator.py --directory ./campaign --recursive --strict
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python nrsp_validator.py --directory ./campaign --recursive --strict
```

### Make it executable

```bash
chmod +x .git/hooks/pre-commit
```

## Version-Specific Differences

### v0.3 → v0.4 Changes

- **File extensions**: `.T.md` (Town) → `.LS.md` (Location Sheet)
- **New sections**: Party State, Linked Files
- **New file types**: `.NPC.md`, `.LGM.md`
- **Character/Location linking**: Enhanced with `NPCSheet` and `GMSheet` fields

The validator automatically detects these differences and adjusts validation accordingly.

## Troubleshooting

### "Missing YAML frontmatter"

Ensure your file starts with `---` on the first line (no spaces or headers before it).

### "Unknown file type"

File must end with one of: `.NRSP.md`, `.SLD.md`, `.CS.md`, `.LS.md`, `.NPC.md`, `.LGM.md`

### "Unknown YAML field" warnings

These are informational in normal mode. Use `--strict` to treat them as errors.

## Contributing

Issues and improvements welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

Part of the Narrative RPG Save Point Format project.
Licensed under [CC BY 4.0](./LICENSE.md)

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

1. **Explicit declaration**: Optional `FormatVersion` field in YAML frontmatter
2. **Filename patterns**: Detects version from patterns like `v0.4.0`, `v0_4`, `v031`
3. **Structural analysis**:
   - Checks for v0.4-specific sections (Party State, Linked Files)
   - Detects v0.3 file references (`.T.md` vs `.LS.md`)
4. **Default**: Assumes latest version (0.4.0) if ambiguous

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

### Strict mode (unknown fields are errors)

```bash
python nrsp_validator.py my_save_point.NRSP.md --strict
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
  Warnings (1):
    ⚠ Unknown YAML field: 'CustomField'
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
  --strict, -s          Strict mode (unknown fields are errors)
  --recursive, -r       Recursively search directory for NRSP files
```

## Exit Codes

- `0`: All files valid
- `1`: One or more files invalid or validation error

## Integration

### CI/CD Integration

Add to your GitHub Actions workflow:

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

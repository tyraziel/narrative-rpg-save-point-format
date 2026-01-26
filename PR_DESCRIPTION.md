# Python Format Validator for NRSP

This PR adds a comprehensive Python validator for the Narrative RPG Save Point Format with automatic version detection.

## Summary

Implements a production-ready validator that checks NRSP format files (.NRSP.md, .SLD.md, .CS.md, .LS.md, .NPC.md, .LGM.md) with intelligent version detection and auto-fix capabilities.

## Key Features

### 🔍 Automatic Version Detection
The validator detects format versions using multiple strategies:
1. **Explicit declaration**: `NRSPFormat` field in YAML frontmatter (recommended)
2. **Filename patterns**: Detects from patterns like `v0.4.0`, `v0_4`, `v031`
3. **Structural analysis**: Checks for version-specific sections and file references
4. **Smart defaults**: Falls back to latest version (0.4.0) when ambiguous

### 📋 NRSPFormat Field (New)
- **Optional but recommended** - generates warning when missing
- **Required in strict mode** - generates error when missing  
- Added to spec documentation as optional field
- Updated examples to include `NRSPFormat: 0.4.0`

### 🔧 Auto-Fix Command
```bash
# Fix single file
python nrsp_validator.py my_save.NRSP.md --fix

# Fix entire campaign directory
python nrsp_validator.py --directory ./campaign --recursive --fix
```

### ✅ Comprehensive Validation
- YAML frontmatter structure and required fields
- Content structure (sections, body)
- Field value validation (TimelineType, etc.)
- Unknown field detection
- Clear error and warning messages

### 🧪 Full Test Suite
- **38 unit tests** covering all functionality
- Tests for version detection, YAML validation, file validation
- Tests for normal vs strict mode behavior
- Tests for --fix functionality
- All tests passing ✓

### 🔄 CI/CD Integration
- GitHub Actions workflow included
- Runs tests on Python 3.8-3.12
- Validates example files
- Linting with flake8 and black

## Files Added/Modified

**New Files:**
- `nrsp_validator.py` - Main validator implementation
- `test_nrsp_validator.py` - Comprehensive test suite
- `requirements.txt` - Runtime dependencies (PyYAML)
- `requirements-dev.txt` - Development dependencies
- `VALIDATOR_README.md` - Complete usage documentation
- `.github/workflows/validate.yml` - CI/CD pipeline
- `.gitignore` - Python artifacts
- `test_example.NRSP.md` - Example file with NRSPFormat

**Modified Files:**
- `spec/001_Narrative_RPG_Save_Point_Format_v0.4.0.NRSP.md` - Added NRSPFormat field documentation
- `examples/CLAUDE-040.NRSP.md` - Added NRSPFormat field
- `examples/CLAUDE-040.SLD.md` - Added NRSPFormat field

## Version Decision

**Staying at v0.4.0** - No version bump needed because:
- `NRSPFormat` is optional and backward-compatible
- Files without it still validate (with warning)
- No breaking changes to existing format

## Usage Examples

```bash
# Validate a single file
python nrsp_validator.py my_save.NRSP.md

# Validate with strict mode (NRSPFormat required)
python nrsp_validator.py my_save.NRSP.md --strict

# Validate entire campaign directory
python nrsp_validator.py --directory ./my_campaign --recursive

# Auto-fix missing NRSPFormat fields
python nrsp_validator.py --directory ./my_campaign --recursive --fix
```

## Testing

All tests pass:
```bash
python test_nrsp_validator.py
# Ran 38 tests in 0.022s
# OK
```

## Documentation

Complete documentation in `VALIDATOR_README.md` covering:
- Installation and dependencies
- Version detection strategy
- Usage examples
- Command-line options
- CI/CD integration
- Testing guide
- Troubleshooting

## Breaking Changes

None - fully backward compatible with existing v0.4.0 files.

## Next Steps

After merge, users can:
1. Install: `pip install pyyaml`
2. Run: `python nrsp_validator.py --directory ./examples --recursive --fix`
3. Integrate into CI/CD pipelines for automated validation

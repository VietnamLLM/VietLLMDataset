# VietLLMDataset Constitution

## Core Principles

### I. Local-First Architecture
All translation processing must occur locally without external API dependencies. The system must function completely offline, ensuring data privacy and security for sensitive academic content. No data shall be transmitted to external services during core translation operations.

### II. Quality-First Translation
Translation quality is paramount - accuracy must exceed 95% for academic content. Every translation must undergo quality validation with confidence scoring. Academic context and technical terminology must be preserved with cultural appropriateness for Vietnamese language.

### III. Test-First Development (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement. Red-Green-Refactor cycle strictly enforced. All translation components must have comprehensive test coverage including unit tests, integration tests, and quality validation tests.

### IV. Modular Design
Every component must be independently testable and self-contained. Translation engine, dataset loaders, and utilities must be modular with clear interfaces. New datasets and models must be easily extensible without modifying core translation logic.

### V. Performance & Resource Management
Translation speed must be < 2 seconds per question. Memory usage must be optimized for both GPU and CPU processing. Batch processing must be efficient with progress tracking. Resource monitoring and optimization are mandatory.

## Security & Privacy Requirements

### Data Protection
- All model weights and datasets must be stored locally
- No external API calls during translation operations
- User data must never leave the local environment
- Comprehensive logging without exposing sensitive content
- Access control for model weights and configuration files

### Academic Integrity
- Original dataset structure must be preserved
- Translation metadata must be maintained
- Quality assurance processes must be documented
- Academic context must be preserved in translations
- Cultural appropriateness for Vietnamese academic content

## Development Workflow

### Code Quality Standards
- All code must be well-documented with docstrings
- Type hints required for all functions and classes
- Code coverage must exceed 80%
- Performance benchmarks must be maintained
- Error handling must be comprehensive and graceful

### Review Process
- All PRs must include tests for new functionality
- Translation quality must be validated before merge
- Performance impact must be assessed
- Documentation must be updated for any API changes
- Security review required for any external dependencies

## Governance

### Constitution Authority
This constitution supersedes all other development practices and guidelines. All development decisions must align with these principles. Amendments require documentation, team approval, and migration plan for existing code.

### Compliance Requirements
- All PRs and code reviews must verify compliance with constitution principles
- Local-first architecture violations are non-negotiable
- Quality standards must be maintained or exceeded
- Performance benchmarks must be met or improved
- Security requirements must be strictly enforced

### Development Guidance
- Use `.specify/` folder for all specification documentation
- Follow the 5-phase development plan in `tasks.md`
- Maintain comprehensive logging and error handling
- Prioritize Vietnamese academic content quality
- Ensure offline operation capability at all times

### Amendment Process
- Constitution changes require team consensus
- Impact assessment required for all amendments
- Migration plan must be provided for breaking changes
- Documentation must be updated to reflect changes
- All stakeholders must be notified of amendments

**Version**: 1.0.0 | **Ratified**: 2024 | **Last Amended**: 2024
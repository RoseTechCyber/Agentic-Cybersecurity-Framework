# CONTRIBUTION GUIDE & PROJECT BOARDS

## 🤝 Contribution Framework

This document provides guidelines for contributing to the Agentic Cybersecurity Framework across all branches, aligned with ISO 27001, CIS, CISA, ISO 42001, and RMF 100.

---

## 📋 Contribution Types by Branch

### Branch: Integrated-Cybersecurity-Framework
**Focus**: Compliance frameworks, control mapping, assessment

#### ✅ Accepted Contributions:
- [ ] Add new compliance framework controls
- [ ] Create control mappings between frameworks
- [ ] Implement assessment engines
- [ ] Develop compliance reports
- [ ] Add evidence templates
- [ ] Enhance tech layer coverage

**Template**: `CONTRIB-INTEGRATED-FRAMEWORK.md`

```
Title: [Add/Enhance] {Framework} Controls
Description: 
- Framework: ISO 27001 / CIS / CISA / ISO 42001 / RMF
- Controls Added/Modified: A.5.1, A.6.2, ...
- Tech Layers Covered: Infrastructure, Platform, Application, Data
- Evidence Type: Documentation, Configuration, Testing

Files Changed:
- frameworks/{framework}/controls.json
- frameworks/{framework}/control_mappings.py
- control_registry/registry.py

Compliance Alignment:
- ISO 27001: A.5.1, A.6.2
- CIS Controls: CIS-1, CIS-2
- CISA Directives: BOD-22-01
- Frameworks Mapped: [List]

Evidence Provided:
- [ ] Control definition document
- [ ] Implementation procedures
- [ ] Testing procedures
- [ ] Evidence checklist
```

---

### Branch: Intelligent-Security-Research-Center
**Focus**: Threat intelligence, incident investigation, AI agents

#### ✅ Accepted Contributions:
- [ ] Add reasoning agents
- [ ] Implement threat detection algorithms
- [ ] Create incident correlation logic
- [ ] Develop anomaly detection models
- [ ] Add threat intelligence feeds
- [ ] Enhance forensic analysis

**Template**: `CONTRIB-RESEARCH-CENTER.md`

```
Title: [Add Agent/Feature] {Agent Name}
Description:
- Agent Type: Threat Intelligence / Incident Correlator / Anomaly Detector / Forensics / Predictor
- Reasoning Logic: [Describe]
- Data Sources: Web IQ / Work IQ / Foundry IQ / Security Tools
- Integration Points: CosmosDB / Milvus / Fabric

Implementation:
- src/agents/{agent_name}.py
- RAG Context: Describes retrieval augmented generation use
- Whitelist/Blacklist Integration: How it uses indicator lists
- Output Format: Structured threat intelligence case

Testing:
- [ ] Unit tests: 80%+ coverage
- [ ] Integration tests with CosmosDB
- [ ] Vector search test
- [ ] Mock data validation

Performance:
- [ ] Response time < 2s for standard queries
- [ ] Memory usage < 500MB
- [ ] Scalable to 1M events
```

---

### Branch: Intelligent-Security-eLearning-Management-System
**Focus**: Security awareness, training, competency management

#### ✅ Accepted Contributions:
- [ ] Add training modules
- [ ] Create awareness campaigns
- [ ] Develop competency assessments
- [ ] Implement role-based paths
- [ ] Add incident response simulations
- [ ] Enhance certification programs

**Template**: `CONTRIB-ELEARNING.md`

```
Title: [Add/Update] Training Module: {Topic}
Description:
- Module Type: Awareness / Certification / Skills / Compliance
- Framework Alignment: ISO 27001 / CIS / CISA / ISO 42001
- Target Audience: Developer / SysAdmin / Executive / Security Team
- Duration: XX hours
- Certification: Yes/No

Content:
- Video: [Link/File]
- Documentation: [Files]
- Labs: [Count and description]
- Assessment: [Type - Quiz/Practical/Capstone]

Competency Mapping:
- Role Competencies: [List]
- Skill Level: Beginner / Intermediate / Advanced / Expert
- Prerequisites: [Module names]

Effectiveness Metrics:
- [ ] Completion rate tracking
- [ ] Knowledge assessment scoring
- [ ] Skills validation
- [ ] Retention measurement
```

---

## 🎯 Contribution Quality Standards

### Code Quality Requirements

```yaml
Python Code:
  Style:
    - Follow PEP 8
    - Use type hints
    - Docstrings required
    - Max line length: 100
  
  Testing:
    - Minimum 80% code coverage
    - Unit tests required
    - Integration tests for external APIs
    - Mock data for testing
  
  Documentation:
    - README.md for new modules
    - Inline code comments
    - API documentation
    - Usage examples
  
  Security:
    - No hardcoded credentials
    - Input validation required
    - Sanitize logs
    - OWASP compliance

Data Quality:
  Structure:
    - Valid JSON/YAML
    - Schema validation
    - No null values without reason
  
  Mapping:
    - Framework controls properly mapped
    - Tech layer assignments verified
    - Duplicate detection
    - Consistency checks

Documentation:
  Completeness:
    - Clear description
    - Purpose and benefits
    - Implementation steps
    - Evidence requirements
  
  Accuracy:
    - Framework alignment verified
    - Tech layer coverage confirmed
    - Cross-references checked
    - Examples provided
```

### Review Checklist

```markdown
# Code Review Checklist

## Functionality
- [ ] Meets requirements
- [ ] No breaking changes
- [ ] Handles edge cases
- [ ] Error handling complete

## Code Quality
- [ ] Follows PEP 8
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] No code duplication

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Coverage >= 80%
- [ ] Test data adequate

## Documentation
- [ ] README updated
- [ ] Code comments clear
- [ ] API docs updated
- [ ] Examples provided

## Security
- [ ] No credentials exposed
- [ ] Input validated
- [ ] Logs sanitized
- [ ] Dependencies secure

## Framework Compliance
- [ ] Controls properly mapped
- [ ] Tech layers assigned
- [ ] Evidence templates included
- [ ] Framework alignment documented
```

---

## 📊 Project Boards Structure

### Board 1: INTEGRATED-CYBERSECURITY-FRAMEWORK-DEVELOPMENT

```
COLUMNS:
│
├─ BACKLOG
│  ├─ [ ] Load ISO 27001 Annex A (114 controls)
│  ├─ [ ] Load CIS Critical Controls v8.1 (20 controls)
│  ├─ [ ] Load CISA Binding Operational Directives
│  ├─ [ ] Load ISO 42001 AI Governance Controls
│  └─ [ ] Load RMF 100 Framework Phases
│
├─ READY FOR DEVELOPMENT
│  ├─ [ ] Framework data import utility
│  ├─ [ ] Control registry schema
│  ├─ [ ] Mapping engine for ISO27001→CIS
│  └─ [ ] Assessment engine initial version
│
├─ IN PROGRESS
│  ├─ [ ] @user-name Building control registry
│  ├─ [ ] @user-name Creating framework orchestrator
│  └─ [ ] @user-name Implementing gap analysis
│
├─ CODE REVIEW
│  ├─ [ ] PR #123 - Framework mappings
│  ├─ [ ] PR #124 - Assessment engine
│  └─ [ ] PR #125 - Reporting module
│
├─ IN TESTING
│  ├─ [ ] Framework data validation
│  ├─ [ ] Control mapping accuracy
│  └─ [ ] Tech layer coverage analysis
│
└─ DONE
   ├─ ✅ Control registry implementation
   ├─ ✅ Framework orchestrator
   └─ ✅ Basic assessment engine

LABELS:
- framework: iso27001, cis, cisa, iso42001, rmf
- component: control-registry, assessment, reporting, mapping
- priority: critical, high, medium, low
- size: small, medium, large
- status: ready, in-progress, review, testing, blocked
```

### Board 2: INTELLIGENT-SECURITY-RESEARCH-CENTER-DEVELOPMENT

```
COLUMNS:
│
├─ BACKLOG
│  ├─ [ ] Design threat intelligence agent
│  ├─ [ ] Design incident correlation agent
│  ├─ [ ] Design anomaly detection agent
│  ├─ [ ] Design forensic investigation agent
│  └─ [ ] Design predictive threat agent
│
├─ ARCHITECTURE REVIEW
│  ├─ [ ] Multi-agent reasoning architecture
│  ├─ [ ] RAG pipeline design
│  ├─ [ ] CosmosDB schema design
│  └─ [ ] Vector store integration
│
├─ IN DEVELOPMENT
│  ├─ [ ] @user-name Threat intelligence agent
│  ├─ [ ] @user-name Vector embedding pipeline
│  ├─ [ ] @user-name Whitelist/Blacklist manager
│  └─ [ ] @user-name RAG implementation
│
├─ INTEGRATION
│  ├─ [ ] CosmosDB integration testing
│  ├─ [ ] Milvus vector store testing
│  ├─ [ ] Ollama LLM integration
│  └─ [ ] Security tools connector testing
│
├─ PERFORMANCE TESTING
│  ├─ [ ] Latency optimization
│  ├─ [ ] Memory profiling
│  ├─ [ ] Throughput testing
│  └─ [ ] Scalability testing
│
└─ DEPLOYED
   ├─ ✅ Threat intelligence agent v1.0
   ├─ ✅ Basic RAG pipeline
   └─ ✅ Indicator management

LABELS:
- agent-type: threat-intel, correlator, anomaly, forensics, predictor
- data-source: web-iq, work-iq, foundry-iq, siem, edr
- priority: critical, high, medium, low
- component: agent, rag, vector-search, indicators
```

### Board 3: INTELLIGENT-SECURITY-ELEARNING-DEVELOPMENT

```
COLUMNS:
│
├─ CURRICULUM DESIGN
│  ├─ [ ] ISO 27001 certification path
│  ├─ [ ] CIS Controls training program
│  ├─ [ ] CISA security guidelines course
│  ├─ [ ] ISO 42001 AI governance training
│  └─ [ ] RMF framework training
│
├─ CONTENT DEVELOPMENT
│  ├─ [ ] @user-name ISO 27001 modules (5)
│  ├─ [ ] @user-name CIS Controls labs (8)
│  ├─ [ ] @user-name Phishing simulation
│  └─ [ ] @user-name Incident response drills
│
├─ ASSESSMENT CREATION
│  ├─ [ ] Knowledge assessment quizzes
│  ├─ [ ] Practical skills labs
│  ├─ [ ] Capstone projects
│  └─ [ ] Competency evaluations
│
├─ LMS INTEGRATION
│  ├─ [ ] Course catalog integration
│  ├─ [ ] Progress tracking
│  ├─ [ ] Certification management
│  └─ [ ] Reporting dashboard
│
├─ PILOT TESTING
│  ├─ [ ] User acceptance testing
│  ├─ [ ] Effectiveness measurement
│  ├─ [ ] Feedback collection
│  └─ [ ] Iteration planning
│
└─ PUBLISHED
   ├─ ✅ Awareness training modules
   ├─ ✅ Certification programs
   └─ ✅ Competency assessments

LABELS:
- framework: iso27001, cis, cisa, iso42001, rmf
- type: awareness, certification, skills, compliance
- audience: developer, sysadmin, executive, security
```

---

## 📋 PR Template

```markdown
# Pull Request

## Description
Brief description of changes

## Branch
- Branch: Integrated-Cybersecurity-Framework / Intelligent-Security-Research-Center / Intelligent-Security-eLearning-Management-System
- Related Issue: #[issue number]

## Changes Made
- [ ] Code changes
- [ ] Documentation updates
- [ ] Data additions
- [ ] Test additions

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Compliance enhancement
- [ ] Documentation
- [ ] Framework alignment

## Framework Alignment
- [ ] ISO 27001: [Controls]
- [ ] CIS Controls: [Controls]
- [ ] CISA: [Directives]
- [ ] ISO 42001: [Controls]
- [ ] RMF 100: [Phases]

## Tech Layer Impact
- [ ] Infrastructure
- [ ] Platform
- [ ] Application
- [ ] Data

## Quality Checklist
- [ ] Code follows PEP 8
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Security reviewed

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Test coverage >= 80%

## Screenshots/Evidence
[Add screenshots or evidence if applicable]

## Reviewers
@reviewer1 @reviewer2

## Merge Requirements
- [ ] Code review approved
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Framework compliance verified
```

---

## 🎓 Developer Onboarding

### Step 1: Setup Development Environment

```bash
# Clone repository
git clone https://github.com/RoseTechCyber/Agentic-Cybersecurity-Framework.git

# Create feature branch
git checkout -b feature/your-contribution-name

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install -r requirements-dev.txt
```

### Step 2: Choose Your Branch

```
Integrated-Cybersecurity-Framework
├─ For compliance framework work
├─ Add controls, mappings, assessments
└─ PR to this branch

Intelligent-Security-Research-Center
├─ For agent and threat intelligence work
├─ Add agents, detection, correlation
└─ PR to this branch

Intelligent-Security-eLearning-Management-System
├─ For training and awareness work
├─ Add courses, assessments, simulations
└─ PR to this branch
```

### Step 3: Make Your Contribution

Follow the contribution template for your chosen branch.

### Step 4: Validate Your Work

```bash
# Run tests
pytest tests/ -v --cov

# Format code
black src/

# Type checking
mypy src/

# Security scan
bandit -r src/

# Lint
flake8 src/
```

### Step 5: Submit Pull Request

1. Push to your branch: `git push origin feature/your-name`
2. Create PR with the PR template
3. Wait for review
4. Address feedback
5. Get approved and merge

---

## 🏆 Recognition & Incentives

### Contribution Levels

**🥉 Contributor (1-5 contributions)**
- Named in CONTRIBUTORS.md
- 'Contributor' badge on profile

**🥈 Active Contributor (6-15 contributions)**
- Monthly recognition in release notes
- 'Active Contributor' badge
- GitHub sponsor eligibility

**🥇 Core Contributor (16+ contributions)**
- Added to core team
- 'Core Contributor' badge
- Code review permissions
- Architecture decision input

**👑 Framework Owner**
- Maintains specific framework module
- Framework-level architecture decisions
- Direct merge privileges for reviews

---

## 📞 Support & Communication

### Channels
- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Security**: security@rosetech.com for vulnerabilities

### Review Timeline
- **Initial Response**: 24-48 hours
- **First Review**: 3-5 days
- **Approval to Merge**: 1-3 days (after approval)

### Escalation Path
1. Post in Issues/Discussions
2. Tag relevant maintainers
3. Email project lead
4. Request in community meeting

---

## 📚 Resources

- [ISO 27001 Official Standard](https://www.iso.org/isoiec-27001-information-security-management.html)
- [CIS Critical Controls](https://www.cisecurity.org/controls/)
- [CISA Security Directives](https://www.cisa.gov/resources-tools/directives/)
- [ISO 42001 AI Security](https://www.iso.org/iso-iec-42001-ai-management-system.html)
- [NIST RMF](https://csrc.nist.gov/projects/risk-management/risk-management-framework-(rmf)-overview)

---

## ✅ Contribution Workflow Example

### Example 1: Adding ISO 27001 Controls

```
1. Fork repository
2. Create branch: git checkout -b feature/iso27001-controls
3. Add controls to: frameworks/iso27001/controls.json
4. Create mapping: frameworks/iso27001/control_mappings.py
5. Add tests: tests/unit/test_iso27001.py
6. Update docs: docs/ISO27001-GUIDE.md
7. Run validation: python scripts/validate_controls.py
8. Create PR with template
9. Address review feedback
10. Merge when approved
```

### Example 2: Adding Reasoning Agent

```
1. Design agent architecture
2. Create agent file: src/agents/new_agent.py
3. Implement base_agent interface
4. Add RAG integration
5. Create tests: tests/integration/test_new_agent.py
6. Update: notebooks/new_agent_demo.ipynb
7. Performance test
8. Create PR with template
9. Integration testing
10. Merge and deploy
```

---

## 🔐 Security Contribution Guidelines

### Reporting Security Issues

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead:
1. Email: security@rosetech.com
2. Include: Description, impact, reproduction steps
3. Allow: 48 hours for initial response
4. Embargo: 90 days before public disclosure (if accepted)

### Security Review Checklist for Contributors

- [ ] No credentials/secrets in code
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] XSS prevention (if applicable)
- [ ] CSRF protection (if applicable)
- [ ] Authentication/authorization checked
- [ ] Sensitive data encrypted
- [ ] Audit logging included
- [ ] Dependencies scanned for vulnerabilities
- [ ] No known CVEs in dependencies


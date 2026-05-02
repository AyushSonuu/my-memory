---
name: spec-driven-dev
description: Interactive specification-driven development with research, planning, and implementation phases
version: 1.0.0
tags: [development, architecture, planning, solid, research]
---

# Spec-Driven Development Skill

An interactive, phased approach to implementing features based on specifications. This skill guides you through research, planning, and implementation while respecting SOLID principles and existing codebase patterns.

## Workflow Phases

### Phase 1: Specification & Research
**Goal**: Understand requirements and existing codebase patterns

1. **Gather Requirements**
   - Ask user for specification (can be OpenAPI spec, user story, feature description, or requirements doc)
   - Clarify any ambiguous requirements with interactive questions
   - Confirm scope and success criteria

2. **Research Codebase**
   - Use `research_codebase` skill to understand:
     - Existing patterns and architecture
     - Reusable components and utilities
     - Similar implementations
     - Database models and data access patterns
     - Authentication/authorization patterns
     - Testing patterns
   - Present findings to user with reuse opportunities

3. **Research Summary**
   - Show what can be reused vs. what needs to be created
   - Identify potential refactoring opportunities
   - Present architectural considerations

**User can**: Modify requirements, request deeper research, ask questions

---

### Phase 2: Planning
**Goal**: Create detailed implementation plan following SOLID principles

1. **Architecture Design**
   - Apply SOLID principles:
     - **S**ingle Responsibility: Each module has one reason to change
     - **O**pen/Closed: Open for extension, closed for modification
     - **L**iskov Substitution: Subtypes must be substitutable
     - **I**nterface Segregation: Many specific interfaces > one general
     - **D**ependency Inversion: Depend on abstractions, not concretions
   - Design modular, testable components
   - Plan for proper separation of concerns

2. **Create Plan with `create_plan`**
   - Break down into discrete tasks
   - Identify dependencies between tasks
   - Plan file structure (keep files under 300-400 lines)
   - Design data models
   - Plan API endpoints
   - Design service layer
   - Plan test coverage
   - Consider error handling and edge cases

3. **Present Plan to User**
   - Show complete implementation plan
   - Explain architectural decisions
   - Highlight reuse opportunities
   - Present trade-offs and alternatives

**User can**: 
- Review and modify the plan
- Request changes to architecture
- Ask for alternative approaches
- Go back to research phase
- Refine requirements
- Approve plan when satisfied

---

### Phase 3: Implementation
**Goal**: Implement the approved plan with user guidance

1. **Confirm Readiness**
   - Explicitly ask: "The plan is ready. Would you like me to implement it?"
   - Wait for user approval before proceeding
   - Confirm if user wants full implementation or step-by-step

2. **Execute with `implement_plan`**
   - Follow the approved plan exactly
   - Implement in logical order
   - Create modular, focused files
   - Write tests alongside implementation
   - Follow project coding standards (see `.claude/rules/`)

3. **User Control During Implementation**
   - User can pause implementation at any time
   - User can request modifications mid-implementation
   - User can skip certain tasks
   - User can request detailed explanation of any step

4. **Validation**
   - Run tests after implementation
   - Verify functionality works as specified
   - Check code quality and style
   - Present summary of changes

**User can**:
- Pause/resume implementation
- Request changes during implementation
- Go back to planning phase
- Request specific parts to be implemented first
- Skip or defer certain tasks

---

## Interactive Commands

Throughout the workflow, user can say:

- **"refine requirements"** → Go back to Phase 1, step 1
- **"research more about X"** → Deep dive into specific area
- **"show me alternative approaches"** → Present different architectural options
- **"modify the plan"** → Edit specific plan tasks
- **"implement X first"** → Change implementation order
- **"pause"** → Stop and wait for user guidance
- **"explain X"** → Detailed explanation of any decision
- **"go back"** → Return to previous phase
- **"start over"** → Restart from Phase 1

---

## Example Usage

### User provides OpenAPI Spec
```
User: "I have an OpenAPI spec for a new reports API. Can you help implement it?"

Skill Response:
1. "Let me review your spec. Could you share the OpenAPI file path?"
2. [Reviews spec] "I understand you need:
   - GET /api/reports - List reports
   - POST /api/reports - Create report
   - GET /api/reports/{id} - Get report details
   
   Before we proceed, I have some clarification questions:
   - Should reports be tenant-scoped?
   - What authentication method (IAS tokens)?
   - Any pagination requirements?"
3. [After clarification] "Great! Let me research the codebase to understand existing patterns..."
4. [Uses research_codebase] "I found:
   - Similar endpoint patterns in apis/chat_routes.py
   - Reusable auth middleware in apis/middleware/
   - Report data models already exist in data_access/entities/
   
   Shall I proceed to create a detailed plan?"
5. [User: "Yes"] [Uses create_plan to generate implementation plan]
6. [Presents plan] "Here's the implementation plan... Would you like to modify anything?"
7. [User approves] "Perfect! Shall I implement the plan now, or would you like to proceed step-by-step?"
```

### User provides User Story
```
User: "As a user, I want to export my reports to PDF so I can share them offline."

Skill Response:
1. "Let me clarify the requirements:
   - Should this work for all report types?
   - Any specific PDF formatting requirements?
   - Should this be async (background job) or synchronous?"
2. [After clarification] "Researching existing export functionality..."
3. [Uses research_codebase] "Found:
   - Existing PDF generation in orchestration/tools/pdf_tool.py
   - Background job pattern in orchestration/workflows/
   - Blob storage for file handling
   
   We can reuse most of this! Shall I create a plan?"
4. [Creates plan] "Here's how we'll implement it... What do you think?"
5. [User: "Can we add email notification when PDF is ready?"]
6. [Modifies plan] "Updated plan to include email notifications. Ready to implement?"
```

---

## SOLID Principles Applied

### Single Responsibility
- **Routes**: Handle HTTP request/response only
- **Services**: Business logic
- **Repositories**: Data access
- **Models**: Data structure

Example structure:
```
apis/
  reports_routes.py          # HTTP layer only
orchestration/
  workflows/
    report_generation.py     # Orchestration logic
data_access/
  entities/
    report_handler.py        # Data access
  models/
    report.py                # Data models
tests/
  apis/test_reports_routes.py
  orchestration/test_report_generation.py
```

### Open/Closed Principle
- Use abstract base classes for extensibility
- Plugin-style architectures
- Strategy patterns for varying behaviors

### Liskov Substitution
- Ensure derived classes honor base class contracts
- Use proper inheritance hierarchies

### Interface Segregation
- Create focused, specific interfaces
- Don't force clients to depend on unused methods

### Dependency Inversion
- Depend on abstractions (interfaces/protocols)
- Inject dependencies rather than hardcode
- Use dependency injection patterns

---

## Best Practices Enforced

### Code Organization
- Files under 300-400 lines (split if larger)
- One class per file (with exceptions for closely related classes)
- Clear separation: routes → services → data access
- Tests colocated with functionality

### Testing
- Write tests alongside implementation
- Unit tests for business logic
- Integration tests for database operations
- API tests for endpoints
- Mock external dependencies

### Security
- Follow `.claude/rules/security.md`
- Validate all inputs
- Enforce tenant isolation
- Never hardcode secrets
- Parameterized queries only

### Data Privacy
- Follow `.claude/rules/data-privacy.md`
- Never log PII
- Implement data retention
- Support GDPR rights (export, delete)
- Multi-tenant data isolation

### Code Style
- Follow `.claude/rules/coding-style.md`
- No emojis in code
- No console.logs
- Professional error messages
- Modular over monolithic

---

## Phase Transitions

The skill always confirms before moving to next phase:

**Research → Planning**:
```
"I've completed the codebase research. Here's what I found:
[Summary of findings]

Would you like me to:
1. Research more (specify what)
2. Proceed to planning phase
3. Refine requirements"
```

**Planning → Implementation**:
```
"The implementation plan is ready:
[Plan summary]

What would you like to do?
1. Review/modify the plan
2. Ask questions about the approach
3. See alternative solutions
4. Approve and start implementation
5. Go back to research"
```

**During Implementation**:
```
"I've implemented tasks 1-3 of 10:
[Summary of what's done]

Continue with remaining tasks, or would you like to:
1. Pause and review current progress
2. Modify upcoming tasks
3. Implement specific task next
4. Continue automatically"
```

---

## Error Recovery

If anything goes wrong:

1. **Plan doesn't work**: "I notice the plan has issues. Let me revise it..."
2. **Implementation fails**: "Implementation hit an issue. Options:
   - Fix and continue
   - Revise plan
   - Try alternative approach"
3. **User changes mind**: "No problem! Let's go back to [phase] and adjust."

---

## Skill Invocation

Invoke this skill when user wants to:
- Implement from OpenAPI/AsyncAPI spec
- Build feature from user story
- Implement technical specification
- Add new endpoints/services
- Refactor existing functionality
- Build new system component

**Examples**:
- "Help me implement this OpenAPI spec"
- "I want to add a new feature based on this spec"
- "Can you help design and implement X?"
- "I have requirements for a new API"
- "I need to refactor the reports module"

---

## Output Quality

Every deliverable includes:

✅ **Code**:
- Modular, focused files
- SOLID principles applied
- Proper error handling
- Type hints
- Docstrings

✅ **Tests**:
- Unit tests
- Integration tests
- Edge case coverage
- Mocked external dependencies

✅ **Documentation**:
- API documentation
- Code comments (where needed)
- Architecture decisions recorded
- Usage examples

✅ **Quality Checks**:
- No hardcoded secrets
- No PII in logs
- Input validation
- Tenant isolation
- No console.logs
- No emojis

---

## Success Criteria

Implementation is complete when:
1. ✅ All planned tasks implemented
2. ✅ All tests passing
3. ✅ Code follows project standards
4. ✅ Security rules followed
5. ✅ Data privacy rules followed
6. ✅ User has reviewed and approved
7. ✅ Documentation updated

---

## Remember

> **This skill is user-driven. Never force progression to next phase. Always wait for user approval before implementing. The user is in control at every step.**
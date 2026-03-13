## ADDED Requirements

### Requirement: List all tags
The system SHALL return all available tags via `GET /api/tags`. No authentication required. Tags are derived from tags associated with articles.

**Response 200**: `{"tags": list[str]}`

#### Scenario: Get tags when tags exist
- **WHEN** a user requests `GET /api/tags` and articles have associated tags
- **THEN** the system returns 200 with a list of all unique tag strings

#### Scenario: Get tags when no tags exist
- **WHEN** a user requests `GET /api/tags` and no tags exist in the system
- **THEN** the system returns 200 with an empty list `{"tags": []}`

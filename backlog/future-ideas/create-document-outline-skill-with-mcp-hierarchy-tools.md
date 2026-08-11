# Create a Document Outline Skill with MCP Hierarchy Tools

## Synopsis

Consider a portable Skill that helps an Agent turn explicitly selected source material into a document outline through the configured MCP hierarchy tools and make targeted changes without rebuilding the whole outline.

## Origin

This was previously the Ready Work Item create-document-outlines-with-mcp-hierarchy-tools. On 2026-08-11, the user deferred it because delivering another bundled Skill currently costs more effort than its priority justifies.

## Notes

If revisited, keep the model responsible for selecting the document structure and call the configured MCP hierarchy operations directly. Do not add a document-specific helper, renderer, adapter, or Python-library fallback.

## Revisit Trigger

Reconsider when document outlining becomes a recurring need whose value justifies full bundled-Skill delivery and maintenance.

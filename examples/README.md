# PolicyIQ Examples

This directory contains example files and sample questions for testing PolicyIQ.

## Sample Questions

The `sample_questions.txt` file contains a comprehensive list of example questions covering:
- GDPR compliance
- PCI-DSS requirements
- SOC2 controls
- Data residency policies
- Encryption standards
- Access control
- Incident response

## Sample PDFs

To test PolicyIQ, you can upload sample regulatory documents such as:
- GDPR regulation documents
- PCI-DSS compliance guides
- SOC2 control descriptions
- Internal bank policy documents

Note: Due to copyright restrictions, actual regulatory documents are not included in this repository. Please obtain official documents from:
- GDPR: https://gdpr-info.eu/
- PCI-DSS: https://www.pcisecuritystandards.org/
- SOC2: Official documentation from AICPA

## Testing Workflow

1. Upload sample PDF documents using the upload interface
2. Wait for documents to be processed (status will show as "processing" then "completed")
3. Use the chat interface to ask questions from `sample_questions.txt`
4. Review answers, citations, and confidence scores
5. Check audit logs to see the full interaction history

## Example Interaction

**Question:** "What does PCI-DSS require for cardholder encryption?"

**Expected Answer Format:**
- Direct answer about encryption requirements
- Explanation with context
- Citations to specific PCI-DSS sections
- Confidence score
- Manual review flag if confidence is low

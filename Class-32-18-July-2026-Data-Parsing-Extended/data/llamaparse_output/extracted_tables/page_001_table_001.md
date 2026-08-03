| Section               | Parsing challenge                                      | Why it matters for RAG                  |
| --------------------- | ------------------------------------------------------ | --------------------------------------- |
| Contracts             | Dense legal text, clause numbers, cross<br/>references | Need section-aware chunks and citations |
| Tables                | Merged headers, numeric columns,<br/>footnotes         | Need row/column preservation            |
| Images                | Architecture diagram, heatmap, scanned<br/>form        | Need OCR or multimodal extraction       |
| Multi-tenant metadata | client\_id, document\_id,<br/>contract\_group\_id      | Need access-safe retrieval              |
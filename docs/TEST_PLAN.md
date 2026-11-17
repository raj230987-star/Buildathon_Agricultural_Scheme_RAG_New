# வேளாண்மை தோழன் AI – Test Plan

## 1. Objective

The objective of this test plan is to verify the functionality, reliability, retrieval quality, and usability of வேளாண்மை தோழன் AI, an AI-powered Agricultural Government Schemes Assistant.

## 2. Testing Scope

Testing covers the following implemented components:

- PDF upload and text extraction
- Document chunking and embedding generation
- Original FAISS vector database
- Multilingual FAISS vector database
- BM25 keyword retrieval
- Hybrid retrieval and Reciprocal Rank Fusion (RRF)
- Tamil query translation and multilingual retrieval
- Context-aware question answering
- Evidence validation
- Source document and page citations
- FastAPI backend
- Streamlit frontend
- Duplicate PDF detection

Farmer profile management and automated eligibility assessment are outside the current implementation scope.

## 3. Functional Test Cases

| Test ID | Test Scenario | Expected Result |
|---|---|---|
| TC-001 | Upload a valid PDF | PDF uploaded and processed successfully |
| TC-002 | Extract PDF text | Text and page information extracted |
| TC-003 | Generate embeddings | Document embeddings generated |
| TC-004 | Original FAISS indexing | Document chunks added to original FAISS database |
| TC-005 | Multilingual FAISS indexing | Document chunks added to multilingual FAISS database |
| TC-006 | Upload duplicate PDF | Duplicate detected and no additional vectors added |
| TC-007 | BM25 keyword retrieval | Relevant keyword matches retrieved |
| TC-008 | Hybrid retrieval | FAISS and BM25 results combined |
| TC-009 | RRF ranking | Combined retrieval results ranked |
| TC-010 | Ask an English scheme question | Relevant answer generated |
| TC-011 | Ask a Tamil scheme question | Tamil query processed and answer generated in Tamil |
| TC-012 | Ask a follow-up question | Conversation context considered |
| TC-013 | Verify citations | Source document and page references displayed |
| TC-014 | Ask an unsupported question | System indicates insufficient supporting information |
| TC-015 | Ask an unrelated question | System avoids presenting unsupported scheme information |
| TC-016 | Upload through Streamlit | Upload processed and both database counts updated |

## 4. API Testing

The following FastAPI endpoints are included in testing:

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Application information |
| `/health` | GET | Backend health status |
| `/upload-pdf` | POST | Upload and process PDF |
| `/search` | POST | Search indexed documents |
| `/ask` | POST | Generate answers using RAG |

Verify successful responses, request validation, duplicate handling, and error handling.

## 5. Retrieval and RAG Evaluation

The following areas are considered during retrieval and answer testing:

- Semantic retrieval relevance
- BM25 keyword retrieval
- Hybrid retrieval results
- RRF ranking
- Tamil-to-English query translation
- Answer relevance
- Evidence support
- Citation correctness
- Follow-up question context

Cross-language embedding tests were performed using sample Tamil and English queries.

Formal precision, recall, and benchmark-based evaluation have not yet been completed.

## 6. User Interface Testing

Verify:

- Dashboard navigation
- Backend connection status
- English and Tamil question input
- Answer display
- Source citation display
- PDF upload interface
- Duplicate upload notification
- Original FAISS vector count
- Multilingual FAISS vector count
- Application branding and layout

## 7. Acceptance Criteria

The application is considered ready for its current functional demonstration when:

1. Valid PDF documents can be uploaded and processed.
2. Duplicate PDFs are detected.
3. Both FAISS databases are updated successfully.
4. Hybrid retrieval returns relevant passages.
5. Answers are generated using retrieved document context.
6. Tamil queries receive Tamil responses.
7. Source documents and page references are displayed.
8. Unsupported questions are handled safely.
9. Backend API and frontend functions operate successfully.

## 8. Test Execution Record

| Test Area | Status | Remarks |
|---|---|---|
| Backend health check | PASS | Backend connection verified |
| PDF upload | PASS | PDF uploaded through application |
| PDF text extraction | PASS | Text and page information extracted |
| Original FAISS indexing | PASS | Vector database updated |
| Multilingual FAISS indexing | PASS | Vector database updated |
| Duplicate PDF detection | PASS | Duplicate upload rejected without adding vectors |
| BM25 retrieval | PASS | Keyword retrieval tested |
| Hybrid retrieval and RRF | PASS | Combined retrieval tested |
| English question answering | PASS | Relevant answer and citation received |
| Tamil question answering | PASS | Tamil response and citation received |
| Follow-up question handling | PASS | Conversation history integrated |
| Evidence validation | PASS | Tested with supported and unsupported questions |
| Source citations | PASS | Source filename and page references verified |
| Streamlit dashboard | PASS | Navigation and display tested |
| Frontend PDF upload | PASS | Upload and database count updates verified |
| Invalid PDF testing | NOT TESTED | Separate execution required |
| Performance benchmarking | NOT TESTED | Processing and response times not measured |
| Formal RAG evaluation | NOT TESTED | Benchmark dataset and metrics not completed |

## 9. Known Limitations

- The source knowledge base is primarily English.
- Tamil queries are translated for retrieval; this does not mean all source documents contain Tamil explanations.
- Evidence validation uses an AI-based review and is not a formal guarantee of factual correctness.
- Retrieval may return less relevant passages for unrelated or broad questions.
- Formal performance benchmarking and quantitative RAG evaluation remain future work.

## 10. Conclusion

The core PDF ingestion, dual FAISS indexing, hybrid retrieval, Tamil query handling, evidence-based answer generation, citation display, and Streamlit frontend workflows have been functionally tested.

Further testing is required for performance benchmarking, invalid-file handling, and formal retrieval evaluation.
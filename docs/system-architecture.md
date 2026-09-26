# System Architecture

```text
React UI → typed fetch services → FastAPI routes → domain services → repositories → SQLAlchemy → PostgreSQL
                                      ↓
                              DocumentService → OCRProvider
```

Routes translate HTTP requests and responses. Pydantic schemas validate boundary data. Services coordinate rules and use cases. Repositories isolate expense persistence. SQLAlchemy models own relationships. `OCRProvider` is an interface implemented by `MockOCRProvider`; future Tesseract or cloud implementations can be injected without route changes.

Uploads are local for development. This is a deliberate MVP limitation, not a production storage design.


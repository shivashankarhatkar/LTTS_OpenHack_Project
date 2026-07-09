@echo off
REM ============================================================
REM  Enterprise Knowledge Assistant - Project Scaffold (CMD)
REM  Idempotent: safe to run multiple times.
REM  Aligned with approved roadmap (SQL Agent + RBAC granularity removed).
REM ============================================================
setlocal

echo Creating directory structure...

REM ---- Root-level dirs ----
for %%D in (
  app
  app\api app\api\v1
  app\core app\core\config
  app\connectors
  app\ingestion app\ingestion\parsers app\ingestion\processing app\ingestion\chunking app\ingestion\metadata
  app\extraction app\extraction\entities app\extraction\relationships app\extraction\claims app\extraction\policies
  app\ontology
  app\resolution
  app\knowledge_graph app\knowledge_graph\neo4j
  app\vector_store app\vector_store\chromadb
  app\embeddings
  app\retrieval app\retrieval\graph app\retrieval\vector app\retrieval\keyword app\retrieval\fusion app\retrieval\rerank
  app\graphrag
  app\orchestration app\orchestration\langgraph app\orchestration\agents
  app\memory
  app\security
  app\evaluation
  app\services
  app\models
  app\schemas
  app\utils
  app\workers
  app\pipelines
  frontend frontend\static frontend\static\css frontend\static\js frontend\templates
  tests tests\unit tests\integration tests\e2e
  docker
  docs
  scripts
  config
  data data\uploads data\chroma
) do (
  if not exist "%%D" (
    mkdir "%%D"
    echo   + %%D
  )
)

echo.
echo Creating files...

REM ---- App root ----
call :mk app\__init__.py
call :mk app\main.py

REM ---- API ----
call :mk app\api\__init__.py
call :mk app\api\dependencies.py
call :mk app\api\v1\__init__.py
call :mk app\api\v1\router.py
call :mk app\api\v1\health.py
call :mk app\api\v1\ingestion.py
call :mk app\api\v1\chat.py
call :mk app\api\v1\search.py
call :mk app\api\v1\graph.py
call :mk app\api\v1\auth.py

REM ---- Core / Config ----
call :mk app\core\__init__.py
call :mk app\core\config\__init__.py
call :mk app\core\config\settings.py
call :mk app\core\logging_config.py
call :mk app\core\exceptions.py
call :mk app\core\container.py

REM ---- Connectors ----
call :mk app\connectors\__init__.py
call :mk app\connectors\neo4j_connector.py
call :mk app\connectors\chroma_connector.py
call :mk app\connectors\gemini_connector.py

REM ---- Ingestion ----
call :mk app\ingestion\__init__.py
call :mk app\ingestion\ingestion_service.py
call :mk app\ingestion\parsers\__init__.py
call :mk app\ingestion\parsers\base_parser.py
call :mk app\ingestion\parsers\parser_factory.py
call :mk app\ingestion\parsers\txt_parser.py
call :mk app\ingestion\parsers\pdf_parser.py
call :mk app\ingestion\parsers\docx_parser.py
call :mk app\ingestion\parsers\pptx_parser.py
call :mk app\ingestion\parsers\excel_parser.py
call :mk app\ingestion\parsers\html_parser.py
call :mk app\ingestion\parsers\ocr_parser.py
call :mk app\ingestion\processing\__init__.py
call :mk app\ingestion\processing\cleaner.py
call :mk app\ingestion\processing\language_detector.py
call :mk app\ingestion\chunking\__init__.py
call :mk app\ingestion\chunking\base_chunker.py
call :mk app\ingestion\chunking\fixed_chunker.py
call :mk app\ingestion\chunking\semantic_chunker.py
call :mk app\ingestion\metadata\__init__.py
call :mk app\ingestion\metadata\metadata_extractor.py

REM ---- Extraction ----
call :mk app\extraction\__init__.py
call :mk app\extraction\entities\__init__.py
call :mk app\extraction\entities\entity_extractor.py
call :mk app\extraction\relationships\__init__.py
call :mk app\extraction\relationships\relationship_extractor.py
call :mk app\extraction\claims\__init__.py
call :mk app\extraction\claims\claim_extractor.py
call :mk app\extraction\policies\__init__.py
call :mk app\extraction\policies\policy_extractor.py

REM ---- Ontology / Resolution ----
call :mk app\ontology\__init__.py
call :mk app\ontology\ontology_mapper.py
call :mk app\ontology\schema.py
call :mk app\resolution\__init__.py
call :mk app\resolution\entity_resolver.py

REM ---- Knowledge Graph ----
call :mk app\knowledge_graph\__init__.py
call :mk app\knowledge_graph\graph_builder.py
call :mk app\knowledge_graph\graph_repository.py
call :mk app\knowledge_graph\neo4j\__init__.py
call :mk app\knowledge_graph\neo4j\neo4j_repository.py
call :mk app\knowledge_graph\neo4j\cypher_queries.py

REM ---- Vector Store ----
call :mk app\vector_store\__init__.py
call :mk app\vector_store\vector_repository.py
call :mk app\vector_store\chromadb\__init__.py
call :mk app\vector_store\chromadb\chroma_repository.py

REM ---- Embeddings ----
call :mk app\embeddings\__init__.py
call :mk app\embeddings\base_embedder.py
call :mk app\embeddings\sentence_transformer_embedder.py

REM ---- Retrieval ----
call :mk app\retrieval\__init__.py
call :mk app\retrieval\base_retriever.py
call :mk app\retrieval\hybrid_retriever.py
call :mk app\retrieval\graph\__init__.py
call :mk app\retrieval\graph\graph_retriever.py
call :mk app\retrieval\vector\__init__.py
call :mk app\retrieval\vector\vector_retriever.py
call :mk app\retrieval\keyword\__init__.py
call :mk app\retrieval\keyword\keyword_retriever.py
call :mk app\retrieval\fusion\__init__.py
call :mk app\retrieval\fusion\context_fusion.py
call :mk app\retrieval\rerank\__init__.py
call :mk app\retrieval\rerank\reranker.py

REM ---- GraphRAG ----
call :mk app\graphrag\__init__.py
call :mk app\graphrag\graphrag_service.py
call :mk app\graphrag\context_builder.py
call :mk app\graphrag\prompt_builder.py
call :mk app\graphrag\answer_generator.py
call :mk app\graphrag\citation_builder.py
call :mk app\graphrag\confidence_scorer.py
call :mk app\graphrag\hallucination_guard.py

REM ---- Orchestration (LangGraph + Agents) ----
call :mk app\orchestration\__init__.py
call :mk app\orchestration\langgraph\__init__.py
call :mk app\orchestration\langgraph\graph_state.py
call :mk app\orchestration\langgraph\workflow.py
call :mk app\orchestration\agents\__init__.py
call :mk app\orchestration\agents\base_agent.py
call :mk app\orchestration\agents\router_agent.py
call :mk app\orchestration\agents\graph_qa_agent.py
call :mk app\orchestration\agents\document_qa_agent.py
call :mk app\orchestration\agents\summarization_agent.py
call :mk app\orchestration\agents\citation_agent.py
call :mk app\orchestration\agents\validation_agent.py

REM ---- Memory ----
call :mk app\memory\__init__.py
call :mk app\memory\base_memory.py
call :mk app\memory\conversation_memory.py
call :mk app\memory\institutional_memory.py

REM ---- Security ----
call :mk app\security\__init__.py
call :mk app\security\auth_service.py
call :mk app\security\jwt_handler.py
call :mk app\security\password_hasher.py
call :mk app\security\audit_logger.py

REM ---- Evaluation ----
call :mk app\evaluation\__init__.py
call :mk app\evaluation\evaluator.py
call :mk app\evaluation\metrics.py

REM ---- Services ----
call :mk app\services\__init__.py
call :mk app\services\health_service.py
call :mk app\services\chat_service.py
call :mk app\services\search_service.py

REM ---- Models ----
call :mk app\models\__init__.py
call :mk app\models\document.py
call :mk app\models\chunk.py
call :mk app\models\entity.py
call :mk app\models\relationship.py
call :mk app\models\user.py
call :mk app\models\conversation.py

REM ---- Schemas ----
call :mk app\schemas\__init__.py
call :mk app\schemas\health.py
call :mk app\schemas\ingestion.py
call :mk app\schemas\chat.py
call :mk app\schemas\search.py
call :mk app\schemas\auth.py

REM ---- Utils ----
call :mk app\utils\__init__.py
call :mk app\utils\text_utils.py
call :mk app\utils\file_utils.py
call :mk app\utils\id_utils.py

REM ---- Workers / Pipelines ----
call :mk app\workers\__init__.py
call :mk app\workers\ingestion_worker.py
call :mk app\pipelines\__init__.py
call :mk app\pipelines\ingestion_pipeline.py
call :mk app\pipelines\indexing_pipeline.py

REM ---- Frontend ----
call :mk frontend\index.html
call :mk frontend\static\css\styles.css
call :mk frontend\static\js\app.js
call :mk frontend\templates\.gitkeep

REM ---- Tests ----
call :mk tests\__init__.py
call :mk tests\conftest.py
call :mk tests\unit\__init__.py
call :mk tests\unit\test_health.py
call :mk tests\integration\__init__.py
call :mk tests\e2e\__init__.py

REM ---- Docker ----
call :mk docker\Dockerfile
call :mk docker\docker-compose.yml
call :mk docker\.dockerignore

REM ---- Docs ----
call :mk docs\ARCHITECTURE.md
call :mk docs\INSTALLATION.md
call :mk docs\API.md

REM ---- Scripts ----
call :mk scripts\run_dev.bat
call :mk scripts\seed_data.py

REM ---- Config ----
call :mk config\logging.yaml

REM ---- Root files ----
call :mk requirements.txt
call :mk .env.example
call :mk .gitignore
call :mk pyproject.toml
call :mk README.md
call :mk Dockerfile
call :mk docker-compose.yml

REM ---- Keep data dirs tracked ----
call :mk data\uploads\.gitkeep
call :mk data\chroma\.gitkeep

echo.
echo Done. Open this folder in VS Code:  code .
endlocal
goto :eof

REM ============================================================
REM  :mk  -> create an empty file only if it does not exist
REM  Uses >> so re-runs never truncate existing content.
REM ============================================================
:mk
if not exist "%~1" (
  type nul >> "%~1"
  echo   + %~1
)
goto :eof
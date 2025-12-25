# Volunteer-First Operating System (Prototype)

## Overview
This project demonstrates a Shadow Source of Truth built from noisy,
human-generated volunteer data and AI-assisted enrichment.

## Architecture
CSV → ETL normalization → AI enrichment → SQLite truth layer → Query-ready schema

## AI Enrichment
- Prompt-driven extraction (config-based YAML)
- Outputs: skills, persona, confidence score
- Low-confidence flagging (<0.6)
- Versioned persona records

## Database Design
Normalized tables for members, skills, personas, and ingestion metadata.

## How to Run
pip install -r requirements.txt  
python main.py

## Assumptions & Limitations
- LLM calls are mocked due to time constraints
- Confidence is heuristic
- Persona labels are subjective

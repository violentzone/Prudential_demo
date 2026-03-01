# 📰 News Intelligence Agentic System

A production-style agentic pipeline built with **Kafka**, **Gemini function-calling**, and **Docker Compose**.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose                          │
│                                                             │
│  ┌──────────────────┐   Kafka Topic    ┌─────────────────┐ │
│  │  Producer Agent  │  "raw-news"  ──► │ Consumer Agent  │ │
│  │                  │                  │                  │ │
│  │ Tools:           │                  │ Tools:           │ │
│  │ • search_news    │                  │ • analyse_sent.. │ │
│  │ • categorize     │                  │ • assess_risk    │ │
│  │ • score_import.. │                  │ • gen_actions    │ │
│  └──────────────────┘                  └────────┬─────────┘ │
│                                                 │           │
│                                    ┌────────────▼─────────┐ │
│                                    │  Kafka Topic         │ │
│                                    │  "processed-insights"│ │
│                                    │  + /output/*.jsonl   │ │
│                                    └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Gemini function-calling | LLM explicitly drives tool selection — true agentic behaviour |
| Separate tool implementations | Tools are pure Python; easy to swap mock → real APIs |
| Manual offset commit | Prevents message loss on agent failure |
| Category-keyed Kafka messages | Enables partition-based parallelism by domain |
| JSONL output | Append-only, easy to stream into downstream analytics |

## Quick Start

```bash
# 1. Set your API key
export GEMINI_API_KEY=your_key_here

# 2. Build and start all services
docker compose up --build

# 3. Watch insights appear
tail -f output/insights.jsonl | python -m json.tool

# 4. Check critical alerts
cat output/alerts.txt
```

## Project Structure

```
kafka-agent/
├── docker-compose.yml
├── producer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── agent.py          # Producer Agent (search + enrich)
├── consumer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── agent.py          # Consumer Agent (analyse + alert)
└── shared/
    └── models.py          # NewsEvent, ProcessedInsight, Kafka configs
```

## Agent Flow Detail

### Producer Agent
1. Cycles through a watchlist of strategic topics
2. LLM calls `search_news(query)` → gets article list
3. LLM calls `categorize_article(headline, snippet)` → category + keywords
4. LLM calls `score_importance(...)` → 0-1 score
5. Publishes `NewsEvent` to `raw-news` topic every 30s

### Consumer Agent
1. Polls `raw-news` topic
2. LLM calls `analyse_sentiment(headline, summary)` → sentiment label + score
3. LLM calls `assess_risk(category, sentiment, raw_score)` → risk level + final score
4. LLM calls `generate_action_items(...)` → analyst action items
5. Saves `ProcessedInsight` to JSONL + publishes to `processed-insights`
6. If `risk_level == "critical"` → appends to `alerts.txt`

## Extending This System

- **Real news API**: Replace `_tool_search_news` with NewsAPI / GDELT / Bloomberg
- **Notification**: Add a Slack/email tool in the consumer for critical alerts  
- **Scaling**: Increase Kafka partitions + run multiple consumer containers
- **Observability**: Add Prometheus metrics on message lag and tool latency
- **Persistence**: Swap JSONL for PostgreSQL or Elasticsearch

# 🏥 Travel Insurance Analyzer System

A production-style agentic pipeline built with **Kafka**, **Google-ADK**, and **Docker Compose**, designed to analyze client data for travel insurance suitability and risk assessment.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Docker Compose                                │
│                                                                         │
│  ┌──────────────────┐      Kafka Topic      ┌────────────────────────┐  │
│  │     Producer     │      "insurance"      │    Consumer Agent      │  │
│  │                  │ ────────────────────► │                        │  │
│  │ • Reads CSV Data │                       │ • LLM Risk Analysis    │  │
│  │ • Data Streaming │                       │ • Suitability Scoring  │  │
│  │ • JSON Encoding  │                       │ • Personalized Actions │  │
│  └──────────────────┘                       └───────────┬────────────┘  │
│                                                         │               │
│                                             ┌───────────▼────────────┐  │
│                                             │    Output Directory    │  │
│                                             │    ./consumer/response/│  │
│                                             │      (1.txt, 2.txt...) │  │
│                                             └────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Workflow

1.  **Producer**: Loads mock client data from `producer/mock_data/client_data.csv`. It streams each client's profile as a JSON message to the `insurance` Kafka topic every 3 seconds.
2.  **Kafka**: Acts as the message broker, ensuring reliable delivery of client data from the producer to the consumer.
3.  **Consumer Agent**: 
    - Polls the `insurance` topic for new client data.
    - Utilizes the **Google-ADK** to process the data through an intelligent pipeline.
    - Performs insurance analysis, risk assessment, and generates recommendations.
    - Saves the final analysis for each client into individual `.txt` files within the `consumer/response/` folder.

## 🚀 Quick Start (Running the System)

The project is fully dockerized and includes helper scripts to start the entire stack from scratch.

### 🪟 Windows System
Run the batch file to stop existing containers, rebuild, and start the services:
```cmd
run.bat
```

### 🐧 Linux / macOS System
Grant execution permissions and run the shell script:
```bash
chmod +x run.sh
./run.sh
```

## 📁 Project Structure

```
Prudential_demo/
├── docker-compose.yml   # Orchestrates Kafka, Producer, and Consumer
├── Dockerfile           # Shared Python environment for producer and consumer
├── run.bat / run.sh     # Quick start scripts
├── producer/
│   ├── producer.py      # Streams client data to Kafka
│   └── mock_data/       # Source CSV data
└── consumer/
    ├── consumer.py      # Kafka consumer & Agent runner
    ├── .env             # Environment variables (GEMINI_API_KEY)
    ├── agents/          # Agent logic and tool definitions
    └── response/        # Generated analysis reports (.txt)
```

## 🛠️ Key Components

| Component          | Description |
|--------------------|---|
| **Kafka**          | Distributed streaming platform for high-throughput messaging. |
| **Google-ADK**     | Powers the intelligent analysis using Google's generative models. |
| **Docker Compose** | Simplifies deployment by running the entire stack in isolated containers. |
| **Loguru**         | Provides structured logging for both producer and consumer. |

## ⚙️ Configuration

1.  Ensure you have a `.env` file in the `consumer/` directory.
2.  Add your Gemini API Key:
    ```env
    GEMINI_API_KEY=your_google_gemini_api_key_here
    ```

## 📈 Scaling & Extensions

- **Real-time Data**: Connect the producer to a CRM or live database instead of a CSV.
- **Enhanced Tools**: Add tools to the agent for checking real-time travel advisories or medical databases.
- **Persistence**: Save results to a database (PostgreSQL/MongoDB) instead of flat files.
- **Monitoring**: Integrate Prometheus and Grafana to track processing latency and Kafka lag.

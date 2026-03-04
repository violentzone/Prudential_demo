@echo off
echo Starting the Travel Insurance Analyzer (Producer -^> Kafka -^> Consumer)...

REM Stop and remove any existing containers to start from scratch
docker compose down

REM Build the images and start the containers
docker compose up --build

pause

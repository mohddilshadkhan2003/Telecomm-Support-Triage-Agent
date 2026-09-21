# Production deployment
up:
	docker compose up -d --build
logs:
	docker compose logs -f telecom-triage
stop:
	docker compose down
backup:
	mkdir -p backups
	docker compose exec -T telecom-triage sh -c 'sqlite3 /app/finalproject/data/triage.db .dump' > backups/triage-$$(date +%Y%m%d-%H%M%S).sql

PACKAGE = interview.com/app

migrateup: 
	migrate -path src/db/migrations/main -database "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable" -verbose up

migratedown: 
	migrate -path src/db/migrations/main -database "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable" -verbose down

dev:
	go run src/server.go
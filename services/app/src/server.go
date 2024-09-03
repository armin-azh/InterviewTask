package main

import (
	"database/sql"
	"fmt"
	"github.com/confluentinc/confluent-kafka-go/kafka"
	"os"

	"github.com/gofiber/fiber/v2/log"
	_ "github.com/lib/pq"
	"interview.com/app/src/api"
	"interview.com/app/src/common"
	sqlcmain "interview.com/app/src/db/sqlc/main"
)

func main() {
	log.Info("Starting App Gateway service")

	cfgPath := os.Getenv("APP_CONFIG")
	if cfgPath == "" {
		cfgPath = "."
	}

	cfgPathInfo, err := os.Stat(cfgPath)
	if err != nil {
		log.Error("Cannot find config file", err)
		return
	}
	if !cfgPathInfo.IsDir() {
		log.Errorf("%s is not a directory", cfgPath)
		return
	}

	// Load configs
	config, err := common.LoadConfig(cfgPath)
	if err != nil {
		log.Error(err)
		return
	}

	// Connect to kafka
	producer, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": config.KafkaBootStr,
	})

	if err != nil {
		log.Error(err)
		return
	}
	defer producer.Close()
	
	// Create database connection
	conn, err := sql.Open("postgres", config.DatabaseUrl)
	if err != nil {
		log.Fatal("Cannot connect to database", err)
	}

	store := sqlcmain.NewStore(conn)

	// Create new server instances
	server := api.NewServer(store, config, producer)

	if err := server.Start(fmt.Sprintf("%s:%d", config.Host, config.Port)); err != nil {
		log.Fatal("Cannot start server", err)
	}
}

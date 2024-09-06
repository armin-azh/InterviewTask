package main

import (
	"context"
	"database/sql"
	"fmt"
	"github.com/confluentinc/confluent-kafka-go/kafka"
	"google.golang.org/protobuf/proto"
	"interview.com/app/src/proto/forwarding"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gofiber/fiber/v2/log"
	_ "github.com/lib/pq"
	"interview.com/app/src/common"
	sqlcmain "interview.com/app/src/db/sqlc/main"
)

func main() {
	const resultTopic = "cmp.forwarding.results"
	const finalTopic = "cmp.forwarding.finalize"
	log.Info("Starting Data Forwarding service")

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
	// Configure the consumer
	consumer, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": config.KafkaBootStr,
		"group.id":          "data-forwarding-group",
		"auto.offset.reset": "earliest",
	})
	if err != nil {
		fmt.Printf("Failed to create consumer: %s\n", err)
		os.Exit(1)
	}
	defer consumer.Close()

	err = consumer.SubscribeTopics([]string{resultTopic, finalTopic}, nil)
	if err != nil {
		log.Error("Failed to subscribe to topic: %s\n", err)
		os.Exit(1)
	}

	// Create database connection
	conn, err := sql.Open("postgres", config.DatabaseUrl)
	if err != nil {
		log.Fatal("Cannot connect to database", err)
	}

	store := sqlcmain.NewStore(conn)

	sigchan := make(chan os.Signal, 1)
	signal.Notify(sigchan, syscall.SIGINT, syscall.SIGTERM)

	run := true
	for run {
		select {
		case sig := <-sigchan:
			fmt.Printf("Caught signal %v: terminating\n", sig)
			run = false
		default:
			ev := consumer.Poll(100)
			if ev == nil {
				continue
			}

			switch e := ev.(type) {
			case *kafka.Message:
				switch *e.TopicPartition.Topic {
				case resultTopic:
					// Parse the message using protobuf
					var data forwarding.DataForwarding
					err := proto.Unmarshal(e.Value, &data)
					if err != nil {
						log.Error("Error unmarshaling protobuf: %v\n", err)
						continue
					}
					sessionId := data.Id

					for _, face := range data.Faces {
						person, err := store.GetPersonByPrime(context.Background(), face.PersonId)
						if err != nil {
							log.Error("Error Get person: %v\n", err)
							break
						}

						_, err = store.CreateResult(context.Background(), sessionId, int32(person.ID), face.Thumbnail, float64(face.Similarity))
						if err != nil {
							log.Error("Error Create result: %v\n", err)
							continue
						}
					}

				case finalTopic:

					var data forwarding.DataForwardingStatus
					err := proto.Unmarshal(e.Value, &data)
					if err != nil {
						log.Error("Error unmarshaling protobuf: %v\n", err)
						continue
					}
					sessionId := data.Id
					_, err = store.UpdateSessionEndTime(context.Background(), sql.NullTime{Time: time.Now(), Valid: true}, int64(sessionId))
					if err != nil {
						log.Error("Error updating session time: %v\n", err)

					}
				}

			case kafka.Error:
				fmt.Printf("Error: %v\n", e)
				if e.Code() == kafka.ErrAllBrokersDown {
					run = false
				}
			}
		}
	}

}

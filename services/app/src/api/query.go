package api

import (
	"context"
	"errors"
	"fmt"
	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/log"
	"github.com/gogo/protobuf/proto"
	"github.com/google/uuid"
	"github.com/lib/pq"
	"interview.com/app/src/api/serializers"
	"interview.com/app/src/proto/query"
	"os"
	"path/filepath"
)

func (server *Server) createQuery(c *fiber.Ctx) error {
	c.Accepts("application/json")
	log.Info("New session is called")

	file, err := c.FormFile("video")
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "No video file provided"})
	}

	basePath := "sessions"

	absolutePath := filepath.Join(server.config.MediaDir, basePath)

	if err := os.MkdirAll(absolutePath, os.ModePerm); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	prefix := uuid.New().String()
	relativePath := filepath.Join(basePath, prefix+filepath.Ext(file.Filename))

	filename := filepath.Join(absolutePath, prefix+filepath.Ext(file.Filename))

	if err := c.SaveFile(file, filename); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to save the video"})
	}

	session, err := server.store.CreateSession(context.Background(), uuid.New().String(), relativePath)
	if err != nil {
		var pgErr *pq.Error
		if errors.As(err, &pgErr) {
			log.Info(pgErr.Code.Name())
			return &fiber.Error{
				Code:    fiber.ErrNotFound.Code,
				Message: fmt.Sprintf("%v", err),
			}
		}
		return &fiber.Error{
			Code:    fiber.ErrBadRequest.Code,
			Message: "Bad request happened",
		}
	}

	// Send to queue
	queryMsg := &query.Query{
		Id:    int32(session.ID),
		Prime: session.Prime,
		Path:  session.VideoPath,
	}

	data, err := proto.Marshal(queryMsg)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "cannot encode the proto data"})
	}

	go func() {
		if err := server.producer.Produce(&kafka.Message{TopicPartition: kafka.TopicPartition{Topic: &server.sessionTopic, Partition: kafka.PartitionAny}, Value: data}, nil); err != nil {
			log.Info(err.Error())
		}
		server.producer.Flush(15 * 1000)
	}()

	return c.JSON(fiber.Map{"data": session})
}

func (server *Server) getQueryList(c *fiber.Ctx) error {

	log.Info("Get query list")

	params := serializers.QueryParamSerializer{
		Page:     1,
		PageSize: 10,
	}

	if err := c.QueryParser(&params); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Failed to parse query parameters",
		})
	}

	sessions, err := server.store.GetSessionList(context.Background(), params.PageSize, (params.Page-1)*params.PageSize)
	if err != nil {
		var pgErr *pq.Error
		if errors.As(err, &pgErr) {
			log.Info(pgErr.Code.Name())
			return &fiber.Error{
				Code:    fiber.ErrBadRequest.Code,
				Message: fmt.Sprintf("%v", err),
			}
		}
		return &fiber.Error{
			Code:    fiber.ErrBadRequest.Code,
			Message: "Bad request happened",
		}
	}

	return c.JSON(fiber.Map{
		"results": sessions,
	})
}

func (server *Server) getQuery(c *fiber.Ctx) error {
	log.Info("Get query by prime")
	id := c.Params("id")

	session, err := server.store.GetSessionByPrime(context.Background(), id)
	if err != nil {
		var pgErr *pq.Error
		if errors.As(err, &pgErr) {
			log.Info(pgErr.Code.Name())
			return &fiber.Error{
				Code:    fiber.ErrNotFound.Code,
				Message: fmt.Sprintf("%v", err),
			}
		}
		return &fiber.Error{
			Code:    fiber.ErrBadRequest.Code,
			Message: "Bad request happened",
		}
	}

	return c.JSON(fiber.Map{
		"data": session,
	})
}

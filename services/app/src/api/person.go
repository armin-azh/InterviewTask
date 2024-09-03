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
	"interview.com/app/src/proto/enrollment"
	"os"
	"path/filepath"

	"interview.com/app/src/api/serializers"
)

func (server *Server) createPerson(c *fiber.Ctx) error {
	c.Accepts("application/json")
	log.Info("create new person")
	serializer := new(serializers.PersonSerializer)

	if err := server.ValidatePayload(serializer, c); err != nil {
		return err
	}

	id := uuid.New()
	person, err := server.store.CreatePerson(context.Background(), id.String(), serializer.FirstName, serializer.LastName)
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
		"data": person,
	})
}

func (server *Server) getPersonList(c *fiber.Ctx) error {

	log.Info("get person list")

	params := serializers.QueryParamSerializer{
		Page:     1,
		PageSize: 10,
	}

	if err := c.QueryParser(&params); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Failed to parse query parameters",
		})
	}

	persons, err := server.store.GetPersonList(context.Background(), params.PageSize, (params.Page-1)*params.PageSize)
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
		"results": persons,
	})
}

func (server *Server) getPerson(c *fiber.Ctx) error {
	id := c.Params("id")

	log.Info("get person")

	person, err := server.store.GetPersonByPrime(context.Background(), id)
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
		"data": person,
	})
}

func (server *Server) uploadImagToPerson(c *fiber.Ctx) error {
	id := c.Params("id")

	log.Info("upload person face")

	person, err := server.store.GetPersonByPrime(context.Background(), id)
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

	// Get the file from the request
	file, err := c.FormFile("image")
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "No video file provided",
		})
	}

	personPath := filepath.Join("persons", person.Prime)

	absolutePath := filepath.Join(server.config.MediaDir, personPath)

	// Create the upload directory if it doesn't exist
	if err := os.MkdirAll(absolutePath, os.ModePerm); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to create upload directory",
		})
	}

	uuid := uuid.New()

	filename := filepath.Join(absolutePath, uuid.String()+file.Filename)

	if err := c.SaveFile(file, filename); err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to save the video",
		})
	}

	relativePath := filepath.Join(personPath, uuid.String()+file.Filename)

	face, err := server.store.CreateNewFace(context.Background(), int32(person.ID), relativePath)

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

	// Send through kafka queue
	enroll := &enrollment.Person{
		Id:    int32(person.ID),
		Prime: person.Prime,
		Path:  face.Path,
	}

	data, err := proto.Marshal(enroll)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "cannot encode the proto data"})
	}

	go func() {
		if err := server.producer.Produce(&kafka.Message{TopicPartition: kafka.TopicPartition{Topic: &server.enrollmentTopic, Partition: kafka.PartitionAny}, Value: data}, nil); err != nil {
			log.Info(err.Error())
		}
		server.producer.Flush(15 * 1000)
	}()

	return c.JSON(fiber.Map{
		"data": face,
	})
}

package api

import (
	"context"
	"errors"
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/log"
	"github.com/google/uuid"
	"github.com/lib/pq"

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

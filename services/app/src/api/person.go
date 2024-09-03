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
	return c.JSON(person)
}

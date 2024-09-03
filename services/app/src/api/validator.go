package api

import (
	"fmt"
	"strings"

	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
)

// Validate is responsible to validate incomming json payloads
func (server *Server) Validate(data interface{}) []ErrorResponse {
	var validationErrors []ErrorResponse

	errs := server.validator.Struct(data)
	if errs != nil {
		for _, err := range errs.(validator.ValidationErrors) {
			var res ErrorResponse

			res.FailedField = err.Field()
			res.Tag = err.Tag()
			res.Value = err.Value()
			res.Error = true

			validationErrors = append(validationErrors, res)
		}

	}

	return validationErrors
}

// ValidatePayload is responsible to make error results when error happened in incomming data
func (server *Server) ValidatePayload(data interface{}, c *fiber.Ctx) error {

	if err := c.BodyParser(data); err != nil {
		return err
	}

	if errs := server.Validate(data); len(errs) > 0 && errs[0].Error {
		errMsgs := make([]string, 0)
		for _, err := range errs {
			msg := fmt.Sprintf("[%s]: '%v' | Needs to implement '%s'", err.FailedField, err.Value, err.Tag)
			errMsgs = append(errMsgs, msg)
		}

		return &fiber.Error{
			Code:    fiber.ErrBadRequest.Code,
			Message: strings.Join(errMsgs, " and "),
		}
	}

	return nil
}

package api

import (
	"context"
	"errors"
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/log"
	"github.com/google/uuid"
	"github.com/lib/pq"
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

	filename := filepath.Join(absolutePath, file.Filename)

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

	return c.JSON(fiber.Map{"data": session})
}

func (server *Server) getQueryList(c *fiber.Ctx) error {
	return nil
}

func (server *Server) getQuery(c *fiber.Ctx) error {
	return nil
}

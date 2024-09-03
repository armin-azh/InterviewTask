package api

import (
	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	sqlcmain "interview.com/app/src/db/sqlc/main"
)

type Server struct {
	app       *fiber.App
	store     sqlcmain.Store
	validator *validator.Validate
}

func NewServer(store sqlcmain.Store) *Server {

	// Create new server
	server := &Server{store: store}

	app := fiber.New(fiber.Config{
		AppName: "App Gateway Service",
	})

	// Set up CORS middleware
	app.Use(cors.New(cors.Config{
		AllowOrigins:     "http://localhost:3000",
		AllowHeaders:     "Origin, Content-Type, Accept",
		AllowMethods:     "GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS",
		AllowCredentials: true,
	}))

	api := app.Group("/api")
	v1 := api.Group("/v1")

	// Person
	person := v1.Group("/persons")
	person.Post("", server.createPerson) // create new person

	// Enrollment
	enroll := v1.Group("/enrollments")
	enroll.Post("", server.createEnroll)            // Create new enrollment
	enroll.Get("", server.getEnrollList)            // Get enrollments
	enroll.Get("/enrollment/:pk", server.getEnroll) // Get enrollment instance

	// Query
	query := v1.Group("/queries")
	query.Post("", server.createQuery)       // Create new query
	query.Get("", server.getQueryList)       // Get query list
	query.Get("/query/:pk", server.getQuery) // Get query instance

	server.app = app

	// Assign validator
	server.validator = validator.New()

	return server
}

func (server *Server) Start(address string) error {
	return server.app.Listen(address)
}

package api

import (
	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/go-playground/validator/v10"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"interview.com/app/src/common"
	sqlcmain "interview.com/app/src/db/sqlc/main"
	"path/filepath"
)

type Server struct {
	app       *fiber.App
	store     sqlcmain.Store
	validator *validator.Validate
	config    *common.Config
	producer  *kafka.Producer

	enrollmentTopic string
	sessionTopic    string
}

func NewServer(store sqlcmain.Store, config *common.Config, producer *kafka.Producer) *Server {

	// Create new server
	server := &Server{
		store:           store,
		config:          config,
		producer:        producer,
		enrollmentTopic: "cmp.enrollment.image",
		sessionTopic:    "cmp.session.videos",
	}

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

	app.Static("/media", filepath.Join(server.config.MediaDir, "thumbnails"))

	api := app.Group("/api")
	v1 := api.Group("/v1")

	// Person
	person := v1.Group("/persons")
	person.Post("", server.createPerson)                         // create new person
	person.Get("", server.getPersonList)                         // Get person list
	person.Get("/person/:id", server.getPerson)                  // Get person by prime
	person.Post("/person/:id/upload", server.uploadImagToPerson) // Get person by prime

	// Query
	query := v1.Group("/queries")
	query.Post("", server.createQuery)       // Create new query
	query.Get("", server.getQueryList)       // Get query list
	query.Get("/query/:id", server.getQuery) // Get query instance

	server.app = app

	// Assign validator
	server.validator = validator.New()

	return server
}

func (server *Server) Start(address string) error {
	return server.app.Listen(address)
}

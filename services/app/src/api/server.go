package api

import "github.com/gofiber/fiber/v2"


type Server struct{
	app *fiber.App
}


func NewServer() *Server{

	// Create new server
	server := &Server{}

	app:=fiber.New(fiber.Config{
		AppName: "App Gateway Service",
	})

	api := app.Group("/api")
	v1 := api.Group("/v1")

	// Enrollment
	enroll := v1.Group("/enrollments")
	enroll.Post("", server.createEnroll) // Create new enrollment
	enroll.Get("", server.queryEnroll) // Get enrollments
	enroll.Get("/enrollment/:pk", server.getEnroll) // Get enrollment instance


	// Query
	query := v1.Group("/queries")
	query.Post("", server.createQuery) // Create new query
	query.Get("", server.getQueryList) // Get query list
	query.Get("/query/:pk", server.getQuery) // Get query instance 
	
	server.app = app

	return server
}


func (server *Server) Start (address string) error{
	return server.app.Listen(address)
}
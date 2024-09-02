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

	server.app = app

	return server
}


func (server *Server) Start (address string) error{
	return server.app.Listen(address)
}
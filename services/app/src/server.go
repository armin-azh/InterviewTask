package main

import (
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/log"
)



func main() {
	log.Info("Starting App Gateway service")

	app:=fiber.New(fiber.Config{
		AppName: "App Gateway Service",
	})

	if err:= app.Listen(":8080");err!=nil{
		log.Fatal("Cannot start server", err)
	}
}
package api

import "github.com/gofiber/fiber/v2"




func (server *Server) createEnroll(c *fiber.Ctx) error{
	c.Accepts("application/json")

	return nil
}


func (server *Server) getEnroll (c *fiber.Ctx) error{
	return nil
}


func (server *Server) getEnrollList (c *fiber.Ctx) error{
	return nil
}
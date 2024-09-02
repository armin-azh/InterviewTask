package api

import "github.com/gofiber/fiber/v2"



func (server *Server) createQuery (c *fiber.Ctx) error{
	c.Accepts("application/json")
	return nil
}

func (server *Server) getQueryList (c *fiber.Ctx) error{
	return nil
}

func (server *Server) getQuery (c *fiber.Ctx) error{
	return nil
}
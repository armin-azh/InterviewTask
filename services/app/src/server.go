package main

import (
	"fmt"
	"os"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/log"
	"interview.com/app/src/common"
)



func main() {
	log.Info("Starting App Gateway service")

	cfgPath:=os.Getenv("APP_CONFIG")
	if cfgPath==""{
		cfgPath = "."
	}

	cfgPathInfo, err:=os.Stat(cfgPath)
	if err!=nil{
		log.Error("Cannot find config file", err)
		return
	}
	if !cfgPathInfo.IsDir(){
		log.Errorf("%s is not a directory", cfgPath)
		return 
	}
	
	config, err := common.LoadConfig(cfgPath)
	if err!=nil{
		log.Error(err)
		return
	}

	app:=fiber.New(fiber.Config{
		AppName: "App Gateway Service",
	})

	if err:= app.Listen(fmt.Sprintf("%s:%d", config.Host,config.Port));err!=nil{
		log.Fatal("Cannot start server", err)
	}
}
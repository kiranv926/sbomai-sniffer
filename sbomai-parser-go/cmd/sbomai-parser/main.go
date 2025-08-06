package main

import (
	"os"

	"github.com/sbomai/sbomai-parser-go/internal/app"
	"github.com/sirupsen/logrus"
)

func main() {
	// Configure logging
	logrus.SetFormatter(&logrus.TextFormatter{
		FullTimestamp: true,
	})
	logrus.SetLevel(logrus.InfoLevel)

	// Create and run the application
	app := app.NewApp()
	if err := app.Run(); err != nil {
		logrus.Errorf("Application failed: %v", err)
		os.Exit(1)
	}
}

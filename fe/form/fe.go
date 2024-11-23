package form

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/charmbracelet/huh"
	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/log"
	"github.com/redis/go-redis/v9"
	"github.com/theredditbandit/stitch/fe/utils"
)

func RunForm() error {
	var err error
	var changeFilename bool
	var newName string
	fileName := os.Args[1]
	fileNameStyle := lipgloss.NewStyle().
		Bold(true).
		Italic(true).
		Foreground(lipgloss.Color("#008080"))
	conf := huh.NewConfirm().
		Title(fmt.Sprintf("Got file name %s.\n Would you like to change the filename", fileNameStyle.Render(fileName))).
		Affirmative("Yes").
		Negative("No").
		Value(&changeFilename)
	newNameInput := huh.NewInput().
		Title("Enter new filename").
		Prompt(">").
		Value(&newName)
	err = conf.Run()
	if err != nil {
		return err
	}

	if changeFilename {
		err = newNameInput.Run()
		if err != nil {
			return err
		}
	}

	rdbChan := make(chan *redis.Client, 2)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	go utils.ConnectToRedis(ctx, cancel, rdbChan)
	rdb := <-rdbChan
	if rdb == nil {
		log.Fatal("Could not connect to redis")
	} else {
		log.Debug("connected to redis successfully")
	}
	log.Debug("Confirm value", "confirm", conf.GetValue())
	log.Debug("new file name", "newName", newName)
	return err
}

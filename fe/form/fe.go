package form

import (
	"fmt"
	"os"

	"github.com/charmbracelet/huh"
	"github.com/charmbracelet/log"
)

func RunForm() error {
	var confirm bool
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewConfirm().
				Title(fmt.Sprintf("Are you sure you want to stitch %s file", os.Args[1])).
				Affirmative("Yes").
				Negative("No").
				Value(&confirm),
		),
	)
	err := form.Run()
	log.Debug("Confirm value", "confirm", confirm)
	return err
}

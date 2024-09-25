package main

import (
	"time"

	"github.com/charmbracelet/log"
	"github.com/theredditbandit/stitch/ares/utils"
)

func init() {
	log.SetReportCaller(true)
	log.SetReportTimestamp(true)
	log.SetTimeFormat(time.Kitchen)
	log.SetPrefix("Ares")
	log.SetLevel(log.DebugLevel)        // TODO : make configurable
	log.SetFormatter(log.TextFormatter) // TODO : make configurable
}

func main() {
	log.Info(utils.GetLogo())
	log.Info("Starting Ares . . . ")
	log.Info("Ares is", "mode", log.GetLevel())
	data := utils.GetData()
	log.Debug("got data successfully", "size of the file", len(data.Data))
}

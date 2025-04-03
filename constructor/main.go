package main

import (
	"constructor/pkg"
	"fmt"
	"os"
)

func main() {
	err := os.Mkdir("decoded_outputs", 0755)
	if err != nil {
		if !os.IsExist(err) {
			fmt.Println("Something went wrong creating decoded_outputs dir")
			fmt.Println(err)
			return
		}
	}
	outFileName := fmt.Sprintf("decoded_outputs/decoded_data")
	file, err := os.Create(outFileName)
	defer file.Close()

	if err != nil {
		fmt.Printf("Error creating decoded file %s", err)
		os.Exit(1)
	}
	constructedData := pkg.ConstructData()

	n, err := file.Write([]byte(constructedData.String()))
	if err != nil {
		fmt.Printf("Error writing to decoded file : %s", err)
		os.Exit(1)
	}
	fmt.Printf("Written %d bytes to %s file successfully", n, outFileName)
	fmt.Println("created decoded file successfully")

}

package main

import (
	"fmt"
	"os"
	// "runtime"
	// "time"
)

func main() {
	// fmt.Println("go version:", runtime.Version())

	// // create a new file
	// const filePath = "example"
	// f, err := os.OpenFile(filePath, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0600)
	// if err != nil {
	// 	panic(err)
	// }
	// f.Close()

	// const filePath = "/Volumes/N1CTF_APFS 1/ctf/0001.txt"
	// stat, err := os.Stat(filePath)
	stat, err := os.Stat(os.Args[1])
	if err != nil {
		panic(err)
	}
	// fmt.Println("mtime after creation:", stat.ModTime())
	fmt.Println(stat.ModTime())

	// change the time with nanosecond precision
	// t := time.Unix(1509480275, 123456789)
	// fmt.Println("setting mtime to:", t)
	// err = os.Chtimes(filePath, t, t)
	// if err != nil {
	// 	panic(err)
	// }
	// stat, err = os.Stat(filePath)
	// if err != nil {
	// 	panic(err)
	// }
	// fmt.Println("mtime after set:", stat.ModTime())
}

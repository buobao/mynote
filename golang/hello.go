package main

import "fmt"

func main() {
	fmt.Println("Hello,Golang!")

	var stockcode = 123
	var enddate = "2022-08-25"

	fmt.Println(fmt.Sprintf("Code=%d&endDate=%s",stockcode,endDate))
}
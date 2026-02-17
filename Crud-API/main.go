package main

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

// Data Model
type Book struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Author string `json:"author"`
}

var books = []Book{
	{ID: 1, Title: "A Thousand Splendid Suns", Author: "Khaled Hosseini"},
	{ID: 2, Title: "Stoner", Author: "John Williams"},
	{ID: 3, Title: "To Kill a Mockingbird", Author: "Harper Lee"},
}
var nextID = 4

func main() {
	r := gin.Default()

	// Root endpoint to check if the server is running
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Server is running!",
			"try_these_urls": []string{
				"http://localhost:8080/books",
				"http://localhost:8080/books/1",
				"http://localhost:8080/books/2",
			},
		})
	})

	// GET all books (Type this in Chrome address bar)
	r.GET("/books", func(c *gin.Context) {
		c.JSON(http.StatusOK, books)
	})

	// GET a specific book by ID
	r.GET("/books/:id", func(c *gin.Context) {
		// Convert the "id" string from URL to an integer
		idParam := c.Param("id")
		id, err := strconv.Atoi(idParam)

		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "ID must be a number"})
			return
		}

		// Find the book
		for _, b := range books {
			if b.ID == id {
				c.JSON(http.StatusOK, b)
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"error": "Book not found"})
	})

	r.Run(":8080")
}

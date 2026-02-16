package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	// Case 1: Success (200 OK)
	if r.URL.Path == "/" {
		w.Header().Set("Content-Type", "text/html")
		w.WriteHeader(http.StatusOK) // 200
		fmt.Fprint(w, "<h1>Welcome! Server is running.</h1>")
	}

	// Case 2: Simulated Error (500 Internal Server Error)
	else if r.URL.Path == "/error" {
		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusInternalServerError) // 500
		fmt.Fprint(w, "Internal Server Error")
	}

	// Case 3: Not Found (404 Not Found)
	else {	
		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusNotFound) // 404
		fmt.Fprint(w, "Not Found")
	}	
}

func main() {
	// Register the handler function to the root path "/"
	http.HandleFunc("/", handler)

	fmt.Println("Server started http://localhost:8081")
	http.ListenAndServe("localhost:8081", nil)
}

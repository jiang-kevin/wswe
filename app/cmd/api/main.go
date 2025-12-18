package main

import (
	"database/sql"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	_ "github.com/jackc/pgx/v5"
	"github.com/jiang-kevin/wswe/config"
)

func main() {
	c := config.New()

	db, err := sql.Open("pgx", c.DB.Host)
	if err != nil {
		log.Fatalf("Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer db.Close()

	var greeting string
	err = db.QueryRow("select 'Hello, world!'").Scan(&greeting)
	if err != nil {
		log.Fatalf("QueryRow failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println(greeting)

	mux := http.NewServeMux()
	mux.HandleFunc("/", handler)

	s := &http.Server{
		Addr:         fmt.Sprintf(":%d", c.Server.Port),
		Handler:      mux,
		ReadTimeout:  c.Server.TimeoutRead,
		WriteTimeout: c.Server.TimeoutWrite,
		IdleTimeout:  c.Server.TimeoutIdle,
	}

	log.Println("Starting server " + s.Addr)

	if err := s.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatal("Server startup failed")
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Hello world!")
}

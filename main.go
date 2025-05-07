package main

import (
	"bytes"
	"fmt"
	"log"
	"os"

	"github.com/SebastiaanKlippert/go-wkhtmltopdf"
	"github.com/russross/blackfriday/v2"
)

func main() {
	resumeFile := "RESUME.md"
	data, err := os.ReadFile(resumeFile)
	if err != nil {
		log.Fatalf("Error reading %s: %v", resumeFile, err)
	}

	html := blackfriday.Run(data)

	htmlTemplate := `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Resume</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      font-size: 12px;
      background-color: #FFF;
      color: #000;
      margin: 20px;
    }
    h1, h2, h3 {
      color: #000;
      margin-bottom: 0.5em;
    }
    p, ul, ol {
      line-height: 1.4;
      margin-bottom: 1em;
    }
.centered-text {
	  text-align: center;
	  font-weight: bold;
	  font-size: 24px;
	}
  </style>
</head>
<body>
  %s
</body>
</html>`

	finalHTML := fmt.Sprintf(htmlTemplate, string(html))

	pdfg, err := wkhtmltopdf.NewPDFGenerator()
	if err != nil {
		log.Fatalf("Failed to create PDF generator: %v", err)
	}

	page := wkhtmltopdf.NewPageReader(bytes.NewReader([]byte(finalHTML)))
	page.Encoding.Set("UTF-8")
	pdfg.Dpi.Set(96)
	pdfg.AddPage(page)

	if err := pdfg.Create(); err != nil {
		log.Fatalf("Error generating PDF: %v", err)
	}

	outFile := "resume.pdf"
	if err := pdfg.WriteFile(outFile); err != nil {
		log.Fatalf("Error writing PDF file: %v", err)
	}

	log.Printf("Successfully generated %s\n", outFile)
}

# UTCN Curriculum Scraper & Grade Calculator

A Python tool for scraping course information from UTCN (Technical University of Cluj-Napoca) curriculum PDF files and calculating weighted harmonic mean grades.

## Features

- 📚 **Curriculum Scraping**: Automatically downloads and extracts course data from official UTCN curriculum PDF files
- 🧮 **Grade Calculator**: Computes weighted harmonic mean of student grades based on course credits
- 🎯 **Multiple Specializations**: Supports CTI, CTI_EN, AU, and AU_EN specializations
- 📊 **Academic Year Support**: Currently configured for 2024-2025 academic year
- 🔍 **Intelligent PDF Parsing**: Uses pdfplumber for accurate table extraction from PDF documents

## Supported Specializations

| Code | Description | Language |
|------|-------------|----------|
| `CTI` | Calculatoare (Romanian) | Romanian |
| `CTI_EN` | Calculatoare (English) | English |
| `AU` | Automatică (Romanian) | Romanian |
| `AU_EN` | Automatică (English) | English |

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CronoXGM/UTCN.git
cd UTCN
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script interactively:

```bash
python main.py
```

The program will prompt you for:
1. **Study Year**: Enter a number from 1 to 4
2. **Specialization**: Choose from CTI, CTI_EN, AU, or AU_EN
3. **Grades**: For each course found, enter your grade

### Example Session

```
Enter your study year (1-4): 2
Enter your specialization (CTI, CTI_EN, AU, AU_EN): CTI

Courses extracted from the curriculum:
Subject: Algoritmi și Structuri de Date (Credits: 6.0)
Enter your grade for 'Algoritmi și Structuri de Date': 9.5

Subject: Programare Orientată pe Obiecte (Credits: 5.0)
Enter your grade for 'Programare Orientată pe Obiecte': 8.7

...

The harmonic mean grade for the semester is: 8.95
```

## How It Works

1. **PDF Download**: The tool constructs the URL for the curriculum PDF based on your inputs
2. **Data Extraction**: Uses Scrapy to download and pdfplumber to parse the PDF tables
3. **Course Processing**: Extracts course names and credit values from the curriculum
4. **Grade Input**: Prompts user to enter grades for each course
5. **Calculation**: Computes the weighted harmonic mean using the formula:

   ```
   Harmonic Mean = Total Credits / Σ(Credits_i / Grade_i)
   ```

## Technical Details

### Dependencies

- **Scrapy**: Web scraping framework for downloading PDFs
- **pdfplumber**: PDF parsing and table extraction
- **requests**: HTTP library for web requests
- **playwright**: Browser automation (if needed)
- **PyPDF2**: Alternative PDF processing library

### PDF Source

The tool fetches curriculum PDFs from:
```
https://ac.utcluj.ro/files/Acasa/Site/documente/planuri_invatamant/
{academic_year}/{year}_L_{specialization}_{academic_year}.pdf
```

### Grade Filtering

- Only grades ≥ 5.0 are included in the harmonic mean calculation
- Courses with grades below 5.0 are automatically excluded
- The calculation uses only credits from courses with valid grades

## Project Structure

```
UTCN/
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore patterns
└── README.md           # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is for educational purposes only. Please respect UTCN's terms of service and use responsibly. The accuracy of grade calculations should be verified independently.

## Author

Created by [CronoXGM](https://github.com/CronoXGM) for UTCN students.
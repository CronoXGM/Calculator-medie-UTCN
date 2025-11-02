# UTCN Curriculum Scraper & Grade Calculator

A modular Python application for scraping course information from UTCN (Technical University of Cluj-Napoca) curriculum PDF files and calculating weighted harmonic mean grades with an interactive CLI interface.

## Features

- 📚 **Curriculum Scraping**: Automatically downloads and extracts course data from official UTCN curriculum PDF files
- ✅ **Interactive Subject Selection**: Choose which courses to include using intuitive checkbox UI
- 🧮 **Grade Calculator**: Computes weighted harmonic mean with special handling for failing grades
- 🎯 **Multiple Specializations**: Supports CTI, CTI_EN, AU, and AU_EN specializations
- 📊 **Academic Year Support**: Currently configured for 2024-2025 academic year
- 🔍 **Intelligent PDF Parsing**: Uses pdfplumber for accurate table extraction from PDF documents
- 🏗️ **Modular Architecture**: Clean separation of concerns for maintainability and testing

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

The program will guide you through 6 steps:

1. **Study Year**: Enter a number from 1 to 4
2. **Specialization**: Select from an interactive menu (CTI, CTI_EN, AU, or AU_EN)
3. **Course Scraping**: Automatically fetches courses from UTCN curriculum PDF
4. **Subject Selection**: Use checkboxes to select which courses you're taking
5. **Grade Entry**: Enter grades (0-10) for each selected course
6. **Results**: View your weighted harmonic mean and statistics

### Example Session

```
==================================================================
UTCN GRADE CALCULATOR
Weighted Harmonic Mean Calculator for Semester Grades
==================================================================

Step 1: Enter your academic information

? Enter your study year (1-4): 2
? Select your specialization: CTI (Calculatoare - Romanian)

Step 2: Fetching curriculum for Year 2, CTI...
This may take a few moments...

✓ Successfully loaded 15 courses from curriculum

Step 3: Select the subjects you are taking this semester

Use arrow keys to navigate, SPACE to select/deselect, ENTER to confirm

? Select subjects that you take and want to insert grade:
  ◯ Algoritmi și Structuri de Date (6.0 credits)
  ◉ Programare Orientată pe Obiecte (5.0 credits)
  ◉ Baze de Date (5.0 credits)
  ◯ Matematică (4.0 credits)
  ...

✓ Selected 2 subject(s)

Step 4: Enter grades for your 2 selected subject(s)

? Grade for Programare Orientată pe Obiecte (5.0 credits): 9.5
  ✓ Passing grade: 9.5
? Grade for Baze de Date (5.0 credits): 8.7
  ✓ Passing grade: 8.7

Step 5: Calculating your weighted harmonic mean grade...

==================================================================
FINAL RESULTS
==================================================================

Total courses evaluated: 2
  - Passing courses (≥ 5): 2
  - Failing courses (< 5): 0

Total credits: 10.0

------------------------------------------------------------------
WEIGHTED HARMONIC MEAN GRADE: 9.08
------------------------------------------------------------------

✓ Your average is PASSING (9.08 ≥ 5.00)
```

## How It Works

### Workflow

1. **PDF Download**: Constructs the URL for the curriculum PDF based on your inputs
2. **Data Extraction**: Uses Scrapy to download and pdfplumber to parse the PDF tables
3. **Course Processing**: Extracts course names and credit values from the curriculum
4. **Interactive Selection**: Displays checkboxes for course selection using questionary
5. **Grade Input**: Prompts user to enter grades (0-10) for each selected course
6. **Calculation**: Computes weighted harmonic mean with special handling:
   - **Passing grades (≥ 5)**: Included in standard harmonic mean formula
   - **Failing grades (< 5)**: Included with full credit weight penalty
   - **Unselected courses**: Excluded from calculation entirely

### Grade Calculation Formula

For selected courses with grades:

```
Weighted Harmonic Mean = Total_Credits / Σ(Credits_i / Grade_i)
```

Where:
- **Grade ≥ 5**: Standard contribution to the sum
- **Grade < 5**: Contributes with actual failing grade (heavily penalizes average)
- Credits are only counted for selected courses

## Technical Details

### Dependencies

- **Scrapy**: Web scraping framework for downloading PDFs
- **pdfplumber**: PDF parsing and table extraction
- **questionary**: Interactive CLI prompts and checkboxes
- **requests**: HTTP library for web requests
- **playwright**: Browser automation (optional)
- **PyPDF2**: Alternative PDF processing library (optional)

### PDF Source

The tool fetches curriculum PDFs from:
```
https://ac.utcluj.ro/files/Acasa/Site/documente/planuri_invatamant/
{academic_year}/{year}_L_{specialization}_{academic_year}.pdf
```

### Grade Handling

- **Passing grades (≥ 5)**: Included in harmonic mean calculation
- **Failing grades (< 5)**: Included but penalize the average significantly
- **Unselected courses**: Completely excluded from calculation
- Courses with zero or negative credits are automatically skipped
- Only selected courses contribute to the final grade

## Project Structure

```
UTCN/
├── main.py              # Main application entry point and orchestration
├── models.py            # Course data model (dataclass)
├── pdf_handler.py       # PDF scraping and parsing logic
├── grade_calculator.py  # Grade calculation algorithms
├── ui_handler.py        # Interactive CLI user interface
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore patterns
└── README.md           # Project documentation
```

### Module Descriptions

- **main.py**: Orchestrates the entire workflow, coordinating all modules
- **models.py**: Defines the `Course` dataclass with validation methods
- **pdf_handler.py**: Contains `CurriculumPDFSpider` and `scrape_subjects()` function
- **grade_calculator.py**: Implements weighted harmonic mean calculation with fail handling
- **ui_handler.py**: Provides all user interaction including checkboxes, input validation, and result display

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
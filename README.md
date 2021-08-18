# AML-1204-final-term-project

This project is the final project for the Lambton College AML-1204 Python Programming in the Canadian context.

## Problem Statement

Generating and maintaining chat-bots manually is a time-consuming task. We need to automate the generation of IBM Watson
skill for enabling a quick Q&A chat-bot.

The input is an Excel file with questions, answers and some classification categories.

The output must be a valid JSON IBM Watson Dialog Skill file, Ready to be uploaded to IBM Watson.

## Installation

1. Download the code to your computer:
    1. Download the code from the repository as a ZIP file and decompress it.
    2. Clone the repository in a local folder.

```
git clone https://github.com/diegoortizmatajira/AML-1204-final-term-project.git
```

3. Open the Terminal / Command line.
4. Navigate to the folder where the code was downloaded.
5. Run the application

## Run the application

```
python .\main.py [input file] [output file]
```

You can provide the input file and the output filename. If you omit the parameters the application will use:

* input file: template.xlsx (Provided with the source code)
* output file: output.json

The application with generate the output file and then you can upload the JSON file
to [IBM Watson](https://us-south.assistant.watson.cloud.ibm.com/)
Note: You will need to create a free account on IBM to use the Watson Assistant feature.

## Collaborators

- [Diego Ortiz](https://github.com/diegoortizmatajira)
- [Henry Ramos](https://github.com/rhenrym)
- [Julio Sánchez](https://github.com/juliosanchez7)
- [Luiz De Mattos](https://github.com/lfmcanada)

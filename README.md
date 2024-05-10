# gestplay_auth
 Authentication service for gestplay

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/project-name.git
    ```

2. Create a virtual environment:

    ```bash
    virtualenv -p python3.12.3  env
    ```

3. Activate the virtual environment:

    ```bash
    .\env\Scripts\activate
    ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn api.main:app --reload
    ```

2. Open your browser and navigate to `http://localhost:8000` to access the API.

## API Documentation

The API documentation can be found at `http://localhost:8000/docs`.

## License

This project is licensed under the [MIT License](LICENSE).
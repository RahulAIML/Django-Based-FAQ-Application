# Bharat_FD_Backend_Intern_Task_Submission

# Backend Developer Hiring Test

This repository contains my solution to the backend developer hiring test, demonstrating my skills in Django development, API design, caching, internationalization, and more.

---

## Objective

The goal of this project is to create a Django application that:

- Stores and manages **FAQs** with multi-language translation support.
- Integrates a **WYSIWYG editor** for FAQ answers.
- Exposes a **REST API** for FAQ management.
- Implements a **caching mechanism** to improve performance.
- Includes **unit tests** to ensure proper functionality.
- Follows **PEP8 conventions** and best practices for code quality.
- Provides a **clear and detailed README**.

---

## Features

- **FAQ Model:** Manages multilingual questions and answers, with support for rich text formatting using the CKEditor.
- **WYSIWYG Support:** Uses `django-ckeditor` to enable rich text formatting for FAQ answers.
- **Multi-language Translations:** Supports translations for FAQs in multiple languages, including English, Hindi, and Bengali.
- **REST API:** Provides endpoints for CRUD operations on FAQs with language selection via query parameters.
- **Caching:** Caches translated FAQs using Redis for faster response times.
- **Admin Interface:** A user-friendly Django admin interface to manage FAQs.
- **Unit Tests:** Includes comprehensive tests for models and API endpoints.

---

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/backend-developer-test.git
    cd backend-developer-test
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables:**

    Create a `.env` file and add the necessary environment variables. For example:

    ```env
    DEBUG=True
    GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key
    ```

5. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The app will be available at `http://localhost:8000`.

---

## API Usage Examples

You can interact with the API to fetch the FAQs in different languages:

- **Get FAQs in English (default):**

    ```bash
    curl http://localhost:8000/api/faqs/
    ```

- **Get FAQs in Hindi:**

    ```bash
    curl http://localhost:8000/api/faqs/?lang=hi
    ```

- **Get FAQs in Bengali:**

    ```bash
    curl http://localhost:8000/api/faqs/?lang=bn
    ```

---


## Unit Tests

The project includes unit tests to ensure proper functionality. You can run them with `pytest`:

```bash
pytest
```


## API Endpoint Documentation

The following API endpoints are available for interacting with the FAQ model. The API supports **multilingual** FAQ retrieval and allows for managing FAQs with easy-to-use HTTP methods.

---

### 1. **GET /api/faqs/**

**Description:**  
Fetch a list of all FAQs in the specified language (or default language if not specified).

**Method:** `GET`

**Query Parameters:**
- `lang` (optional): The language code in which to fetch the FAQs. Supported languages: `en` (English), `hi` (Hindi), `bn` (Bengali). Defaults to `en` if not provided.

**Example Request:**
```bash
curl http://localhost:8000/api/faqs/?lang=en

[
    {
        "id": 1,
        "question": "What is Django?",
        "answer": "<p>Django is a high-level Python web framework...</p>",
        "question_translations": {
            "hi": "Django क्या है?",
            "bn": "Django কী?"
        }
    },
    {
        "id": 2,
        "question": "How do I install Django?",
        "answer": "<p>To install Django, you can use pip...</p>",
        "question_translations": {
            "hi": "मैं Django को कैसे इंस्टॉल करूं?",
            "bn": "আমি Django কিভাবে ইনস্টল করব?"
        }
    }
]



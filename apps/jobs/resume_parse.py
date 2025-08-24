def parse_resume_file(file):
    """
    Simple resume parsing function.
    In a real implementation, this would use AI/ML to extract resume data.
    For now, we'll return a basic structure.
    """
    return {
        "filename": file.name,
        "file_size": file.size,
        "content_type": file.content_type,
        "parsed_at": "2024-01-01T00:00:00Z",
        "extracted_data": {
            "name": "Extracted from resume",
            "email": "extracted@example.com",
            "phone": "555-1234",
            "skills": ["Python", "Django", "JavaScript"],
            "experience": [
                {
                    "title": "Software Developer",
                    "company": "Example Corp",
                    "duration": "2020-2024"
                }
            ]
        }
    }

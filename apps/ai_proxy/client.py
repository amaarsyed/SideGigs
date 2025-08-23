import os
import requests
from django.conf import settings


AI_URL = getattr(settings, 'AI_SERVICE_URL', 'http://localhost:8010')
AI_TOKEN = getattr(settings, 'AI_SHARED_TOKEN', 'devtoken')


def snapquote(media_urls):
    """
    Get AI-powered snapquote for job based on media URLs.
    
    Args:
        media_urls (list): List of media URLs to analyze
        
    Returns:
        dict: Quote data with price_cents, eta_minutes, checklist, confidence
    """
    try:
        response = requests.post(
            f"{AI_URL}/snapquote",
            json={"media_urls": media_urls},
            headers={"Authorization": f"Bearer {AI_TOKEN}"},
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Return fallback data if AI service is unavailable
        return {
            "price_cents": 0,
            "eta_minutes": 0,
            "checklist": [],
            "confidence": 0.0,
            "error": str(e)
        }


def risk_assessment(job_data):
    """
    Get AI-powered risk assessment for a job.
    
    Args:
        job_data (dict): Job information for risk assessment
        
    Returns:
        dict: Risk assessment data
    """
    try:
        response = requests.post(
            f"{AI_URL}/risk-assessment",
            json=job_data,
            headers={"Authorization": f"Bearer {AI_TOKEN}"},
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "risk_level": "unknown",
            "risk_factors": [],
            "confidence": 0.0,
            "error": str(e)
        }


def hazard_detection(media_urls):
    """
    Detect hazards in job photos.
    
    Args:
        media_urls (list): List of media URLs to analyze for hazards
        
    Returns:
        dict: Hazard detection results
    """
    try:
        response = requests.post(
            f"{AI_URL}/hazard-detection",
            json={"media_urls": media_urls},
            headers={"Authorization": f"Bearer {AI_TOKEN}"},
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "hazards": [],
            "safety_score": 0.0,
            "recommendations": [],
            "error": str(e)
        }

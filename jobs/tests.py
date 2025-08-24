from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch

from .models import Resume, IDVerification

User = get_user_model()


class StorageTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")
        self.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)

    def auth(self, user):
        resp = self.client.post("/api/auth/login", {"username": user.username, "password": "pass"})
        token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    @patch("jobs.views.parse_resume", return_value={"email": None, "phone": None, "skills": [], "raw_excerpt": ""})
    @patch("core.storage.create_signed_url", return_value="https://example.com/file")
    @patch("core.storage.upload_bytes")
    def test_upload_resume(self, m_upload, m_signed, m_parse):
        self.auth(self.user)
        file = SimpleUploadedFile("resume.pdf", b"PDF", content_type="application/pdf")
        resp = self.client.post("/api/storage/resume", {"file": file})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Resume.objects.count(), 1)
        self.assertIn("signed_url", resp.data)

    @patch("core.storage.create_signed_url", return_value="https://example.com/file")
    @patch("core.storage.upload_bytes")
    def test_upload_id(self, m_upload, m_signed):
        self.auth(self.user)
        file = SimpleUploadedFile("id.jpg", b"JPEG", content_type="image/jpeg")
        resp = self.client.post("/api/storage/id", {"id_image": file})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["status"], "PENDING")
        self.assertEqual(IDVerification.objects.count(), 1)

    @patch("core.storage.create_signed_url", return_value="https://example.com/path")
    def test_signed_url_permissions(self, m_signed):
        self.auth(self.user)
        resp = self.client.get("/api/storage/signed-url", {"path": "foo"})
        self.assertEqual(resp.status_code, 403)
        self.client.credentials()  # reset
        self.auth(self.staff)
        resp = self.client.get("/api/storage/signed-url", {"path": "foo"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("url", resp.data)

    @patch("core.views.ensure_bucket")
    @patch("core.views.get_supabase")
    def test_health(self, m_get, m_ensure):
        class DummyStorage:
            def list_buckets(self):
                return [{"name": "uploads"}]
        class DummyClient:
            storage = DummyStorage()
        m_get.return_value = DummyClient()
        resp = self.client.get("/api/health/storage")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["ok"])

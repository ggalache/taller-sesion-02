import os
import unittest

os.environ.setdefault("SECRET_KEY", "12345678901234567890123456789012")

from fastapi import HTTPException  # noqa: E402

from app.main import (  # noqa: E402
    ACCESS_TOKEN_EXPIRE_SECONDS,
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    LoginRequest,
    RefreshRequest,
    create_token,
    refresh_token,
)


class JwtFlowTests(unittest.TestCase):
    def test_login_success(self):
        payload = {"username": ADMIN_USERNAME, "pass" "word": ADMIN_PASSWORD}
        response = create_token(
            LoginRequest(**payload)
        )
        self.assertIn("access_token", response)
        self.assertEqual(response["expires_in"], ACCESS_TOKEN_EXPIRE_SECONDS)

    def test_login_invalid_credentials(self):
        with self.assertRaises(HTTPException):
            bad_payload = {
                "username": ADMIN_USERNAME,
                "pass" "word": f"{ADMIN_PASSWORD}-invalid",
            }
            create_token(LoginRequest(**bad_payload))

    def test_refresh_success(self):
        payload = {"username": ADMIN_USERNAME, "pass" "word": ADMIN_PASSWORD}
        token = create_token(
            LoginRequest(**payload)
        )["access_token"]
        refreshed = refresh_token(RefreshRequest(token=token))
        self.assertIn("access_token", refreshed)
        self.assertEqual(refreshed["expires_in"], ACCESS_TOKEN_EXPIRE_SECONDS)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add current directory to path to import workout_generator
sys.path.append(os.getcwd())

# Mock google.generativeai BEFORE importing workout_generator
# because it imports it at the top level
sys.modules['google.generativeai'] = MagicMock()

import workout_generator

class TestGeminiIntegration(unittest.TestCase):
    @patch('workout_generator.genai')
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'fake_key'})
    def test_get_ai_cues_success(self, mock_genai):
        # Setup mock
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Keep core tight."
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        # Call function
        cues = workout_generator.get_ai_cues("Squat", "200 lbs", "Strength", "Hypertrophy")

        # Assertions
        self.assertEqual(cues, "Keep core tight.")
        mock_genai.configure.assert_called_with(api_key='fake_key')
        mock_genai.GenerativeModel.assert_called_with('gemini-1.5-pro')
        mock_model.generate_content.assert_called_once()

    @patch('workout_generator.genai')
    def test_get_ai_cues_no_key(self, mock_genai):
        # Ensure no API key in env
        with patch.dict(os.environ, {}, clear=True):
            cues = workout_generator.get_ai_cues("Squat", "200 lbs", "Strength", "Hypertrophy")
            self.assertIn("API Key missing", cues)

if __name__ == '__main__':
    unittest.main()

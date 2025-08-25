import unittest
from unittest.mock import patch
from helpermodules.utils.error_handling import ErrorTimerContext


class TestErrorTimerContext(unittest.TestCase):
    @patch("helpermodules.utils.error_handling.Pub")
    @patch("helpermodules.utils.error_handling.timecheck")
    @patch("helpermodules.utils.error_handling.log")
    def test_error_sets_timestamp_and_logs(self, mock_log, mock_timecheck, mock_pub):
        mock_timecheck.create_timestamp.return_value = 1234567890
        mock_timecheck.check_timestamp.return_value = False

        ctx = ErrorTimerContext("test/topic", "Fehler überschritten", timeout=60, hide_exception=False)
        # Simuliere eine Exception im Context
        with self.assertRaises(ValueError):
            with ctx:
                raise ValueError("Testfehler")

        # Timestamp sollte gesetzt und gepublished werden
        self.assertEqual(ctx.error_timestamp, 1234567890)
        mock_pub().pub.assert_called_with("test/topic", 1234567890)
        mock_log.error.assert_called()  # Logging wurde aufgerufen

    @patch("helpermodules.utils.error_handling.Pub")
    @patch("helpermodules.utils.error_handling.timecheck")
    def test_error_counter_exceeded(self, mock_timecheck, mock_pub):
        ctx = ErrorTimerContext("test/topic", "Fehler überschritten", timeout=60)
        ctx.error_timestamp = 1234567890
        mock_timecheck.check_timestamp.return_value = False

        with patch("helpermodules.utils.error_handling.log") as mock_log:
            result = ctx.error_counter_exceeded()
            self.assertTrue(result)
            mock_log.error.assert_called_with("Fehler überschritten")

    @patch("helpermodules.utils.error_handling.Pub")
    def test_reset_error_counter(self, mock_pub):
        ctx = ErrorTimerContext("test/topic", "Fehler überschritten", timeout=60)
        ctx.error_timestamp = 1234567890
        ctx.reset_error_counter()
        self.assertIsNone(ctx.error_timestamp)
        mock_pub().pub.assert_called_with("test/topic", None)


if __name__ == "__main__":
    unittest.main()

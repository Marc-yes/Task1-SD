import unittest
from unittest.mock import MagicMock
from InsultFilter import InsultFilter  # Assuming InsultFilter code is in insult_filter.py

class TestInsultFilter(unittest.TestCase):
    
    def setUp(self):
        # Create a mock for the RabbitMQ channel
        self.mock_channel = MagicMock()
        # Create an instance of InsultFilter and inject the mock
        self.filter = InsultFilter()
        self.filter.channel = self.mock_channel  # Replace the actual channel with mock

    def test_filter_text(self):
        # Simulate receiving the insult list
        self.filter.insults_list = ["tonto", "idiota"]
        # Simulate receiving a text that needs to be censored
        text = "Eres un tonto y un idiota"
        censored_text = self.filter.filter_text(text)
        # Check if the censored text contains "CENSORED" instead of insults
        self.assertEqual(censored_text, "Eres un CENSORED y un CENSORED")

    def test_callback_insults(self):
        # Simulate receiving the list of insults
        insults = "tonto,idiota,imbécil"
        # Simulate the `method` object with a fake `delivery_tag`
        mock_method = MagicMock()
        mock_method.delivery_tag = "1234"
        
        # Call the callback method with the mock channel and method
        self.filter.callback_insults(self.mock_channel, mock_method, None, insults.encode())
        
        # Check if the insults list was updated correctly
        self.assertEqual(self.filter.insults_list, ["tonto", "idiota", "imbécil"])
        # Ensure that basic_ack was called with the correct delivery_tag
        self.mock_channel.basic_ack.assert_called_with(delivery_tag="1234")

    def test_callback_text(self):
        # Simulate receiving a text from the queue
        text = "Eres un tonto"
        # Simulate the `method` object with a fake `delivery_tag`
        mock_method = MagicMock()
        mock_method.delivery_tag = "5678"
        
        # Call the callback method with the mock channel and method
        self.filter.callback_text(self.mock_channel, mock_method, None, text.encode())
        
        # Ensure that the text was processed and filtered
        self.mock_channel.basic_ack.assert_called_with(delivery_tag="5678")
        
if __name__ == '__main__':
    unittest.main()

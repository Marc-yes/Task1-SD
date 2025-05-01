import unittest
from unittest.mock import MagicMock
from InsultService import InsultService  # Assuming InsultService code is in insult_service.py

class TestInsultService(unittest.TestCase):
    
    def setUp(self):
        # Create a mock for the RabbitMQ channel
        self.mock_channel = MagicMock()
        # Create an instance of InsultService and inject the mock
        self.service = InsultService()
        self.service.channel = self.mock_channel  # Replace the actual channel with mock
        
    def test_add_insult(self):
        # Add a new insult
        result = self.service.add_insult("tonto")
        self.assertTrue(result)
        # Try adding the same insult again
        result = self.service.add_insult("tonto")
        self.assertFalse(result)

    def test_broadcast_insults(self):
        # Ensure that InsultService sends insults correctly
        self.service.insults = {"tonto", "idiota"}
        # Simulate sending insults
        self.service.broadcast_insults()  # Run one loop
        self.mock_channel.basic_publish.assert_called()  # Check that basic_publish was called

    def test_process_text(self):
        # Simulate sending text
        text = "Eres un tonto"
        self.service.process_text(text)
        self.mock_channel.basic_publish.assert_called_with(
            exchange='',
            routing_key='text_queue',
            body=text
        )
        
if __name__ == '__main__':
    unittest.main()

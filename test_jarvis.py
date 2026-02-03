import sys
from unittest.mock import MagicMock, patch

# Mock problematic modules before importing jarvis
sys.modules['pyautogui'] = MagicMock()
sys.modules['speech_recognition'] = MagicMock()
sys.modules['pyttsx3'] = MagicMock()

import pytest
# Now we can safely import Jarvis
from jarvis import Jarvis

@pytest.fixture
def assistant():
    # Patching dependencies that might fail in headless/restricted environment
    with patch('ollama.list'), \
         patch('ollama.chat'):
        return Jarvis()

def test_execute_command_time(assistant):
    with patch.object(assistant, 'speak') as mock_speak:
        assistant.execute_command("que horas são")
        mock_speak.assert_called()
        assert "São exatamente" in mock_speak.call_args[0][0]

def test_check_hardware(assistant):
    with patch.object(assistant, 'speak') as mock_speak, \
         patch('psutil.cpu_percent', return_value=10.0), \
         patch('psutil.virtual_memory') as mock_vm, \
         patch('psutil.disk_usage') as mock_disk:
        mock_vm.return_value.percent = 50.0
        mock_disk.return_value.percent = 30.0
        assistant.check_hardware()
        # Verify the report was spoken
        calls = [call.args[0] for call in mock_speak.call_args_list]
        assert any("CPU em 10.0%" in text for text in calls)
        assert any("RAM em 50.0%" in text for text in calls)
        assert any("Disco em 30.0%" in text for text in calls)

def test_run_network_diagnostics(assistant):
    with patch.object(assistant, 'speak') as mock_speak, \
         patch('jarvis.conf') as mock_conf, \
         patch('jarvis.sniff', return_value=[MagicMock(), MagicMock()]):
        mock_conf.iface = "eth0"
        assistant.run_network_diagnostics()
        calls = [call.args[0] for call in mock_speak.call_args_list]
        assert any("eth0" in text for text in calls)
        assert any("Capturados 2 pacotes" in text for text in calls)

def test_execute_command_llm_fallback(assistant):
    with patch.object(assistant, 'ask_llm', return_value="Resposta do modelo") as mock_ask, \
         patch.object(assistant, 'speak') as mock_speak:
        assistant.execute_command("como está o tempo hoje?")
        mock_ask.assert_called_with("como está o tempo hoje?")
        mock_speak.assert_called_with("Resposta do modelo")

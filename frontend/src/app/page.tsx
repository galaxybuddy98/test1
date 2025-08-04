'use client';

import { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';

export default function Home() {
  const { 
    health, 
    services, 
    users, 
    orders, 
    products,
    isHealthLoading,
    isServicesLoading,
    isLoading,
    error,
    fetchHealth,
    fetchServices,
    fetchUsers,
    fetchOrders,
    fetchProducts
  } = useStore();

  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [message, setMessage] = useState('준비되면 얘기해 주세요.');
  const [inputValue, setInputValue] = useState('');

  useEffect(() => {
    // 초기 데이터 로드
    fetchHealth();
    fetchServices();
    fetchUsers();
    fetchOrders();
    fetchProducts();
  }, [fetchHealth, fetchServices, fetchUsers, fetchOrders, fetchProducts]);

  const handleVoiceCommand = async () => {
    if (!('webkitSpeechRecognition' in window)) {
      setMessage('음성 인식이 지원되지 않는 브라우저입니다.');
      return;
    }

    setIsListening(true);
    setMessage('듣고 있습니다...');

    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'ko-KR';

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setTranscript(transcript);
      setInputValue(transcript);
      processVoiceCommand(transcript);
    };

    recognition.onerror = (event: any) => {
      console.error('음성 인식 오류:', event.error);
      setMessage('음성 인식에 실패했습니다. 다시 시도해주세요.');
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
      setMessage('준비되면 얘기해 주세요.');
    };

    recognition.start();
  };

  const processVoiceCommand = (command: string) => {
    const lowerCommand = command.toLowerCase();
    
    if (lowerCommand.includes('상태') || lowerCommand.includes('헬스')) {
      setMessage('시스템 상태를 확인합니다...');
      fetchHealth();
    } else if (lowerCommand.includes('서비스') || lowerCommand.includes('서비스 목록')) {
      setMessage('등록된 서비스 목록을 확인합니다...');
      fetchServices();
    } else if (lowerCommand.includes('사용자') || lowerCommand.includes('유저')) {
      setMessage('사용자 목록을 확인합니다...');
      fetchUsers();
    } else if (lowerCommand.includes('주문') || lowerCommand.includes('오더')) {
      setMessage('주문 목록을 확인합니다...');
      fetchOrders();
    } else if (lowerCommand.includes('상품') || lowerCommand.includes('제품')) {
      setMessage('상품 목록을 확인합니다...');
      fetchProducts();
    } else if (lowerCommand.includes('전체') || lowerCommand.includes('모든')) {
      setMessage('모든 데이터를 새로고침합니다...');
      fetchHealth();
      fetchServices();
      fetchUsers();
      fetchOrders();
      fetchProducts();
    } else {
      setMessage(`"${command}" 명령을 인식했습니다.`);
    }
  };

  const handleInputSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      processVoiceCommand(inputValue);
      setInputValue('');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'healthy':
      case 'active':
        return 'text-green-600';
      case 'unhealthy':
      case 'inactive':
        return 'text-red-600';
      default:
        return 'text-yellow-600';
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8">
      {/* Main Content */}
      <div className="w-full max-w-2xl">
        {/* Central Prompt */}
        <div className="text-center mb-12">
          <h1 className="text-3xl font-medium text-gray-800 mb-4">
            {message}
          </h1>
        </div>

        {/* Input Field */}
        <form onSubmit={handleInputSubmit} className="w-full">
          <div className="relative w-full">
            <div className="flex items-center bg-gray-100 rounded-full px-6 py-4 shadow-sm">
              {/* Left side - Tools */}
              <div className="flex items-center mr-4">
                <button
                  type="button"
                  className="flex items-center text-gray-500 hover:text-gray-700 transition-colors"
                >
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium">도구</span>
                </button>
              </div>

              {/* Center - Input */}
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="무엇이든 물어보세요"
                className="flex-1 bg-transparent border-none outline-none text-gray-700 placeholder-gray-500 text-lg"
              />

              {/* Right side - Voice and Wave icons */}
              <div className="flex items-center ml-4 space-x-3">
                <button
                  type="button"
                  onClick={handleVoiceCommand}
                  disabled={isListening}
                  className={`p-2 rounded-full transition-all duration-200 ${
                    isListening 
                      ? 'bg-red-500 text-white animate-pulse' 
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                  </svg>
                </button>
                
                {/* Wave/Sound icon */}
                <div className="flex items-center space-x-1">
                  <div className={`w-1 h-3 bg-gray-400 rounded-full ${isListening ? 'animate-pulse' : ''}`}></div>
                  <div className={`w-1 h-5 bg-gray-400 rounded-full ${isListening ? 'animate-pulse' : ''}`}></div>
                  <div className={`w-1 h-3 bg-gray-400 rounded-full ${isListening ? 'animate-pulse' : ''}`}></div>
                </div>
              </div>
            </div>
          </div>
        </form>

        {/* Transcript Display */}
        {transcript && (
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              인식된 명령: "{transcript}"
            </p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 text-center">{error}</p>
          </div>
        )}

        {/* Quick Status (Optional - Minimal) */}
        {health && (
          <div className="mt-8 text-center">
            <div className="inline-flex items-center space-x-2 px-4 py-2 bg-green-50 rounded-full">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-green-700">
                시스템 정상 ({health.active_services}/{health.total_services} 서비스)
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

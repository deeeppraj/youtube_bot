// src/YouTubeChatUI.jsx
import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Youtube, CheckCircle2, X, Play } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function YouTubeChatUI() {
  const [videoUrl, setVideoUrl] = useState('');
  const [videoId, setVideoId] = useState('');
  const [isTranscriptLoaded, setIsTranscriptLoaded] = useState(false);
  const [isLoadingTranscript, setIsLoadingTranscript] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [inputMessage]);

  const extractVideoId = (url) => {
    const regex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
  };

  const handleLoadTranscript = async () => {
    const extractedId = extractVideoId(videoUrl);
    if (!extractedId) {
      alert('Invalid YouTube URL');
      return;
    }

    setIsLoadingTranscript(true);
    setVideoId(extractedId);

    try {
      const res = await fetch(`${API_BASE}/load-transcript`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ videoId: extractedId })
      });

      if (!res.ok) {
        throw new Error("Failed to load transcript");
      }

      const data = await res.json();
      console.log("load-transcript:", data);

      setIsTranscriptLoaded(true);
      setMessages([{
        role: 'assistant',
        content: '✨ Transcript loaded and processed! I can now answer any questions about this video. What would you like to know?'
      }]);
    } catch (err) {
      console.error(err);
      alert("Error loading transcript. Check backend logs.");
    } finally {
      setIsLoadingTranscript(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !isTranscriptLoaded) return;

    const userMessage = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMessage]);
    const queryToSend = inputMessage;
    setInputMessage('');
    setIsTyping(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          videoId,
          query: queryToSend
        })
      });

      if (!res.ok) {
        throw new Error("Chat request failed");
      }

      const data = await res.json();
      const botMessage = {
        role: 'assistant',
        content: data.response || "I couldn't generate a response."
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: '⚠️ Something went wrong talking to the backend.' }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleReset = () => {
    setVideoUrl('');
    setVideoId('');
    setIsTranscriptLoaded(false);
    setMessages([]);
    setInputMessage('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900 flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-800/50 to-slate-900/50 backdrop-blur-xl border-b border-slate-700/50 px-6 py-4 shadow-2xl">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-red-500 to-red-600 p-2.5 rounded-xl shadow-lg">
              <Youtube className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-slate-100 to-slate-300">
                YouTube Transcript Chat
              </h1>
              <p className="text-xs text-slate-400 mt-0.5">Ask questions about any YouTube video</p>
            </div>
          </div>
          {isTranscriptLoaded && (
            <button
              onClick={handleReset}
              className="flex items-center gap-2 px-4 py-2 bg-slate-700/50 hover:bg-slate-700 text-slate-300 rounded-lg transition-all border border-slate-600/50"
            >
              <X className="w-4 h-4" />
              New Video
            </button>
          )}
        </div>
      </div>

      {/* Main Layout */}
      <div className="flex-1 overflow-hidden flex max-w-7xl w-full mx-auto px-6 py-6 gap-6">
        {/* Video Preview Column */}
        {isTranscriptLoaded && videoId && (
          <div className="w-96 flex-shrink-0 flex flex-col gap-4">
            <div className="bg-slate-800/40 backdrop-blur-xl rounded-2xl border border-slate-700/50 overflow-hidden shadow-2xl">
              <div className="aspect-video bg-black relative">
                <iframe
                  className="w-full h-full"
                  src={`https://www.youtube.com/embed/${videoId}`}
                  title="YouTube video preview"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>
            </div>
            <div className="bg-slate-800/40 backdrop-blur-xl rounded-2xl border border-slate-700/50 p-4 shadow-xl">
              <div className="flex items-center gap-2 text-emerald-400 text-sm font-medium mb-2">
                <CheckCircle2 className="w-4 h-4" />
                Transcript Ready
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                The video transcript has been loaded and processed. You can now ask any questions about the content.
              </p>
            </div>
          </div>
        )}

        {/* Chat Column */}
        <div className="flex-1 flex flex-col min-w-0">
          {!isTranscriptLoaded ? (
            /* Initial screen */
            <div className="flex-1 flex items-center justify-center">
              <div className="w-full max-w-2xl space-y-6">
                <div className="text-center mb-8">
                  <div className="inline-block bg-gradient-to-br from-red-500/20 to-red-600/20 p-4 rounded-2xl mb-4">
                    <Play className="w-12 h-12 text-red-400" />
                  </div>
                  <h2 className="text-3xl font-bold text-slate-200 mb-3">Get Started</h2>
                  <p className="text-slate-400">Paste a YouTube URL below to load the transcript and start chatting</p>
                </div>

                <div className="bg-slate-800/40 backdrop-blur-xl rounded-2xl border border-slate-700/50 p-8 shadow-2xl">
                  <label className="block text-sm font-medium text-slate-300 mb-3">
                    YouTube Video URL
                  </label>
                  <div className="flex gap-3">
                    <input
                      type="text"
                      value={videoUrl}
                      onChange={(e) => setVideoUrl(e.target.value)}
                      placeholder="https://youtube.com/watch?v=..."
                      className="flex-1 bg-slate-900/60 border border-slate-600/50 rounded-xl px-4 py-3.5 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-500/50 focus:border-transparent transition-all"
                      disabled={isLoadingTranscript}
                      onKeyPress={(e) => e.key === 'Enter' && handleLoadTranscript()}
                    />
                    <button
                      onClick={handleLoadTranscript}
                      disabled={isLoadingTranscript || !videoUrl.trim()}
                      className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-8 py-3.5 rounded-xl font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-lg hover:shadow-red-500/25"
                    >
                      {isLoadingTranscript ? (
                        <>
                          <Loader2 className="w-5 h-5 animate-spin" />
                          Loading...
                        </>
                      ) : (
                        'Load Transcript'
                      )}
                    </button>
                  </div>
                  
                  {isLoadingTranscript && (
                    <div className="mt-4 flex items-center gap-3 text-sm text-slate-400">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                        <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                        <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                      </div>
                      <span>Processing transcript and building vector store...</span>
                    </div>
                  )}
                </div>

                {videoUrl && extractVideoId(videoUrl) && !isLoadingTranscript && (
                  <div className="bg-slate-800/40 backdrop-blur-xl rounded-2xl border border-slate-700/50 overflow-hidden shadow-2xl">
                    <div className="aspect-video bg-black">
                      <iframe
                        className="w-full h-full"
                        src={`https://www.youtube.com/embed/${extractVideoId(videoUrl)}`}
                        title="YouTube video preview"
                        frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            /* Chat after loading transcript */
            <div className="flex-1 bg-slate-800/40 backdrop-blur-xl rounded-2xl border border-slate-700/50 overflow-hidden shadow-2xl flex flex-col">
              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className="flex gap-3 max-w-[85%]">
                      {msg.role === 'assistant' && (
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center shadow-lg">
                          <Youtube className="w-4 h-4 text-white" />
                        </div>
                      )}
                      <div
                        className={`rounded-2xl px-5 py-3.5 ${
                          msg.role === 'user'
                            ? 'bg-gradient-to-r from-red-500 to-red-600 text-white shadow-lg'
                            : 'bg-slate-700/50 text-slate-200 border border-slate-600/30'
                        }`}
                      >
                        <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                      </div>
                      {msg.role === 'user' && (
                        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-slate-600 to-slate-700 flex items-center justify-center text-white text-sm font-medium border border-slate-500/50">
                          U
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {isTyping && (
                  <div className="flex justify-start">
                    <div className="flex gap-3 max-w-[85%]">
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center shadow-lg">
                        <Youtube className="w-4 h-4 text-white" />
                      </div>
                      <div className="bg-slate-700/50 border border-slate-600/30 rounded-2xl px-5 py-3.5 flex items-center gap-2">
                        <div className="flex gap-1">
                          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                          <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              <div className="p-4 bg-slate-900/60 border-t border-slate-700/50">
                <div className="flex gap-3 items-end">
                  <textarea
                    ref={textareaRef}
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask anything about this video..."
                    rows={1}
                    className="flex-1 bg-slate-800/60 border border-slate-600/50 rounded-xl px-4 py-3 text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-red-500/50 focus:border-transparent transition-all resize-none overflow-hidden"
                    style={{ maxHeight: '150px' }}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputMessage.trim() || isTyping}
                    className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white p-3.5 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-red-500/25 flex items-center justify-center flex-shrink-0"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

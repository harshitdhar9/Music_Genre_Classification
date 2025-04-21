"use client";

import { useState } from "react";
import { Input } from "./components/input";
import { Button } from "./components/button";
import { Upload, Music, Youtube, Headphones, Volume2 } from "lucide-react";

export default function Home() {
  const [youtubeLink, setYoutubeLink] = useState("");
  const [genreResults, setGenreResults] = useState<string[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [generatedMusicUrl, setGeneratedMusicUrl] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPredicting, setIsPredicting] = useState(false);

  const handleGenrePrediction = async () => {
    if (!youtubeLink) return;
  
    setIsPredicting(true);
  
    try {
      const response = await fetch("http://127.0.0.1:8000/predict-youtube", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: youtubeLink }),
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Predicted genre:", data.predicted_genre); 
        setGenreResults([data.predicted_genre]); 
      } else {
        console.error("Error fetching genres:", response.statusText);
      }
    } catch (error) {
      console.error("Error during API call:", error);
    }
  
    setIsPredicting(false);
  };
  
  
  

  const handleMusicGeneration = async () => {
    if (!file) return;
  
    setIsGenerating(true);
  
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch("http://127.0.0.1:8000/generate-music", {
        method: "POST",
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        setGeneratedMusicUrl(data.generatedMusicUrl); 
      } else {
        console.error("Error generating music:", response.statusText);
      }
    } catch (error) {
      console.error("Error during API call:", error);
    }
  
    setIsGenerating(false);
  };
  
  

  const formatFileName = (name: string) => {
    if (name.length > 20) {
      return name.substring(0, 17) + '...';
    }
    return name;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Music className="h-10 w-10 text-purple-400 mr-3" />
            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
              SoundSage
            </h1>
          </div>
          <p className="text-gray-300 text-lg">Understand and generate music with AI</p>
        </div>

        <div className="grid md:grid-cols-1 gap-10">
          {/* 🎵 YouTube Genre Classifier Card */}
          <div className="bg-gray-800 bg-opacity-50 rounded-xl p-6 shadow-lg border border-gray-700 backdrop-blur-sm transition hover:shadow-purple-900/30">
            <div className="flex items-center mb-6">
              <Youtube className="h-6 w-6 text-purple-400 mr-3" />
              <h2 className="text-xl font-semibold text-purple-300">Predict Genre from YouTube Link</h2>
            </div>
            
            <div className="space-y-4">
              <Input
                placeholder="Paste YouTube link here"
                value={youtubeLink}
                onChange={(e) => setYoutubeLink(e.target.value)}
              />
              <Button 
                onClick={handleGenrePrediction} 
                disabled={!youtubeLink || isPredicting}
                className="w-full"
              >
                {isPredicting ? (
                  <>
                    <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                    Processing...
                  </>
                ) : (
                  <>Predict Genre</>
                )}
              </Button>
              {genreResults.length > 0 && (
  <div className="mt-6 bg-gray-900 bg-opacity-40 rounded-lg p-4">
    <div className="flex items-center mb-3">
      <Headphones className="h-5 w-5 text-purple-400 mr-2" />
      <p className="text-lg font-medium text-white">Predicted Genre:</p>
    </div>
    <div className="space-y-3">
      {genreResults.map((genre, idx) => (
        <div key={idx} className="relative">
          <div className="flex justify-between text-sm mb-1">
            <span>{genre}</span>
          </div>
        </div>
      ))}
    </div>
  </div>
)}

            </div>
          </div>

          {/* 🎼 Music Generator Card */}
          <div className="bg-gray-800 bg-opacity-50 rounded-xl p-6 shadow-lg border border-gray-700 backdrop-blur-sm hover:shadow-purple-900/30 transition">
            <div className="flex items-center mb-6">
              <Music className="h-6 w-6 text-purple-400 mr-3" />
              <h2 className="text-xl font-semibold text-purple-300">Generate Music from WAV</h2>
            </div>
            
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center hover:border-purple-400 transition cursor-pointer">
                <input
                  type="file"
                  accept=".wav"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="wav-upload"
                />
                <label htmlFor="wav-upload" className="cursor-pointer flex flex-col items-center">
                  <Upload className="h-8 w-8 text-purple-400 mb-2" />
                  {file ? (
                    <span className="text-purple-300 font-medium">{formatFileName(file.name)}</span>
                  ) : (
                    <span className="text-gray-400">Choose or drop a WAV file</span>
                  )}
                  <span className="text-xs text-gray-500 mt-2">Only .wav files are supported</span>
                </label>
              </div>
              
              <Button 
                onClick={handleMusicGeneration} 
                disabled={!file || isGenerating}
                className="w-full"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Upload className="w-4 h-4 mr-2" /> Generate Music
                  </>
                )}
              </Button>

              {generatedMusicUrl && (
                <div className="mt-6 bg-gray-900 bg-opacity-40 rounded-lg p-4">
                  <div className="flex items-center mb-3">
                    <Volume2 className="h-5 w-5 text-purple-400 mr-2" />
                    <p className="text-lg font-medium text-white">Generated Music</p>
                  </div>
                  
                  <div className="bg-gray-800 rounded-lg p-3">
                    <div className="flex items-center justify-center">
                      <div className="w-full">
                        <audio controls src={generatedMusicUrl} className="w-full" />
                        <div className="flex justify-between text-xs text-gray-400 mt-2">
                          <span>Generated from {file?.name}</span>
                          <span>AI Generated</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Footer */}
        <footer className="mt-16 text-center text-gray-400 text-sm">
          <p>Made with 💜 by SoundSage AI</p>
          <p className="mt-1">© 2025 All rights reserved</p>
        </footer>
      </div>
    </div>
  );
}
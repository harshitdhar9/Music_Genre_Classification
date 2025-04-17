# 🎵 Music Genre Classification 🎧

A deep learning project for classifying music into genres using **Mel Spectrograms** and a **Convolutional Neural Network (CNN)** built with **TensorFlow/Keras**. The model predicts genres from audio clips and provides confidence scores using a softmax output layer. Also features **music generation** using a **Variational Autoencoder (VAE)** and a sleek **Next.js frontend** to showcase results.

---

## 📁 Dataset

- **GTZAN Genre Collection**
- https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification/data
  Contains 10 genres, 100 audio clips per genre (`.wav`, 30 sec each):
  - `blues`, `classical`, `country`, `disco`, `hiphop`, `jazz`, `metal`, `pop`, `reggae`, `rock`
- Each clip is converted to a **Mel Spectrogram** using `librosa`
- Spectrograms are saved as images and used as CNN input

---

## 🔥 Features

- 🎼 Converts audio to spectrograms using `librosa`
- 🖼️ Saves each spectrogram as an image
- 🧹 Manually splits into `train`, `val`, and `test` using `os` (no deprecated Keras utilities!)
- 🧠 Trains a CNN model on spectrogram images
- 📊 Predicts top genres with confidence scores using `softmax`
- 🎶 **Music generation** using a **Variational Autoencoder (VAE)** 
- 🌐 **Frontend web app** built with **Next.js** to demo predictions and display visualizations
- 🚀 Deployed on **Vercel**

---

## 🛠️ Tech Stack

- **Python** – Core language for model development
- **TensorFlow / Keras** – CNN model training
- **Librosa** – Audio processing and Mel Spectrogram generation
- **NumPy / Matplotlib** – Data manipulation and visualization
- **OS / shutil** – Manual dataset splitting (train/val/test)
- **Jupyter Notebooks** – Exploratory analysis and prototyping
- **Git + GitHub** – Version control
- **Kaggle Kernels** – Training environment
- **VAE (Variational Autoencoder)** – For music generation (by teammate)
- **Next.js + TypeScript** – Frontend deployment for predictions & visualizations
- **Vercel** – Hosting the frontend app

---

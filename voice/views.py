from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import AudioFile
import librosa
import numpy as np
import faiss
import pickle
import os
import base64

MODEL_DIR = os.path.join(settings.BASE_DIR, 'static', 'model')
MEDIA_DIR = os.path.join(settings.BASE_DIR)
scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
index_path = os.path.join(MODEL_DIR, 'faiss_index.bin')


def get_high_energy_segment(y, sr, target_duration):
    window_length = int(target_duration * sr)
    half_window = window_length // 2
    max_rms = 0
    max_rms_center = 0

    for center in range(half_window, len(y) - half_window):
        start = center - half_window
        end = center + half_window
        segment = y[start:end]
        rms = np.sqrt(np.mean(segment ** 2))
        if rms > max_rms:
            max_rms = rms
            max_rms_center = center

    start = max(0, max_rms_center - half_window)
    end = start + window_length

    if end > len(y):
        end = len(y)
        start = end - window_length

    return y[start:end]


def process_new_audio(input_path, target_duration=5, target_rms=0.04, sr=22050, n_fft=2048, hop_length=512):
    y, sr = librosa.load(input_path, sr=sr)
    current_duration = librosa.get_duration(y=y, sr=sr)
    original_rms = float(librosa.feature.rms(y=y).mean())  # Convert to Python float

    if current_duration < target_duration or original_rms < target_rms:
        return None

    y_segment = get_high_energy_segment(y, sr, target_duration)
    current_rms = float(np.sqrt(np.mean(y_segment ** 2)))  # Convert to Python float
    if current_rms > 0:
        y_segment *= (target_rms / current_rms)

    mfccs = librosa.feature.mfcc(y=y_segment, sr=sr, n_mfcc=13, n_fft=n_fft, hop_length=hop_length)
    mfccs_flat = mfccs.flatten()

    return mfccs_flat


def find_similar_voices(new_mfccs, index, n_neighbors=3):
    distances, indices = index.search(new_mfccs, n_neighbors)
    return indices[0], distances[0]


def find_similar_files(indices):
    similar_files = []
    for idx in indices:
        similar_file = AudioFile.objects.filter(faiss_index=idx).first()
        if similar_file:
            similar_files.append(similar_file.path)
    return similar_files


def remove_file():
    for file_name in os.listdir(os.path.join(MEDIA_DIR)):
        if file_name.endswith('.wav') or file_name.endswith('.mp3'):
            os.remove(file_name)


def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['audio_file']
        fs = FileSystemStorage(location=MEDIA_DIR)
        name = fs.save(uploaded_file.name, uploaded_file)
        audio_path = fs.path(name)
        if process_new_audio(audio_path) is None:
            response_data = {'status': "error", 'mess': "File audio không đạt yêu cầu về thời lượng hoặc RMS"}
            remove_file()
            return JsonResponse(response_data)

        new_mfccs = process_new_audio(audio_path)

        scaler = pickle.load(open(scaler_path, 'rb'))
        index = faiss.read_index(index_path)

        # Normalize the MFCCs of the new file
        new_mfccs_normalized = scaler.transform(new_mfccs.reshape(1, -1)).flatten()

        # Search for similar files
        new_mfccs_for_search = np.array([new_mfccs_normalized], dtype=np.float32)
        indices, _ = find_similar_voices(new_mfccs_for_search, index)

        # Find similar files in the database
        similar_files = find_similar_files(indices)

        # Convert audio files to base64
        audio_base64 = []
        for dir_path in similar_files:
            # Liệt kê các tệp trong thư mục và chỉ chọn các tệp có đuôi .wav hoặc .mp3
            for file_name in os.listdir(os.path.join(MEDIA_DIR, dir_path)):
                if file_name.endswith('.wav') or file_name.endswith('.mp3'):
                    file_path = os.path.join(MEDIA_DIR, dir_path, file_name)
                    with open(file_path, 'rb') as file:
                        encoded_string = base64.b64encode(file.read()).decode('utf-8')
                        audio_base64.append(encoded_string)
        response_data = {'status': "success", 'similar_files': audio_base64, 'similar_files_names': similar_files}
        remove_file()
        return JsonResponse(response_data)
    else:
        return render(request, 'index.html')


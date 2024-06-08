import json
import librosa
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import AudioFile


def get_high_energy_segment(y, sr, target_duration):
    window_length = int(target_duration * sr)
    half_window = window_length // 2
    max_rms = 0
    max_rms_center = 0

    # Calculate RMS for sliding window
    for center in range(half_window, len(y) - half_window):
        start = center - half_window
        end = center + half_window
        segment = y[start:end]
        rms = np.sqrt(np.mean(segment**2))
        if rms > max_rms:
            max_rms = rms
            max_rms_center = center

    # Determine start and end points for the 5-second segment
    start = max(0, max_rms_center - half_window)
    end = start + window_length

    # Ensure the segment is within bounds
    if end > len(y):
        end = len(y)
        start = end - window_length

    return y[start:end]

@csrf_exempt
def index(request):
    # if request.method == 'POST':
    #     file = request.FILES.get('file')
    #     if not file:
    #         return JsonResponse({'success': False, 'error': 'No file uploaded'})
    #
    #     try:
    #         y, sr = librosa.load(file, sr=None)
    #         duration = librosa.get_duration(y=y, sr=sr)
    #         rms = np.mean(librosa.feature.rms(y=y))
    #
    #         # Kiểm tra điều kiện
    #         if duration < 5:
    #             return JsonResponse({'success': False, 'error': 'Âm thanh chưa đủ 5s'})
    #         if rms < 0.04:
    #             return JsonResponse({'success': False, 'error': 'Âm thanh quá bé'})
    #
    #         # Lấy đoạn 5 giây có mức năng lượng RMS cao nhất
    #         y_segment = get_high_energy_segment(y, sr, target_duration=5.0)
    #
    #         # Chuẩn hóa RMS về 0.04
    #         target_rms = 0.04
    #         current_rms = np.sqrt(np.mean(y_segment**2))
    #         if current_rms > 0:
    #             y_segment *= (target_rms / current_rms)
    #
    #         mfccs = np.mean(librosa.feature.mfcc(y=y_segment, sr=sr, n_mfcc=13), axis=1).tolist()
    #
    #         # Lưu vào model
    #         audio_file = AudioFile(mfccs=mfccs, path=file.name)
    #         audio_file.save()
    #
    #         return JsonResponse({'success': True, 'id': audio_file.id})
    #     except Exception as e:
    #         return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'index.html')

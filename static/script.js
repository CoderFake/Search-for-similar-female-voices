
$(document).ready(function() {
    const dropArea = $('.drop-section');
    const fileSelectorInput = $('.file-selector-input');

    // Trigger file selector when clicked
    $('.file-selector').click(function() {
        fileSelectorInput.click();
    });

    fileSelectorInput.change(function() {
        if (this.files.length > 0) {
            let file = this.files[0]; // Lấy file đầu tiên
            if (typeValidation(file.type)) {
                uploadFile(file);
            } else {
                alert('Chỉ chấp nhận file âm thanh .wav hoặc .mp3');
            }
        }
    });

    // Handle drag over
    dropArea.on('dragover', function(e) {
        e.preventDefault();
        dropArea.addClass('drag-over-effect');
    });

    // Handle drag leave
    dropArea.on('dragleave', function() {
        dropArea.removeClass('drag-over-effect');
    });

    // Handle file drop
    dropArea.on('drop', function(e) {
        e.preventDefault();
        dropArea.removeClass('drag-over-effect');
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            let file = files[0]; // Lấy file đầu tiên
            if (!typeValidation(file.type)) {
                alert('Chỉ chấp nhận file âm thanh .wav hoặc .mp3');
            }
        }
    });

    // Validate file type
    function typeValidation(type) {
        return type === 'audio/wav' || type === 'audio/mp3';
    }
});

$(document).ready(function () {
    const listSection = $('.list-section');
    const listContainer = $('.list');
    const fileSelector = $('.file-selector');
    const fileSelectorInput = $('.file-selector-input');
    const container = $('.container');
    const showFileCol = $('.show-file .row');

    // Kích hoạt lựa chọn file khi nhấn vào button
    fileSelector.on('click', function (e) {
        e.preventDefault();
        fileSelectorInput.click();
    });

    // Xử lý sự kiện thay đổi input file (lựa chọn mới hoặc kéo và thả)
    fileSelectorInput.on('change', function (e) {
        handleFiles(e.target.files);
    });

    // Xử lý sự kiện kéo và thả
    $('.drop-section').on('dragover', function (e) {
        e.preventDefault();
    }).on('drop', function (e) {
        e.preventDefault();
        handleFiles(e.originalEvent.dataTransfer.files);
    });

    // Xử lý danh sách các file được chọn hoặc thả vào
    function handleFiles(files) {
        Array.from(files).forEach(file => {
            if (typeValidation(file)) {
                const li = createListItem(file);
                listContainer.prepend(li); // Thêm vào đầu danh sách
                simulateUpload(li, file); // Mô phỏng quá trình tải lên
            } else {
                alert('Chỉ chấp nhận tệp WAV và tệp MP3 dưới 2MB.');
            }
        });

        // Kiểm tra xem có file nào không
        checkFiles();
    }

    // Tạo một mục li trong danh sách dựa trên file
    function createListItem(file) {
        const iconName = iconSelector(file.type);
        const li = $('<li>').addClass('in-prog').html(`
            <div class="col play-audio">
                <img src="/static/icons/${iconName}" alt="">
            </div>
            <div class="col play-audio">
                <div class="file-name">
                    <div class="name text-truncate d-none d-sm-flex">${file.name}</div>
                    <span>0%</span>
                </div>
                <div class="file-progress d-block align-content-end">
                    <span></span>
                </div>
                <div class="file-size">${(file.size / (1024 * 1024)).toFixed(2)} MB</div>
            </div>
            <div class="col col-btn align-content-center mr-2 d-none">
                <button class="btn btn-danger btn-sm rounded-2 cancel-upload" type="button"><i class="fa fa-trash"></i></button>
            </div>
        `);

        // Thêm sự kiện cho nút hủy tải lên
        li.find('.cancel-upload').on('click', function () {
            li.remove();
            stopPlayingAudio(file);
            $(`#audio-container-${file.name.replace(/\W/g, '_')}`).remove();
            checkFiles();
        });

        return li;
    }

    // Mô phỏng quá trình tải lên
    function simulateUpload(li, file) {
        listSection.show();
        const progressSpan = li.find('.file-progress span');
        let progress = 0;

        const interval = setInterval(() => {
            progress += 10;
            if (progress <= 100) {
                li.find('.file-name span').text(progress + '%');
                progressSpan.css('width', progress + '%');
            } else {
                clearInterval(interval);
                li.removeClass('in-prog').addClass('complete pr-2');
                li.find('.col-btn').removeClass('d-none');
                li.find('.file-progress').css('background-color', '#28a745');
                addAudioPlayer(showFileCol, file);
            }
        }, 100);
    }

    function iconSelector(type) {
        return type.startsWith('audio/') ? 'mp3.png' : 'mp3.png';
    }

    // Kiểm tra loại file
    function typeValidation(file) {
        const isAudioType = file.type === 'audio/wav' || file.type === 'audio/mpeg';
        const isMp3Under2MB = file.type === 'audio/mpeg' && file.size <= 2 * 1024 * 1024;
        return isAudioType && (file.type !== 'audio/mpeg' || isMp3Under2MB);
    }

    // Thêm trình phát âm thanh
    function addAudioPlayer(parent, file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const audioContainer = $('<div>')
                .addClass('col-lg-12 mb-2')
                .attr('id', `audio-container-${file.name.replace(/\W/g, '_')}`);
            const title = $('<h5>').text(`Uploaded File: ${file.name}`).addClass('mt-2 d-flex justify-content-start');
            const audio = $('<audio controls>')
                .attr('src', e.target.result)
                .addClass('mt-2 w-100');

            audioContainer.append(title).append(audio);
            parent.append(audioContainer);
        };
        reader.readAsDataURL(file);
    }

    // Dừng phát âm thanh
    function stopPlayingAudio(file) {
        const audioContainer = $(`#audio-container-${file.name.replace(/\W/g, '_')}`);
        const audio = audioContainer.find('audio')[0];
        if (audio && !audio.paused) {
            audio.pause();
            audio.currentTime = 0;
        }
    }


    // Kiểm tra xem có file nào không và điều chỉnh giao diện
    function checkFiles() {
        if (listContainer.children().length > 0) {
            container.removeClass('compact').addClass('full');
            showFileCol.parent().removeClass('d-none').addClass('col-lg-6');
            $('.form-file').removeClass('col-lg-12').addClass('col-lg-6');
        } else {
            container.removeClass('full').addClass('compact');
            showFileCol.parent().addClass('d-none').removeClass('col-lg-6');
            $('.form-file').removeClass('col-lg-6').addClass('col-lg-12');
        }
    }
});

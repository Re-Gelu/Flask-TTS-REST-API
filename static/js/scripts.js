jQuery(document).ready( () => {

const basic_url =  window.location.protocol + '//' + window.location.host + '/';

const error_text = $('#APIerror')


/* Error API handler */

const error_handler = (response) => {
    if (response.message) {error_text.text(JSON.stringify(response.message));}
    if (response.task_result) {error_text.text(response.task_result);}
    if (response.error) {error_text.text(response.error)}
}


/* Get selection of voices */

$.getJSON(
    url = basic_url + 'api/tts',
    success = (data) => {
        for (const [key, value] of data.voices.entries()) {
            $('#formVoiceSelect').append(`<option value="${key}">${value.name}</option>`);
        }
    }
);


/* Upload event handler */

const event_handler = (data) => {

    /* Place spinner while waiting */
    $('#downloadResultLink').html($('<div class="spinner-border" role="status"><span class="visually-hidden">Идёт обработка...</span></div>'))

    /* Get task info every 1 sec  */
    setTimeout(() => {
        $.getJSON(
            url =  data.task_url,
            success = (data) => {
                if (data.task_status === 'SUCCESS') {
                    if (data.task_result_url) {
                        $('#downloadResultLink').text("Скачать результат!");
                        $('#downloadResultLink').attr('href', data.task_result_url);
                    }
                    else {error_handler(data);}
                }
            }
        );
    }, 1000);

};


/* Submit button event handler */

$('#uploadForm').submit( (event) => {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: basic_url + 'api/tts',
        cache: false,
        contentType: false,
        processData: false,
        data: new FormData(document.querySelector('#uploadForm')),
        dataType : 'json',
        success: (data) => {
            error_text.text('');
            event_handler(data);
        },
        error: (data) => {
            const response = JSON.parse(data.responseText);
            error_handler(response);
        }
    });
});


/* UIKit file uploader handler */

var bar = document.getElementById('js-progressbar');

UIkit.upload('.js-upload', {
    
    type: "POST",
    method: "POST",
    url: basic_url + 'api/tts',
    multiple: false,
    name: "file",

    beforeSend: function (environment) {
        environment.data.set('voice_rate', $('#voiceRateRange').val());
        environment.data.set('voice_id', $('#formVoiceSelect').val());
        environment.data.set('voice_volume', $('#voiceVolumeRange').val());
    },

    loadStart: function (e) {
        error_text.text('');
        bar.removeAttribute('hidden');
        bar.max = e.total;
        bar.value = e.loaded;
    },

    progress: function (e) {
        bar.max = e.total;
        bar.value = e.loaded;
    },

    loadEnd: function (e) {
        bar.max = e.total;
        bar.value = e.loaded;
    },

    complete: function (e) {
        setTimeout(function () {
            bar.setAttribute('hidden', 'hidden');
        }, 500);
        event_handler(JSON.parse(e.responseText));
    },

    error: function () {
        setTimeout(function () {
            bar.setAttribute('hidden', 'hidden');
        }, 500);
        const response = JSON.parse(arguments[0].xhr.responseText);
        error_handler(response);
    },
});

});
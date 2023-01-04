jQuery(document).ready( () => {

const basic_url =  window.location.protocol + '//' + window.location.host + '/';

/* Upload event handler */

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
        success: function(data) {
            $('#downloadResultLink').html($('<div class="spinner-border" role="status"><span class="visually-hidden">Идёт обработка...</span></div>'))
            get_task_info(data);
        }
    });
});


/* Get task info every 1 sec  */

const get_task_info = (data) => {
    const task_url = data.task_url;
    setTimeout(() => {
        $.getJSON(
            url = task_url,
            success = (data) => {
                if (data.task_status === 'SUCCESS') {
                    if (data.task_result_url) {
                        $('#downloadResultLink').text("Скачать результат!");
                        $('#downloadResultLink').attr('href', data.task_result_url);
                    }
                }
            }
        );
    }, 1000);
};

});
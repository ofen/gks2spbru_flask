$(document).ready(function() {

    $('form').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);

        $.post({
            url: '#',
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log(data);
                $('div').removeClass('has-error')
                $('div').find('.help-block').remove();
                $('.selectpicker').val('default').selectpicker('refresh');

                if (data.result == 'OK') {
                    form[0].reset();
                    $('#submitModal').modal();
                } else {
                    for (error in data.result) {
                        $(`#${error}`).parents('.form-group').addClass('has-error');
                        $(`#${error}`).parents('.form-group').append(`<span class="help-block">${data.result[error]}</span>`);
                    }
                }
                
                
            }
        });
    });

    $("#search_data").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#data_list tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    $("#select_data").on("change", function() {
        var value = $(this).val().toLowerCase();
        $("#data_list tbody tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    
    var current_page = 0;

    $('#load_more').on('click', function() {
        var button = $(this);
        $.get({
            url: '#',
            data: {page: current_page += 1},
            success: function(data) {
                console.log(data);
                
                data.result.forEach(function(result) {
                    var item = `<div class="panel panel-default">
                                    <div class="panel-body">
                                        ${result}
                                    </div>
                                </div>`;
                    button.before($(item).hide().fadeIn(500));
                });

                if (current_page == data.lenght - 1) {
                    button.remove();
                    button.unbind('click');
                }

                lazyImageLoading();
            }
        });
    });

    // Lazy image loading
    function lazyImageLoading() {
        var options = {
            rootMargin: '0px',
            trashold: 0
        };

        var preloadImage = function(image) {
            var image_url = image.getAttribute('data-src');
            image.removeAttribute('data-src');
            return image.setAttribute('src', image_url);
        }

        var callback = function(entries, observer) {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    preloadImage(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        };

        var observer = new IntersectionObserver(callback, options);

        var imgs = document.querySelectorAll('[data-src]');

        imgs.forEach(img => {
            observer.observe(img);
        });
    }

    lazyImageLoading();

});
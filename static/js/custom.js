jQuery(document).ready(function($){
    $('.menu-bar').on('click', function(){
        $('body').toggleClass('menubar-show');
    });
    $('.menu-backdrop').on('click', function(){
        $('body').removeClass('menubar-show');
    });
    function process (event) {
        if (!event.lengthComputable) return; // guard
        var downloadingPercentage = Math.floor(event.loaded / event.total * 100);
        // what to do ...
    };
    function onloadstart () {
        alert('start');
    }
    $(document).on('click', '.result-thumb-wrapper .download-btn', function(){
        var dataUrl = $(this).data('download');
        // Then somewhere in your code
        // new jsFileDownloader({ url: dataUrl })
        // .then(function () {
        //     alert('end');
        // })
        // .catch(function (error) {
        //     alert(error);
        //     // Called when an error occurredv
        // });
    }) 
});
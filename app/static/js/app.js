$(document).ready(function() {
    $('.return-btn').on('click', function(event) {
        var bookId = $(this).data('bookId');
        var quantity = $('#quantity' + bookId);
        event.preventDefault();
        $.get('/returnbook/' + bookId, function(data) {
            swal("Good job!", data.status, "success")
            setTimeout(function() {
                location.reload();
            }, 2000);
            console.log(data.status);
            console.log(data.quantity);
        });
    });

    $('.borrow-btn').on('click', function(event) {
        var bookId = $(this).data('bookId');
        event.preventDefault();
        $.get('/borrowbook/' + bookId, function(data) {
            swal("Good job!", data.status, "success");
            setTimeout(function() {
                location.reload();
            }, 2000);
            console.log(data.status);
            console.log(data.quantity);
        });
    });
});

$(document).ready(function() {
    $('#login-btn').click(function() {
        const username = $('#username').val().trim();
        const password = $('#password').val().trim();

        if (!username || !password) {
            $('#error-msg').text('Vui lòng nhập đầy đủ thông tin.');
            return;
        }

        $.ajax({
            url: '/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, password }),
            success: function(response) {
                if (response.success) {
                    window.location.href = "/dashboard";
                } else {
                    $('#error-msg').text(response.message);
                }
            },
            error: function() {
                $('#error-msg').text('Có lỗi xảy ra khi kết nối đến máy chủ.');
            }
        });
    });
});

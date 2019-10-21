$(function() {
    $("#submit")[0].onclick = function() {
        let login = $('#login').val();
        let password = $('#pass').val();
        $.ajax({
            type: "POST",
            data: JSON.stringify({ login, password }),
            url: '/signin',
            headers: {
                'Content-Type': 'application/json'
            },
            success: function (data) {
                console.log(data);
                if (data.status === 'auth') {
                    /**
                     * 1. save token in localStorage
                     * 2. redirect to home page
                     */
                    localStorage.setItem('token', data.token);
                    window.location.replace("/user");
                } else {
                    alert(data.message);
                }
            }
        });
        
    }
});



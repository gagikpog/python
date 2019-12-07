// объект содержащий данные текущего пользователя
let currentUserData = {};

/**
 * @description при загрузки страницы получает данные текущего пользователя
 */
function updateUsedData() {
    return $.ajax({
        url: '/me',
        type: 'get',
        contentType: "application/json",
        success: function(userData) {
            currentUserData = userData;
        }
    });
}

updateUsedData();


function showConfirm(message, description, buttons) {
    return new Promise((res, rej) => {
        showConfirm.done = (answer) => {
            res(answer)
            $('#confirm').hide();
        }
        $('#confirm').show();
        if (!buttons) {
            buttons = {
                MBCANCEL: true,
                MBOK: true
            }
        }
        document.querySelector('#mbOk').style.display = buttons.MBOK ? 'inline-block' : 'none';
        document.querySelector('#mbCancel').style.display = buttons.MBCANCEL ? 'inline-block' : 'none';
        document.querySelector('#messageTitle').textContent = message;
        document.querySelector('#messageDescription').textContent = description;
    });
}

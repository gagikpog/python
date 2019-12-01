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

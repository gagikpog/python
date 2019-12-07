let btnAutoris = document.getElementById('btnAutoris');
let btnRegister = document.getElementById('btnRegister');
let contentForm = document.getElementById('contentForm');
let autoris = document.getElementById('autoris');
let register = document.getElementById('register');

function a(method) {
   if(method) {
        btnRegister.classList.add('button-bordered'); 
        btnAutoris.classList.remove('button-bordered'); 
        contentForm.style.left = '-69%';  
        autoris.classList.add('block-opacity'); 
        register.classList.remove('block-opacity');
   }    
    else {
        btnRegister.classList.remove('button-bordered'); 
        btnAutoris.classList.add('button-bordered');
        contentForm.style.left = '11%';  
        register.classList.add('block-opacity'); 
        autoris.classList.remove('block-opacity'); 
   }
   updateUrl(method)
}

let url = new URL(window.location.href);
a(url.searchParams.get("page") === 'register')

/**
 * @param {string} curLoc - new url
 * @returns {void}
 */
function setLocation(curLoc){
    try {
        history.pushState(null, null, curLoc);
        return;
    } catch(e) {}
    location.hash = '#' + curLoc;
}

/**
 * @url https://stackoverflow.com/questions/1090948/change-url-parameters
 * @param {string} url
 * @param {string} param
 * @param {string} paramVal
 * @returns {string} - new url
 */
function updateURLParameter(url, param, paramVal){
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";
    if (additionalURL) {
        tempArray = additionalURL.split("&");
        for (var i=0; i<tempArray.length; i++){
            if(tempArray[i].split('=')[0] != param){
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }
    }

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}

function updateUrl(method) {
    const _url = url.href;
    const _pageName = method ? 'register' : 'login';
    const newUrl = updateURLParameter(_url, 'page', _pageName);
    setLocation(newUrl);
    url = new URL(window.location.href);
}
let status = true;
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

}

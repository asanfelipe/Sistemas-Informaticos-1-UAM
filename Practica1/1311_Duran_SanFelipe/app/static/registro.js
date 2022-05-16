function validacion(){
    if (document.getElementById("name").value.length <= 3){
        alert("El nombre de usuario introducido es demasiado corto. Debe contener al menos 4 caracteres.");
        console.log(document.getElementById("name").value.length);
        return false;
    }

    else if (document.getElementById("psw").value != document.getElementById("psw2").value){
        alert("Las contraseñas introducidas no coinciden.");
        return false;
    }

    else if (document.getElementById("psw").value.length < 8){
        alert("La contraseña debe tener al menos 8 caracteres.");
        return false;
    }

    else if (document.getElementById("card").value.length != 16 || isNaN(+document.getElementById("card").value)){
        alert("Error al procesar la tarjeta. Debe contener solo números y una longitud de 16.");
        return false;
    }
    
    return true;
}


$(document).ready(function() {
    $('#psw').keyup(function() {
        $('#fortaleza').html(comp_fortaleza($('#psw').val()))
    })

    function comp_fortaleza(psw) {
        var fortaleza = 0
        if (psw.length < 8) {
            $('#fortaleza').removeClass()
            $('#fortaleza').addClass('corta')
            return 'Corta'
        }

        //Como es mayor que 7, adquiere fortaleza
        if (psw.length > 7) fortaleza += 1 
        //Si contiene minúsculas y mayúsculas, adquiere fortaleza
        if (psw.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) fortaleza += 1
        //Si además de letras contiene números, adquiere fortaleza
        if (psw.match(/([a-zA-Z])/) && psw.match(/([0-9])/)) fortaleza += 1
        //Si contiene al menos un caracter especial, adquiere fortaleza
        if (psw.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) fortaleza += 1

        if (fortaleza < 2) {
            $('#fortaleza').removeClass()
            $('#fortaleza').addClass('debil')
            return 'Debil'
        } else if (fortaleza == 2) {
            $('#fortaleza').removeClass()
            $('#fortaleza').addClass('buena')
            return 'Buena'
        } else {
            $('#fortaleza').removeClass()
            $('#fortaleza').addClass('fuerte')
            return 'Fuerte'
       }
    }
});


$(function num_usuarios(){
    setTimeout(num_usuarios, 3000);    //El tiempo va en milisegundos

    $.ajax({
        url: "ajax",
        success: function(response){
            $("#num_usuarios").html(response+" usuarios")
        },
        error: function(error){
            console.log(error);
        }
    });
});

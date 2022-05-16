function check_name() {
    if (document.getElementById('thename').value == 'root') {
        console.log('tip_name: '+document.getElementById('tip_name').outerHTML)
        document.getElementById('tip_name').innerHTML = 'root no es un nombre válido'
        $('#tip_name').css('color','red')
        return false;
    } else {
        return true;
    }
}

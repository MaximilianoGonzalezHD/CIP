$(document).ready(function () {
    $('#formLogin').submit(function (e) {
        e.preventDefault();
        let errores = [];

        const usuario = $('#username').val().trim();
        const contrasena = $('#password').val().trim();

        // Validaciones
        if (usuario === '') errores.push("Debe ingresar su nombre de usuario.");
        if (contrasena === '') errores.push("Debe ingresar su contraseña.");

        // errores 
        if (errores.length > 0) {
            $('#mensajeLogin').html('<div class="alert alert-danger"><ul>' + errores.map(e => `<li>${e}</li>`).join('') + '</ul></div>');
        } else {
            $('#mensajeLogin').html(''); 
            this.submit(); 
        }
    });
});
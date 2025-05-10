$(document).ready(function () {
    $('#formRegistro').submit(function (e) {
        e.preventDefault();
        let errores = [];

        const rut = $('#rut').val().trim();
        const nombre = $('#nombre_primero').val().trim();
        const apellido = $('#apellido').val().trim();
        const correo = $('#correo').val().trim();
        const rol = $('#rol').val();

        if (apellido.length < 3) errores.push("El apellido debe tener al menos 3 caracteres.");
        if (apellido.length > 15) errores.push("El apellido no debe exceder los 15 caracteres.");
        if (!/^[a-zA-Z\s]+$/.test(apellido)) errores.push("El apellido solo debe contener letras y espacios.");

        if (rut === '') errores.push("El RUT es obligatorio.");
        if (!/^\d{1,2}\.\d{3}\.\d{3}-[0-9kK]$/.test(rut)) errores.push("El RUT no es válido.");

        if (nombre.length < 3) errores.push("El nombre debe tener al menos 3 caracteres.");
        if (nombre.length > 15) errores.push("El nombre no debe exceder los 15 caracteres.");
        if (!/^[a-zA-Z\s]+$/.test(nombre)) errores.push("El nombre solo debe contener letras y espacios.");

        if (!correo.match(/^[^@\s]+@[^@\s]+\.[^@\s]+$/)) errores.push("Correo electrónico inválido.");
        if (rol === '') errores.push("Debe seleccionar un rol.");

        if (errores.length > 0) {
            $('#mensaje').html('<ul>' + errores.map(e => `<li>${e}</li>`).join('') + '</ul>');
        } else {
            $('#mensaje').html('');
            this.submit();
        }
    });
});
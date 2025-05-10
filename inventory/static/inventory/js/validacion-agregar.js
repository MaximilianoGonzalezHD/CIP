$(document).ready(function () {
    $('#formagregar').on('submit', function (e) {
        let valido = true;

        $('.text-danger').text('');

        const nombre = $('#nombre').val().trim();
        const metros = parseFloat($('#metros').val());
        const ancho = parseFloat($('#ancho').val());
        const altura = parseFloat($('#altura').val());
        const cantidad = parseInt($('#cantidad').val());
        const codigo = $('#codigo').val().trim();
        const descripcion = $('#descripcion').val().trim();

        if (nombre === '') {
            $('#errorNombre').text('Debe ingresar el nombre del producto.');
            valido = false;
        }
        if (nombre.length < 3) {
            $('#errorNombre').text('El nombre debe tener al menos 3 caracteres.');
            valido = false;
        }
        if (nombre.length > 50) {
            $('#errorNombre').text('El nombre no puede tener más de 50 caracteres.');
            valido = false;
        }
        if (nombre.match(/[^a-zA-Z0-9\s]/)) {
            $('#errorNombre').text('El nombre solo puede contener letras, números y espacios.');
            valido = false;
        }
        if (isNaN(metros) || metros <= 0) {
            $('#errorMetros').text('Debe ingresar una cantidad válida de metros (> 0).');
            valido = false;
        }
        if (metros < 0) {
            $('#errorMetros').text('Los metros no pueden ser negativos.');
            valido = false;
        }

        if (isNaN(ancho) || ancho <= 0) {
            $('#errorAncho').text('Debe ingresar un ancho válido (> 0).');
            valido = false;
        }
        if (ancho < 0) {
            $('#errorAncho').text('El ancho no puede ser negativo.');
            valido = false;
        }

        if (isNaN(altura) || altura <= 0) {
            $('#errorAltura').text('Debe ingresar una altura válida (> 0).');
            valido = false;
        }
        if (altura < 0) {
            $('#errorAltura').text('La altura no puede ser negativa.');
            valido = false;
        }

        if (isNaN(cantidad) || cantidad <= 0) {
            $('#errorCantidad').text('Ingrese una cantidad válida (> 0).');
            valido = false;
        }
        if (cantidad < 0) {
            $('#errorCantidad').text('La cantidad no puede ser negativa.');
            valido = false;
        }

        if (codigo === '') {
            $('#errorCodigo').text('Debe ingresar el código del producto.');
            valido = false;
        }
        if (codigo.match(/[^a-zA-Z0-9]/)) {
            $('#errorCodigo').text('El código solo puede contener letras y números.');
            valido = false;
        }

        if (descripcion.length < 5) {
            $('#errorDescripcion').text('La descripción debe tener al menos 5 caracteres.');
            valido = false;
        }
        if (descripcion.length > 2000) {
            $('#errorDescripcion').text('La descripción no puede tener más de 2000 caracteres.');
            valido = false;
        }

        if (!valido) {
            e.preventDefault();
        }
    });
});
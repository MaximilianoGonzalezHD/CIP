$(document).ready(function () {
    $('#formPedido').on('submit', function (e) {
        let isValid = true;


        $('.text-danger').text('');

        const proveedor = $('#proveedor').val();
        const codigo = $('#codigoProducto').val().trim();
        const cantidad = $('#cantidad').val();

        if (!proveedor) {
            $('#errorProveedor').text('Debe seleccionar un proveedor.');
            isValid = false;
        }

        if (codigo === '') {
            $('#errorCodigo').text('Debe ingresar el código del producto.');
            isValid = false;
        }

        if (cantidad === '' || isNaN(cantidad) || parseInt(cantidad) <= 0) {
            $('#errorCantidad').text('Ingrese una cantidad válida mayor que cero.');
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });
});
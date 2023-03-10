
function NoDescargar() {
    const titulo = '<h2>No es posible descargar reportes.</h2>'
    const texto  = '<p style="font-size:24px;">El usuario actual es <strong style="color:green;">"Asistente"</strong> por lo tanto no debería tener reportes descargables.</p>'
    Swal.fire({
        html: titulo+texto,
        icon: 'info',
        confirmButtonText: 'Ok',
        backdrop: 'rgba(0, 0, 255, 0.1)',
    })
}
function DescargarReporte(idPersona, nombreCompleto) {
    const titulo = "<h2>¿Estás seguro?</h2>"
    const texto  = '<p style="font-size:24px;">Descargarás todos los reportes de <strong style="color:blue;">"' + nombreCompleto + '"</strong></p>'
    Swal.fire({
        html: titulo+texto,
        icon: 'warning',
        confirmButtonText: 'Si, descargar',
        showDenyButton: true,
        denyButtonText: 'No, cancelar',
        backdrop: 'rgba(255, 255, 0, 0.1)',
    }).then((result) => {
        if (result.isDenied) {
            const titulo = '<h2>Cancelado</h2>'
            const texto = '<p style="font-size:24px;">No se descargarán los reportes de este usuario.</p>'
            Swal.fire({
                html: titulo+texto,
                icon: 'info',
                confirmButtonText: 'Ok',
                backdrop: 'rgba(0, 0, 255, 0.1)',
            })
        } else if (result.isConfirmed) {
            const titulo = '<h2>¡Ok!</h2>'
            const texto  = '<p style="font-size:24px;">Se descargarán los reportes de <strong style="color:blue;">"' + nombreCompleto + '"</strong> en los próximos segundos...</p>'
            Swal.fire({
                html: titulo+texto,
                icon: 'success',
                confirmButtonText: 'Ok',
                backdrop: 'rgba(0, 255, 0, 0.1)',
            })
            setTimeout(function(){ window.location.href = "/Reporte-Usuario/"+idPersona+"/"; }, 2000);
        }
    })
}
function EditarUsuario(nombreCompleto) {
    const titulo = "<h2>¿Estás seguro?</h2>"
    const texto = '<p style="font-size:24px;">Editarás algunos datos del usuario: <strong style="color:blue;">"' + nombreCompleto + '"</strong></p>'
    Swal.fire({
        html: titulo+texto,
        icon: 'warning',
        confirmButtonText: 'Si, actualizar',
        showDenyButton: true,
        denyButtonText: 'No, cancelar',
        backdrop: 'rgba(255, 255, 0, 0.1)',
    }).then((result) => {
        if (result.isDenied) {
            const titulo = '<h2>Cancelado</h2>'
            const texto  = '<p style="font-size:24px;">No se han editado los datos del usuario: <strong style="color:blue;">"' + nombreCompleto + '"</strong>.</p>'
            Swal.fire({
                html: titulo+texto,
                icon: 'info',
                confirmButtonText: 'Ok',
                backdrop: 'rgba(0, 0, 255, 0.1)',
            })
        } else if (result.isConfirmed) {
            const titulo = '<h2>¡Ok!</h2>'
            const texto  = '<p style="font-size:24px;">Se actualizarán los datos de <strong style="color:blue;">"' + nombreCompleto + '"</strong> en los próximos segundos...</p>'
            Swal.fire({
                html: titulo+texto,
                icon: 'success',
                confirmButtonText: 'Ok',
                backdrop: 'rgba(0, 255, 0, 0.1)',
            })
            Swal.fire(
                '¡Ok!',
                'Se actualizarán los datos de <strong style="color:blue;">"' + nombreCompleto + '"</strong> en los próximos segundos...',
                'success'
            )
            setTimeout(function(){ document.forms["formulario-editar-usuario"].submit(); }, 2000);
        }
    })
}
function DesactivarActivarUsuario(isActive, nombreCompleto) {
    
    if (isActive == 1) {
        var activo = 'desactivar'
        var accion = 'ya <strong style="color:red;">NO</strong> '
    } else if (isActive == 0) {
        var activo = 'activar'
        var accion = ''
    }
    const titulo = '<h2>¿Estás seguro de querer <strong style="color:red;">' + activo + '</strong> este usuario?</h2>'
    const texto  = '<p style="font-size:24px;"><strong style="color:red;">' + activo.charAt(0).toUpperCase() + activo.slice(1) + 'ás</strong> al usuario <strong style="color:blue;">"' + nombreCompleto + '"</strong>, con esto ' + accion + 'podrá acceder a las funcionalidades de este sistema.</p>'
    Swal.fire({
        html: titulo+texto,
        icon: 'warning',
        showDenyButton: true,
        denyButtonText: 'Si, ' + activo,
        confirmButtonText: 'No, cancelar',
        backdrop: 'rgba(255, 0, 0, 0.1)',
    }).then((result) => {
        if (result.isConfirmed) {
            const titulo = '<h2>Cancelado</h2>'
            const texto = '<p style="font-size:24px;">No se <strong style="color:red;">' + activo + 'á</strong> al usuario.</p>'
            Swal.fire({
                html: titulo+texto,
                icon: 'info',
                confirmButtonText: 'Ok',
                backdrop: 'rgba(0, 0, 255, 0.1)',
            })
        } else if (result.isDenied) {
            const titulo = '<h2>¡Ok!</h2>'
            const texto  = '<p style="font-size:24px;">Se <strong style="color:red;">' + activo + 'á</strong> al usuario <strong style="color:red;">"' + nombreCompleto + '"</strong> en los próximos segundos...</p>'
            Swal.fire({
                html: titulo+texto,
                icon: 'success',
                confirmButtonText: 'Ok',
                backdrop: 'rgba(0, 255, 0, 0.1)',
            })
            setTimeout(function(){ document.forms["formulario-cambiar-activo"].submit(); }, 2000);
        }
    })
}
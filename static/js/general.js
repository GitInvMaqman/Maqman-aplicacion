function mostrarImagen(input, prev){
    const image = document.getElementById(prev);
    //CAPTURAMOS LA IMAGEN SELECCIONADA
    input.addEventListener("change", (e) => {
        console.log(e.target.files[0]);
        let imageBinary = null;
        //LEEMOS EL BINARIO DE LA IMAGEN
        const reader = new FileReader();
        reader.readAsDataURL(e.target.files[0]);
        reader.onload = (e) => {
            e.preventDefault();
            image.setAttribute('src', e.target.result)
        };
    });
}
function formatRut(idRut){
    // XXXXXXXX-X
    const rut = document.getElementById(idRut).value;
    const newRut = rut.replace(/\./g,'').replace(/\-/g, '').trim().toLowerCase();
    const lastDigit = newRut.substr(-1, 1);
    const rutDigit = newRut.substr(0, newRut.length-1)
    let format = '';
    for (let i = rutDigit.length; i > 0; i--) {
        const e = rutDigit.charAt(i-1);
        format = e.concat(format);
        // XX.XXX.XXX-X
        // if (i % 3 === 0){
        //     format = '.'.concat(format);
        // }
    }
    format = format.concat('-').concat(lastDigit);
    document.getElementById(idRut).value = format
  }
function ChangeColColor(chkCol,col) {
    var varCol = document.getElementById(col);
    var varColor = "gainsboro";
    if (chkCol.checked == true) {
        varColor = "palegreen";
    }
    varCol.style.backgroundColor = varColor;
}
function changeFunc() {
    var selectBox = document.getElementById("id_nombre_usuario");
    let selectedValue = selectBox.options[selectBox.selectedIndex].value;
    document.getElementById("idUsuarioInput").innerHTML = '<input type="hidden" name="p_id_persona" id="id_p_id_persona" value="'+selectedValue+'">'
}

function onLoadImage(files){
    console.log(files)
    if (files && files[0]) {
        console.log(files[0])
        const objetoURL = URL.createObjectURL(files[0]);
        document
        .getElementById('nombreArchivo')
        .innerHTML = files[0].name
    }
}
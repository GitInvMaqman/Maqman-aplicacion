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
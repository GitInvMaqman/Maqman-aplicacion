function CalculoHorasArriendo(){
    var input1 = document.getElementById('time1');
    var input2 = document.getElementById('time2');
    var strMsg = '';

    var date1 = input1.valueAsDate;
    var date2 = input2.valueAsDate;

    var s = (date2.getTime() - date1.getTime());

    var ms = s % 1000;
    s = (s - ms) / 1000;
    var secs = s % 60;
    s = (s - secs) / 60;
    var mins = s % 60;
    var decimal = mins/60;
    var hrs = (s - mins) / 60;
    var horas_arriendo = parseFloat(hrs)+parseFloat((decimal).toFixed(2))

    if ( horas_arriendo < 0 )
        horas_arriendo = 0
    else if ( horas_arriendo > 6)
        horas_arriendo -= 1

    strMsg = horas_arriendo;

    document.getElementById('horasArriendo').innerHTML = '<input value="'+strMsg+'" min="1" type="number" name="horas_arriendo" class="form-reporte" placeholder="Horas de Arriendo" id="id_horas_arriendo" required="" step="0.01">';
}
function CalculoHorometroTotal(){
    var input1 = document.getElementById('horometer1');
    var input2 = document.getElementById('horometer2');
    var strMsg = '';

    var horometer1 = input1.value;
    var horometer2 = input2.value;

    var horometro_total = (horometer2 - horometer1);

    if ( horometro_total < 0 )
        horometro_total = 0

    strMsg = horometro_total.toFixed(2);

    document.getElementById('horometroTotal').innerHTML = '<input style="background-color: palegreen;" value="'+strMsg+'" type="number" name="horometro_total" class="form-reporte" placeholder="Horómetro Total" id="id_horometro_total" required="" step="0.01">';
}

function btnDisabledEnabled(){
    elemet_1 = document.getElementById("inputNumero").value
    elemet_2 = document.getElementById("inputNombre").value
    elemet_3 = document.getElementById("selectMes").value
    elemet_4 = document.getElementById("selectYear").value
    elemet_5 = document.getElementById("inputCCV").value
    val = 0

    if(elemet_1 === ""){
        val++;
    }
    if(elemet_2 === ""){
        val++;
    }
    if(elemet_3 === ""){
        val++;
    }
    if(elemet_4 === ""){
        val++;
    }
    if(elemet_5 === ""){
        val++;
    }
    if(val === 0){
        document.getElementById("btn-enviar").disabled = false;
    }else{
        document.getElementById("btn-enviar").disabled = true;
        localStorage.clear();
    }
}
document.getElementById("inputNumero").addEventListener("keyup", btnDisabledEnabled);
document.getElementById("inputNombre").addEventListener("keyup", btnDisabledEnabled);
document.getElementById("inputCCV").addEventListener("keyup", btnDisabledEnabled);
document.getElementById("selectMes").addEventListener("change", btnDisabledEnabled)
document.getElementById("selectYear").addEventListener("change", btnDisabledEnabled)
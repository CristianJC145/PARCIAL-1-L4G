const compra = new Carrito();
const listaCompra  = document.querySelector('.cart-pay');
const pago =document.querySelector('.cart')
cargarEventos();
function cargarEventos() {

    document.addEventListener('DOMContentLoaded', compra.leerLocalStorageCompra());
    pago.addEventListener("click", (e) => {carro.eliminarProducto(e)});
    compra.calcularTotalCompra();
}
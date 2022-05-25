const compra = new Carrito();
const listaCompra  = document.querySelector('.cart-pay');
const pago =document.querySelector('.restaurant-cart-footer')
cargarEventos();
function cargarEventos() {

    document.addEventListener('DOMContentLoaded', compra.leerLocalStorageCompra());
    compra.calcularTotalCompra();
}
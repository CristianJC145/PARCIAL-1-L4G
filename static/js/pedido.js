const carro = new Carrito();
document.querySelectorAll('.dashboard-content .wrapper-dashboard').forEach(wrapper =>{
    let preveiwContainer=wrapper.querySelector('.products-preview')
    let previewBox = preveiwContainer.querySelector('.preview')
    previewBox.querySelector('.cart').onclick = (e) =>{
      carro.agregarProducto(e);
      preveiwContainer.style.display = 'none';
      previewBox.classList.remove('active');

    };
});

const carrito = document.getElementById("dashboard-order");
const productos = document.getElementById("products-preview");
const listaProductos = document.querySelector("#order-wrapper");
const procesarPedidoBtn = document.getElementById('checkout');

//const cantidadPedidoBtn = document.querySelector('.cantidadPedidoBtn')
//const vaciarCarritoBtn = document.getElementById("vaciar-carrito");

cargarEventListeners();

function cargarEventListeners() {
    carrito.addEventListener("click", (e) => {carro.eliminarProducto(e)});
    document.addEventListener("DOMContentLoaded", carro.leerLocalStorage());
    procesarPedidoBtn.addEventListener("click", (e) => {carro.procesarPedido(e)})
    carro.calcularTotal();
}
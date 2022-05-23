document.querySelectorAll('.dashboard-content .wrapper-dashboard').forEach(wrapper =>{
    let preveiwContainer=wrapper.querySelector('.products-preview')
    let previewBox = preveiwContainer.querySelector('.preview')
    previewBox.querySelector('.cart').onclick = () =>{
      preveiwContainer.style.display = 'none';
      previewBox.classList.remove('active');
    };
});

const carrito = document.getElementById("dashboard-order");
const productos = document.getElementById("products-preview");
const listaProductos = document.querySelector("#order-wrapper");
//const vaciarCarritoBtn = document.getElementById("vaciar-carrito");
console.log(carrito)
cargarEventListeners();

function cargarEventListeners() {
    productos.addEventListener("click", agregarProducto);
    carrito.addEventListener("click", eliminarProducto);
    document.addEventListener("DOMContentLoaded", leerLocalStorage);
}

function agregarProducto(e) {
    e.preventDefault();
    if(e.target.classList.contains("cart")){
        const producto = e.target.parentElement.parentElement;
        leerDatosProducto(producto);
    }
}
function leerDatosProducto(producto){
    const infoProducto = {
        imagen: producto.querySelector('img').src,
        titulo: producto.querySelector('h3').textContent,
        precio: producto.querySelector('.price').textContent,
        id: producto.querySelector('.cart').getAttribute("data-id")
    }

    insertarCarrito(infoProducto);
}
function insertarCarrito(producto){
    const div = document.createElement('div');
    div.innerHTML = `
        <div class="order-card" id="order-card">
            <img class="order-image" src="${producto.imagen}">
            <div class="order-detail">
                <p>${producto.titulo}</p>
                <a href="" class="delete-product" data-id="${producto.id}"><i class="fa fa-times"></i><input type="text" value="1"></a>
            </div>
            <h4 class="order-price">${producto.precio}</h4>
        </div>
    `;
    listaProductos.appendChild(div);
    guardarProductoLocalStorage(producto);
}

function eliminarProducto(e){
    e.preventDefault();
    let producto,
        productoId;
    if(e.target.classList.contains('delete-product')){
        e.target.parentElement.parentElement.remove();
        producto = e.target.parentElement.parentElement;
        productoId = producto.querySelector('.delete-product').getAttribute('data-id');
    }
    eliminarProductoLocalStorage(productoId)
}
function guardarProductoLocalStorage(producto){
    let productos;
    productos = obtenterProductosLocalStorage();
    productos.push(producto);
    localStorage.setItem('productos', JSON.stringify(productos));
}
function obtenterProductosLocalStorage(){
    let productosLS;
    if(localStorage.getItem('productos') == null){
        productosLS = [];
    }else {
        productosLS = JSON.parse(localStorage.getItem('productos'));
    }
    return productosLS;
}

function leerLocalStorage(){
    let productosLS;
    productosLS = obtenterProductosLocalStorage();
    productosLS.forEach(function(producto){
        const div = document.createElement('div');
        div.innerHTML = `
        <div class="order-card" id="order-card">
            <img class="order-image" src="${producto.imagen}">
            <div class="order-detail">
                <p>${producto.titulo}</p>
                <a href="" class="delete-product" data-id="${producto.id}"><i class="fa fa-times"></i><input type="text" value="1"></a>
            </div>
            <h4 class="order-price">${producto.precio}</h4>
        </div>
        `;
        listaProductos.appendChild(div);
    });
}
function eliminarProductoLocalStorage(producto){
    let productosLS;
    productosLS = obtenterProductosLocalStorage();
    productosLS.forEach(function(productosLS, index){
        if(productosLS.id == producto){
            productosLS.splice(index, 1)
        }
    });
    localStorage.setItem('productos', JSON.stringify(productosLS));
}
function vaciarLocalStorage(){
    localStorage.clear();
}
class Carrito{
    agregarProducto(e) {
        e.preventDefault();
        if(e.target.classList.contains("add-cart")){
            const producto = e.target.parentElement.parentElement;
            this.leerDatosProducto(producto);
        }
    }
    leerDatosProducto(producto){
        const infoProducto = {
            imagen: producto.querySelector('img').src,
            titulo: producto.querySelector('h3').textContent,
            precio: producto.querySelector('.price').textContent,
            id: producto.querySelector('.add-cart').getAttribute("data-id"),
            cantidad : 1
        }
        let productosLS; 
        productosLS= this.obtenterProductosLocalStorage();
        productosLS.forEach(function(productoLS){
            if(productoLS.id === infoProducto.id){
                productosLS = productoLS.id;
            }
        });
        if(productosLS === infoProducto.id){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'El producto ya esta agregado',
                timer: 1500,
                showConfirmButton: false
            })
        }
        else{
            this.insertarCarrito(infoProducto);
        }
    }
    insertarCarrito(producto){
        const div = document.createElement('div');
        div.innerHTML = `
            <div class="order-card" id="order-card">
                <img class="order-image" src="${producto.imagen}">
                <div class="order-detail">
                    <p>${producto.titulo}</p>
                    <a href="" class="delete-product" data-id="${producto.id}"><i class="fa fa-times"></i><input type="number" class="cantidadPedidoBtn" value="1" min="0" max="10"></a>
                </div>
                <h4 class="order-price">${producto.precio}</h4>
            </div>
        `;
        listaProductos.appendChild(div);
        this.guardarProductoLocalStorage(producto);
        this.calcularTotal()  
    }
    
    eliminarProducto(e){
        e.preventDefault();
        let producto,
            productoId;
        if(e.target.classList.contains('delete-product')){
            e.target.parentElement.parentElement.remove();
            producto = e.target.parentElement.parentElement;
            productoId = producto.querySelector('.delete-product').getAttribute('data-id');
        }
        if(e.target.classList.contains('restaurant-cart-item-button')){
            e.target.parentElement.parentElement.remove();
            producto = e.target.parentElement.parentElement;
            productoId = producto.querySelector('.restaurant-cart-item-button').getAttribute('data-id');
            console.log("aqui")
        }
        this.eliminarProductoLocalStorage(productoId)
        this.calcularTotal()
    }

    guardarProductoLocalStorage(producto){
        let productos;
        productos = this.obtenterProductosLocalStorage();
        productos.push(producto);
        localStorage.setItem('productos', JSON.stringify(productos));
        
    }
    obtenterProductosLocalStorage(){
        let productoLS;
        if(localStorage.getItem('productos') === null){
            productoLS = [];
        }else {
            productoLS = JSON.parse(localStorage.getItem('productos'));
        }
        return productoLS;
    }
    
    leerLocalStorage(){
        let productosLS;
        productosLS = this.obtenterProductosLocalStorage();
        productosLS.forEach(function(producto){
            const div = document.createElement('div');
            div.innerHTML = `
            <div class="order-card" id="order-card">
                <img class="order-image" src="${producto.imagen}">
                <div class="order-detail">
                    <p>${producto.titulo}</p>
                    <a href="" class="delete-product" data-id="${producto.id}"><i class="fa fa-times"></i><input type="number" class="cantidadPedidoBtn" value="1" min="0" max="10"></a>
                </div>
                <h4 class="order-price">${producto.precio}</h4>
            </div>
            `;
            listaProductos.appendChild(div);
        });
        this.calcularTotal()
    }
    eliminarProductoLocalStorage(productoId){
        let productosLS;
        productosLS = this.obtenterProductosLocalStorage();
        productosLS.forEach(function(productoLS, index){
            if(productoLS.id == productoId){
                productosLS.splice(index, 1);
            }
        });
        localStorage.setItem('productos', JSON.stringify(productosLS));
    }
    vaciarLocalStorage(){
        localStorage.clear();
    }
    procesarPedido(e){
        e.preventDefault();
        if(this.obtenterProductosLocalStorage().length === 0){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'El carrito esta vacio',
                timer: 1500,
                showConfirmButton: false
            })
        }
        else{
            location.href = "/pedido/finalizar";
        }
    }
    calcularTotal(){
        /*listaProductos.querySelectorAll('.cantidadPedidoBtn').forEach((amount)=>{
            amount.addEventListener('change', () =>{
            });
        });*/
        let total = 0, subtotal = 0 , tax = 0;
        //const itemAmount = Number(amount.value);
        let productoLS;
        productoLS = this.obtenterProductosLocalStorage();
            for(let i = 0; i < productoLS.length; i++){
                let element = Number(productoLS[i].precio * productoLS[i].cantidad);
                total = total + element;
            }
            tax = parseFloat(total * 0.19).toFixed(2);
            subtotal = parseFloat(total-tax).toFixed(2);

        document.getElementById('subtotal').innerHTML = subtotal;
        document.getElementById('tax').innerHTML =  tax;
        document.getElementById('total').innerHTML = total.toFixed(2);
    }

    calcularTotalCompra(){
        let productoLS;
        let total = 0, subtotal = 0 , tax = 0;
        productoLS = this.obtenterProductosLocalStorage();
        for(let i = 0; i < productoLS.length; i++){
            let element = Number(productoLS[i].precio * productoLS[i].cantidad);
            total = total + element;
        }
        tax = parseFloat(total * 0.19).toFixed(2);
        subtotal = parseFloat(total-tax).toFixed(2);

        document.getElementById('subtotal-compra').innerHTML = subtotal;
        document.getElementById('tax-compra').innerHTML =  tax;
        document.getElementById('total-compra').innerHTML = total.toFixed(2);

    }
    leerLocalStorageCompra(){
        let productosLS;
        productosLS = this.obtenterProductosLocalStorage();
        productosLS.forEach(function(producto){
            const div = document.createElement('div');
            div.innerHTML = `
                <div class="restaurant-cart-items-list">
                    <p class="restaurant-cart-group-name">Pollos</p>
                    <div class="restaurant-cart-item">
                        <div class="restaurant-cart-item-description">
                            <span>${producto.cantidad}x ${producto.titulo}</span>
                            <span>$ ${producto.precio}</span>
                        </div>
                    </div>
                    <div class="restaurant-cart-item-garnish">
                        <span>Con cubiertos</span>
                    </div>
                </div>

                <div class="restaurant-cart-item-buttons-wrapper">
                    <button type="button" role="button" label="Editar" class="restaurant-cart-item-button">
                        <span class="btn-label">Editar</span>
                    </button>
                    <button type="button" role="button" class="restaurant-cart-item-button btn--delete" data-id="${producto.id}">
                        <span class="btn-label">Eliminar</span>
                    </button>
                </div>
            `;
            listaCompra.appendChild(div);
            this.eliminarProducto(e)
        });
        
    }
}




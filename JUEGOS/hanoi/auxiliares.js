// Contenido final para el archivo: hanoi/auxiliares.js
window.juegoAuxiliares = {
    dibujarEstado: function (q, contenedor) {
        contenedor.innerHTML = '';
        const colores = ['#e74c3c', '#f1c40f', '#3498db', '#2ecc71', '#9b59b6', '#e67e22'];
        const torres = q.split('|').map(torreStr => torreStr ? torreStr.split(',').map(Number) : []);

        torres.forEach((discos, index) => {
            const torreEl = document.createElement('div');
            torreEl.className = 'torre';
            torreEl.dataset.torreId = index;

            const baseEl = document.createElement('div');
            baseEl.className = 'base';
            
            const posteEl = document.createElement('div');
            posteEl.className = 'poste';

            const discosContenedor = document.createElement('div');
            discosContenedor.className = 'discos-contenedor';

            discos.forEach(tamanoDisco => {
                const discoEl = document.createElement('div');
                discoEl.className = 'disco';
                discoEl.style.width = `${30 + tamanoDisco * 15}%`;
                discoEl.style.backgroundColor = colores[tamanoDisco - 1];
                discosContenedor.prepend(discoEl);
            });
            
            torreEl.appendChild(discosContenedor);
            torreEl.appendChild(posteEl);
            torreEl.appendChild(baseEl);
            contenedor.appendChild(torreEl);
        });
    },

    capturarEntrada: function (q, contenedor, leerEntradaUsuario) {
        let torreOrigen = null;
        if (window.hanoiClickListener) {
            contenedor.removeEventListener('click', window.hanoiClickListener);
        }
        window.hanoiClickListener = (event) => {
            const torreClicadaEl = event.target.closest('.torre');
            if (!torreClicadaEl) return;
            const idTorreClicada = torreClicadaEl.dataset.torreId;
            if (torreOrigen === null) {
                torreOrigen = idTorreClicada;
                torreClicadaEl.classList.add('seleccionada');
            } 
            else if (torreOrigen === idTorreClicada) {
                torreOrigen = null;
                torreClicadaEl.classList.remove('seleccionada');
            }
            else {
                const entrada = `${torreOrigen}${idTorreClicada}`;
                leerEntradaUsuario(entrada);
                torreOrigen = null; 
            }
        };
        contenedor.addEventListener('click', window.hanoiClickListener);
    },
};
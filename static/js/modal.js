

document.querySelectorAll('.dashboard-content .wrapper-dashboard').forEach(wrapper =>{
  let dashboardcard=wrapper.querySelector('.dashboard-card')
  let preveiwContainer=wrapper.querySelector('.products-preview')
  let previewBox = preveiwContainer.querySelector('.preview')

  dashboardcard.onclick = () =>{
    preveiwContainer.style.display = 'flex';
    previewBox.classList.add('active');
  };

  previewBox.querySelector('.fa-times').onclick = () =>{
    preveiwContainer.style.display = 'none';
    previewBox.classList.remove('active');
  };
});


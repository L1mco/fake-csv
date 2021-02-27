'use strict';

const datasetRows = document.querySelectorAll('.dataset_row_block');
const checkStatus = () => {
  for (let row of datasetRows) {

    fetch(`${checkIsReadyUrl}?dataset_id=${row.dataset.datasetId}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
    })
      .then(response => {
          if (!response.ok)
            throw Error(response.statusText);
          return response.json();
        }
      )
      .then(responseJSON => {
        if (responseJSON['rendered_html']) {
          row.innerHTML = '';
          row.innerHTML = responseJSON['rendered_html'];
        }
      })
  }
};

// setInterval(
//   checkStatus, 5000
// );

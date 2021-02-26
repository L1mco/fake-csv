'use strict';

/* delete schema */

const schemaDeleteBtns = document.querySelectorAll('.schema_delete_btn');

for (let schemaDeleteBtn of schemaDeleteBtns) {
  schemaDeleteBtn.onclick = (e) => {
    const schemaBlock = schemaDeleteBtn.parentElement.parentElement
    e.preventDefault()
    const data = {
      schema_id: schemaDeleteBtn.dataset.schemaId,
    };

    fetch(schemaDeleteBtn.dataset.targetUrl, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(data),
    })
      .then(response => {
          if (!response.ok)
            throw Error(response.statusText);
          schemaBlock.remove()
        }
      )
  }
}


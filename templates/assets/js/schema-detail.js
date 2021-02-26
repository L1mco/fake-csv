'use strict';


/* Update schema`s main info */

const schemaMainForm = document.querySelector('.schema-main-form');
const schemaTitleInput = document.querySelector('#schema_title');
const schemaSeparator = document.querySelector('#schema_separator');
const schemaQuote = document.querySelector('#schema_quote');
const updateErrorMsg = document.querySelector('.update-error-msg');

schemaMainForm.onsubmit = (e) => {
  e.preventDefault()
  const data = {
    schema_id: schemaMainForm.dataset.schemaId,
    title: schemaTitleInput.value,
    separator: schemaSeparator.value,
    quote: schemaQuote.value,
  }
  fetch(schemaMainForm.dataset.targetUrl, {
    method: 'POST',
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
        return response.json();
      }
    )
    .then(responseJSON => {
      if (responseJSON['success'] === true)
        updateErrorMsg.classList.add('d-none');
    })
    .catch(error => {
        updateErrorMsg.classList.remove('d-none');
      }
    )
}


/* Add new column */
const newColumnForm = document.querySelector('.new_column_form');
const newColumnType = document.querySelector('#new_column_type');
const newColumnRangeBlocks = document.querySelectorAll('.new_column_range');
const newColumnName = document.querySelector('#new_column_name');
const newColumnRangeFrom = document.querySelector('#new_range_from');
const newColumnRangeTo = document.querySelector('#new_range_to');
const newColumnOrder = document.querySelector('#new_column_order');
const schemaColumnBlock = document.querySelector('.schema_columns_container');
const columnAddBtn = document.querySelector('.add_column_btn');

newColumnType.onchange = () => {
  if (columnTypes[newColumnType.value] === 'True') {
    for (let block of newColumnRangeBlocks) {
      block.classList.add('d-block');
    }
  } else {
    for (let block of newColumnRangeBlocks) {
      block.classList.remove('d-block');
    }
  }
}

newColumnForm.onsubmit = (e) => {
  e.preventDefault();
  const data = {
    'schema_id': schemaId,
    'name': newColumnName.value,
    'type_name': newColumnType.value,
    'order': newColumnOrder.value,
  };
  if (columnTypes[newColumnType.value] === 'True') {
    data.range_from = newColumnRangeFrom.value
    data.range_to = newColumnRangeTo.value
  }

  fetch(newColumnForm.dataset.targetUrl, {
    method: 'POST',
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
        return response.json();
      }
    )
    .then(responseJSON => {
      schemaColumnBlock.append(stringToHTML(responseJSON['rendered_html']));
      newColumnOrder.classList.remove('border', 'border-danger', 'text-danger');
      newColumnOrder.value = (parseInt(newColumnOrder.value.toString()) + 1)
      updateColumnInfo();
      deleteColumn();
    })
    .catch(error => {
        updateErrorMsg.classList.remove('d-none');
        newColumnOrder.classList.add('border', 'border-danger', 'text-danger');
        updateColumnInfo();
        deleteColumn();
      }
    )
  columnAddBtn.setAttribute('disabled', 'disabled');
  setTimeout(() => {
    columnAddBtn.removeAttribute('disabled')
  }, 1000);
  toggleRange();
}


/* column update */


const updateColumnInfo = () => {
  const columnInputs = document.querySelectorAll('.column_input');
  for (let input of columnInputs) {
    const columnId = input.parentElement.parentElement.dataset.columnId;
    input.onfocus = () => {
      input.classList.add('text-warning');
    }
    input.onblur = () => {
      const data = {
        column_id: columnId,
        column_info: {
          field: input.dataset.field,
          value: input.value
        }
      };
      fetch(columnUpdateUrl, {
        method: 'PATCH',
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
            return response.json()
          }
        )
        .then(responseJSON => {
          input.classList.remove('text-warning','text-danger')
          input.classList.add('text-success')
        })
        .catch(error => {
            input.classList.remove('text-warning','text-success')
            input.classList.add('text-danger')
          }
        )
      setTimeout(() => {
        input.classList.remove('text-success','text-warning');
      }, 1000)
    }
  }
  toggleRange();
}


const toggleRange = () => {
  const columnTypeSelects = document.querySelectorAll('.column_type_select');
  for (let columnTypeSelect of columnTypeSelects) {
    columnTypeSelect.onchange = () => {
      const columnRow = columnTypeSelect.parentElement.parentElement;
      const fromBlock = columnRow.childNodes[5];
      const toBlock = columnRow.childNodes[7];
      const rangeBlocks = [fromBlock.childNodes[1], toBlock.childNodes[1]]

      for (let block of rangeBlocks) {
        if (columnTypes[columnTypeSelect.value] === 'True') {
          block.classList.add('d-block');
          block.classList.remove('d-none');
        } else {
          block.classList.add('d-none');
          block.classList.remove('d-block');
        }
      }
    }
  }
}

const deleteColumn = () => {
  const deleteColumnBtns = document.querySelectorAll('.delete_column_btn');

  for (let deleteColumnBtn of deleteColumnBtns) {
    deleteColumnBtn.onclick = (e) => {
      const columnBlock = deleteColumnBtn.parentElement.parentElement.parentElement
      e.preventDefault()
      const data = {
        column_id: columnBlock.dataset.columnId,
      };

      fetch(columnUpdateUrl, {
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
            columnBlock.remove()
          }
        )
    }
  }
}

updateColumnInfo();
toggleRange();
deleteColumn();


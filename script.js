let query = window.location.search
let url_params = new URLSearchParams(query)
let tasks = url_params.get('tasks')
let name = url_params.get('name')

try {
    tasks = JSON.parse(tasks)
    console.log(localStorage.getItem('task'))
    if (tasks != null && tasks.length > 0) {
        localStorage.setItem('task', JSON.stringify(tasks))
    }
    console.log(localStorage.getItem('name'))
    if (name != null && name.length > 0) {
        localStorage.setItem('name', JSON.stringify(name))
    }
}

catch(err) {
    console.log(err, 'test')
}

if (tasks == null) {
    tasks = JSON.parse(localStorage.getItem('task'))
}

if (name == null) {
    name = JSON.parse(localStorage.getItem('name'))
}

document.getElementById('name').textContent = name

let list_area = document.getElementById('list')
tasks.forEach((task)=> {
    let taskElement = document.createElement('a')
    let form = document.createElement('form')
    let button = document.createElement('button')
    taskElement.textContent = task.title
    taskElement.href = task.url
    form.action = `/test/${task.title}`
    console.log(form.action)
    button.type = 'submit'
    button.innerHTML = 'Study'
    list_area.appendChild(form)
    form.appendChild(taskElement)
    form.appendChild(button)
})

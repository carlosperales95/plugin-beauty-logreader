// prevent the default behavior of web browser
['dragleave', 'drop', 'dragenter', 'dragover'].forEach(function (evt) {
    document.addEventListener(evt, function (e) {
        e.preventDefault();
    }, false);
});

// Create previews for visible data in hidden rows
let table = document.getElementsByTagName('table')[0];
let tableParts = table.children;
let tableHeaders = tableParts[0].children;
let tableRows = tableParts[1].children;

for (var i = 0; i < tableRows.clientHeight; i++) {
    tableRows[i].addEventListener('click', function (e) {
        e.preventDefault();
        let emptyTh = document.createElement('th');
        let emptyTd = document.createElement('td');
    
        let emptyTr = document.createElement('tr');
        emptyTr.appendChild(emptyTh);
        emptyTr.appendChild(emptyTd);
    
        emptyTr.appendChild(tableRows[i].children[3]);
        emptyTr.appendChild(emptyTd);

        tableParts[1].appendChild(emptyTr);
    })
}

function collapseSideBar() {
    let stickyCont = document.getElementsByClassName('position-sticky')[0];
    let container = document.getElementsByClassName('container')[0];
    let sidebar = document.getElementById('sidebarMenu');
    let toggleIcon = document.getElementById('sidebar-toggle');

    if(sidebar.classList.contains('collapsed')) {
        sidebar.classList.remove('collapsed');
        stickyCont.classList.remove('collapsed');
        container.classList.remove('expanded');
        toggleIcon.innerHTML = '&#8612;';
    }
    else {
        sidebar.classList.add('collapsed');
        stickyCont.classList.add('collapsed');
        container.classList.add('expanded');
        toggleIcon.innerHTML = '&#8614;';
    }
}



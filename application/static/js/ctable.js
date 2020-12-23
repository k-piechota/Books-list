'use strict';
// https://davidwalsh.name/javascript-debounce-function
function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

function api(title, author, from, to, language){
    let request = new XMLHttpRequest();
    request.open('GET', 'api?title=' + encodeURIComponent(title) + '&author=' + encodeURIComponent(author)
                        + '&from=' + encodeURIComponent(from) + '&to=' + encodeURIComponent(to)
                        + '&language=' + encodeURIComponent(language));
    request.send();
    request.onload = () => {
        return createBookList(JSON.parse(request.response))
    }
}

function createAuthors(authorsList){
   const authors = authorsList.join(", ");
   return document.createTextNode(authors);
}

function createThumbnailLink(thumbnail) {
    if(thumbnail !== null){
    const i = document.createElement('i');
    i.className = "material-icons";
    i.appendChild(document.createTextNode('link'));

    const link = document.createElement('a');
    link.href = thumbnail;
    link.appendChild(i);
    return link;
    }
}

function createEditLink(isbn) {
    const div = document.createElement('div');
    const i_edit = document.createElement('i');
    i_edit.className = "material-icons";
    i_edit.appendChild(document.createTextNode('edit'));

    const link = document.createElement('a');
    link.href = 'edit?isbn=' + isbn;
    link.appendChild(i_edit);

    const i_delete = document.createElement('i');
    i_delete.className = "material-icons";
    i_delete.appendChild(document.createTextNode('delete'));

    const delete_link = document.createElement('a');
    delete_link.href = 'delete?isbn=' + isbn;
    delete_link.appendChild(i_delete);

    div.appendChild(link);
    div.appendChild(document.createTextNode(' '));
    div.appendChild(delete_link);

    return div;
}

function createBookList(books) {
    const table = document.getElementById("table-body");
    table.innerHTML = '';
    books.forEach( function(book){
        let tr = document.createElement('TR');
        [
            document.createTextNode(book['title']),
            createAuthors(book['authors']),
            document.createTextNode(book['publishedDate']),
            document.createTextNode(book['isbn']),
            document.createTextNode(book['pageCount']),
            createThumbnailLink(book['thumbnail']),
            document.createTextNode(book['language']),
            createEditLink(book['isbn'])

        ].forEach( function(cell){
            const td = document.createElement('TD');
            td.appendChild(cell);
            tr.appendChild(td);
        });

        table.appendChild(tr);
    });
}

function updateFilter(e) {
    const title = document.getElementById('title');
    const author = document.getElementById('author');
    const fromDate = document.getElementById('from');
    const toDate = document.getElementById('to');
    const language = document.getElementById('language');
    api(title.value, author.value, fromDate.value, toDate.value, language.value);
}


function createTable() {
    api('','','','','');
    const title = document.getElementById('title');
    const author = document.getElementById('author');
    const fromDate = document.getElementById('from');
    const toDate = document.getElementById('to');
    const language = document.getElementById('language');
    title.addEventListener('input', debounce(updateFilter, 400));
    author.addEventListener('input', debounce(updateFilter, 400));
    fromDate.addEventListener('input', debounce(updateFilter, 400));
    toDate.addEventListener('input', debounce(updateFilter, 400));
    language.addEventListener('input', debounce(updateFilter, 400));


}


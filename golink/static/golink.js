async function fetchSuggestions(current) {
    let headers = new Headers();
    headers.append('Accept', 'application/json');
    let url = `/+search?q=${encodeURIComponent(current)}`;
    let request = new Request(url, {headers: headers});
    let response = await fetch(request);
    return await response.json();
}

function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

window.onload = evt => {
    document.querySelector('input[type=search]').addEventListener('input', async (evt) => {
        if (!(evt instanceof InputEvent)) {
            // Only fire for user input
            return;
        }

        let initialQuery = evt.target.value;
        await sleep(250);
        let query = evt.target.value;
        if (query !== initialQuery) {
            // Query changed - don't fetch yet!
            return;
        }

        let golinks = [];
        if (query) {
            let results = await fetchSuggestions(query);
            golinks = results.golinks;
        }

        let datalist = document.createElement('datalist');
        datalist.id = 'search_datalist';
        for (let golink of golinks) {
            // \u21D2 (double-right arrow - &rArr;)
            datalist.appendChild(new Option(`${golink.name} \u21D2 ${golink.url}`, golink.name));
        }

        // Switch out old datalist with new one
        let oldDatalist = document.getElementById('search_datalist');
        oldDatalist.parentNode.insertBefore(datalist, oldDatalist);
        oldDatalist.parentNode.removeChild(oldDatalist);
    })
};

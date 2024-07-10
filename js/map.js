d3.csv('/csv/processed_data_map.csv', function(err, rows) { //parse data with d3
    function unpack(rows, key) {
        return rows.map(function(row) {return row[key];}); 
    }
    let origin = unpack(rows, 'Origin'),
        title = unpack(rows, 'Title'),
        authors = unpack(rows, 'Author'),
        recipient = unpack(rows, 'Recipient')
        lat = unpack(rows, 'start_lat'),
        long = unpack(rows, 'start_long'),
        years = unpack(rows, 'Year'),
        month = unpack(rows, 'Month'),
        day = unpack(rows, 'Day'),
        color = unpack(rows, 'Color'),
        seasons = unpack(rows, 'Season');
      
    let uniqueAuthor = []; 
    for (let i = 0; i < authors.length; i++) {
        if (!uniqueAuthor.includes(authors[i])) {
            uniqueAuthor.push(authors[i])
        }
    }
    let list = document.getElementById('author_list')
    uniqueAuthor.forEach(function(item) {
        let option = document.createElement('option');
        option.value = item;
        list.appendChild(option);
    })
        
    let uniqueYears = Array.from({ length: 101 }, (value, index) => index + 1820); //Create array [1820, 1821, ... , 1920]

    let data = [];


    let map = L //set up the map to center on Philadelphia and limit panning
        .map("map", {
            maxBounds: [[-90, -260],[90, 260]],
            maxBoundsViscosity: 1
        })
        .setView([39.9526,-75.1652], 2);

    L.tileLayer( //Actual map layer used, with attribution
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
        maxZoom: 10,
    }).addTo(map);

    for (var i = 0; i < title.length; i++) { //add circular markers w/ popups for each location
        circle = L.circleMarker([lat[i], long[i]], { 
            color: color[i],
            fillColor: color[i],
            radius: 2,
        })
        .bindPopup(title[i] +  '<br />' + authors[i] + '<br />' + recipient[i] + '<br /> Season: ' + seasons[i] + '<br /> Year: ' + years[i] + '<br /> Origin: ' + origin[i])
        .addTo(map);

        data.push({'marker': circle, 'season': seasons[i], 'author': authors[i], 'year': Number(years[i])});
    };


    filterDict = { //determines what points are kept based on current filters
        'season': ['Winter', 'Spring', 'Summer', 'Fall'],
        'author': uniqueAuthor,
        'year': uniqueYears
    };

    function filterMap() {
        for (let i = 0; i < data.length; i++) { //repeat for every data point
            map.removeLayer(data[i].marker) //start by removing every marker
            add = true //if any below value is false, this will be false, else true
            for (let key in filterDict) { //check that the marker's variables include the value of the key in the dictionary
                add *= (filterDict[key].includes(data[i][key])) //true * true = true, true * false = false, false * false = false
            }
            if (add == true) { //check that all filters are met
                data[i].marker.addTo(map) //add to map
            }
        }
    }

    function allChecked() { //used to add all markers if all the season boxes and neither author nor year box are checked
        return winterBox.box.checked && springBox.box.checked && summerBox.box.checked && fallBox.box.checked && (!authorBox.checked && !yearBox.checked)
    }

    let allBox = document.querySelector("#all"),
        yearBox = document.querySelector("#year"),
        authorBox = document.querySelector("#author"),
        winterBox = {box: document.querySelector("#winter"), name: "Winter"},
        springBox = {box: document.querySelector("#spring"), name: 'Spring'},
        summerBox = {box: document.querySelector("#summer"), name: 'Summer'},
        fallBox = {box: document.querySelector("#fall"), name: 'Fall'};

    seasonBoxes = [winterBox, springBox, summerBox, fallBox]

    let value = document.querySelector("#year_value");
    let yearInput = document.querySelector("#year_input")
    value.textContent = yearInput.value;
    
    allBox.addEventListener("click", (event => {
        if (allBox.checked) {
            for (let i = 0; i < data.length; i++) {
                map.removeLayer(data[i]) //remove current markers
                data[i].marker.addTo(map) //add back all markers
            }
            winterBox.box.checked = true //check all the season boxes
            springBox.box.checked = true
            summerBox.box.checked = true
            fallBox.box.checked = true
            yearBox.checked = false //uncheck the year and author boxes
            authorBox.checked = false
            //authorInput.value = ''
            filterDict = { //reset filter dictionary
                season: ['Winter', 'Spring', 'Summer', 'Fall'],
                author: uniqueAuthor,
                year: uniqueYears
            };
        }
        filterMap()
    }));


    yearBox.addEventListener("click", (event => {
        allBox.checked = allChecked()
        if (yearBox.checked) {
            filterDict.year = [Number(yearInput.value)] //current year, needs to be in a list as the function iterates over each variable
        }
        else {
            filterDict.year = uniqueYears
        }
        filterMap()
    }))

    authorBox.addEventListener("click", (event => {
        allBox.checked = allChecked()  //uncheck all box if any season box unchecked 
        if (uniqueAuthor.includes(authorInput.value) && authorBox.checked) {
            filterDict.author = [authorInput.value];
        }
        else {
            filterDict.author = uniqueAuthor;
        }
        filterMap();
    }));
    
    winterBox.box.addEventListener("click", (event => {
        allBox.checked = allChecked();
        if (!winterBox.box.checked) {
            filterDict.season = filterDict.season.filter(item => item !== 'Winter'); //remove Winter from season list in filterDict
        }
        else {
            filterDict.season.push('Winter')
        }
        filterMap()
    }));

    springBox.box.addEventListener("click", (event => {
        allBox.checked = allChecked();
        if (!springBox.box.checked) {
            filterDict.season = filterDict.season.filter(item => item !== 'Spring');
        }
        else {
            filterDict.season.push('Spring')
        }
        filterMap()
    }));

    summerBox.box.addEventListener("click", (event => {
        allBox.checked = allChecked();
        if (!summerBox.box.checked) {
            filterDict.season = filterDict.season.filter(item => item !== 'Summer');
        }
        else {
            filterDict.season.push('Summer')
        }
        filterMap()
    }));

    fallBox.box.addEventListener("click", (event => {
        allBox.checked = allChecked();
        if (!fallBox.box.checked) {
            filterDict.season = filterDict.season.filter(item => item !== 'Fall');
        }
        else {
            filterDict.season.push('Fall')
        }
        filterMap()
    }));

    yearInput.addEventListener("input", (event) => {
        value.value = event.target.value; //updates year text input
        filterDict.year = [Number(value.value)]
        if (yearBox.checked) {
            filterMap() //only apply filters if box checked
        }
    });

    value.addEventListener("input", (event) => {
        yearInput.value = value.value //updates year slider
        filterDict.year = [Number(value.value)]
        if (yearBox.checked) {
            filterMap()
        }
    })

    let authorInput = document.querySelector('#author_input')
    authorInput.addEventListener("input", (event) => {
        if (uniqueAuthor.includes(authorInput.value) && authorBox.checked) {
            filterDict.author = [authorInput.value]
            filterMap()
        }
        else {
            filterDict.author = uniqueAuthor
        }
        
    });

    /* Below adapted from https://leafletjs.com/examples/choropleth/ */
    let legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

        let div = L.DomUtil.create('div', 'info legend'),
            grades = ['Winter', 'Spring', 'Summer', 'Fall'],
            colors = ['darkred', 'green', 'yellow', 'orange'];

        
        for (let i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + colors[i] + '"></i> ' +
                grades[i] + '</br>';
        }

        return div;
    };

    legend.addTo(map);

})
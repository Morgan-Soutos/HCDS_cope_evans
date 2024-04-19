d3.csv('/csv/processed_data_timeline.csv', function(err, rows) {
    function unpack(rows, key) {
        return rows.map(function(row) {return row[key];}); 
    }
    
    let title = unpack(rows, 'Title'),
        authors = unpack(rows, 'Author'),
        years = unpack(rows, 'Year'),
        month = unpack(rows, 'Month'),
        day = unpack(rows, 'Day'),
        date = unpack(rows, 'Date Created')

    
    
    let minYear = Math.min.apply(null, years),
        maxYear = Math.max.apply(null, years);
    let uniqueYears = [];
    for (let i = minYear; i <= maxYear; i++) {
        uniqueYears.push(i)
    }
    let uniqueMonths = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    let data = [];

    let uniqueAuthor = []; 
    for (let i = 0; i < authors.length; i++) { //gets an array including each author once
        if (!uniqueAuthor.includes(authors[i])) {
            uniqueAuthor.push(authors[i])
        }
    }

    let list = document.getElementById('author_list')

    uniqueAuthor.forEach(function(item) { //creates valid options for the author text input
        let option = document.createElement('option');
        option.value = item;
        list.appendChild(option);
    })

    for (let i = 0; i < uniqueAuthor.length; i ++) {
        let x = [],
            y = [],
            text = []

        for (let j = 0; j < title.length; j ++) {
            if (authors[j] == uniqueAuthor[i]) {
                x.push(years[j])
                yVal = Number(month[j])
                /* Logic for handling position within months, based on number of days in that month */
                if (['January', 'March', 'May', 'July', 'August', 'October', 'December'].includes(month[i])) {
                    yVal += (Number(day[j]) / 32) //31 day months
                }
                else if (['April', 'June', 'September', 'November'].includes(month[i])){
                    yVal += (Number(day[j]) / 31) //30 day months
                }
                else {
                    if (years[j] % 4 == 0 && years[j] % 100 != 0) { //february, leapyear
                        yVal += (Number(day[j]) / 30) 
                    }
                    else {
                        yVal += (Number(day[j]) / 29) //february, non-leapyear
                    }
                }
                y.push(yVal)
                text.push(uniqueAuthor[i] + '<br>Title: ' + title[j] + '<br>Sent: ' + date[j])
            }
        }
        data.push({ //data is a set of markers
            x: x,
            y: y,
            mode: 'markers',
            type: 'scatter',
            hoverinfo: uniqueAuthor[i], //doesn't actually do anything on its own, but allows for disabling traces by text input
            name: '',
            hovertemplate: text,
            marker: {size: 5}
        })
     }


    let layout = {
        xaxis: {
            autorange: false, //prevents auto-updating range
            range: [1820, 1920]
        },
        yaxis: {
            tickmode: "array",
            tickvals: [1, 2, 3, 4 ,5, 6, 7, 8, 9, 10, 11, 12],
            ticktext: uniqueMonths
        },
        showlegend: false, //legend not useful with this many distince authors
        paper_bgcolor: '#f9efd7', //match char background to website background
        plot_bgcolor: '#f9efd7'
        };

    
    let config = {responsive: true} //updates when window size changes
    Plotly.newPlot('timeline', data, layout, config);

    function filter(authorInput, yearInput) {
        for (let i = 0; i < uniqueAuthor.length; i++) {
            data[i].visible = "legendonly" //data is still part of the chart, but disabled. accessible by (hidden) legend
            if (authorInput == data[i].hoverinfo) { //only make points with correct author visible
                data[i].visible = true 
            }
            else if (authorInput == '') { //if no input, make all points visible
                data[i].visible = true
            } 
        }
        layout.xaxis.range = [Number(yearInput[0]), Number(yearInput[1])] //forces the range to these values, rather than automatically update
        Plotly.react('timeline', data, layout, config) //faster than creating an entire new plot
    }

    let authorInput = document.querySelector('#author_input'), //add query selectors for each input
        authorClear = document.querySelector('#clear_author')
        yearClear = document.querySelector('#clear_year'),
        startYear = document.querySelector('#start_year'),
        endYear = document.querySelector('#end_year'),
        startYearInput = document.querySelector('#start_year_value'),
        endYearInput = document.querySelector('#end_year_value'),
        sliderReset = document.querySelector('#slider_reset')
        


    authorInput.addEventListener("input", (event) => {
        if (uniqueAuthor.includes(authorInput.value)) {
            filter(authorInput.value, [startYear.value, endYear.value])
        }
    });

    authorClear.addEventListener("click", (event) => {
        authorInput.value = ''
        filter('', [startYear.value, endYear.value])
    })

    startYear.addEventListener("input", (event) => {
        if (startYear.value >= endYear.value - 5) {
            startYear.value = Number(endYear.value) - 5
        }
        startYearInput.value = startYear.value
        filter(authorInput.value, [startYear.value, endYear.value])
    })

    endYear.addEventListener("input", (event) => {
        if (endYear.value <= Number(startYear.value) + 5) {
            endYear.value = Number(startYear.value) + 5
        }
        endYearInput.value = Number(endYear.value)
        filter(authorInput.value, [startYear.value, endYear.value])
    })


    sliderReset.addEventListener("click", (event) => {
        startYear.value = startYearInput.value = 1820
        endYear.value = endYearInput.value = 1920
        filter(authorInput.value, [1820, 1920])
    })

    startYearInput.addEventListener("input", (event) => {
        endYearInput.min = Number(startYearInput.value) + 5
        startYearInput.max = Number(endYearInput.value) - 5
        startYear.value = startYearInput.value
        filter(authorInput.value, [startYear.value, endYear.value])
    })

    endYearInput.addEventListener("input", (event) => {
        endYearInput.min = Number(startYearInput.value) + 5
        startYearInput.max = Number(endYearInput.value) - 5
        endYear.value = endYearInput.value
        filter(authorInput.value, [startYear.value, endYear.value])
    })



});
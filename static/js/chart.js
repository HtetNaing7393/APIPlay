const width = 500;
const height = 500;
const radius = Math.min(width, height) / 2;

// Test data
const data = [10, 20, 30, 40];


const svg = d3.select("svg")
    .attr("width", width)
    .attr("heigth", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + ", " + height / 2 + ")");

const colour = d3.scaleOrdinal(d3.schemeCategory10);
const pie = d3.pie();
const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius)

const arcs = svg.selectAll("arc")
    .data(pie(data)) // My own data will come here
    .enter()
    .append("g")
    .attr("class", "arc");


// Adding color to the piechart
arcs.append("path")
    .attr("fill", function (d, i) { return colour(i); })
    .attr("d", arc);

// Adding labels to the piechart
arcs.append("text")
    .attr("transform", function (d) {
        let degree = arc.centroid(d);
        degree[0] *= 1.5;
        degree[1] *= 1.5;
        return "translate(" + degree + ")";
    })
    .attr("text-anchor", "middle")
    .text(function (d, i) { return data[i]; });


// Test button for selenium






const width_1 = 300;
const height_1 = 300;
const radius = Math.min(width_1, height_1) / 2;

// Test data
const input_1 = [30, 40];
const colour_1 = d3.scaleOrdinal(d3.schemeCategory10);


function draw(data, selector) {

    const svg = d3.select(selector)
        .attr("width", width_1)
        .attr("heigth", height_1)
        .append("g")
        .attr("transform", "translate(" + width_1 / 2 + ", " + height_1 / 2 + ")");

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
}


function update_render_1(new_input) {
    render_1(new_input, "#piechart");
}

render_1(input, "piechart");






